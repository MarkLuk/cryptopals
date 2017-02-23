#! python
import utils

def padPKCS7(bytes, size):
    padSize = size - (len(bytes) % size);
    if padSize == 0:
        padSize = size
    return bytes + bytearray([padSize]*padSize);

def unpadPKCS7(bytes):
    pad_size = bytes[len(bytes)-1]
    return bytes[:-pad_size];
    
def main(str='YELLOW SUBMARINE', blockSize=20):
    bytes = utils.string_bytes(str);
    print (padPKCS7(bytes,blockSize));

if __name__ == "__main__":
    main()
    