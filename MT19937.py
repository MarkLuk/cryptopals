#!python

index = 0
mt    = [0]*624


def twist():
    global index
    global mt

    for i in range(624):
        y = ((mt[i] & 0x80000000) + (mt[(i + 1) % 624] & 0x7fffffff)) & 0xFFFFFFFF
        mt[i] = mt[(i + 397) % 624] ^ y >> 1

        if y % 2 != 0:
            mt[i] = mt[i] ^ 0x9908b0df
    index = 0

def init(seed):
    global index
    global mt

    # Initialize the index to 0
    index = 624
    mt = [0] * 624
    mt[0] = seed  # Initialize the initial state to the seed
    for i in range(1, 624):
        mt[i] = (1812433253 * (mt[i - 1] ^ mt[i - 1] >> 30) + i) & 0xFFFFFFFF

def get_num():
    global index
    global mt

    if index >= 624:
        twist()

    y = mt[index]
    y = y ^ y >> 11
    y = y ^ y << 7 & 2636928640
    y = y ^ y << 15 & 4022730752
    y = y ^ y >> 18

    index = index + 1

    return y & 0xFFFFFFFF

    
    