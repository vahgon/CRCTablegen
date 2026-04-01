import logging
from argparse import Namespace
from ctypes import Array, sizeof
from dataclasses import dataclass, fields
from functools import partial
from io import StringIO
from itertools import zip_longest
from pathlib import Path
from re import sub
from typing import override

from polynomials import (
    C_DataTypes,
    DefaultPoly,
    DefaultRevPoly,
    Unsigned_types,
    UnsignedInt,
)

logger = logging.getLogger(__name__)

def gen_crc(uint_type: type[UnsignedInt], poly: int) -> Array[UnsignedInt]:
    """
    MSB implementation
    """
    crc_arr:    Array[Unsigned_types] = (uint_type * 256)(*range(256))
    b_count:    int = sizeof(uint_type) * 8

    for ubyts in crc_arr:
        crc = ubyts << (b_count - 8)
        for bit in range(8):
            crc = ((crc << 1) ^ poly) if crc & (1 << b_count - 1) else crc << 1
        crc_arr[ubyts] = crc

    return crc_arr

def rgen_crc(uint_type: type[UnsignedInt], poly) -> Array[UnsignedInt]:
    """
    LSB implementation (reflected poly)
    """
    crc_arr: Array[Unsigned_types] = (uint_type * 256)(*range(256))

    for ubyts in crc_arr:
        crc = ubyts
        for bit in range(8):
            crc = ((crc >> 1) ^ poly) if (crc & 1) else crc >> 1
        crc_arr[ubyts] = crc

    return crc_arr

def gen_table(args: Namespace) -> None:
    """
    First need to determine whether we are using the LSB or MSB implementation.
    Default will be `gen_crc`() - the MSB implementation - left shift operations.
    """
    @dataclass()
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

    (c_typ, c_typ_str)  = C_DataTypes[args.degree]
    crc_gen_func: partial[Array[UnsignedInt]] = partial([gen_crc, rgen_crc][args.reflected], uint_type=c_typ)

    if args.poly is None:
        logger.info(" - No generator polygon provided. Using default values for the "
                 + ("LSB" if args.reflected else "MSB") +
                    " implementation of CRC%s" % args.degree)

        args.poly = [DefaultPoly, DefaultRevPoly][args.reflected][args.degree]

    getopts: TableGenOpts = TableGenOpts(c_typ, args.poly)

    logger.info(" - Generator polygon set as '%s'" % getopts)
    logger.info(" - Type of array elements set to be '%s'" % c_typ_str)

    logger.info(" - Generating CRC lookup table...")
    table = output_table(crc_gen_func(poly=args.poly), args)

    logger.info(" - Successfully generated lookup table!")
    return

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

    rows        = zip_longest(*[iter(arr_list)] * cr_val, fillvalue=args.sep)
    textio      = StringIO()

    if args.container:
        args.container = { 'b': ["[", "]"], 'c': ["{", "}"] }[args.container]

    logger.info(" - Formatting table...")
    if args.container:
        textio.writelines(args.container[0] + '\n')

    for row in rows:
        textio.writelines(f'{indent}' + args.sep.join(hex for hex in row if row != ''))
        textio.writelines(trail_ws + '\n')

    if args.container:
        textio.writelines(args.container[1])

    return textio
