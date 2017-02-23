#! python
import utils

def padPKCS7(bytes, size):
    padSize = size - (len(bytes) % size);
    return bytes + bytearray([padSize]*padSize);
    
def main(str='YELLOW SUBMARINE', blockSize=20):
    bytes = utils.string_bytes(str);
    print (padPKCS7(bytes,blockSize));

if __name__ == "__main__":
    main()
    