from oolongt.typedefs.content import Content


class TextContent(Content):
    def __init__(self, body, title='', keywords=[]):
        super.__init__(body, title, keywords)
