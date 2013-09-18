# -*- coding: utf-8 -*-
import hummus
from .parser import parse


def overlay_document(output, source, text):
    """Overlay a PDF document with the text from a HOCR file.

    Writes the overlaid document as a PDF file to the output filename or
    file-like object.

    @param[in] source
        Either a file-like object or a filename of the PDF document.
    """

    with hummus.Document(output) as document:

        with document.Page() as page:

            page.add(hummus.Document(source, 'r')[0])

            page.add(hummus.Text(text, font, size, x, y))


def overlay_image(output, source, text):
    """Overlay a JPEG image with the text from a HOCR file.

    Writes the overlaid image as a PDF file to the output filename or
    file-like object.

    @param[in] source
        Either a file-like object or a filename of the image.
    """


def overlay(output, source, text):
    """Overlay a PDF document or JPEG image with the text from a HOCR file.

    Writes the overlaid source as a PDF file to the output filename or
    file-like object.

    @param[in] text
        Either a file-like object or a filename of the HOCR text.
    """

    overlay_document(output, source, text)


# >>> overlay(output='pass.pdf', source='media/document.tiff', text='')
# >>> overlay(output='out.pdf',  source='media/document.tiff', text='')
