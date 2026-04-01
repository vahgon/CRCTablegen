import json
import logging
from argparse import Namespace
from ctypes import Array, sizeof
from dataclasses import dataclass, fields
from functools import partial
from io import StringIO, TextIOWrapper
from pathlib import Path
import string
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
    crc_arr:    Array[Unsigned_types] = (uint_type * 256)(*range(256))
    b_count:    int = sizeof(uint_type) * 8

    for ubyts in crc_arr:
        crc = ubyts << (b_count - 8)
        for bit in range(8):
            crc = ((crc << 1) ^ poly) if crc & (1 << b_count - 1) else crc << 1
        crc_arr[ubyts] = crc

    return crc_arr

def rgen_crc(uint_type: type[UnsignedInt], poly) -> Array[UnsignedInt]:
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
    Default will be `gen_crc`() - the MSB implementation - left shifts.
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
        logger.info(" - No generator polygon provided. Using default values for "
                    + ("LSB" if args.reflected else "MSB") +
                    " implementation of degree %s" % args.degree)

        args.poly = [DefaultPoly, DefaultRevPoly][args.reflected][args.degree]

    getopts: TableGenOpts = TableGenOpts(c_typ, args.poly)
    logger.info(" - Generator polygon set as '%s'" % getopts)
    logger.info(" - Type of array elements set to be '%s'" % c_typ_str)
    logger.info(" - Generating CRC lookup table...")

    output_table(crc_gen_func(poly=args.poly), args)

def output_table(crc_table: Array[UnsignedInt], args: Namespace) -> None:
    logger.info(" - Successfully generated lookup table")

    #  {width + 2} to account for '0x' when --prefix in argv
    width = max(len(f'{hex:x}') for hex in crc_table)

    logger.info(" - Converting C Array to python list")
    arr_list = [(f'{hex:#0{width+2}x}' if args.prefix else f'{hex:0{width}x}') for hex in crc_table]

    logger.info(" - Converting list to conform with user's specified formatting")
    out_table = str(('{\n\t' if args.container == "c" else '[\n\t') if args.container else "\t")
    for idx, hex in enumerate(arr_list):
        if (idx + 1) % 8 == 0:
            out_table+=(f'{hex}\n\t')
        else:
            out_table+=(f'{hex}, ')

    logger.info(" - Writing output to '%s'" % Path(args.output).absolute())
    if args.output:
        with open(args.output,'w') as rf:
            rf.write(out_table)
            rf.close()

    if args.json:
        output_json(arr_list, args.output)

def output_json(arr_list: list[str], output: Path) -> None:
    io_text: (TextIOWrapper | str | None)

    path = Path(output).with_suffix('.json')

    if path.exists():
        logger.warning(" - '%s' already exists, ignoring '--json'" % path.absolute())
        return

    logger.info("Creating new json file in write mode...")
    io_text = path.open('w')

    logger.info("Writing json file to %s..." % path)
    json.dump(arr_list, io_text, indext=4)

    io_text.close()
    
    return
