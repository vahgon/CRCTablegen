#!/bin/env python

import logging
from argparse import ArgumentParser, ArgumentTypeError, Namespace
from pathlib import Path
from typing import Callable

from gen import gen_table

logger = logging.getLogger(__name__)

def polynomial(poly_str: str) -> int:
    if poly_str.startswith('-'):
        raise ArgumentTypeError("invalid polynomial value: '%s'" % poly_str)

    poly = int(poly_str, base=16)
    return poly

def main() -> tuple[Namespace, Callable[[], None]]:
    parser  =   ArgumentParser(prog="crctablegen.py", color=False, add_help=False)

    core            =   parser.add_argument_group()
    poly            =   parser.add_argument_group("polygon opts")
    form            =   parser.add_argument_group("formatting opts")

    col_row_opts    =   form.add_mutually_exclusive_group()

    #  Generator polygon specific args
    poly.add_argument("-p", "--polynomial", type=polynomial, metavar="HEX",
                      dest="poly", help="the hexadecimal representation of chosen polynomial")

    poly.add_argument("-d", "--degree", type=int, metavar="INT", dest="degree", default=32,
                      choices=(8, 16, 32), help="degree of polynomial (default = 32)")

    poly.add_argument("-r", "--reflect-poly", dest="reflected", action="store_true",
                      help="perform right-shift (LSB) operations on polynomial while computing table")

    #  Formatting args
    form.add_argument("-c", "--container", metavar="STR", dest="container", choices=['b', 'c'],
                      help="surround entire table in STR - choose from ['b'racket, 'c'urly].")

    form.add_argument("-s", "--separator", type=str, metavar="STR", dest="sep", default=" ",
                      help="will separate elements with STR (default = \" \")")

    form.add_argument("-i", "--indent", type=str, metavar="INT", dest="indent",
                      help="specify indent width (default = 0)")

    form.add_argument("--prefix", dest="prefix", action='store_true',
                      help="append `0x` to all table elements")

    col_row_opts.add_argument("--row-len", type=int, metavar="INT", dest='rlen',
                              help="specify the amount of table elements to append to a given line")

    col_row_opts.add_argument("--horizontal", action="store_true", dest="hori",
                              help="output all table elements on the same line")

    col_row_opts.add_argument("--vertical", action="store_true", dest="vert",
                              help="output each table element on a newline")

    #  Core args
    core.add_argument("-o", "--output", type=Path, metavar="FILE", dest="output",
                      help="write lookup table to FILE")

    core.add_argument("-h", "--help", dest="help", action="store_true", help="display help")

    core.add_argument("-v", "--verbose", dest="verbose", action="store_const",
                      default=logging.WARN, const=logging.INFO,
                      help="print updates from the logger as script executes")

    return (parser.parse_args(), parser.print_help)

def _main() -> None:
    (args, print_func) = main()
    if args.help:
        exit(print_func())

    logging.basicConfig(filename=None, level=args.verbose)
    gen_table(args)

if __name__ == "__main__":
    exit(_main())
