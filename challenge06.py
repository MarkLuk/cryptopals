#!python
import sys
import challenge03 as ch3;
import challenge05 as ch5;
import utils
import numpy as np

# Hamming weight
def hw(n):
    c = 0
    while n!=0:
        c += 1
        n &= n - 1
    return c

# Hamming distance    
def hd(x,y):
    return hw(x^y)
# Hamming distance normalized with key length
def hd_normalized(x,y, byte_size):
    return hd(x,y) / (byte_size*8)

# Converts Base64 to byte array   
def base64_bytes(base64):
    b64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    x = 0;
    for b in base64:
        if (b=='='):
            y = 0
        else:
            y = b64.index(b)
        x = (x << 6) | y
    return utils.int_bytes(x)

# Get heuristical scoring per key size    
def get_keysize_score(enc_bytes, keysize):
    x1=utils.bytes_int(enc_bytes[0:keysize]);
    x2=utils.bytes_int(enc_bytes[1*keysize:2*keysize]);
    x3=utils.bytes_int(enc_bytes[2*keysize:3*keysize]);
    x4=utils.bytes_int(enc_bytes[3*keysize:4*keysize]);
    score= (hd_normalized(x1, x2, keysize) + 
            hd_normalized(x2, x3, keysize) +
            hd_normalized(x3, x4, keysize))/3;
    return score

# Get array of most highly probably key sizes    
def get_keysize(enc_bytes):
    dict = {}
    for size in range(2,41):
        score = get_keysize_score(enc_bytes, size)
        dict.update({size:score})
    
    sorted_guesses = sorted(dict, key=dict.__getitem__,reverse=False);
    return list(sorted_guesses);

# Split list into chunks    
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

# For given keysize - determine the most probable key        
def extract_key_per_keysize(enc_bytes, keysize):
    # Split lists by keysize (we ignore the lefovers)
    lists = list(chunks(list(enc_bytes), keysize))[:-1]
    # Transpose list matrix (all 1st bytes in each array into 1st array, etc.)
    trans_list=list(map(list, zip(*lists)));
    # For each array, find 1byte XOR key
    key=[];
    for l in trans_list:
        key.append(ch3.XOR_1B_guess_key(l)[0]);
    return key;

# For given keysize - decrypt with the most probable key    
def decrypt_per_keysize(enc_bytes, keysize):
    key = extract_key_per_keysize(enc_bytes, keysize);
    return ch5.encrypt_key(enc_bytes, key);
    
# Main entry point
def main(in_file='6.txt'):
    f = open(in_file, 'r');
    bigline="";
    # Convert input base64 to byte array
    for line in f:
        bigline+=line.rstrip('\r\n')
    enc_bytes = base64_bytes(bigline)
    # Guess key size
    keysizes = get_keysize(enc_bytes)
    # Decrypt with each keysize (we try only few best candidates)
    # then score the decrypted text with english score and determine best decryption
    guesses = {}
    for k in keysizes[0:5]:
        dec_bytes = decrypt_per_keysize(enc_bytes, k)
        score = ch3.english_score(dec_bytes)
        dec_text = utils.bytes_string(dec_bytes)
        guesses.update({dec_text:score})
    # Sort guesses by their frequency (lower -> better)
    sorted_guesses = sorted(guesses, key=guesses.__getitem__,reverse=False);
    # Eventually print the best scored decryption
    print (sorted_guesses[0])
    
if __name__ == "__main__":
    main()