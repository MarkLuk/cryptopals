#!python
from utils import *
import Crypto.Cipher.AES as CryptAES

block_size = CryptAES.block_size

def randomKey():
    return  bytes(random_bytes(16))
    
def randomIV():
    return random_bytes(16)
 
def randomNonce():
    return bytes_int(random_bytes(8))


def padPKCS7(bytes, size=CryptAES.block_size):
    padSize = size - (len(bytes) % size);
    if padSize == 0:
        padSize = size
    return bytes + bytearray([padSize]*padSize);

def verifyUnpadPKCS7(bytes):
    pad_size = bytes[-1]
    if (pad_size==0) or (pad_size > CryptAES.block_size):
        raise Exception('Padding is incorrect');
    for i in range(1, pad_size+1):
        if (bytes[-i] != pad_size):
            raise Exception('Padding is incorrect');
    return bytes[:-pad_size];
            
def unpadPKCS7(bytes):
    pad_size = bytes[len(bytes)-1]
    return bytes[:-pad_size];

def ECB_encrypt_raw(key_str, bytes):
    iv = '';
    cipher = CryptAES.new(key_str, CryptAES.MODE_ECB, iv)
    return cipher.encrypt(bytes)

def ECB_decrypt_raw(key_str, bytes):
    iv = '';
    cipher = CryptAES.new(key_str, CryptAES.MODE_ECB, iv)
    return cipher.decrypt(bytes)
    
def ECB_encrypt(key_str, bytes):
    iv = '';
    cipher = CryptAES.new(key_str, CryptAES.MODE_ECB, iv)
    return cipher.encrypt(padPKCS7(bytes))

def ECB_decrypt(key_str, bytes):
    iv = '';
    cipher = CryptAES.new(key_str, CryptAES.MODE_ECB, iv)
    return verifyUnpadPKCS7(cipher.decrypt(bytes))
    
def CBC_encrypt(key, data, iv):
    # Padding data
    padded_data = padPKCS7(data);
    # Split to blocks
    blocks = chunks(padded_data, CryptAES.block_size)
    # Perform CBC loop
    out=bytearray();
    for b in blocks:
        # Ecrypt block
        cipher = ECB_encrypt_raw(key, xor_bytes(iv, b))
        # Attach to output
        out += cipher
        # Set next IV
        iv = cipher
    return out;

def CBC_decrypt(key, data, iv):
    # Split to blocks
    blocks = chunks(data, CryptAES.block_size)
    # Perform CBC loop
    out=bytearray();
    for b in blocks:
        # Ecrypt block
        plain = xor_bytes(ECB_decrypt_raw(key, b), iv);
        # Attach to output
        out += plain
        # Set next IV
        iv = b
    # Remove padding
    return verifyUnpadPKCS7(out)

def CTR_encrypt(key, data, nonce):
    ctr = 0
    # Split to blocks
    blocks = chunks(data, CryptAES.block_size)
    out=bytearray();
    for b in blocks:
        # Ecrypt block
        ctr_bytes = int_bytes(ctr<<64 | nonce, 'little', 128//8)
        plain = xor_bytes(b, ECB_encrypt_raw(key, ctr_bytes))
        out += plain
        ctr += 1
    return out

def CTR_decrypt(key, data, nonce):
    return CTR_encrypt(key, data, nonce)
