#!python
import os
from Crypto.Random import random

# Ceil division
def ceildiv(a,b): 
    return (a + (b-1))//b;

# Integer <-> Bytes    
def int_bytes(x):
    return x.to_bytes(ceildiv(x.bit_length(),8), 'big')

def bytes_int(bytes):
    return int.from_bytes(bytes, 'big')

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

def bytes_hexstr(bytes):
   return int_hexstr(bytes_int(bytes))

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

