

class BoundingBox:

    def __init__(self, text=None, *, left=0, right=0, top=0, bottom=0):

        # Parse the text string representation if given.
        if text is not None:
            left, top, right, bottom = map(int, text.split())

        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom


class Base:

    _allowed_ocr_classes = {}

    def __init__(self, element):
        """
        @param[in] element
            XML node for the OCR element.
        """

        # Store the element for later reference.
        self._element = element

        # Create an element cache.
        self._cache = {}

        # Parse the properties of the HOCR element.
        properties = element.attrib.get('title', '').split(';')
        for prop in properties:
            name, value = prop.split(maxsplit=1)
            if name == 'bbox':
                self.bbox = BoundingBox(value)

            elif name == 'image':
                self.image = value.strip('" ')

    def __dir__(self):
        return super().__dir__() + list(self._allowed_ocr_classes)

    def __getattr__(self, name):
        # Return the cached version if present.
        if name in self._cache:
            return self._cache[name]

        # Parse the named OCR elements.
        if name in self._allowed_ocr_classes:
            ref = OCR_CLASSES[name]
            nodes = self._element.findall('.//*[@class="%s"]' % ref['name'])
            self._cache[name] = elements = list(map(ref['class'], nodes))
            return elements

        # Attribute is not present.
        raise AttributeError(name)


class Word(Base):

    _allowed_ocr_classes = {}

    def __init__(self, element):
        # Initialize the base.
        super().__init__(element)

        # Discover if we are "bold".
        # A word element is bold if its text node is wrapped in a <strong/>.
        self.bold = bool(element.xpath('.//*[local-name() = "strong"]'))

        # Discover if we are "italic".
        # A word element is italic if its text node is wrapped in a <em/>.
        self.italic = bool(element.xpath('.//*[local-name() = "em"]'))

        # Find the text node.
        node = element.xpath('.//*[text()]')
        if node:
            self.text = node[0].text


class Line(Base):
    _allowed_ocr_classes = {'words'}


class Paragraph(Base):
    _allowed_ocr_classes = {'lines', 'words'}


class Block(Base):
    _allowed_ocr_classes = {'paragraphs', 'lines', 'words'}


class Page(Base):
    _allowed_ocr_classes = {'blocks', 'paragraphs', 'lines', 'words'}


OCR_CLASSES = {
    'words': {'name': 'ocrx_word', 'class': Word},
    'lines': {'name': 'ocr_line', 'class': Line},
    'paragraphs': {'name': 'ocr_par', 'class': Paragraph},
    'blocks': {'name': 'ocr_carea', 'class': Block}
}
