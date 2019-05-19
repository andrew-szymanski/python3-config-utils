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



def read_into_dictionary(input_file):
    """ read a file into dictionary
    """
    logger.debug("%s %s (%s)..." %  (LOG_INDENT, inspect.stack()[0][3], input_file))

    input_file_format = (pathlib.Path(input_file).suffix)
    ret_dict = {}
    if input_file_format == '.csv':
        logger.debug("%s opening file [%s]" % (LOG_INDENT,input_file))
        reader = csv.reader(open(input_file, 'r'))
        for row in reader:
            # read in and strip of comments / blank lines etc..
            variable_name = row[0].strip()
            variable_value = row[1].strip()
            if not variable_name:
                continue
            if variable_name.startswith('#') or variable_value.startswith('#'):
                continue
            logger.debug("%s %s=%s" % (LOG_INDENT,variable_name,variable_value))
            # save in dictionary
            ret_dict[variable_name] = variable_value
        return ret_dict




def convert(input_file, output_file):
    """ convert files
    """
    logger.debug("%s %s (%s,%s)..." %  (LOG_INDENT, inspect.stack()[0][3], input_file, output_file))

    #output_file_format = (pathlib.Path(output_file).suffix)

    # read file into dictionary regardless of format
    input_dict = read_into_dictionary(input_file)
    logger.debug(input_dict)



#                      **********************************************************
#                      **** mainRun - parse args and decide what to do
#                      **********************************************************
def mainRun(opts, parser):
    logger.setLevel(opts.loglevel)
    logger.debug("%s starting..." % inspect.stack()[0][3])

    if opts.action == 'convert':
        if not opts.input:
            parser.print_help()
            sys.exit("ERROR: you must specify input file")
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
