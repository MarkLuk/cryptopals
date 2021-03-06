#!python
import os
from Crypto.Random import random

# Ceil division
def ceildiv(a,b):
    return (a + (b-1))//b;

# Integer <-> Bytes
def int_bytes(x, endianness='big',size=0):
    return x.to_bytes(size if size!=0 else ceildiv(x.bit_length(),8), endianness)

def bytes_int(bytes, endianness='big'):
    return int.from_bytes(bytes, endianness)

# Hex-String <-> Int
def hexstr_int(hexstr):
    return int(hexstr, 16)

def int_hexstr(int):
    return hex(int)[2:]

# String <-> Bytes
def string_bytes(str):
    return bytearray([ord(x) for x in list(str)])

def bytes_string(bytes):
    str="";
    for b in bytes:
        str+=chr(b);
    return str;

# Hex-String <--> Bytes
def hexstr_bytes(hexstr):
   return int_bytes(hexstr_int(hexstr))

def bytes_hexstr(bs):
   return bytes(bs).hex()

# Random int
def random_num(start=0, end=0x100000000):
    return (bytes_int(random_bytes(4))%(end-start)) + start

# Random bytes
def random_bytes(n):
    return random.getrandbits(8*n).to_bytes(n, byteorder='big')

def random_bool():
    return random_bytes(1)[0] & 1 == 1

# Hamming weight
def hw(n):
    c = 0
    while n!=0:
        c += 1
        n &= n - 1
    return c

# Hamming distance
def hd(x,y):
    return hw(x^y)

# Hamming distance normalized with key length
def hd_normalized(x,y, byte_size):
    return hd(x,y) / (byte_size*8)

# Split list into chunks
def chunks(l, n):
    blocks = []
    for i in range(0, len(l), n):
        blocks.append(l[i:i + n])
    return blocks

def xor_bytes(b1, b2):
    xor = [b1[i] ^ b2[i] for i in range(len(b1))]
    return bytes(xor);

def bit_get(n, i):
    return int((n>>i)&1)

def bit_set(n, i, val):
    if val==0:
        return n & ~(1<<i)
    else:
        return n | (1<<i)

# Rotate left: 0b1001 --> 0b0011
rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))

# Rotate right: 0b1001 --> 0b1100
ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))


def modular_pow(base, exponent, modulus):
    if modulus == 1:
        return 0
    result = 1
    base = base % modulus
    while exponent > 0:
        if (exponent % 2 == 1):
           result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result


