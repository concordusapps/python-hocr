from lxml import etree
from .page import Page


def parse(obj):
    """Parse a HOCR stream into page elements.

    @param[in] obj
        Either a file-like object or a filename of the HOCR text.
    """

    # Parse the HOCR xml stream.
    tree = etree.parse(obj)

    # Get all the pages and parse them into page elements.
    return [Page(x) for x in tree.findall('//*[@class="ocr_page"]')]
