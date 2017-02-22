#!python
import sys
import numpy as np;

# Metric function to compare histograms
def chi2_distance(histA, histB, eps = 1e-10):
	# compute the chi-squared distance
	d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
		for (a, b) in zip(histA, histB)])
 
	# return the chi-squared distance
	return d
 
# Score frequency dictonary (lower -> better)
def score(freq):
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
    
    # build input histogram
    letters = [ord(x) for x in list(real_hist)];
    hist=[0]*len(letters);
    for i in range(len(letters)):
        if (letters[i] in freq):
            hist[i] = freq[letters[i]];
    # Compare 2 histograms and calculate score (lower -> better)
    return chi2_distance(hist, real_hist.values());
    
# Main entry point
def main():
    # Convert input to bytes
    hexstr = sys.argv[1]
    hex_bytes = bytearray.fromhex(hexstr);
    # Guesses score dictonary
    guesses = {};
    # Try to guess the key (0-255)
    for i in range(256):
        # Apply guess key
        guess = [i^x for x in hex_bytes];
        # Calculate byte frequency
        freq = dict((x, guess.count(x)) for x in guess)
        #Score the frequency dictonary
        guess_score = score(freq);
        #Add to scores database
        guesses.update({i:guess_score});

    # Sort guesses by their frequency (lower -> better)
    sorted_guesses = sorted(guesses, key=guesses.__getitem__,reverse=False);
    
    # Print 5 best guesses
    print ("Key", "\tScore", "\t\tDecoded string");
    for i in sorted_guesses[0:5]:
        decoded_bytes = [i^x for x in hex_bytes]
        decoded_str="".join(map(chr, decoded_bytes))
        print (i, guesses[i], decoded_str)
    
if __name__ == "__main__":
    main()