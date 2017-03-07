#!python

import SHA1


def main():
    for x in (list(SHA1.keyed_hash(b'PASSWORD', b'The quick brown fox jumps over the lazy cog The quick brown fox jumps over the lazy cog'))):
        print (hex(x))
        
if __name__ == "__main__":
    main()