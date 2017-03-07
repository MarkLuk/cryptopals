#!python
from utils import *


# Rotate left: 0b1001 --> 0b0011
rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))
 
# Rotate right: 0b1001 --> 0b1100
ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

def int32(x):
    return x&0xFFFFFFFF
    
def padding(input):
    ml = len(input)*8
    # Adding 0x80
    input = bytes(input) + bytes([0x80])
    # Num of zeros to add
    num_zeros = 64-(len(input)%64)
    if num_zeros < 8:
        input += bytes([0]*(64 - num_zeros + 76))
    else:
        input += bytes([0]*(num_zeros - 8))
    # Append 64bit length
    input += int_bytes(ml, endianness='big', size=8);
    
    return input
    
def digest(input):
    # Set constants
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0
    # Add padding
    input = padding(input)
    # Split into blocks
    blocks = chunks(input, 64)
    w = [0]*80
    # Process each block
    for b in blocks:
        # Split each block in 32bit variables
        wb = chunks(b, 4)
        for i in range(16):
            w[i]=bytes_int(wb[i], endianness='big')
        for i in range(16, 80):
            w[i] = int32(rol(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1, 32))
    
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
    
        #Main loop
        for i in range(80):
            if i<20:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            else:
                if i < 40:
                    f = b ^ c ^ d
                    k = 0x6ED9EBA1
                else: 
                    if i < 60:
                        f = (b & c) | (b & d) | (c & d) 
                        k = 0x8F1BBCDC
                    else: 
                        f = b ^ c ^ d
                        k = 0xCA62C1D6
    
            temp = int32(rol(a, 5, 32) + f + e + k + w[i])
            e = d
            d = c
            c = rol(b,30, 32)
            b = a
            a = temp
    
        #Add this chunk's hash to result so far:
        h0 = int32(h0 + a)
        h1 = int32(h1 + b) 
        h2 = int32(h2 + c)
        h3 = int32(h3 + d)
        h4 = int32(h4 + e)

    #Produce the final hash value (big-endian) as a 160-bit number:
    hh = (h0 << 128) | (h1 << 96) | (h2 << 64) | (h3 << 32) | h4
    return int_bytes(hh, endianness='big',size=160//8)
    
    
def keyed_hash(key, msg):
    return digest(key + msg)
