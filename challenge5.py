#!python
import sys
import utils
   
def encrypt_key(data, key):
    out=[0]*len(data);
    for i in range(len(data)):
        out[i]=data[i]^key[i % len(key)]
    return out
    
# Main entry point
def main(in_file='5.txt', key_str='ICE'):
    # Convert key to bytes
    key_bytes = utils.string_bytes(key_str);
    f = open(in_file, 'r')
    # Agregate file into 1 big string
    bigline=""
    for line in f:
        bigline+=line
    # Prepare plaintext for encryptoin
    plain_bytes = utils.string_bytes(bigline)
    # Encrypt plaintext with key
    enc_bytes = encrypt_key(plain_bytes,key_bytes);
    # Print results
    print(utils.bytes_hexstr(enc_bytes));
    
if __name__ == "__main__":
    main()