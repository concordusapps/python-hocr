from lxml.etree import ElementTree
from lxml import etree
from .page import Page


def parse(stream=None, filename=None):
    """Parse a file like object or filename."""

    if filename is not None and not stream:
        tree = etree.parse(filename)
    elif filename is None and stream:
        tree = etree.parse(stream)
    else:
        raise ValueError('Provide either filename or stream.')

    # Get all the pages that this
    pages = tree.findall('//*[@class="ocr_page"]')

    return [Page(x) for x in pages]
