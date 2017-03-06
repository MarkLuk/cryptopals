#!python

import utils
import AES
import b64
import challenge03 as ch3

key = AES.randomKey();

def get_ciphertexts(file):
    ciphers = []
    f = open(file, 'r');
    for line in f:
        line = line.rstrip('\r\n')
        bytes = b64.decode(line)
        ciphers.append(AES.CTR_encrypt(key, bytes, 0))

    return ciphers

def attack_ctr_constant_nonce(ciphers):
    cipher_len = 0
    key_array = []
    # Find maximum length
    for c in ciphers:
        if (len(c)>cipher_len):
            cipher_len = len(c)
            
    for code in range(cipher_len):
        chars = []
        for c in ciphers:
            if (code < len(c)):
                chars.append(c[code])
                
        key = ch3.XOR_1B_guess_key(chars)
        key_array += [key[0]]

    return key_array
    
def main(in_file='19.txt'):
    ciphers = get_ciphertexts(in_file)
    key_array = attack_ctr_constant_nonce(ciphers)
    
    for c in ciphers:
        plain = utils.xor_bytes(c, key_array)
        print(plain)
    
if __name__ == "__main__":
    main()
