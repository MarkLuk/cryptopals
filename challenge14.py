#! python
import utils
import AES
import b64
import challenge11 as ch11

key = AES.randomKey()
secret_bytes = b64.decode_file('12.txt')
random_prefix = utils.random_bytes(utils.random_bytes(1)[0])


def encryption_oracle(bytes):
    return AES.ECB_encrypt(key, random_prefix + bytes + secret_bytes)

def detect_block_size(encryption_oracle):
    b = encryption_oracle(b'')
    for i in range(1, 1024):
        b1 = encryption_oracle(bytes([0]*i));
        if (len(b1) != len(b)):
            return len(b1)-len(b);
            
def detect_prefix_size(block_size, encryption_oracle):
    # Detect prefix block size
    for j in range(1,1024):
        b = encryption_oracle(bytes([0]*j));
        # Check if we find duplicated block
        for i in range(0, len(b) - block_size, block_size):
            if b[i:i+block_size]==b[i+block_size:i+2*block_size]: 
                # Found!
                return i-j%(2*block_size);
    return 0;
    
def brute_force_oracle(block_size, prefix_size, encryption_oracle):
    decrypted = b'';
    prefix_pad = bytes([0]*(block_size - prefix_size%block_size));
    prefix_block = utils.ceildiv(prefix_size, block_size)*block_size;
    while True:
        # Calculate prefix
        decrypted_blocks = utils.ceildiv(len(decrypted), block_size)
        if (decrypted_blocks == 0):
            decrypted_blocks = 1;
        decrypted_size = decrypted_blocks * block_size
        prefix = prefix_pad + bytes([0]*(decrypted_size - len(decrypted) - 1))
        # Build dictionary
        dict = {}
        for b in range(256):
            p = prefix + decrypted + bytes([b])
            enc_p = encryption_oracle(p)[prefix_block:prefix_block+decrypted_size]
            dict[enc_p] = b
        # Perform oracle encryption
        enc = encryption_oracle(prefix)[prefix_block:prefix_block+decrypted_size]
        
        
        # Extract next encrypted byte by dictionary attack 
        if (enc in dict):
            decrypted += bytes([dict[enc]])
        else:
            break
            
    return decrypted;

def main():
    # Detect block size
    block_size = detect_block_size(encryption_oracle);
    # Detect prefix size
    prefix_size = detect_prefix_size(block_size, encryption_oracle)
    # Brute-force secret message
    decrypted_bytes = brute_force_oracle(block_size, prefix_size, encryption_oracle)
    print (decrypted_bytes)
    
if __name__ == "__main__":
    main()
    