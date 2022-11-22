class Affine(object):

    VALID_FACTORS = (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)

    
    def single_encode(ch, f, m):
        return chr(((f * (ord(ch) - 64) + m) % 26) + 64) if ch.isupper() else chr(((f * (ord(ch) - 96) + m) % 26) + 96)

    
    def single_decode(ch, f, m):
        corrector = 64 if ch.isupper() else 96
        invf = 0
        try:
            invf = pow(f, -1, 26)
        except ValueError:
            print("ERROR: Base is not invertible for given modulus")
            exit(1)
        decoded = ((ord(ch) - corrector - m) * invf) % 26
        if decoded < 1:
            decoded += 26
        return chr(decoded + corrector)

    
    def decode_line(l, f, m):
        return "".join([Affine.single_decode(c, f, m) if c.isalpha() else c for c in l])

    
    def encode(srcFile, dstFile, keyFile):
        with open(srcFile) as f:
            text = f.readline()
        with open(keyFile) as f:
            line = f.readline().strip().split(' ')
            factor = int(line[1])
            move = int(line[0])
            if factor not in Affine.VALID_FACTORS or move not in range(1, 27):
                print("ERROR: invalid key")
                exit(1)
        with open(dstFile, 'w') as f:
            f.write("".join([Affine.single_encode(c, factor, move) if c.isalpha() else c for c in text]))
    
    
    def decode(srcFile, dstFile, keyFile):
        with open(srcFile) as f:
            cipher = f.readline()
        with open(keyFile) as f:
            line = f.readline().strip().split(' ')
            factor = int(line[1])
            move = int(line[0])
        with open(dstFile, 'w') as f:
            f.write("".join([Affine.single_decode(c, factor, move) if c.isalpha() else c for c in cipher]))
    
    
    def analysis_extra(srcFile, extra, dstFile):
        with open(srcFile) as f:
            cipher = f.readline().lower()
        with open(extra) as f:
            helper = f.readline().lower()
        if len(helper) < 1:
            print("ERROR: Helper text has no alphabet characters")
            exit(1)
        if len(helper) < 2:
            print("ERROR: Helper text is too short")
            exit(1)
        cipher_letter = [ord(cipher[0]) - 96, ord(cipher[1]) - 96]
        helper_letter = [ord(helper[0]) - 96, ord(helper[1]) - 96]
        a = 0
        try:
            y = (cipher_letter[0] - cipher_letter[1])
            if y < 0:
                y += 26
            x = pow(helper_letter[0] - helper_letter[1], -1, 26)
            a = (y * x) %  26
        except ValueError:
            print("ERROR: Difference is uninversible.")
            exit(1)
        b = cipher_letter[0] - (a * helper_letter[0]) % 26
        if b < 1:
            b += 26
        for i, character in enumerate(helper):
            if character.isalpha():
                if Affine.single_encode(character, a, b) != cipher[i]:
                    print("ERROR: keys not matching")
                    exit(1)
        with open(dstFile, 'w') as f:
            f.write(f"{b} {a}\n")

    
    def analysis(srcFile, dstFile):
        with open(srcFile) as f:
            cipher = f.readline()
        with open(dstFile, 'w') as f:
            for factor in Affine.VALID_FACTORS:
                for move in range(1, 27):
                    f.write(f"{Affine.decode_line(cipher, factor, move)}")