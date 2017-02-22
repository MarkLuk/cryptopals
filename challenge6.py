#!python
import sys
import challenge5 as ch5;
import utils

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

def hd_normalized(x,y, byte_size):
    return hd(x,y) / (byte_size)

def base642bytes(base64):
    b64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    x = 0;
    for b in base64:
        if (b=='='):
            y = 0
        else:
            y = b64.index(b)
        x = (x << 6) | y
    return int2bytes(x)

def bytes2ints(bytes, int_size):
    [bytes2int(bytes[i:i+int_size]) for i in range(int_size)]

def get_keysize_score(enc_bytes, keysize):
    elem_num = (len(enc_bytes) // keysize);
    sum = 0;
    count = 0;
    for j in range(0, elem_num, keysize):
        for i in range(0, elem_num, keysize):
            if (i!=j):
                x1=bytes2int(enc_bytes[i:i+keysize]);
                x2=bytes2int(enc_bytes[j:j+keysize]);
                sum += hd_normalized(x1, x2, keysize)
                count+=1
        
    # return average hamming distance normalized by keysize
    return (sum / count)
    
def get_keysize(enc_bytes):
    dict = {}
    for size in range(2,41):
        score = get_keysize_score(enc_bytes, size)
        dict.update({size:score})
    
    sorted_guesses = sorted(dict, key=dict.__getitem__,reverse=True);
    return list(sorted_guesses)[0];
        
    
# Main entry point
def main():
    in_file = sys.argv[1];
    f = open(in_file, 'r');
    bigline="";
    # Convert intput base64 to byte array
    for line in f:
        bigline+=line.rstrip('\r\n')
    enc_bytes = base642bytes(bigline)
    # Guess key size
    keysize = get_keysize(enc_bytes)
    print("Keysize = ", keysize)
    
    
if __name__ == "__main__":
    main()