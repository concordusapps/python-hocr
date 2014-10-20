# -*- coding: utf-8 -*-
import itertools
import six
from hummus import Document, Font, Text, Image
from .parser import parse
from PIL import ImageFont
import magic


class Line:

    def __init__(self):
        self.words = []


def _is_within(value, compare, threshold=0.005):
    return (compare * (1 - threshold)) < value < (compare * (1 + threshold))


def _collect_lines(words):
    words.sort(key=lambda w: w.box.top)
    lines = []
    current_line = []
    current_top = None
    for word in words:
        if current_top is None:
            current_line.append(word)
            current_top = word.box.top

        elif _is_within(word.box.top, current_top):
            current_line.append(word)
            current_top = (current_top + word.box.top) / 2.0

        else:
            lines.append(current_line)
            current_line = []
            current_line.append(word)
            current_top = word.box.top
    if current_line:
        lines.append(current_line)
    return lines


def _join_words(groups):
    words = []
    for group in groups:
        group.sort(key=lambda w: w.box.left)
        text = ""
        top = group[0].box.top
        left = group[0].box.left
        for word in group:
            text = text + " " + word.text
            top = (top + word.box.top) / 2.0
        top = int(round(top))
        word = group[0]
        word.box.top = top
        word.box.right = group[-1].box.right
        word.box.left = left
        word.text = text
        words.append(word)
    return words


def _align_words(groups):
    words = []
    for group in groups:
        group.sort(key=lambda w: w.box.left)
        top = group[0].box.top
        for word in group:
            word.box.top = top
            words.append(word)

    return words


def _split_lines(lines):
    chunks = []
    for line in lines:
        blocks = []
        cur_block = []
        cur_right = None
        line.sort(key=lambda w: w.box.left)
        for word in line:
            if cur_right is None:
                cur_block.append(word)
                cur_right = word.box.right

            elif _is_within(word.box.left, cur_right, threshold=0.25):
                cur_right = word.box.right
                cur_block.append(word)

            else:
                blocks.append(cur_block)
                cur_right = word.box.right
                cur_block = [word]
        if cur_block:
            blocks.append(cur_block)
        chunks.append(blocks)
    return list(itertools.chain(*chunks))


def _is_document(source):
    """Check if the source refers to a PDF document or not.
    """
    test = 'id_filename' if isinstance(source, str) else 'id_buffer'
    with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
        return getattr(m, test)(source) == 'application/pdf'


def overlay(output, source, text, index=0, font='TimesNewRoman', dpi=72.0):
    """Overlay a PDF document or JPEG image with the text from a HOCR file.

    Writes the overlaid source as a PDF file to the output filename or
    file-like object.

    @param[in] source
        Either a file-like object or a filename of the image or PDF document
        to embed as the background.

    @param[in] text
        Either a file-like object or a filename of the HOCR text.
    """

    # Parse the HOCR text.
    page = parse(text)[0]

    # Initialize PDF document.
    with Document(output) as document:

        # Initialize a new page and begin its context.
        with document.Page() as ctx:

            # Prepare to embed the target as the background of the
            # new PDF.
            if _is_document(source):
                with Document(source, 'r') as target:

                    # Set the box to be equivalent as the source.
                    target_page = target[index]
                    ctx.box = target_page.box

                    # Embed the target.
                    ctx.embed(target_page)

            else:
                # Assume we have an image to embed. This will do
                # hilarious things if we "dont" have an image as
                # image magick.. is magick.
                with Image(source, index=index) as target:

                    # Set the box to be equivalent as the source.
                    ctx.box = target.box

                    # Embed the target.
                    ctx.embed(target)

            # Figure out scale.
            scale = ctx.box.right / page.box.right

            # Filter out any words that are "empty"
            words = list(filter(lambda w: bool(w.text.strip()), page.words))

            # Collect the words into the lines of the page.
            lines = _collect_lines(words)

            # Split the lines if it does go across the whole page.
            lines = _split_lines(lines)

            # Join the list of list of boxes
            words = _join_words(lines)

            # Iterate through words in the HOCR page.
            for word in words:

                # Skip if we don't have text.
                text = word.text.strip()
                if not text:
                    continue

                # Get x,y position where text should begin.
                x, y = word.box.left, word.box.top

                # Apply the scale factor.
                x *= scale
                y *= scale

                # Mirror the Y axis as HOCR and PDF are in differnet
                # quadrants because.
                y = ctx.box.bottom - y

                # Build a font object.
                fobj = Font(font, bold=word.bold, italic=word.italic)

                # Approximate the font size by measuring the width of
                # the text using pillow.
                pil_font = ImageFont.truetype(fobj.file, 10)
                base_width, _ = pil_font.getsize(text)
                base_width /= dpi
                expected_width = (word.box.width * scale) / dpi
                scale_width = expected_width / base_width
                fsize = 10 * scale_width

                # Measure the font again and shift it down.
                pil_font = ImageFont.truetype(fobj.file, int(fsize))
                _, actual_height = pil_font.getsize(text)
                y -= actual_height

                # Write text.
                # print(text, x, y)
                ctx.add(Text(text, fobj, size=fsize, x=x, y=y, mode=7))
