# Author: Weronika Wdowiak

# Task: Program o nazwie xor powinien umożliwiać wywołanie z linijki rozkazowej z następującymi opcjami:
#    -p (przygotowanie tekstu do przykładu działania),
#    -e (szyfrowanie),
#    -k (kryptoanaliza wyłącznie w oparciu o kryptogram)

# Nazwy plików są następujące:
# ---orig.txt: plik zawierający dowolny tekst,
# ---plain.txt: plik z tekstem zawierającym co najmniej kilkanaście linijek równej długości, np. 64,
# ---key.txt: plik zawierający klucz, który jest ciągiem dowolnych znaków podanej wyżej długości,
# ---crypto.txt: plik z tekstem zaszyfrowanym, każda jego linijka jest operacją ⊕ z kluczem,
# ---decrypt.txt: plik z tekstem odszyfrowanym.
import os
import sys
from itertools import repeat

len_of_lines = 64


class Prepare:

    @staticmethod
    def prepare_file():
        new_lines = list()
        for line in Operations.get_file_content("orig.txt"):
            line = line.lower()
            line = line.replace('\n', '')
            if len(line) == 0:
                continue
            if len(line) > len_of_lines:
                after_split = Operations.split_line_to_many(line)
                for l in after_split:
                    new_lines.append(l)
            elif len(line) < len_of_lines:
                new_lines.append(Prepare.add_line_fillers(line, len_of_lines - len(line)))
            else:
                new_lines.append(line)
        if len(new_lines[-1]) < len_of_lines:
            line = new_lines.pop(-1)
            line_new = Prepare.add_line_fillers(line, len_of_lines - len(line))
            new_lines.append(line_new)
        read_lines = list()
        for line in new_lines:
            if len(line) == len_of_lines:
                read_lines.append(line)
        Operations.write_result("plain.txt", Operations.list_to_str(read_lines))

    @staticmethod
    def prepare_key():
        key = Operations.get_file_content("key.txt")[0]
        key = key.replace("\n", "")
        if len(key) > len_of_lines:
            Operations.write_result("key.txt", Operations.shorten(len_of_lines, key))
        elif len(key) < len_of_lines:
            Operations.write_result("key.txt", Prepare.add_line_fillers(key, len_of_lines - len(key)))

    @staticmethod
    def add_line_fillers(line, how_many):
        spaces = ""
        for i in range(how_many):
            spaces += "x"
        if line[-1] == "\n":
            return line[: len(line) - 1] + spaces + line[-1]
        else:
            return line + spaces


class PrepareForShorterLastLine:
    def __init__(self):
        self.file = Operations.get_file_content('orig.txt')

    def prepare(self):
        fixed_lines = ""
        for line in self.file:
            line = line.replace('\n', '')
            line = line.lower()
            fixed_lines += line
        fixed_lines = Operations.split_line_to_many(fixed_lines)
        Operations.write_result('plain.txt', Operations.list_to_str(fixed_lines))


class EncryptForShorterLastLine:
    def __init__(self):
        self.file = Operations.get_file_content("plain.txt")
        self.key = Operations.get_file_content("key.txt")[0]

    def encrypt(self):
        encrypted_lines = list()
        for line in self.file:
            line = line.replace('\n', '')
            if len(line) == len_of_lines:
                encrypted_line = ""
                for i in range(len_of_lines):
                    encrypted_line += chr(Binary.do_xor(ord(line[i]), ord(self.key[i])))
            else:
                encrypted_line = ""
                for i in range(len(line)):
                    encrypted_line += chr(Binary.do_xor(ord(line[i]), ord(self.key[i])))
            encrypted_lines.append(encrypted_line)
        Operations.write_result('crypto.txt', Operations.list_to_str2(encrypted_lines))


class Encrypt:
    def __init__(self):
        self.file = Operations.get_file_content("plain.txt")
        self.key = Operations.get_file_content("key.txt")

    def encrypt(self):
        key_chars = Operations.split(self.key[0])
        encrypted = list()
        for line in self.file:
            line = line.replace("\n", "")
            encrypted.append(self.encrypt_line(line, key_chars))
        Operations.write_result_with_whole_result("crypto.txt", Operations.list_to_str2(encrypted))

    @staticmethod
    def encrypt_line(line, key_chars):
        line_chars = Operations.split(line)
        encrypted_line = ""
        num = 0
        for c in line_chars:
            encrypted_line += chr(Binary.do_xor(ord(c), ord(key_chars[num])))
            num += 1
        return encrypted_line


