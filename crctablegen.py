#!/bin/env python

import logging
from argparse import ArgumentParser, ArgumentTypeError, Namespace
from ctypes import Array, c_ubyte, c_uint16, c_uint32, sizeof
from dataclasses import dataclass, fields
from functools import partial
from io import StringIO
from itertools import zip_longest
from pathlib import Path
from re import sub
from shutil import copyfileobj
from typing import Any, Callable, TypeAlias, override

logger = logging.getLogger(__name__)

UnsignedInt:   TypeAlias = (c_uint32 | c_uint16 | c_ubyte)
UnsignedTypes: TypeAlias = Any  # for c Array type hinting 
UIntType:      TypeAlias = type[UnsignedInt]

CRCTable:      TypeAlias = Array[UnsignedInt]
SlicedTables:  TypeAlias = list[Array[UnsignedTypes]]

C_DataTypes = {
    8:      ( c_ubyte,   'uint8_t' ),
    16:     ( c_uint16, 'uint16_t' ),
    32:     ( c_uint32, 'uint32_t' ),
}

DefaultPoly = {
     8:     0x31,
    16:     0x1021,
    32:     0x04c11db7,
}
"""
Generator polynomials for: 
    - CRC8  `x^8 + x^5 + x^4 + 1`                    (Dallas 1-wire)
    - CRC16 `x^16 + x^12 + x^5 + 1`                  (x.25 ITU-T protocol)
    - CRC32 `x^32 + x^26 + x^23 + ... + x^2 + x + 1` (File formats/compression, etc...)
"""

DefaultRevPoly = {
     8:     0x8c,
    16:     0x8408,
    32:     0xedb88320,
}
"""
Bit-reversed generator polynomials for:
    - CRC8  `x^8 + x^5 + x^4 + 1`                    (Dallas 1-wire)
    - CRC16 `x^16 + x^12 + x^5 + 1`                  (x.25 ITU-T protocol)
    - CRC32 `x^32 + x^26 + x^23 + ... + x^2 + x + 1` (File formats/compression, etc...)
"""

def gen_crc(uint_type: type[UnsignedInt], poly: int) -> Array[UnsignedInt]:
    """
    Big-Endian implementation
    """
    crc_arr:    Array[UnsignedTypes] = (uint_type * 256)(*range(256))
    b_count:    int = sizeof(uint_type) * 8

    for byte in range(256):
        crc = byte << (b_count - 8)
        for _ in range(8):
            crc = ((crc << 1) ^ poly) if crc & (1 << b_count - 1) else crc << 1
        crc_arr[byte] = crc

    return crc_arr

def rgen_crc(uint_type: type[UnsignedInt], poly) -> Array[UnsignedInt]:
    """
    Little-Endian implementation (reflected generator)
    """
    crc_arr: Array[UnsignedTypes] = (uint_type * 256)(*range(256))

    for byte in range(256):
        crc = byte
        for _ in range(8):
            crc = ((crc >> 1) ^ poly) if crc & 1 else crc >> 1
        crc_arr[byte] = crc

    return crc_arr

def gen_slice_table(uint_type: type[UnsignedInt], t: Array[UnsignedInt], args: Namespace) -> SlicedArrays:
    """
    Function to generate tables for slice-by-4 and slice-by-8 implementations
    """
    num_tables:   int            = 7 if args.slice8 else 3
    slice_tables: SlicedArrays = [((uint_type * 256)(*range(256)))] * num_tables

    slice_tables[0] = t

    for cell in range(256):
        slice_tables[1][cell] = (slice_tables[0][cell] >> 8) ^ slice_tables[0][slice_tables[0][cell]] & 0xff
        slice_tables[2][cell] = (slice_tables[1][cell] >> 8) ^ slice_tables[0][slice_tables[1][cell]] & 0xff
        slice_tables[3][cell] = (slice_tables[2][cell] >> 8) ^ slice_tables[0][slice_tables[2][cell]] & 0xff

        if num_tables == 7:
            slice_tables[4][cell] = (slice_tables[3][cell] >> 8) ^ slice_tables[0][slice_tables[3][cell]] & 0xff
            slice_tables[5][cell] = (slice_tables[4][cell] >> 8) ^ slice_tables[0][slice_tables[4][cell]] & 0xff
            slice_tables[6][cell] = (slice_tables[5][cell] >> 8) ^ slice_tables[0][slice_tables[5][cell]] & 0xff
            slice_tables[7][cell] = (slice_tables[6][cell] >> 8) ^ slice_tables[0][slice_tables[6][cell]] & 0xff

    return slice_tables

