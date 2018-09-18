"""Parameters for Summarizer testing"""
import typing

from src.oolongt.summarizer import ScoredSentence
from src.oolongt.typings import AnyList, StringList
from tests.constants import SAMPLES
from tests.helpers import get_sample
from tests.params.helpers import pad_to_longest, parametrize
from tests.typings import Sample, SampleKeyword, SampleSentence

SampleGenerator = typing.Generator[Sample, None, None]
SampleSentenceGenerator = typing.Generator[
    typing.Tuple[Sample, SampleSentence], None, None]

SPAM = 'spam'
SPAM_PARAMS = [SPAM, 1.1, 3.1] + list(range(4, 11))
SPAM_RESULT = [SPAM, 1, 3, 4.0, 5.0, 6.0, 7.0, 65.0, 0.06, 34.64]


def reverse_kw(score: float) -> SampleKeyword:
    """Reverse a SampleKeyword from the score

    Arguments:
        score {float} -- keyword score

    Returns:
        SampleKeyword -- a full-fledged SampleKeyword
    """
    return SampleKeyword.by_score(score)


def param_calc_decile():
    """Parametrize `test_calc_decile`"""
    names = 'index,total,expected'
    vals = (
        (0, 10, 1),
        (9, 100, 1),
        (1, 10, 2),
        (2, 10, 3),
        (3, 10, 4),
        (4, 10, 5),
        (5, 10, 6),
        (6, 10, 7),
        (7, 10, 8),
        (8, 10, 9),
        (9, 10, 10),
        (-1, 100, IndexError),
        (10, 10, IndexError),
        (10, 0, IndexError),
    )
    ids = (
        '00-of-10)',
        '01-of-10)',
        '02-of-10)',
        '03-of-10)',
        '04-of-10)',
        '05-of-10)',
        '06-of-10)',
        '07-of-10)',
        '08-of-10)',
        '09-of-10)',
        '09-of-00)',
        '-1-of-00)',
        '10-of-10)',
        '10-of-00)',
    )

    return parametrize(names, vals, ids)


def param_score_position():
    """Parametrize `test_score_position`"""
    names = 'index,expected'
    vals = (
        (0, .17),
        (99, .17),
        (100, .23),
        (999, .15),
        (-1, IndexError),
        (1000, IndexError),
    )
    ids = (
        '0-of-1000',
        '99-of-1000',
        '100-of-1000',
        '999-of-1000',
        'neg-of-1000',
        '1000-of-1000',
    )

    return parametrize(names, vals, ids)


def param_scored_sentence__init_():
    """Parametrize `TestScoredSentence.test__init_`"""
    names = 'init,expected'
    vals = ((
        SPAM_PARAMS,
        SPAM_RESULT[:-3] + list(float(x) for x in range(8, 11))), )
    ids = (SPAM, )

    return parametrize(names, vals, ids)


def param_scored_sentence___init__():
    """Parametrize `TestScoredSentence.test___init__`"""
    names = 'init,expected'
    vals = ((SPAM_PARAMS, SPAM_RESULT), )
    ids = (SPAM, )

    return parametrize(names, vals, ids)


def param_scored_sentence__str__():
    """Parametrize `TestScoredSentence.test___str__`"""
    names = 'init,expected'
    vals = ((SPAM_PARAMS, SPAM), )
    ids = (SPAM, )

    return parametrize(names, vals, ids)


def param_scored_sentence__repr__():
    """Parametrize `TestScoredSentence.test___repr___`"""
    names = 'init,expected'
    vals = (
        (SPAM_PARAMS, 'ScoredSentence(\'spam\', 1, 3, 4.0, 5.0, 6.0, 7.0)'),
    )
    ids = (SPAM, )

    return parametrize(names, vals, ids)


def param_pluck_keyword_words():
    """Parametrize `test_pluck_keyword_words`"""
    names = 'keyword_list,expected'
    vals = (
        (
            [
                SampleKeyword({'word': 'spam'}, 1),
                SampleKeyword({'word': 'eggs'}, 1),
                SampleKeyword({'word': 'bacon'}, 1)
            ],
            ['bacon', 'eggs', 'spam'],
        ),
    )
    ids = ('spam-eggs', )

    return parametrize(names, vals, ids)


def param__float_len():
    """Parametrize `test__float_len`"""
    names = 'item_list,expected'
    vals = (([], 0.0), ([1], 1.0), (range(10), 10.0), (range(10000), 10000.0))
    ids = ('    0', '    1', '   10', '10000', )

    return parametrize(names, vals, ids)


def param_score_by_title():
    """Parametrize `test_score_by_title`"""
    names = 'samp'
    vals = get_samples((
        'sentence_1word',
        'sentence_short',
        'sentence_medium',
        'sentence_ideal',
        'sentence_overlong',
    ))
    ids = (get_sample_ids((
        'sentence_1word',
        'sentence_short',
        'sentence_medium',
        'sentence_ideal',
        'sentence_overlong',
    )))

    return parametrize(names, vals, ids)


