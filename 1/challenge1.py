#!python
import sys

# Ceil division
def ceildiv(a,b): 
    return (a + (b-1))//b;
    
def int2bytes(x):
    ln = ceildiv(x.bit_length(), 6);
    bytes = [0]*ln;
    for i in range(ln):
        bytes[ln - i - 1] = x & 0x3F;
        x >>= 6;
        
    return bytes;
    
def base64_byte(x):
    b64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+\\'
    return b64[x];

def baset64(bytes):
    str = '';
    for b in bytes:
        str += base64_byte(b);
    return str;
    
# Main entry point
def main():
    # Get hex 
    x = int(sys.argv[1], 16);
    # Convert hex to bytes
    bytes = int2bytes(x);
    # Convert bytes to base64
    print (baset64(bytes));
    
    


if __name__ == "__main__":
    main()