#!python
from utils import *

def _f(x, y, z): return x & y | ~x & z
def _g(x, y, z): return x & y | x & z | y & z
def _h(x, y, z): return x ^ y ^ z

def _f1(a, b, c, d, k, s, X): return rol(a + _f(b, c, d) + X[k], s, 32)
def _f2(a, b, c, d, k, s, X): return rol(a + _g(b, c, d) + X[k] + 0x5a827999, s, 32)
def _f3(a, b, c, d, k, s, X): return rol(a + _h(b, c, d) + X[k] + 0x6ed9eba1, s, 32)

def padding(msg, forged_len=None):
    if forged_len is None:
        bit_len = len(msg) * 8
    else:
        bit_len = forged_len * 8

    index = (bit_len >> 3) & 0x3f
    pad_len = 120 - index
    if index < 56:
        pad_len = 56 - index
    padding = b'\x80' + b'\x00'*63
    return padding[:pad_len] + int_bytes(bit_len, 'little', size=8)

def digest(message_string, A=0x67452301, B=0xefcdab89, C=0x98badcfe, D=0x10325476, forged_size=None):
    msg = bytes(message_string)
    msg_bytes = msg + padding(msg, forged_size)
    for i in range(0, len(msg_bytes), 64):
        block = msg_bytes[i:i+64]
        a, b, c, d = A, B, C, D
        x = []
        for j in range(0, 64, 4):
            x.append(bytes_int(block[j:j+4],'little'))

        a = _f1(a,b,c,d, 0, 3, x)
        d = _f1(d,a,b,c, 1, 7, x)
        c = _f1(c,d,a,b, 2,11, x)
        b = _f1(b,c,d,a, 3,19, x)
        a = _f1(a,b,c,d, 4, 3, x)
        d = _f1(d,a,b,c, 5, 7, x)
        c = _f1(c,d,a,b, 6,11, x)
        b = _f1(b,c,d,a, 7,19, x)
        a = _f1(a,b,c,d, 8, 3, x)
        d = _f1(d,a,b,c, 9, 7, x)
        c = _f1(c,d,a,b,10,11, x)
        b = _f1(b,c,d,a,11,19, x)
        a = _f1(a,b,c,d,12, 3, x)
        d = _f1(d,a,b,c,13, 7, x)
        c = _f1(c,d,a,b,14,11, x)
        b = _f1(b,c,d,a,15,19, x)

        a = _f2(a,b,c,d, 0, 3, x)
        d = _f2(d,a,b,c, 4, 5, x)
        c = _f2(c,d,a,b, 8, 9, x)
        b = _f2(b,c,d,a,12,13, x)
        a = _f2(a,b,c,d, 1, 3, x)
        d = _f2(d,a,b,c, 5, 5, x)
        c = _f2(c,d,a,b, 9, 9, x)
        b = _f2(b,c,d,a,13,13, x)
        a = _f2(a,b,c,d, 2, 3, x)
        d = _f2(d,a,b,c, 6, 5, x)
        c = _f2(c,d,a,b,10, 9, x)
        b = _f2(b,c,d,a,14,13, x)
        a = _f2(a,b,c,d, 3, 3, x)
        d = _f2(d,a,b,c, 7, 5, x)
        c = _f2(c,d,a,b,11, 9, x)
        b = _f2(b,c,d,a,15,13, x)

        a = _f3(a,b,c,d, 0, 3, x)
        d = _f3(d,a,b,c, 8, 9, x)
        c = _f3(c,d,a,b, 4,11, x)
        b = _f3(b,c,d,a,12,15, x)
        a = _f3(a,b,c,d, 2, 3, x)
        d = _f3(d,a,b,c,10, 9, x)
        c = _f3(c,d,a,b, 6,11, x)
        b = _f3(b,c,d,a,14,15, x)
        a = _f3(a,b,c,d, 1, 3, x)
        d = _f3(d,a,b,c, 9, 9, x)
        c = _f3(c,d,a,b, 5,11, x)
        b = _f3(b,c,d,a,13,15, x)
        a = _f3(a,b,c,d, 3, 3, x)
        d = _f3(d,a,b,c,11, 9, x)
        c = _f3(c,d,a,b, 7,11, x)
        b = _f3(b,c,d,a,15,15, x)

        # update state
        A = (A + a) & 0xffffffff
        B = (B + b) & 0xffffffff
        C = (C + c) & 0xffffffff
        D = (D + d) & 0xffffffff

    return  int_bytes(A, endianness='little',size=4) +        \
            int_bytes(B, endianness='little',size=4) +        \
            int_bytes(C, endianness='little',size=4) +        \
            int_bytes(D, endianness='little',size=4)

def keyed_hash(key, msg):
    return digest(key + msg)

if __name__ == '__main__':

    def Check(msg, sig):
        #print (msg, digest(msg),sig)
        print (bytes_hexstr(digest(msg))==sig)


    Check(b'', '31d6cfe0d16ae931b73c59d7e0c089c0')
    Check(b'a', 'bde52cb31de33e46245e05fbdbd6fb24')
    Check(b'abc', 'a448017aaf21d8525fc10ae87aa6729d')
    Check(b'message digest',
            'd9130a8164549fe818874806e1c7014b')
    Check(b'abcdefghijklmnopqrstuvwxyz',
            'd79e1c308aa5bbcdeea8ed63df412da9')
    Check(b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',
            '43f8582f241db351ce627e153e7f0e4')
    Check(b'12345678901234567890123456789012345678901234567890123456789012345678901234567890',
            'e33b4ddc9c38f2199c3e7b164fcc0536')
