#!python
from utils import *
import AES
import b64

key=AES.randomKey();
nonce=AES.randomNonce();

def get_ciphertext(in_file, ecb_key):
    # Convert input base64 to byte array
    enc_bytes = b64.decode_file(in_file)
    # Decrypt ECB file
    plaintext = AES.ECB_decrypt(ecb_key, enc_bytes)
    # Encrypt with CTR
    return AES.CTR_encrypt(key, plaintext, nonce);

def edit(ciphertext, offset, newtext):
    input = bytes([0]*offset) + bytes(newtext)
    new_cipher = AES.CTR_encrypt(key, input, nonce)
    return ciphertext[:offset] + new_cipher[offset:]

def main(in_file='25.txt', ecb_key='YELLOW SUBMARINE'):
    # Get cipher text
    ciphertext = get_ciphertext(in_file, ecb_key)
    # Send ciphertext as 'new text'. Double encryption with CTR will 
    # cancel-out revealing the plaintext
    plaintext = edit(ciphertext, 0, ciphertext);
    print (bytes_string(plaintext))
    
if __name__ == "__main__":
    main()