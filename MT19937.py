#!python

class MT19937:
    def __init__(self, seed, cloned_state=[]):
        if len(cloned_state) != 624:
            self.index = 624
            self.mt = [0] * 624
            self.mt[0] = seed  # Initialize the initial state to the seed
            for i in range(1, 624):
                self.mt[i] = (1812433253 * (self.mt[i - 1] ^ self.mt[i - 1] >> 30) + i) & 0xFFFFFFFF
        else:
            self.index = 624
            self.mt = cloned_state
    
    def get_mt(self):
        return self.mt
        
    def get_num(self):
        if self.index >= 624:
            for i in range(624):
                y = ((self.mt[i] & 0x80000000) + (self.mt[(i + 1) % 624] & 0x7fffffff)) & 0xFFFFFFFF
                self.mt[i] = self.mt[(i + 397) % 624] ^ y >> 1

                if y % 2 != 0:
                    self.mt[i] = self.mt[i] ^ 0x9908b0df
            self.index = 0

        y = self.mt[self.index]
        y ^= y >> 11
        y ^= y << 7 & 2636928640
        y ^= y << 15 & 4022730752
        y ^= y >> 18

        self.index = self.index + 1

        return y & 0xFFFFFFFF

    
    