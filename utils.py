#!python

# Ceil division
def ceildiv(a,b): 
    return (a + (b-1))//b;

# Integer <-> Bytes    
def int_bytes(x):
    return x.to_bytes(ceildiv(x.bit_length(),8), 'big')

def bytes_int(bytes):
    return int.from_bytes(bytes, 'big')

# Hex-String <-> Int    
def hexstr_int(hexstr):
    return int(hexstr, 16)

def int_hexstr(int):
    return hex(int)[2:]

# String <-> Bytes    
def string_bytes(str):
    return [ord(x) for x in list(str)]

def bytes_string(bytes):
    str="";
    for b in bytes:
        str+=chr(b);
    return str;

# Hex-String <--> Bytes    
def hexstr_bytes(hexstr):
   return int_bytes(hexstr_int(hexstr))

def bytes_hexstr(bytes):
   return int_hexstr(bytes_int(bytes))
