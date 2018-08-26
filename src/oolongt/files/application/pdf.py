"""Content extractor for PDF files"""
import typing

from PyPDF2 import PdfFileReader

from oolongt.typedefs import Content


def get_page(pdf: PdfFileReader, page_num: int) -> str:
    page = pdf.getPage(page_num)

    return page.extractText()


def get_body(pdf: PdfFileReader) -> str:
    num_pages = pdf.getNumPages()
    pages = [get_page(pdf, i) for i in range(num_pages)]

    return '\n'.join(pages)


def get_title(pdf: PdfFileReader) -> typing.Any:
    info = pdf.getDocumentInfo()

    return info.title


def get_keywords(pdf: PdfFileReader) -> str:
    # TODO
    return ''


def load(path: str) -> typing.Dict[str, typing.Any]:
    with open(path, 'rb') as fp:
        pdf = PdfFileReader(fp)

        body = get_body(pdf)
        title = get_title(pdf)
        keywords = get_keywords(pdf)

    return {'body': body, 'title': title, 'keywords': keywords}


def parse(path: str) -> Content:
    return Content(load, path)
