#!python
import sys
import utils
import base64

    
# Main entry point
def main(hexstr):
    # Convert to bytes
    bytes = utils.hexstr_bytes(hexstr)
    # Calculate base64 bytes
    enc_bytes=base64.b64encode(bytes)
    # Convert bytes to string
    str = utils.bytes_string(enc_bytes)
    print (str)


if __name__ == "__main__":
    main('49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d')
