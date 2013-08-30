import hocr
from os import path

BASE_DIR = path.dirname(__file__)


def parse(filename='example.html'):
    return hocr.parse(filename=path.join(BASE_DIR, filename))


def test_get_number_of_pages():
    assert len(parse()) == 1


def test_parse_return_datastructure_is_pages():
    for item in parse():
        assert isinstance(item, hocr.Page)


def test_page_has_page_number():
    pages = parse()

    for item in pages:
        assert hasattr(item, 'index')
        assert item.index >= 0

# def test_page_has_unique_page_number():
#     pages = parse()
#     numbers = {x.index for x in pages}

#     assert len(pages) == len(numbers)


def test_page_has_bounding_box():
    for page in parse():
        assert page.bbox.left >= 0


def test_page_bounding_box_has_correct_value():
    page = parse()[0]

    assert page.bbox.left == 0
    assert page.bbox.right == 0
    assert page.bbox.top == 5100
    assert page.bbox.bottom == 6600
