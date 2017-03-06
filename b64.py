#!python
import utils
import base64 as b64

def encode(bytes):
    return b64.b64encode(bytes)

def decode(base64):
    return b64.b64decode(base64)
    
def decode_file(file):
    return decode(open(file, 'r').read().replace('\n','').replace('\r',''))
    