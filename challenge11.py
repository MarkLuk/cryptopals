#! python
import utils
import AES

def randomPadLen():
    return utils.random_bytes(1)[0] % 6 + 5;
    
def encryption_oracle(input):
    pad1 = utils.random_bytes(randomPadLen());
    pad2 = utils.random_bytes(randomPadLen());
    input = pad1 + input + pad2
    if (utils.random_bool()):
        print ('Performing CBC')
        return ('CBC', AES.CBC_encrypt(AES.randomKey(), input, AES.randomIV()))
    else:
        print ('Performing ECB')
        return ('ECB', AES.ECB_encrypt(AES.randomKey(), input))

def encryption_guess(input):
    if (input[16:32] == input[32:48]):
        return 'ECB'
    return 'CBC'
        
def main():
    for i in range(1000):
        input = bytes(bytearray([0]*64))
        (type, input) = encryption_oracle(input)
        guess = encryption_guess(input);
        if (guess == type):
            print ("Guessed correctly: " + guess)
        else:
            print ("Failed to guess correctly")
            exit(0)
            
if __name__ == "__main__":
    main()
    