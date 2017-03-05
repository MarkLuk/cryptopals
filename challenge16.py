#!python

import AES
import utils

key = AES.randomKey()
iv = AES.randomIV();

def prepareUserData(data):
    data = data.replace(b';',b'').replace(b'=',b'');
    return b'comment1=cooking%20MCs;userdata=' + data + b';comment2=%20like%20a%20pound%20of%20bacon'
    
def encData(data):
    return bytearray(AES.CBC_encrypt(key, prepareUserData(data), iv))
    
def decData(data):
    return AES.CBC_decrypt(key, bytes(data), iv)

def parseData(data):
    pairs = data.split(b';')
    for p in pairs:
        v =p.split(b'=')
        print (bytes(v[0]), bytes(v[1]))
    
    
def main():
    data = b'aaaaaaaaaaaaaaaa:admin<true'
    enc  = encData(data)
    enc[32] ^= 1;
    enc[38] ^= 1;
    parseData(decData(enc))

if __name__ == "__main__":
    main()
