#!python
import MT19937

def main():
    # Init seed
    MT19937.init(0)
    # Print some numbers
    for i in range(100):
        print (MT19937.get_num())
        
    
if __name__ == "__main__":
    main()