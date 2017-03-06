#!python
from MT19937 import MT19937
import time
from utils import bit_get
from utils import bit_set

def unroll_shift_right(y, shift):
    for i in range(32-shift):
        y = bit_set(y, 32-i-1-shift, bit_get(y, 32-i-1)^bit_get(y, 32-i-1-shift))
    return y

def unroll_shift_left(y, shift, mask):
    for i in range(32-shift):
        y = bit_set(y, i+shift, bit_get(y, i+shift)^(bit_get(y, i) & bit_get(mask, i+shift)))
    return y
    
def unroll_state(y):
    y = unroll_shift_right(y, 18)
    y = unroll_shift_left(y, 15, 4022730752)
    y = unroll_shift_left(y, 7, 2636928640)
    y = unroll_shift_right(y, 11)
    return y
    
def clone_prng(prng):
    # Get 624 PRNG outputs, for each output unroll PRNG state
    mt = []
    for i in range(624):
        mt += [unroll_state(prng.get_num())];
    return MT19937(0, mt)
    
def main():
    # Initialize PRNG with random seed
    prng = MT19937(int(time.time()));
    # Clone PRNG
    cloned_prng = clone_prng(prng)
    # Test cloned PRNG
    for i in range(1000):
        x = prng.get_num()
        y = cloned_prng.get_num();
        if x!=y:
            print (x,y)
            print ('PRNG was not cloned successfully')
            return
    print ('PRNG was cloned successfully')
    
if __name__ == "__main__":
    main()
