"""Content extractor for PDF files"""
from PyPDF2 import PdfFileReader

from .binary_document import BinaryDocument


def get_page(doc: PdfFileReader, page_num: int) -> str:
    """Get page of content from PDF document

    Arguments:
        doc {PdfFileReader} -- PDF document
        page_num {int} -- page number

    Returns:
        str -- text of an individual page
    """
    page = doc.getPage(page_num)

    return page.extractText()


def get_body(doc: PdfFileReader) -> str:
    """Get body of PDF document

    Arguments:
        doc {PdfFileReader} -- PDF document

    Returns:
        str -- document body property
    """
    num_pages = doc.getNumPages()
    pages = [get_page(doc, i) for i in range(num_pages)]

    return '\n'.join(pages)


def get_title(doc: PdfFileReader) -> str:
    """Get title (if any)

    Arguments:
        doc {PdfFileReader} -- PDF document

    Returns:
        str -- document title property
    """
    info = doc.getDocumentInfo()

    return info.title


class PdfDocument(BinaryDocument):
    def __init__(self, path: str) -> None:
        stream = self.get_stream(path)
        doc = PdfFileReader(stream)

        body = get_body(doc)
        title = get_title(doc)
        keywords = self.get_keywords(doc)  # TODO: implement get_keywords

        super().__init__(body, title, keywords, path)

    @staticmethod
    def supports(_: str, ext: str) -> bool:
        return ext in ['pdf']
