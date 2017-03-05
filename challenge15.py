#!python

import AES


def main():
    paddings = [b'ICE ICE BABY\x04\x04\x04\x04', b'ICE ICE BABY\x05\x05\x05\x05', b'ICE ICE BABY\x01\x02\x03\x04']
    
    for p in paddings:
        try:
            AES.verifyUnpadPKCS7(p);
            print (str(p) + " is correctly padded")
        except Exception as error:
            print(str(p) + " is incorrectly padded")

if __name__ == "__main__":
    main()