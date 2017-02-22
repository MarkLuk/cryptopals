#!python
import sys
   
# Main entry point
def main():
    # Get 2 hex integers
    x1 = int(sys.argv[1], 16);
    x2 = int(sys.argv[2], 16);
    
    print(hex(x1^x2))
    
if __name__ == "__main__":
    main()