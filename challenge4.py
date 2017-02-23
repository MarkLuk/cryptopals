#!python
import sys
import numpy as np;
import challenge3 as ch3;
import utils
    
# Main entry point
def main(in_file='4.txt'):
    guesses={}
    f = open(in_file, 'r')
    for line in f:
        # Extract line bytes
        line = line.rstrip('\r\n')
        line_bytes = utils.hexstr_bytes(line)
        # Try to decrypt it
        decrypt_bytes = ch3.XOR_1B_decrypt(line_bytes);
        # Get English score
        guess_score = ch3.english_score(decrypt_bytes);
        # Add to guesses dictionary
        guesses.update({line:guess_score});
    
    # Sort guesses by their frequency (lower -> better)
    sorted_guesses = sorted(guesses, key=guesses.__getitem__,reverse=False);
       
    # Print guess
    line            = sorted_guesses[0]
    line_bytes      = utils.hexstr_bytes(line)
    decrypt_bytes   = ch3.XOR_1B_decrypt(line_bytes);
    decrypt_str     = utils.bytes_string(decrypt_bytes);
    print (decrypt_str);
    
if __name__ == "__main__":
    main()