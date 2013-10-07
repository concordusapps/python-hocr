from .page import Page
import six
from bs4 import UnicodeDammit, BeautifulSoup
# from lxml.etree import fromstring


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
    ud = UnicodeDammit(content, is_html=True)
    soup = BeautifulSoup(ud.unicode_markup)

    # Get all the pages and parse them into page elements.
    return [Page(x) for x in soup.find_all(class_='ocr_page')]
