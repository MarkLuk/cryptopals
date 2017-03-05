#!python

import utils
import AES

key = AES.randomKey()

def profile_encode(dict):
    str=''
    for v in dict:
        str += v[0] + '='+ v[1]+'&';
    return str[:-1]
    
def profile_decode(str):
    pairs = str.split("&")
    dict = []
    for p in pairs:
        v = p.split("=")
        dict.append([v[0],v[1]])
    return dict

def profile_for(email):
    filtered = email.replace("=",'').replace("&", '')
    return profile_decode("email="+filtered + "&uid=10&role=user")

def profile_encrypt(str):
    return AES.ECB_encrypt(key, bytes(utils.string_bytes(str)));

def profile_decrypt(bytes):
    return utils.bytes_string(AES.ECB_decrypt(key, bytes));
    
def main():
    # Create 'admin' block with padding
    enc1 = profile_encrypt(profile_encode(profile_for("mark@a.com" +"admin" + utils.bytes_string(bytes([11]*11)))))
    # Create target email account
    enc2 = profile_encrypt(profile_encode(profile_for("mrk@gmail.com")))
    # Concatinate target + admin blocks
    enc=enc2[0:32] + enc1[16:32];
    # Decrypt new profile
    dec = profile_decode(profile_decrypt(enc))
    print(dec)
    
if __name__ == "__main__":
    main()