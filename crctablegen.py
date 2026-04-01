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

    core    =   parser.add_argument_group()
    poly    =   parser.add_argument_group("polygon opts")
    form    =   parser.add_argument_group("formatting opts")

    #  Generator polygon specific args
    poly.add_argument("-p", "--polynomial", type=polynomial, metavar="POLYNOMIAL", 
                      dest="poly", help="the hexadecimal representation of chosen polynomial")

    poly.add_argument("-d", "--degree", type=int, metavar="INT", dest="degree", default=32,
                      choices=(8, 16, 32), help="polynomial degree. default = 32")

    poly.add_argument("-r", "--reflect-poly", dest="reflected", action="store_true",
                      help="use the LSB implementation when computing table")

    #  Formatting args
    form.add_argument("--json", dest="json", action="store_true", help="convert table to json")

    form.add_argument("--prefix", dest="prefix", action='store_true',
                      help="append `0x` to all table elements")

    form.add_argument("--container", metavar="CHAR", dest="container", choices=['b', 'c'],
                      help="surround entire table in CHAR. choose from ['b'racket, 'c'urly].")

    form.add_argument("--separator", type=str, metavar="CHAR", dest="sep",
                      help="will separate every byte in hex table elements with CHAR.")

    #  Core args
    core.add_argument("-o", "--output", type=Path, metavar="FILE", dest="output",
                      default="./output", help="will write or append table contents to to FILE.")

    core.add_argument("-h", "--help", dest="help", action="store_true", help="display help")

    core.add_argument("-v", "--verbose", dest="verbose", action="store_const",
                      default=logging.WARN, const=logging.INFO,
                      help="suppress all output except for finished table.")

    return (parser.parse_args(), parser.print_help)

def _main() -> None:
    (args, print_func) = main()
    if args.help:
        exit(print_func())

    logging.basicConfig(filename=None, level=args.verbose)
    gen_table(args)

if __name__ == "__main__":
    exit(_main())
