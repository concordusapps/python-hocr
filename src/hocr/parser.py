from lxml import etree, html
from .page import Page
import six
from bs4 import UnicodeDammit


def parse(source):
    """Parse a HOCR stream into page elements.

    @param[in] source
        Either a file-like object or a filename of the HOCR text.
    """

    # Corece the source into content.
    if isinstance(source, six.string_types):
        with open(source, 'rb') as stream:
            content = stream.read()

    else:
        content = source.read()

    # Parse the HOCR xml stream.
    ud = UnicodeDammit(content, is_html=False)
    root = etree.fromstring(ud.unicode_markup.encode('utf8'))

    # Get all the pages and parse them into page elements.
    return [Page(x) for x in root.findall('.//*[@class="ocr_page"]')]
