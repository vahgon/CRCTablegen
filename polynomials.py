from ctypes import c_ubyte, c_uint16, c_uint32
from typing import Any, TypeAlias

UnsignedInt:    TypeAlias = (c_uint32 | c_uint16 | c_ubyte)
Unsigned_types: TypeAlias = Any  # c Array hinting in tablegen.py

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
