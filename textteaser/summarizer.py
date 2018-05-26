#!/usr/bin/python
# -*- coding: utf-8 -*-
from .parser import Parser


class Summarizer:
    def __init__(self):
        self.parser = Parser()

    def summarize(self, text, title, source, category):
        sentences = self.parser.splitSentences(text)
        titleWords = self.parser.removePunctations(title)
        titleWords = self.parser.splitWords(title)
        (keywords, wordCount) = self.parser.getKeywords(text)

        topKeywords = self.get_top_keywords(
            keywords, wordCount, source, category)

        result = self.computeScore(sentences, titleWords, topKeywords)
        result = self.sortScore(result)

        return result

    def score_keyword(self, keyword, wordCount):
        """Calculate totalScore of keyword

        Arguments:
            keyword {Dict} -- {word, count}
            wordCount {int} -- total number of keywords

        Returns:
            Dict -- {word, count, totalScore}
        """
        keyword['totalScore'] = 1.5 * keyword['count'] / wordCount

        return keyword

    def get_top_keyword_threshold(self, keywords):
        """Get minimum frequency for top keywords

        Arguments:
            keywords {List[Dict]} -- list of keyword Dicts

        Returns:
            int -- minimum frequency
        """
        counts = sorted([x['count'] for x in keywords], reverse=True)

        return counts[:10].pop()

    def get_top_keywords(self, keywords, wordCount, source, category):
        """Get list of the 1st-10th ranked keywords

        Arguments:
            keywords {List[Dict]} -- keyword list
            wordCount {int} -- total number of keywords
            source {any} -- unused
            category {any} -- unused

        Returns:
            List[Dict] -- ten most frequently used words (more if same count)
        """
        min_count = self.get_top_keyword_threshold(keywords)

        top_keywords = [
            self.score_keyword(keyword, wordCount)
            for keyword in keywords
            if keyword['count'] >= min_count]

        return top_keywords

    def sortScore(self, dictList):
        return sorted(dictList, key=lambda x: -x['totalScore'])

    def sortSentences(self, dictList):

        return sorted(dictList, key=lambda x: x['order'])

    def computeScore(self, sentences, titleWords, topKeywords):
        keywordList = [keyword['word'] for keyword in topKeywords]
        summaries = []

        for i, sentence in enumerate(sentences):
            sent = self.parser.removePunctations(sentence)
            words = self.parser.splitWords(sent)

            sbsFeature = self.sbs(words, topKeywords, keywordList)
            dbsFeature = self.dbs(words, topKeywords, keywordList)

            titleFeature = self.parser.getTitleScore(titleWords, words)
            sentenceLength = self.parser.getSentenceLengthScore(words)
            sentencePosition = self.parser.getSentencePositionScore(
                i, len(sentences))
            keywordFrequency = (sbsFeature + dbsFeature) / 2.0 * 10.0
            totalScore = (
                titleFeature * 1.5 + keywordFrequency * 2.0 +
                sentenceLength * 0.5 + sentencePosition * 1.0) / 4.0

            summaries.append({
                # 'titleFeature': titleFeature,
                # 'sentenceLength': sentenceLength,
                # 'sentencePosition': sentencePosition,
                # 'keywordFrequency': keywordFrequency,
                'totalScore': totalScore,
                'sentence': sentence,
                'order': i
            })

        return summaries

    def sbs(self, words, topKeywords, keywordList):
        score = 0.0

        if len(words) == 0:
            return 0

        for word in words:
            word = word.lower()
            index = -1

        if word in keywordList:
            index = keywordList.index(word)

        if index > -1:
            score += topKeywords[index]['totalScore']

        return 1.0 / abs(len(words)) * score

    def dbs(self, words, topKeywords, keywordList):
        k = len(list(set(words) & set(keywordList))) + 1
        summ = 0.0
        firstWord = {}
        secondWord = {}

        for i, word in enumerate(words):
            if word in keywordList:
                index = keywordList.index(word)

                if firstWord == {}:
                    firstWord = {
                        'i': i,
                        'score': topKeywords[index]['totalScore']}
                else:
                    secondWord = firstWord
                    firstWord = {
                        'i': i,
                        'score': topKeywords[index]['totalScore']}
                    distance = firstWord['i'] - secondWord['i']

                    summ += (firstWord['score'] * secondWord['score']) / (distance ** 2)  # nopep8

        return (1.0 / k * (k + 1.0)) * summ
