#!python

import AES
from challenge16 import prepareUserData, parseData

key = AES.randomKey()
nonce = AES.randomNonce();

def encData(data):
    return bytearray(AES.CTR_encrypt(key, prepareUserData(data), nonce))
    
def decData(data):
    return AES.CTR_decrypt(key, bytes(data), nonce)

def main():
    data = b'aaaaaaaaaaaaaaaa:admin<true'
    enc  = encData(data)
    enc[48] ^= 1;
    enc[54] ^= 1;
    parseData(decData(enc))

if __name__ == "__main__":
    main() 