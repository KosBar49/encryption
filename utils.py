import struct

def get_mantissa(f: float) -> int:
    # Pack the float into 4 bytes (as in C++), then unpack the first byte
    bytes_ = struct.pack('f', f)
    return bytes_[0]