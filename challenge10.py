#! python
import utils
import challenge02 as ch2
import challenge06 as ch6
import challenge07 as ch7
import challenge09 as ch9
from Crypto.Cipher import AES

def AES_CBC_encrypt(key, data, iv):
    # Padding data
    padded_data = ch9.padPKCS7(data, AES.block_size);
    # Split to blocks
    blocks = ch6.chunks(padded_data, AES.block_size)
    # Perform CBC loop
    out=bytearray();
    for b in blocks:
        # Ecrypt block
        cipher = ch7.AES_ECB_encrypt(key, ch2.xor_bytes(iv, b))
        # Attach to output
        out += cipher
        # Set next IV
        iv = out
    return out;

def AES_CBC_decrypt(key, data, iv):
    # Split to blocks
    blocks = ch6.chunks(data, AES.block_size)
    # Perform CBC loop
    out=bytearray();
    for b in blocks:
        # Ecrypt block
        plain = ch2.xor_bytes(ch7.AES_ECB_decrypt(key, b), iv);
        # Attach to output
        out += plain
        # Set next IV
        iv = b
    # String padding
    return ch9.unpadPKCS7(out);
    
def main(file_name='10.txt', key='YELLOW SUBMARINE'):
    # Extract raw data from file
    bytes=ch6.base64file_bytes(file_name)
    # Set default IV
    iv = bytearray([0]*AES.block_size)
    # Decrypt the file
    plain = AES_CBC_decrypt(key,bytes,iv)
    # Print output
    print(utils.bytes_string(plain));
    
if __name__ == "__main__":
    main()
    