# -*- coding: utf-8 -*-
import six
from hummus import Document, Font, Text, Image
from .parser import parse
import magic


def _is_document(source):
    """Check if the source refers to a PDF document or not.
    """

    test = magic.from_buffer
    if isinstance(source, six.string_types):
        test = magic.from_file
        source = source.encode('utf8')

    elif isinstance(source, six.binary_type):
        test = magic.from_file

    return test(source, mime=True) == b'application/pdf'


def overlay(output, source, text, index=0):
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
                    taget_page = target.pages[index]
                    ctx.box = target_page.box

                    # Embed the target.
                    ctx.embed(target)
