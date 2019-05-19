#!/usr/bin/env python3

__author__ = "Andrew Szymanski ()"
__version__ = "0.1"

"""Utilities to convert (csv to json etc) and manage config files
"""

import sys
import logging
import csv
import json
import os
import inspect
import pathlib


LOG_INDENT = "  "
console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s: %(levelname)-8s %(message)s',"%Y-%m-%d %H:%M:%S")
console.setFormatter(formatter)
logging.getLogger(__name__).addHandler(console)
logger = logging.getLogger(__name__)

#                      **********************************************************
#                      **** convert csv to json and vice versa
#                      **********************************************************
def convert(input_file, output_file):
    """ publish json
    """
    logger.debug("%s %s (%s,%s)..." %  (LOG_INDENT, inspect.stack()[0][3], input_file, output_file))

    input_file_format = (pathlib.Path(input_file).suffix)
    output_file_format = (pathlib.Path(output_file).suffix)



#                      **********************************************************
#                      **** mainRun - parse args and decide what to do
#                      **********************************************************
def mainRun(opts, parser):
    logger.setLevel(opts.loglevel)
    logger.debug("%s starting..." % inspect.stack()[0][3])

    if opts.action == 'convert':
        if not opts.input or not opts.output:
            parser.print_help()
            sys.exit("ERROR: you must specify input and output files")
        convert(opts.input, opts.output)

    logger.info("all done")


def main(argv=None):
    from optparse import OptionParser, OptionGroup
    #logger.debug("main starting...")

    argv = argv or sys.argv
    parser = OptionParser(description="Vote test harness",
                      version=__version__,
                      usage="usage: %prog [options]")
    # cat options
    cat_options = OptionGroup(parser, "options")
    cat_options.add_option("-l", "--loglevel", help="debug logging, specify any value to enable debug, omit this param to disable, example: -l DEBUG", default="INFO")
    cat_options.add_option("-a", "--action", help="action, currently 'convert' only, example: --action=convert", default="convert")
    cat_options.add_option("-i", "--input", help="input file, example: -i ./config.json", default=None)
    cat_options.add_option("-o", "--output", help="output file, example: --output=/tmp/spec.csv", default=None)
    parser.add_option_group(cat_options)

    try:
        opts, args = parser.parse_args(argv[1:])
    except Exception as e:
        sys.exit("ERROR: [%s]" % e)

    try:
        mainRun(opts, parser)
    except Exception as e:
        sys.exit("ERROR: [%s]" % e)

# use cases / examples:
# ./config-utils.py
# ./config-utils.py -l DEBUG
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sys.exit("ERROR: [%s]" % e)
