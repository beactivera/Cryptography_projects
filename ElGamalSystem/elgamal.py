# Zadanie 5 - System ElGamala
# Paweł Randzio <pawelrandzio99@gmail.com>
# 

from sys import argv
from random import randint
from math import gcd


ELGAMAL_PATH = "./elgamal.txt"
PLAINTXT_PATH = "./plain.txt"
MSGTXT_PATH = "./message.txt"
PUBKEY_PATH = "./public.txt"
PRIVKEY_PATH = "./private.txt"
SIGN_PATH = "./signature.txt"
CRYPTO_PATH = "./crypto.txt"
DECRYPT_PATH = "./decrypt.txt"
VERIFY_PATH = "./verify.txt"


def generate_keys():
    with open(ELGAMAL_PATH, "r") as f:
        elgamal_lines = [line.strip() for line in f.readlines()]
    
    prime = int(elgamal_lines[0])
    alpha = int(elgamal_lines[1])
    
    private_key = randint(2, prime - 2)
    public_key = pow(alpha, private_key, prime)
    
    with open(PUBKEY_PATH, "w") as pub, open(PRIVKEY_PATH, "w") as priv:
        pub.write(f"{prime}\n{alpha}\n{public_key}")
        priv.write(f"{prime}\n{alpha}\n{private_key}")


def encrypt():
    with open(PUBKEY_PATH) as f:
        pubkey_contents = [line.strip() for line in f.readlines()]
    
    prime = int(pubkey_contents[0])
    alpha = int(pubkey_contents[1])
    public_key = int(pubkey_contents[2])
    
    with open(PLAINTXT_PATH) as f:
        ptxt_contents = "".join(f.readlines())
    
    ptxt_numeric = int.from_bytes(ptxt_contents.encode('utf-8'), 'big')
    
    if ptxt_numeric >= prime:
        print("[ERROR] message is too long to encrypt.")
        exit(1)
    
    k = randint(2, prime - 2)
    r = pow(alpha, k, prime)
    t = (pow(public_key, k, prime) * ptxt_numeric) % prime
    
    with open(CRYPTO_PATH, "w") as f:
        f.write(f"{r}\n{t}")


def decrypt():
    with open(PRIVKEY_PATH, "r") as f:
        privkey_contents = [line.strip() for line in f.readlines()]
    
    prime = int(privkey_contents[0])
    private_key = int(privkey_contents[2])
    
    with open(CRYPTO_PATH, "r") as f:
        crypto_contents = [line.strip() for line in f.readlines()]
    
    r = int(crypto_contents[0])
    t = int(crypto_contents[1])
    
    message_numeric = (t * pow(r, -private_key, prime)) % prime
    message_txt = message_numeric.to_bytes((message_numeric.bit_length() + 7) // 8, 'big').decode('utf-8')
    
    with open(DECRYPT_PATH, "w") as f:
        f.write(f"{message_txt}")


def sign():
    with open(PRIVKEY_PATH, "r") as f:
        privkey_contents = [line.strip() for line in f.readlines()]
    
    prime = int(privkey_contents[0])
    alpha = int(privkey_contents[1])
    private_key = int(privkey_contents[2])
    
    with open(MSGTXT_PATH, "r") as f:
        msgtxt_contents = "".join(f.readlines())
    
    msgtxt_numeric = int.from_bytes(msgtxt_contents.encode('utf-8'), 'big')
    
    k = randint(2, prime - 2)
    while gcd(k, prime) != 1:
        k = randint(2, prime - 2)
    
    r = pow(alpha, k, prime)
    s = ((msgtxt_numeric - private_key * r) * pow(k, -1, prime - 1)) % (prime - 1)
    
    with open(SIGN_PATH, "w") as f:
        f.write(f"{r}\n{s}")


def verification(result):
    with open(VERIFY_PATH, "w") as f:
        f.write(f"{result}")
    print(result)


def verify():
    with open(PUBKEY_PATH, "r") as f:
        pubkey_contents = [line.strip() for line in f.readlines()]
    
    prime = int(pubkey_contents[0])
    alpha = int(pubkey_contents[1])
    public_key = int(pubkey_contents[2])
    
    with open(MSGTXT_PATH, "r") as f:
        msgtxt_contents = "".join(f.readlines())
    
    msgtxt_numeric = int.from_bytes(msgtxt_contents.encode('utf-8'), 'big')
    
    with open(SIGN_PATH, "r") as f:
        signature_contents = [line.strip() for line in f.readlines()]
    
    r = int(signature_contents[0])
    s = int(signature_contents[1])
    
    if 0 >= r >= prime:
        verification("N")
        
    if 0 >= s >= prime - 1:
        verification("N")
    
    final_verification = pow(alpha, msgtxt_numeric, prime) == ((pow(public_key, r, prime) * pow(r, s, prime)) % prime)
    
    if final_verification:
        verification("T")
    else:
        verification("N")


def main(args):
    if "-k" in args:
        generate_keys()
    elif "-e" in args:
        encrypt()
    elif "-d" in args:
        decrypt()
    elif "-s" in args:
        sign()
    elif "-v" in args:
        verify()
    else:
        print("[ERROR]: Unknown option.")
        exit(1)
    

if __name__ == '__main__':
    main(argv)
