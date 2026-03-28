#!/bin/env python

from ctypes import c_uint32 as uint32_t # doubleword
from ctypes import Array

N_POLY_CRC32 = 0x04C11DB7
"""
`x^32 + x^26 + x^23 + ... + x^2 + x + 1`
"""
R_POLY_CRC32 = 0xEDB88320
"""
Reversed(`x^32 + x^26 + x^23 + ... + x^2 + x + 1`)
"""

def gen_crc(POLY: int = N_POLY_CRC32, b_len: int = 32) -> Array[uint32_t]:
    crc_arr: Array[uint32_t] = (uint32_t * 256)(*range(256))

    for ubyts in crc_arr:
        crc = ubyts << (b_len - 8)
        for bit in range(8):
            crc = ((crc << 1) ^ POLY) if crc & (1 << 31) else crc << 1
        crc_arr[ubyts] = crc

    return crc_arr

def rgen_crc(R_POLY: int) -> Array[uint32_t]:
    crc_arr: Array[uint32_t] = (uint32_t * 256)(*range(256))

    for ubyts in crc_arr:
        crc = ubyts
        for bit in range(8):
            crc = ((crc >> 1) ^ R_POLY) if (crc & 1) else crc >> 1
        crc_arr[ubyts] = crc

    return crc_arr