# pylint: disable=dangerous-default-value
def param_samples(sample_names: StringList = SAMPLES):
    """Parametrize with list of samples"""
    names = 'samp'
    vals = get_samples(sample_names)
    ids = sample_names

    return parametrize(names, vals, ids)


# pylint: enable=dangerous-default-value
def param_threshold():
    """Parametrize for `get_keyword_threshold`"""
    names = 'keywords,expected'
    vals = (
        (
            [
                reverse_kw(.11),
                reverse_kw(.08),
                reverse_kw(.07),
                reverse_kw(.10),
                reverse_kw(.09),
                reverse_kw(.12),
            ],
            .07
        ),
        (
            [
                reverse_kw(.02),
                reverse_kw(.04),
                reverse_kw(.07),
                reverse_kw(.01),
                reverse_kw(.08),
                reverse_kw(.05),
                reverse_kw(.12),
                reverse_kw(.09),
                reverse_kw(.11),
                reverse_kw(.06),
                reverse_kw(.10),
                reverse_kw(.03),
            ],
            .03
        ),
        (
            [
                reverse_kw(.04),
                reverse_kw(.01),
                reverse_kw(.04),
                reverse_kw(.07),
                reverse_kw(.04),
                reverse_kw(.06),
                reverse_kw(.05),
                reverse_kw(.08),
                reverse_kw(.11),
                reverse_kw(.09),
                reverse_kw(.12),
                reverse_kw(.10),
            ],
            .04
        ),
    )
    ids = ('all_pass', 'simple', 'complex')

    return parametrize(names, vals, ids)


def permute_sentences():
    """List 3 `ScoredSentence` tuples: [(a < b), (a == b), (a > b)]"""
    eq_params = SPAM_PARAMS[:-3]
    lt_params = eq_params.copy()
    lt_params[2] += 1
    gt_params = eq_params.copy()
    gt_params[1] += 1

    eq_perm = (ScoredSentence(*eq_params), 0, 0)
    lt_perm = (ScoredSentence(*lt_params), 0, 0)
    gt_perm = (ScoredSentence(*gt_params), 0, 0)

    return (
        (lt_perm, eq_perm, True, False),
        (eq_perm, eq_perm, False, True),
        (gt_perm, eq_perm, False, False),
    )


def param_comp():
    """Parametrize `ScoredSentence` comparisons"""
    names = 'sent_a,sent_b,is_lt,is_eq'
    vals = permute_sentences()
    ids = ('lt', 'eq', 'gt', )

    return parametrize(names, vals, ids)


def get_inst_comp(inst: ScoredSentence) -> AnyList:
    """List properties of a `ScoredSentence` instance for comparison

    Arguments:
        inst {ScoredSentence} -- instance of `ScoredSentence`

    Returns:
        AnyList -- list of properties
    """
    return [
        inst.text,
        inst.index,
        inst.of,
        inst.title_score,
        inst.length_score,
        inst.dbs_score,
        inst.sbs_score,
        inst.keyword_score,
        inst.position_score,
        inst.total_score
    ]


def get_samples(sample_names: typing.Iterable[str]) -> SampleGenerator:
    """Get Samples by name

    Returns:
        typing.Iterable[Sample] - iterable of samples
    """
    for sample_name in sample_names:
        yield get_sample(sample_name)


def get_sample_ids(sample_names: typing.Iterable[str]) -> StringList:
    """List test IDs from list of samples

    Arguments:
        sample_names {StringList} -- [description]

    Returns:
        StringList -- [description]
    """
    return pad_to_longest(sample_names)


def get_sample_sentences(
        sample_names: StringList) -> SampleSentenceGenerator:
    """Get Sample, each sentence from Sample

    Arguments:
        sample_names {StringList} -- names of samples

    Returns:
        typing.Iterable[Sample] -- Iterator of Samples
    """
    for sample_name in sample_names:
        samp = get_sample(sample_name)

        for sentence in samp.sentences:
            yield samp, sentence


def get_sample_sentence_ids(sample_names: typing.Iterable[str]) -> StringList:
    """List friendly names of sample sentences

    Returns:
        StringList -- IDs of sample sentences
    """
    ids = []  # type: StringList
    for sample_name in sample_names:
        samp = get_sample(sample_name)

        for sentence in samp.sentences:
            ids.append('src: {}, sent: {}'.format(samp.name, sentence.id))

    return pad_to_longest(ids)


def param_sentences():
    """Parametrize for a `ScoredSentence` and its `Sample`"""
    names = 'sample,sentence'
    vals = get_sample_sentences(SAMPLES)
    ids = get_sample_sentence_ids(SAMPLES)

    return parametrize(names, vals, ids)


def param_score_by_length():
    """Parametrize `test_score_by_length`"""
    samples = (
        'empty',
        'sentence_short',
        'sentence_medium',
        'sentence_ideal',
        'sentence_overlong',
    )

    names = 'samp'
    vals = get_samples(samples)
    ids = samples

    return parametrize(names, vals, ids)
