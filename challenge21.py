#!python
from MT19937 import MT19937

def main():
    # Init seed
    prng = MT19937(0)
    # Print some numbers
    for i in range(100):
        print (prng.get_num())
        
    
if __name__ == "__main__":
    main()