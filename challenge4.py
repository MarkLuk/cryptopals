#!python
import sys
import numpy as np;
import challenge3 as ch3;
    
# Main entry point
def main():
    guesses={}
    # Get input file
    in_file = sys.argv[1];
    f = open(in_file, 'r')
    for line in f:
        # Extract line 
        line = line.rstrip('\r\n')
        # Try to decrypt it
        decrypt_bytes = ch3.decrypt_hexstr(line);
        # Get frequency dictionary;
        freq = dict((x, decrypt_bytes.count(x)) for x in decrypt_bytes);
        # Get score
        guess_score = ch3.score(freq);
        # Add to guesses dictionary
        guesses.update({line:guess_score});
    
    # Sort guesses by their frequency (lower -> better)
    sorted_guesses = sorted(guesses, key=guesses.__getitem__,reverse=False);
       
    # Print guess
    line = sorted_guesses[0]
    decrypt_bytes = ch3.decrypt_hexstr(line);
    decrypt_str=ch3.bytes2string(decrypt_bytes);
    print (decrypt_str);
    
if __name__ == "__main__":
    main()