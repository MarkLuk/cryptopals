#!python
import sys
import utils
import AES
import b64
    
# Main entry point
def main(in_file='7.txt', key_str='YELLOW SUBMARINE'):
    # Convert input base64 to byte array
    enc_bytes = b64.decode_file(in_file)
    # Decrypt
    plain_bytes = AES.ECB_decrypt(key_str, enc_bytes)
    # Print output
    print (utils.bytes_string(plain_bytes))
    
if __name__ == "__main__":
    main()