class Decrypt:
    def __init__(self):
        self.file = Operations.get_file_content_whole("crypto.txt")

    def decrypt(self):
        merged = Operations.split_line_to_many(self.file)
        columns = Decrypt.into_columns(merged)
        decrypted_lines = [bytearray() for _ in range(len(columns[0]))]
        for column in columns:
            for i, byte in enumerate(Decrypt.key_for_column(column)):
                decrypted_lines[i].append(byte)
        str_lines = ""
        for line in decrypted_lines:
            str_lines += str(line, "utf-8") + "\n"
        Operations.write_result("decrypt.txt", str_lines)

    @staticmethod
    def find_key_for_column(column):
        for c in column:
            if Binary.is_xor_with_space(ord(c)):
                print(c)
                return Binary.do_xor(ord(c), ord(" "))
        return "_"

    @staticmethod
    def key_for_column(column):
        if len(column) < 3:
            return repeat(ord("_"), len(column))
        pairs = zip(column, column[1:])
        for num, pair in enumerate(pairs):
            c_1, c_2 = pair
            after_xor = Binary.do_xor(c_1, c_2)
            if Binary.is_xor_with_space(after_xor):
                remaining_c = column[:num] + column[(num + 2):]
                space_place = Decrypt.space_position(remaining_c, c_1, c_2)
                if space_place is None:
                    continue
                if space_place == 1:
                    c = c_1
                else:
                    c = c_2
                decoded_column = list()
                for char in column:
                    decoded_column.append(char ^ c ^ ord(" "))
                return decoded_column
        return repeat(ord("_"), len(column))

    @staticmethod
    def space_position(characters, c_1, c_2):
        for character in characters:
            if Binary.do_xor(c_1, character) == 0 or Binary.do_xor(c_2, character) == 0:
                continue
            elif Binary.is_xor_with_space(Binary.do_xor(c_1, character)):
                return 1
            else:
                return 2
        return None

    def merge(self):
        merged = ""
        for line in self.file:
            merged += line
        return merged

    @staticmethod
    def into_columns(text):
        amount_of_columns = len(text[0])
        all_columns = list()
        for _ in range(amount_of_columns):
            all_columns.append(list())
        for line in text:
            i = 0
            for character in line:
                all_columns[i].append(character)
                i += 1
        return all_columns


class Binary:
    @staticmethod
    def do_xor(c_1, c_2):
        return c_1 ^ c_2

    @staticmethod
    def is_xor_with_space(c):
        return (c & 0b11100000) == 0b01000000

    @staticmethod
    def char_to_bin(c):
        """Takes (char) c and returns a String showing binary representation"""
        x = bin(ord(c))
        x = x[2:]
        while len(str(x)) < 8:
            x = "0" + x
        return x + " "

    @staticmethod
    def bin_to_char(b):
        n = int(b, 2)
        return n.to_bytes((n.bit_length() + 7) // 8, "big").decode()

    @staticmethod
    def change_binary_line_to_string(line):
        new_line = ""
        line = line.split(" ")
        for l in line:
            if l != "\n" and l != "":
                new_line += Binary.bin_to_char(l)
            elif l == "00000000":
                new_line += "-"
        return new_line


class Operations:
    @staticmethod
    def split_line_to_many(x):
        chunks, chunk_size = len(x), len_of_lines
        return [x[i: i + chunk_size] for i in range(0, chunks, chunk_size)]

    @staticmethod
    def wrong_args():
        print("please try: python3 xor.py [-p|-e|-k]")
        sys.exit(1)

    @staticmethod
    def get_file_content(file):
        if not os.path.exists(file):
            print("file ", file, " is needed to perform this operation, but does not exist")
            sys.exit(1)
        return open(file, "r").readlines()

    @staticmethod
    def get_file_content_whole(file):
        if not os.path.exists(file):
            print("file ", file, " is needed to perform this operation, but does not exist")
            sys.exit(1)
        return open(file, "rb").read()

    @staticmethod
    def write_result(file, result):
        if result is None:
            print("There was an error, the files might contain wrong data.")
            sys.exit(1)
        f = open(file, "w")
        f.write(result[:-1])

    @staticmethod
    def write_result_with_whole_result(file, result):
        if result is None:
            print("There was an error, the files might contain wrong data.")
            sys.exit(1)
        f = open(file, "w")
        f.write(result)

    @staticmethod
    def list_to_str(list_to_change):
        st = ""
        for l in list_to_change:
            st += l
            st += "\n"
        return st

    @staticmethod
    def list_to_str2(list_to_change):
        st = ""
        for l in list_to_change:
            st += l
        return st

    @staticmethod
    def split(word):
        return [char for char in word]

    @staticmethod
    def shorten(how_short, line):
        return line[: how_short + 1] if len(line) > how_short else line


if __name__ == "__main__":
    if len(sys.argv) != 2:
        Operations.wrong_args()
    if sys.argv[1] == "-p":
        p = PrepareForShorterLastLine()
        p.prepare()
        # Prepare.prepare_file()
        Prepare.prepare_key()
    elif sys.argv[1] == "-e":
        e = EncryptForShorterLastLine()
        # e = Encrypt()
        e.encrypt()
    elif sys.argv[1] == "-k":
        d = Decrypt()
        d.decrypt()
    else:
        Operations.wrong_args()
