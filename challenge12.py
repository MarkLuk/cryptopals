#! python
import utils
import AES
import b64
import challenge11 as ch11

key = AES.randomKey()
secret_bytes = b64.decode_file('12.txt')

def encryption_oracle(bytes):
    return AES.ECB_encrypt(key, bytes + secret_bytes)
    
def detect_block_size(encryption_oracle):
    b = encryption_oracle(b'')
    for i in range(1, 1024):
        b1 = encryption_oracle(bytes([0]*i));
        if (len(b1) != len(b)):
            return len(b1)-len(b);

def brute_force_oracle(block_size, encryption_oracle):
    decrypted = b'';
    while True:
        # Calculate prefix
        decrypted_blocks = utils.ceildiv(len(decrypted), block_size)
        if (decrypted_blocks == 0):
            decrypted_blocks = 1;
        decrypted_size = decrypted_blocks * block_size
        prefix = bytes([0]*(decrypted_size - len(decrypted) - 1))
        # Build dictionary
        dict = {}
        for b in range(256):
            p = prefix + decrypted + bytes([b])
            enc_p = encryption_oracle(p)[0:decrypted_size]
            dict[enc_p] = b
        # Perform oracle encryption
        enc = encryption_oracle(prefix)[0:decrypted_size]
        # Extract next encrypted byte by dictionary attack 
        if (enc in dict):
            decrypted += bytes([dict[enc]])
        else:
            break
    return decrypted;

def main():
    # Detect block size
    block_size = detect_block_size(encryption_oracle);
    # Confirm ECB encryption
    print(ch11.encryption_guess(encryption_oracle(bytes([0]*128))))
    # Brute-force secret message
    decrypted_bytes = brute_force_oracle(block_size, encryption_oracle)
    print (decrypted_bytes)
    
if __name__ == "__main__":
    main()
    