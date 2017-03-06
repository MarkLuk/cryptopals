#!python
import time
import utils
import MT19937

def main():
    # Generate random delay 
    time.sleep(utils.random_num(1, 5))
    # Get time
    t = int(time.time()) 
    # Init seed with current time
    MT19937.init(t)
    # Sleep a bit 
    time.sleep(utils.random_num(1, 10))
    # Get value
    v = MT19937.get_num();
    print ("PRNG val = ", v)

    # Brute-force PRNG seed backwards in time
    t = int(time.time());
    print ("Time now = ", t)
    for i in range(20000000):
        seed = t-i
        # Try seed 
        MT19937.init(seed)
        # Get number
        x = MT19937.get_num();
        # Check if seed found
        if x==v:
            print ("Seed is  = ", seed)
            break
    
if __name__ == "__main__":
    main()