def gen_table(args: Namespace) -> None:
    """
    First need to determine whether we are using the LSB or MSB implementation.
    Default will be `gen_crc`() - the MSB implementation - left shift operations.
    """
    @dataclass
    class TableGenOpts:
        c_typ:          type[UnsignedInt]
        polygon:        int

        @override
        def __str__(self) -> str:
            return f'{self.polygon:#x}'
        
        def __iter__(self):
            return (getattr(self, field.name) for field in fields(self))
        
    c_typ:     type[UnsignedInt]
    c_typ_str: str

    (c_typ, c_typ_str) = C_DataTypes[args.degree]

    crc_gen_func: partial[Array[UnsignedInt]] = partial([gen_crc, rgen_crc][args.reflected], uint_type=c_typ)

    if args.poly is None:
        logger.info(" - No generator polygon provided. Using default values for the "
                 + ("LSB" if args.reflected else "MSB") +
                    " implementation of CRC%s", args.degree)

        args.poly = [DefaultPoly, DefaultRevPoly][args.reflected][args.degree]

    getopts: TableGenOpts = TableGenOpts(c_typ, args.poly)
    logger.info(" - Generator polygon set as '%s'", getopts)
    logger.info(" - Type of array elements set to be '%s'", c_typ_str)

    logger.info(" - Generating CRC lookup table...")
    crc_table = crc_gen_func(poly=args.poly)
    logger.info(" - Successfully generated lookup table!")

    table: StringIO
    
    if args.slice4 or args.slice8:
        crc_tables = gen_slice_table(uint_type=c_typ, t=crc_table, args=args)

    if args.output:
        logger.info(" - Printing to file...")

        with open(args.output, 'w') as fd:
            table.seek(0)
            copyfileobj(table, fd)
    else:
        table = output_table(crc_table, args)
        print(table.getvalue())

    return  # Success...

def output_table(crc_table: Array[UnsignedInt], args: Namespace) -> StringIO:
    """
    Table buffer creation

    :ret: `StringIO` of formatted table
    """
    logger.info(" - Retrieving and preparing set formatting args...")

    width       = max(len(f'{hex:x}') for hex in crc_table)
    arr_list    = [(f'{hex:#0{width+2}x}' if args.prefix else f'{hex:0{width}x}') for hex in crc_table]
    cr_val      = args.rlen if args.rlen else (1 if args.vert else (len(arr_list) if args.hori else 8))
    indent      = (int(args.indent) * " " if args.indent != 4 else "\t") if args.indent else ""
    trail_ws    = sub(pattern=r'\s*', repl='', string=args.sep)

    rows        = zip_longest(*[iter(arr_list)] * cr_val, fillvalue=None)
    textio      = StringIO()

    if args.container:
        args.container = { 'b': ["[", "]"], 'c': ["{", "}"] }[args.container]

    logger.info(" - Formatting table...")
    if args.container:
        textio.writelines(args.container[0] + '\n')

    for row in rows:
        textio.writelines(f'{indent}' + args.sep.join(hex for hex in row if hex is not None))
        textio.writelines(trail_ws + '\n')

    if args.container:
        textio.writelines(args.container[1])

    return textio

def polynomial(poly_str: str) -> int:
    if poly_str.startswith('-'):
        raise ArgumentTypeError("invalid polynomial value: '%s'", poly_str)

    poly = int(poly_str, base=16)
    return poly

def main() -> tuple[Namespace, Callable[[], None]]:
    parser          =   ArgumentParser(prog="crctablegen.py", color=False, add_help=False)

    core            =   parser.add_argument_group()
    poly            =   parser.add_argument_group("polygon opts")
    form            =   parser.add_argument_group("formatting opts")

    col_row_opts    =   form.add_mutually_exclusive_group()
    slice_opts      =   poly.add_mutually_exclusive_group()

    #  Generator polygon specific args
    poly.add_argument("-p", "--polynomial", type=polynomial, metavar="HEX",
                      dest="poly", help="the hexadecimal representation of chosen polynomial")

    poly.add_argument("-d", "--degree", type=int, metavar="INT", dest="degree", default=32,
                      choices=(8, 16, 32), help="degree of polynomial (default = 32)")

    poly.add_argument("-r", "--reflect-poly", dest="reflected", action="store_true",
                      help="perform right-shift (LSB) operations on polynomial while computing table")

    slice_opts.add_argument("--sb4", dest="slice4", action="store_true",
                      help="generate 4 lookup tables based on the slicing-by-4 algorithm")

    slice_opts.add_argument("--sb8", dest="slice8", action="store_true",
                      help="generate 8 lookup tables based on the slicing-by-8 algorithm")

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
