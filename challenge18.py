#!python

import utils
import AES
import b64

def main(str='L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==', key=b'YELLOW SUBMARINE', nonce=0):
    enc = b64.decode(str);
    dec = AES.CTR_decrypt(key, enc, nonce);

    print(dec)

if __name__ == "__main__":
    main()