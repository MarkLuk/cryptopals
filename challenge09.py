#! python
import utils
import AES

def main(str='YELLOW SUBMARINE', blockSize=20):
    bytes = utils.string_bytes(str);
    print (AES.padPKCS7(bytes,blockSize));

if __name__ == "__main__":
    main()
    