#!python
import sys

def string2bytes(str):
    return [ord(x) for x in list(str)]

def encrypt_key(data, key):
    out=[0]*len(data);
    for i in range(len(data)):
        out[i]=data[i]^key[i % len(key)]
    return out
    
# Main entry point
def main():
    in_file = sys.argv[1];
    key = sys.argv[2];
    # Convert key to bytes
    key_bytes = string2bytes(key);
    f = open(in_file, 'r')
    bigline=""
    for line in f:
        bigline+=line
    enc_line=encrypt_key(string2bytes(bigline),key_bytes);
    print(''.join('%02x'%i for i in enc_line));
    
if __name__ == "__main__":
    main()