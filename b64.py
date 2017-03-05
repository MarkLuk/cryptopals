#!python
import utils
import base64 as b64

def encode(bytes):
    return b64.b64encode(bytes)

def decode(base64):
    return b64.b64decode(base64)
    
def decode_file(file):
    f = open(file, 'r');
    bigline="";
    # Convert input base64 to byte array
    for line in f:
        bigline+=line.rstrip('\r\n')
    # Convert to bytes
    return decode(bigline)
    