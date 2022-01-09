from fifteen import Interpreter as I
import sys

def main(path):
    I(path).run()


if __name__ == '__main__':
    try:
        path = sys.argv[1]
    except:
        print("usage: python 15 filename.15")
    main(path)