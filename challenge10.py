#! python
import utils
import AES
import b64

def main(file_name='10.txt', key=b'YELLOW SUBMARINE'):
    # Extract raw data from file
    bytes=b64.decode_file(file_name)
    # Set default IV
    iv = bytearray([0]*AES.block_size)
    # Decrypt the file
    plain = AES.CBC_decrypt(key,bytes,iv)
    # Print output
    print(utils.bytes_string(plain));

if __name__ == "__main__":
    main()
