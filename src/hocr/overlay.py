# -*- coding: utf-8 -*-
import hummus
from .parser import parse


def overlay_document(output, source, text, page=0):
    """Overlay a PDF document with the text from a HOCR file.

    Writes the overlaid document as a PDF file to the output filename or
    file-like object.

    @param[in] source
        Either a file-like object or a filename of the PDF document.
    """

    # Parse the HOCR text.
    target = parse(text)[0]
    # print(target.bbox.right, target.bbox.bottom)

    # Prepare fonts.
    arial = hummus.Font('arial')

    # Initialize PDF document.
    with hummus.Document(output) as document:

        # Initialize a new page and begin its context.
        with document.Page() as ctx:

            # Establish the media box.
            # ctx.media_box = hummus.Rectangle(
            #     right=target.bbox.right, bottom=target.bbox.bottom)

            # Embed the passed PDF document.
            ctx.embed_document(source, page=page)

            ctx.write_text('Tom Foolery', font=arial, size=10,
                           a=1, b=1, c=1, d=1)



def overlay_image(output, source, text, page=0):
    """Overlay a JPEG image with the text from a HOCR file.

    Writes the overlaid image as a PDF file to the output filename or
    file-like object.

    @param[in] source
        Either a file-like object or a filename of the image.
    """


def overlay(output, source, text, page=0):
    """Overlay a PDF document or JPEG image with the text from a HOCR file.

    Writes the overlaid source as a PDF file to the output filename or
    file-like object.

    @param[in] text
        Either a file-like object or a filename of the HOCR text.
    """

    overlay_document(output, source, text, page)


# >>> overlay(output='pass.pdf', source='media/document.tiff', text='')
# >>> overlay(output='out.pdf',  source='media/document.tiff', text='')
