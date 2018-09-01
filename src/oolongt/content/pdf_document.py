"""Content extractor for PDF files"""
from PyPDF2 import PdfFileReader
from PyPDF2.pdf import DocumentInformation

from .binary_document import BinaryDocument


def get_page(src: PdfFileReader, page_num: int) -> str:
    """Get page of content from PDF document

    Arguments:
        src {PdfFileReader} -- PDF document
        page_num {int} -- page number

    Returns:
        str -- text of an individual page
    """
    page = src.getPage(page_num)

    return page.extractText()


def get_body(src: PdfFileReader) -> str:
    """Get body of PDF document

    Arguments:
        src {PdfFileReader} -- PDF document

    Returns:
        str -- document body property
    """
    num_pages = src.getNumPages()
    pages = [get_page(src, i) for i in range(num_pages)]

    return '\n'.join(pages)


def get_title(info: DocumentInformation) -> str:
    """Get title (if any)

    Arguments:
        info {DocumentInformation} -- PDF document info

    Returns:
        str -- document title property
    """
    try:
        title = info.title

        if title is not None:
            return title

    except AttributeError:
        pass

    try:
        return info['/Title']

    except KeyError:
        pass

    return ''


def get_keywords(info: DocumentInformation) -> str:
    """Get keywords (if any)

    Arguments:
        info {DocumentInformation} -- PDF document info

    Returns:
        str -- document keywords property
    """
    try:
        return info.keywords
    except AttributeError:
        pass

    try:
        return info['/Keywords']
    except KeyError:
        pass

    return ''


class PdfDocument(BinaryDocument):
    """Parse PDF"""
    def __init__(self, path: str) -> None:
        with self.get_stream(path) as stream:
            src = PdfFileReader(stream)
            info = src.getDocumentInfo()

            body = get_body(src)
            title = get_title(info)
            keywords = get_keywords(info)

        super().__init__(body, title, keywords, path)

    @staticmethod
    def supports(_: str, ext: str) -> bool:
        return ext in ['pdf']
