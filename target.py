import sys
from yaplox.main import Yaplox

def target(*args):
    return main

def main(argv):
    if len(argv) != 2:
        print("Usage: %s [script]" % (argv[0], ))
        return 64
    
    return Yaplox().run_file(argv[1])

if __name__ == '__main__':
    main(sys.argv)
