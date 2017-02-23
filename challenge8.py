#!python
import sys
import challenge6 as ch6
import utils
from Crypto.Cipher import AES

def score_ECB(bytes):
    # Split into 16 bytes chunks
    lists = ch6.chunks(bytes, 16)
    # Do hamming distance between all blocks
    xor = 0
    for l in lists:
        xor ^= utils.bytes_int(l)
    return ch6.hw(xor)
        
    
# Main entry point
def main(in_file):
    f = open(in_file, 'r');
    # Check each line and get it score
    guesses = {}
    for line in f:
        line  = line.rstrip('\r\n')
        bytes = utils.string_bytes(line)
        score = score_ECB(bytes)
        # Add line with score to dictonary
        guesses.update({line:score});
    
    # Sort guesses by score
    sorted_guesses = sorted(guesses, key=guesses.__getitem__,reverse=False);
    
    # Print detected line
    print (sorted_guesses[0]);
    
    
if __name__ == "__main__":
    main('8.txt')