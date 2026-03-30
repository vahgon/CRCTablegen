from ctypes import Array

from polynomials import UnsignedInt, unsigned_type


def gen_crc(POLY: int, bit_count: int, uint_type: type[UnsignedInt]) -> Array[UnsignedInt]:
    crc_arr: Array[unsigned_type] = (uint_type * 256)(*range(256))

    for ubyts in crc_arr:
        crc = ubyts << (bit_count - 8)
        for bit in range(8):
            crc = ((crc << 1) ^ POLY) if crc & (1 << 31) else crc << 1
        crc_arr[ubyts] = crc

    return crc_arr

def rgen_crc(R_POLY: int, uint_type: type[UnsignedInt]) -> Array[UnsignedInt]:
    crc_arr: Array[unsigned_type] = (uint_type * 256)(*range(256))

    for ubyts in crc_arr:
        crc = ubyts
        for bit in range(8):
            crc = ((crc >> 1) ^ R_POLY) if (crc & 1) else crc >> 1
        crc_arr[ubyts] = crc

    return crc_arr
