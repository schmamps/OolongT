"""Content extractor for PDF files"""
import typing

from PyPDF2 import PdfFileReader

from oolongt.typedefs import Content


def get_page(pdf: PdfFileReader, page_num: int) -> str:
    """Get page of content from PDF document

    Arguments:
        pdf {PdfFileReader} -- PDF document
        page_num {int} -- page number

    Returns:
        str -- text of an individual page
    """
    page = pdf.getPage(page_num)

    return page.extractText()


def get_body(pdf: PdfFileReader) -> str:
    """Get body of PDF document

    Arguments:
        pdf {PdfFileReader} -- PDF document

    Returns:
        str -- document body property
    """
    num_pages = pdf.getNumPages()
    pages = [get_page(pdf, i) for i in range(num_pages)]

    return '\n'.join(pages)


def get_title(pdf: PdfFileReader) -> typing.Any:
    """Get title (if any)

    Arguments:
        pdf {PdfFileReader} -- PDF document

    Returns:
        str -- document title property
    """
    info = pdf.getDocumentInfo()

    return info.title


def get_keywords(pdf: PdfFileReader) -> str:  # pylint: disable=unused-argument
    """Get keywords (if any)

    Arguments:
        pdf {PdfFileReader} -- PDF document

    Returns:
        str -- document keywords property
    """
    return ''


def load(path: str) -> typing.Dict[str, typing.Any]:
    """Load PDF and extract properties

    Arguments:
        path {str} -- path to document

    Returns:
        typing.Dict[str, typing.Any] -- {body: str, title: str, keywords: Any}
    """
    with open(path, 'rb') as fp:  # pylint: disable=invalid-name
        pdf = PdfFileReader(fp)

        body = get_body(pdf)
        title = get_title(pdf)
        keywords = get_keywords(pdf)

    return {'body': body, 'title': title, 'keywords': keywords}


def parse(path: str) -> Content:
    """Get content of document at `path`

    Arguments:
        path {str} -- path to document

    Returns:
        Content -- text properties of document
    """
    return Content(load, path)
