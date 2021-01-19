import sys

from rpython.rlib import jit

from yaplox.main import Yaplox

def target(*args):
    return main

def main(argv):
    # terrible argument handling
    for i in range(len(argv)):
        if argv[i] == "--jit":
            if len(argv) == i + 1:
                print "missing argument after --jit"
                return 2
            jitarg = argv[i + 1]
            del argv[i:i+2]
            jit.set_user_param(None, jitarg)
            break

    if len(argv) != 2:
        print("Usage: %s [script]" % (argv[0], ))
        return 64
    
    return Yaplox().run_file(argv[1])

if __name__ == '__main__':
    main(sys.argv)
