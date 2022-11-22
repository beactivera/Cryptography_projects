import argparse

def parsingArgumentsFromCommandLine():

    parser = argparse.ArgumentParser(
        prog = "Caesar_and_Affine_Cipher",
        description = "Caesar and Affine Cipher",
        epilog = "Please provide arguments."
        )

    parser.add_argument('-c', '--caesar', help="Run Ceaser Cipher", required=False)
    parser.add_argument('-a', '--affine', help="Run Affine Cipher", required=False)
    parser.add_argument('-e', help="szyfrowanie", required=False)
    parser.add_argument('-d', help="odszyfrowanie", required=False)
    parser.add_argument('-j', help="kryptoanaliza z tekstem jawnym", required=False)
    parser.add_argument('-a', help="kryptoanaliza wyłącznie w oparciu o kryptogram", required=False)


    args = vars(parser.parse_args())
    
    return args

if  __name__ == "__main__":
    command = parsingArgumentsFromCommandLine()