#!python
import sys
import challenge06 as ch6
import utils
import AES

    
# Main entry point
def main(in_file='7.txt', key_str='YELLOW SUBMARINE'):
    f = open(in_file, 'r');
    bigline="";
    # Convert input base64 to byte array
    for line in f:
        bigline+=line.rstrip('\r\n')
    enc_bytes = ch6.base64_bytes(bigline)
    # Decrypt
    plain_bytes = AES.ECB_decrypt(key_str, enc_bytes)
    # Print output
    print (utils.bytes_string(plain_bytes))
    
    
if __name__ == "__main__":
    main()