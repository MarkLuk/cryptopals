#! python
import utils
import challenge06 as ch6
import AES
    
def main(file_name='10.txt', key='YELLOW SUBMARINE'):
    # Extract raw data from file
    bytes=ch6.base64file_bytes(file_name)
    # Set default IV
    iv = bytearray([0]*AES.block_size)
    # Decrypt the file
    plain = AES.CBC_decrypt(key,bytes,iv)
    # Print output
    print(utils.bytes_string(plain));
    
if __name__ == "__main__":
    main()
    