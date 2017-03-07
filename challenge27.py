#!python

import AES
from utils import *

key = AES.randomKey()
iv = bytes(key)


def enc(url):
    return AES.CBC_encrypt(key, url, iv)

def is_ascii(data):
    for b in data:
        if b>127:
            return False
    return True
    
def dumb_dec(cipher):
    plain = AES.CBC_decrypt(key, bytes(cipher), iv)
    if (not (is_ascii(plain))):
        raise ValueError(plain);
    return plain
    
def main():
    url = b'https://cryptopals.com/sets/4/challenges/27                     '
    # Encrypt URL
    cipher = enc(url)
    # Attack the ciphertext + add correct padding
    attack_cipher = cipher[0:16] + bytes([0]*16) + cipher[0:16] + cipher[48:]
    #Decrypt attacked ciphertext
    plain=b''
    try:
        plain = dumb_dec(attack_cipher)
    except Exception as error:
        plain = bytes(error.args[0])
    
    # Recover IV (which is the key)
    recover_key = xor_bytes(plain[0:16], plain[32:48]);
    print ('Recover key = ', list(recover_key))
    print ('Real key    = ', list(key))
    
    
if __name__ == "__main__":
    main()
