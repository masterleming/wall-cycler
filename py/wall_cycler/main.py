# main

from .Config.ArgumentsParser import ArgumentsParser

import sys


def main(argv):
    conf = ArgumentsParser().parse()

    print(conf)


if __name__ == "__main__":
    main(sys.argv)
