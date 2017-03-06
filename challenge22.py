#!python
import time
import utils
from MT19937 import MT19937

def main():
    # Generate random delay 
    time.sleep(utils.random_num(1, 5))
    # Get time
    t = int(time.time()) 
    # Init seed with current time
    prng = MT19937(t)
    # Sleep a bit 
    time.sleep(utils.random_num(1, 10))
    # Get value
    v = prng.get_num();
    print ("PRNG val = ", v)

    # Brute-force PRNG seed backwards in time
    t = int(time.time());
    print ("Time now = ", t)
    for i in range(20000000):
        seed = t-i
        # Try seed 
        prng = MT19937(seed)
        # Get number
        x = prng.get_num();
        # Check if seed found
        if x==v:
            print ("Seed is  = ", seed)
            break
    
if __name__ == "__main__":
    main()