import hocr
from os import path
from io import StringIO
from pytest import raises

BASE_DIR = path.dirname(__file__)


def parse(filename='example.html'):
    return hocr.parse(path.join(BASE_DIR, filename))


def test_parse_from_stream():
    with open(path.join(BASE_DIR, 'example.html'), 'rb') as stream:
        pages = hocr.parse(stream)

        assert len(pages) == len(parse('example.html'))


def test_get_number_of_pages():
    assert len(parse()) == 1


def test_parse_return_datastructure_is_pages():
    for item in parse():
        assert isinstance(item, hocr.Page)


# def test_page_has_page_number():
#     pages = parse()

#     for item in pages:
#         assert hasattr(item, 'index')
#         assert item.index >= 0


# def test_page_has_unique_page_number():
#     pages = parse()
#     numbers = {x.index for x in pages}

#     assert len(pages) == len(numbers)


def test_page_elements_in_dir():
    page = parse()[0]

    assert 'words' in dir(page)
    assert 'blocks' in dir(page)


def test_page_has_proper_attribute_error():
    page = parse()[0]

    with raises(AttributeError):
        page.shjgioda


def test_page_has_bounding_box():
    for page in parse():
        assert page.bbox.left >= 0


def test_page_bounding_box_has_correct_value():
    page = parse()[0]

    assert page.bbox.left == 0
    assert page.bbox.top == 0
    assert page.bbox.right == 5100
    assert page.bbox.bottom == 6600


def test_page_has_image_name():
    page = parse()[0]

    assert page.image == '/tmp/tmpepham8.tiff'


def test_page_has_blocks():
    page = parse()[0]

    assert len(page.blocks) == 3


def test_page_blocks_have_paragraphs():
    page = parse()[0]

    assert len(page.blocks[0].paragraphs) == 1
    assert len(page.blocks[1].paragraphs) == 50
    assert len(page.blocks[2].paragraphs) == 1


def test_page_block_paragraphs_have_lines():
    page = parse()[0]

    assert len(page.blocks[1].paragraphs[0].lines) == 2
    assert len(page.blocks[1].paragraphs[10].lines) == 1
    assert len(page.blocks[1].paragraphs[20].lines) == 1
    assert len(page.blocks[2].paragraphs[0].lines) == 1


def test_page_block_paragraph_lines_have_words():
    page = parse()[0]

    assert len(page.blocks[0].paragraphs[0].lines[0].words) == 3
    assert len(page.blocks[1].paragraphs[0].lines[0].words) == 3
    assert len(page.blocks[1].paragraphs[10].lines[0].words) == 54


def test_page_has_words():
    page = parse()[0]

    assert len(page.words) == 2665


def test_words_have_text():
    page = parse()[0]

    assert page.words[0].text == 'TABLE'
    assert page.words[2].text == 'CONTENTS'
    assert page.words[102].text == '.'


def test_words_have_boldness():
    page = parse()[0]

    assert page.words[0].bold
    assert not page.words[73].bold


def test_words_have_italicness():
    page = parse()[0]

    assert not page.words[0].italic
    assert page.words[2].italic
    assert not page.words[73].italic


def test_words_have_bounding_box():
    page = parse()[0]

    assert page.words[0].bbox.left == 2216
    assert page.words[0].bbox.top == 1049
    assert page.words[0].bbox.right == 2449
    assert page.words[0].bbox.bottom == 1098
