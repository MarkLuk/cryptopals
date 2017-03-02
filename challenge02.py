#!python
import sys
import utils

# Main entry point
def main(hstr1='1c0111001f010100061a024b53535009181c', hstr2='686974207468652062756c6c277320657965'):
    # Get 2 hex integers
    x1 = utils.hexstr_bytes(hstr1)
    x2 = utils.hexstr_bytes(hstr2)
    
    xor = utils.xor_bytes(x1, x2)
    
    print(utils.bytes_hexstr(xor));
    
if __name__ == "__main__":
    main()