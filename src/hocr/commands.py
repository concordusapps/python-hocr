# -*- coding: utf-8 -*-
from argparse import ArgumentParser
import re
from hocr import overlay
import sys
import os


def hocr2pdf():
    # Build command arguments.
    parser = ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('hocr')
    parser.add_argument('-o', '--output')

    # Parse command arguments.
    arguments = parser.parse_args()

    # Parse source.
    source_filename = arguments.source
    source_index = 0
    match = re.match(r'^(.*)\[(.*)\]$', arguments.source)
    if match is not None:
        source_filename, source_index = match.groups()

    # Decide on output.
    if arguments.output:
        output_stream = open(arguments.output, 'wb')

    else:
        output_stream = os.fdopen(sys.stdout.fileno(), 'wb')

    # Invoke the overlay method.
    overlay(output=output_stream,
            source=source_filename,
            text=arguments.hocr,
            index=int(source_index))

    # Close the stream.
    output_stream.close()
