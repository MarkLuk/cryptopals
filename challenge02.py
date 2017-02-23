#!python
import sys
import utils

def xor_bytes(b1, b2):
    x1  = utils.bytes_int(b1)
    x2  = utils.bytes_int(b2)
    xor = x1^x2;
    return utils.int_bytes(xor)
    
 
# Main entry point
def main(hstr1='1c0111001f010100061a024b53535009181c', hstr2='686974207468652062756c6c277320657965'):
    # Get 2 hex integers
    x1 = utils.hexstr_bytes(hstr1)
    x2 = utils.hexstr_bytes(hstr2)
    
    xor = xor_bytes(x1, x2)
    
    print(utils.bytes_hexstr(xor));
    
if __name__ == "__main__":
    main()