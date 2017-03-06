#!python 
import challenge19 as ch19
import utils

def main(in_file='20.txt'):
    ciphers = ch19.get_ciphertexts(in_file)
    key_array = ch19.attack_ctr_constant_nonce(ciphers)
    
    for c in ciphers:
        plain = utils.xor_bytes(c, key_array)
        print(plain)
    
if __name__ == "__main__":
    main()