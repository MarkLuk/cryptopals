#!python
import SHA1
from utils import *

def generate(key, message):
    blk_size = SHA1.block_size
    if (len(key) > blk_size):
        key = SHA1.digest(key)

    if (len(key) < blk_size):
        key = key + bytes([0x00] * (blk_size - len(key)))

    o_key_pad = xor_bytes(bytes([0x5c] * blk_size), key)
    i_key_pad = xor_bytes(bytes([0x36] * blk_size), key)

    return SHA1.digest(o_key_pad + SHA1.digest(i_key_pad + message))
