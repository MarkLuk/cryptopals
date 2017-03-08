#!python
from utils import *


def int32(x):
    return x&0xFFFFFFFF
    
def padding(input, forged_len=None):
    if forged_len is None:
        ml = len(input)*8
    else:
        ml = forged_len*8
    # Adding 0x80
    pad = bytes([0x80])
    # Num of zeros to add
    num_zeros = 64-((ml//8+1)%64)
    if num_zeros < 8:
        pad += bytes([0]*(num_zeros + 56))
    else:
        pad += bytes([0]*(num_zeros - 8))
    # Append 64bit length
    pad += int_bytes(ml, endianness='big', size=8);
    
    return pad
    
def digest(input, h0 = 0x67452301, h1 = 0xEFCDAB89, h2 = 0x98BADCFE, h3 = 0x10325476, h4 = 0xC3D2E1F0, forged_len=None):
    # Add padding
    input += padding(bytes(input),forged_len)
    # Split into blocks
    blocks = chunks(bytes(input), 64)
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
        # print ('A = ', hex(a))
        # print ('B = ', hex(b))
        # print ('C = ', hex(c))
        # print ('D = ', hex(d))
        # print ('E = ', hex(e))
        
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
        
        # print('H0 = ', hex(h0))
        # print('H1 = ', hex(h1))
        # print('H2 = ', hex(h2))
        # print('H3 = ', hex(h3))
        # print('H4 = ', hex(h4))
        
    #Produce the final hash value (big-endian) as a 160-bit number:
    hh = (h0 << 128) | (h1 << 96) | (h2 << 64) | (h3 << 32) | h4
    return int_bytes(hh, endianness='big',size=160//8)
    
    
def keyed_hash(key, msg):
    return digest(key + msg)
