from ctypes import c_uint8, c_uint16, c_uint32

from enum import IntEnum
from typing import Any, TypeAlias

UnsignedInt:   TypeAlias = (c_uint32 | c_uint16 | c_uint8)
unsigned_type: TypeAlias = Any  # alias for type hints

n_crc = {
     8:   (c_uint8,   'uint8_t', 0x31,       '0x31'),
    16:   (c_uint16, 'uint16_t', 0x1021,     '0x1021'),
    32:   (c_uint32, 'uint32_t', 0x04c11db7, '0x04c11db7'),
}
"""
Generator polynomials for: 
    - CRC8  `x^8 + x^5 + x^4 + 1`                    (Dallas 1-wire)
    - CRC16 `x^16 + x^12 + x^5 + 1`                  (x.25 ITU-T protocol)
    - CRC32 `x^32 + x^26 + x^23 + ... + x^2 + x + 1` (File formats/compression, etc...)
"""

r_crc = {
     8:   (c_uint8,   'uint8_t', 0x8c,       '0x8c'),
    16:   (c_uint16, 'uint16_t', 0x8408,     '0x8408'),
    32:   (c_uint32, 'uint32_t', 0xedb88320, '0xedb88320'),
}
"""
Bit-reversed generator polynomials for:
    - CRC8  `x^8 + x^5 + x^4 + 1`                    (Dallas 1-wire)
    - CRC16 `x^16 + x^12 + x^5 + 1`                  (x.25 ITU-T protocol)
    - CRC32 `x^32 + x^26 + x^23 + ... + x^2 + x + 1` (File formats/compression, etc...)
"""

class ByteEnum(IntEnum):
    TYPE        = 0
    TYPE_STR    = 1
    HEX         = 2
    HEX_STR     = 3
