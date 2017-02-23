#!python
import sys
import numpy as np
import utils

# Metric function to compare histograms
def chi2_distance(histA, histB, eps = 1e-10):
	# compute the chi-squared distance
	d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
		for (a, b) in zip(histA, histB)])
 
	# return the chi-squared distance
	return d
 
# This function calculates score according to similarity to english language distribution of given byte array
def english_score(bytes):
    # English letters frequency dictonary from  https://www.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
    real_hist = {'e':12.02,
                 't':9.10,
                 'a':8.12,
                 'o':7.68,
                 'i':7.31,
                 'n':6.95,
                 's':6.28,
                 'r':6.02,
                 'h':5.92,
                 'd':4.32,
                 'l':3.98,
                 'u':2.88,
                 'c':2.71,
                 'm':2.61,
                 'f':2.30,
                 'y':2.11,
                 'w':2.09,
                 'g':2.03,
                 'p':1.82,
                 'b':1.49,
                 'v':1.11,
                 'k':0.69,
                 'x':0.17,
                 'q':0.11,
                 'j':0.10,
                 'z':0.07};
    # Calculate byte frequency
    freq = dict((x, bytes.count(x)/len(bytes)) for x in bytes)
    # build input histogram
    letters = [ord(x) for x in list(real_hist)];
    hist=[0]*len(letters);
    for i in range(len(letters)):
        if (letters[i] in freq):
            hist[i] = freq[letters[i]];
    # Compare 2 histograms and calculate score (lower -> better)
    return chi2_distance(hist, real_hist.values());

def XOR_1B_guess_key(bytes):
    # Guesses score dictonary
    guesses = {};
    # Try to guess the key (0-255)
    for i in range(256):
        # Apply key and generate guess result
        guess = [i^x for x in bytes];
        #Score the frequency dictonary
        guess_score = english_score(guess);
        #Add to scores database
        guesses.update({i:guess_score});

    # Sort guesses by their frequency (lower -> better)
    sorted_guesses = sorted(guesses, key=guesses.__getitem__,reverse=False);
    
    return sorted_guesses;
    
def XOR_1B_decrypt(bytes):
    # Extract keys and take the 1st one
    key = XOR_1B_guess_key(bytes)[0];

    decoded_bytes = [key^x for x in bytes]
    
    return decoded_bytes;
    
# Main entry point
def main(hex_str='1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'):
    # Convert input to bytes
    bytes = utils.hexstr_bytes(hex_str)
    # Perfomr decryption
    decrypted_bytes = XOR_1B_decrypt(bytes);
    # Print output
    print(utils.bytes_string(decrypted_bytes));
    
if __name__ == "__main__":
    main()