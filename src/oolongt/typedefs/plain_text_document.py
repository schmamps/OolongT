from .text_document import TextDocument


class PlainTextDocument(TextDocument):
    def __init__(self, path: str) -> None:
        src = self.get_source(path)

        body = self.get_body(src)
        title = self.get_title(src)
        keywords = self.get_keywords(src)

        super().__init__(body, title, keywords, path)

    @staticmethod
    def supports(_: str, __: str) -> bool:
        return True
