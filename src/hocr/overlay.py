# -*- coding: utf-8 -*-
import six
from hummus import Document, Font, Text, Image
from .parser import parse
from PIL import ImageFont
import magic


def _is_document(source):
    """Check if the source refers to a PDF document or not.
    """
    test = 'id_filename' if isinstance(source, str) else 'id_buffer'
    with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
        return getattr(m, test)(source) == b'application/pdf'


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

            # Iterate through words in the HOCR page.
            for word in page.words:

                # Skip if we don't have text.
                if word.text is None:
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
                base_width, _ = pil_font.getsize(word.text)
                base_width /= dpi
                expected_width = (word.box.width * scale) / dpi
                scale_width = expected_width / base_width
                fsize = 10 * scale_width

                # Measure the font again and shift it down.
                pil_font = ImageFont.truetype(fobj.file, int(fsize))
                _, actual_height = pil_font.getsize(word.text)
                y -= actual_height

                # Write text.
                ctx.add(Text(word.text, fobj, size=fsize, x=x, y=y, mode=7))
