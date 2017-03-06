#!python

import AES
import utils
import b64

secret_key = AES.randomKey()
secret_iv = AES.randomIV()

ciphers = [ 'MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=',
            'MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=',
            'MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==',
            'MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==',
            'MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl',
            'MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==',
            'MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==',
            'MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=',
            'MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=',
            'MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93' ]

def get_random_string():
    return b64.decode(ciphers[utils.random_num()%len(ciphers)])
    
def get_encrypted_msg():
    return AES.CBC_encrypt(secret_key, get_random_string(), secret_iv), secret_iv

def padding_oracle(cipher, custom_iv):
    try:
        plain = AES.CBC_decrypt(secret_key, bytes(cipher), bytes(custom_iv));
    except Exception as error:
        return False;
    return True;

def generate_custom_C1(P2, b, i):
    if b!=1:
        return bytes([0xFF]*(AES.block_size-b) + [i] + [x^b for x in P2[-(b-1):]])
    else:
        return bytes([0xFF]*(AES.block_size-b) + [i])
    
def cbc_padding_oracle_attack(enc, iv):
    block = utils.chunks(iv + enc, AES.block_size);
    result = []
    # Perform attack on each block pair (i-1,i)
    for i in reversed(range(1, len(block))):
        C2 = block[i]
        C1 = block[i-1]
        I2 = [0]*AES.block_size
        P2 = [0]*AES.block_size
        # Guess each byte in the block
        for byte in range(AES.block_size):
            exp_len = byte+1
            # Brute force all byte options
            for guess in range(256):
                custom_C1 = generate_custom_C1(I2, exp_len, guess)
                if padding_oracle(C2, custom_C1):
                    I2[-exp_len] = guess^exp_len;
                    P2[-exp_len] = I2[-exp_len]^C1[-exp_len]
                    break;
                    
        # Adding plaintext to result
        result.insert(0, P2)
    
    # Flatten result
    result = bytes([j for i in result for j in i])

    # Strip padding
    return AES.unpadPKCS7(result);

def main():
    for i in range(50):
        enc, iv = get_encrypted_msg()
        plain = cbc_padding_oracle_attack(enc, iv)
        print (plain);
    
if __name__ == "__main__":
    main()