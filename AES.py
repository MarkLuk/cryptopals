#!python
import utils
import Crypto.Cipher.AES as CryptAES

block_size = CryptAES.block_size

def randomKey():
    return  bytes(utils.random_bytes(16))
    
def randomIV():
    return utils.random_bytes(16)
 
def padPKCS7(bytes, size):
    padSize = size - (len(bytes) % size);
    if padSize == 0:
        padSize = size
    return bytes + bytearray([padSize]*padSize);

def verifyUnpadPKCS7(bytes):
    pad_size = bytes[-1]
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
    return cipher.encrypt(padPKCS7(bytes, CryptAES.block_size))

def ECB_decrypt(key_str, bytes):
    iv = '';
    cipher = CryptAES.new(key_str, CryptAES.MODE_ECB, iv)
    return unpadPKCS7(cipher.decrypt(bytes))
    
def CBC_encrypt(key, data, iv):
    # Padding data
    padded_data = padPKCS7(data, CryptAES.block_size);
    # Split to blocks
    blocks = utils.chunks(padded_data, CryptAES.block_size)
    # Perform CBC loop
    out=bytearray();
    for b in blocks:
        # Ecrypt block
        cipher = ECB_encrypt_raw(key, utils.xor_bytes(iv, b))
        # Attach to output
        out += cipher
        # Set next IV
        iv = cipher
    return out;

def CBC_decrypt(key, data, iv):
    # Split to blocks
    blocks = utils.chunks(data, CryptAES.block_size)
    # Perform CBC loop
    out=bytearray();
    for b in blocks:
        # Ecrypt block
        plain = utils.xor_bytes(ECB_decrypt_raw(key, b), iv);
        # Attach to output
        out += plain
        # Set next IV
        iv = b
    # String padding
    return unpadPKCS7(out);
