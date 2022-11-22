class Caesar(object):

    def __init__(self):
        pass


    def single_encode(ch, k):
        return chr(((ord(ch) - 64 + k) % 26) + 64) if ch.isupper() else chr(((ord(ch) - 96 + k) % 26) + 96)

     
    def single_decode(ch, k):
        corrector = 64 if ch.isupper() else 96
        decoded = (ord(ch) - corrector - k)
        if decoded < 1:
            decoded += 26
        return chr(decoded + corrector)

     
    def decode_line(line, k):
        return "".join([Caesar.single_decode(c, k) if c.isalpa() else c for c in line])

     
    def encode(srcFile, dstFile, keyFile):
        with open( srcFile) as f:
            text = f.readline()
        with open(keyFile) as f:
            key = int(f.readline().strip().split(' ')[0])
            if key not in range(1, 26):
                print("ERROR: invalid key!")
                exit(1)
        with open(dstFile, 'w') as f:
            f.write("".join([Caesar.single_encode(c, key) if c.isalpha() else c for c in text]))
    
     
    def decode( srcFile, dstFile, keyFile):
        with open( srcFile) as f:
            cipher = f.readline()
        with open(keyFile) as f:
            key = int(f.readline().strip().split(' ')[0])
        with open(dstFile, 'w') as f:
            f.write("".join([Caesar.single_decode(c, key) if c.isalpha() else c for c in cipher]))

     
    def analysis_extra( srcFile, extra, dstFile):
        with open( srcFile) as f:
            cipher = f.readline().lower()
        with open (extra) as f:
            helper = f.readline().lower()
        if len(helper) < 1:
            print("ERROR: Helper text has no alphabet characters")
            exit(1)
        ch_a = ord(cipher[0]) - 64
        ch_b = ord(helper[0]) - 64
        key = (ch_a - ch_b) % 26
        for i, character in enumerate(helper):
            if character.isalpha():
                if Caesar.single_encode(character, key) != cipher[i]:
                    print("ERROR: keys not matching")
                    exit(1)
        with open(dstFile, 'w') as f:
            f.write(f"{key}\n")

     
    def analysis( srcFile, dstFile):
        with open( srcFile) as f:
            cipher = f.readline()
        with open(dstFile, 'w') as f:
            for k in range(1, 26):
                f.write(f"{Caesar.decode_line(cipher, k)}")