#!python
import utils
from MT19937 import MT19937
import time

key = utils.random_num(0, 2**16);

def MT19937_encrypt(key, stream):
    prng = MT19937(key)
    return bytes([(x^prng.get_num())&0xFF for x in stream])
    
def MT19937_decrypt(key, stream):
    return MT19937_encrypt(key, stream)

def encryption_oracle(plain):
    prefix = utils.random_bytes(utils.random_num(10,20))
    return MT19937_encrypt(key, prefix + plain)

def recover_key(plaintext):
    # Perform encryption by oracle
    ciphertext = encryption_oracle(plaintext);
    # Recover prefix size
    prefix_size = len(ciphertext) - len(plaintext)
    # Brute-force key
    for k in range(2**16):
        dec = MT19937_decrypt(k, ciphertext)
        if (dec[prefix_size:]==plaintext):
            return k;
    print ('Key not found')

def pwd_reset_token():
    return MT19937_encrypt(int(time.time()), bytes([0]*utils.random_num(10,20)));
    
def pwd_token_current_time(token):
    if (token == MT19937_encrypt(int(time.time()), bytes([0]*len(token)))):
        return True
    return False

def main():
    plaintext = b'AAAAAAAAAAAAAA'
    print ('Real key = ', key)
    # Try to recover the key
    rec_key = recover_key(plaintext)
    print ('Recovered key = ', rec_key)
    
    token = pwd_reset_token();
    if (pwd_token_current_time(token)):
        print ('Password reset token was generated NOW')
    
    
if __name__ == "__main__":
    main()