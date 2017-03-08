#!python

import SHA1
from utils import *

secret_key = random_bytes(16)

def encryption_oracle(msg):
    return SHA1.keyed_hash(secret_key, msg)

def verify_mac(encryption_oracle, msg, mac):
    if (encryption_oracle(msg) != mac):
        return False
    return True

def reverse_SHA_state(digest):
    h = [0]*5
    for i in range(len(h)):
        h[i] = bytes_int(bytes(digest[4*i:4*i+4]))
    return h;

def main():
    # Perform keyed hash of original msg
    original_msg = b'comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon'
    original_mac= encryption_oracle(original_msg)
    print('Original msg    = ', original_msg)
    print('Orignal msg MAC = ', bytes_hexstr(original_mac))
    print('Origianal msg verify passed = ', verify_mac(encryption_oracle, original_msg, original_mac))
    # Re-create SHA state from hash value
    print ('---------------')
    print ('Trying to forge')
    # Reverse SHA state
    h = reverse_SHA_state(original_mac)
    # Set string that we want to append
    forged_str=b';admin=true'
    # Try all key lengthes
    for keylen in range(1,100):
        forged_msg=original_msg + SHA1.padding(original_msg, len(original_msg) + keylen) + forged_str
        forged_str_len=len(forged_msg)+keylen
        forged_mac=SHA1.digest(forged_str,h[0],h[1],h[2],h[3],h[4], forged_str_len)
        if verify_mac(encryption_oracle, forged_msg, forged_mac):
            break;
    print('Forged msg     = ', forged_msg)
    print('Forged msg MAC = ', bytes_hexstr(forged_mac))
    print('Forged msg verify passed = ', verify_mac(encryption_oracle, forged_msg, forged_mac))

if __name__ == "__main__":
    main()