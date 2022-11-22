# Author: Weronika Wdowiak
# Date: 2022-11-22
from sys import argv
from caesar.cipher import Caesar
from affine.cipher import Affine


def programCipher(args):


    if "-c" in args:
        encoder = Caesar
    elif "-a" in args:
        encoder = Affine
    else:
        print("ERROR: cipher not specified!")
        exit(1)
    

    if "-e" in args:
        encoder.encode("plain.txt", "crypto.txt", "key.txt")
    elif "-d" in args:
        encoder.decode("crypto.txt", "decrypt.txt", "key.txt")
    elif "-j" in args:
        encoder.analysis_extra("crypto.txt", "extra.txt", "key-found.txt")
    elif "-k" in args:
        encoder.analysis("crypto.txt", "decrypt.txt")
    else:
        print(f"ERROR: operation not specified!")
        exit(1)
    
    exit(0)


if __name__ == '__main__':
    programCipher(argv)