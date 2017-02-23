#!python
import sys
import utils

# Integer to 6bit bytes    
def int_6bit_bytes(x):
    ln = utils.ceildiv(x.bit_length(), 6);
    bytes = [0]*ln;
    for i in range(ln):
        bytes[ln - i - 1] = x & 0x3F;
        x >>= 6;
    return bytes;

# Convert 6bit byte to base64    
def 6bit_base64(x):
    b64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    return b64[x];

# Convert byte array to base64 string
def bytes_base64(bytes):
    str = '';
    for b in bytes:
        str += 6bit_base64(b);
    return str;
    
# Main entry point
def main(hexstr):
    # Get integer for hex-string
    x = utils.hexstr_int(hexstr);
    # Convert integer to 6bit bytes
    bytes = int_6bit_bytes(x);
    # Convert 6bit bytes to base64
    print (bytes_base64(bytes));
    
if __name__ == "__main__":
    main('49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d')