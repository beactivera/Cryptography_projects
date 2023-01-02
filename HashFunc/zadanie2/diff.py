# Author
# Weronika Wdowiak
# date 02/01/2022

HASH_SUMS = ("md5sum", "sha1sum", "sha224sum", "sha256sum", "sha384sum", "sha512sum")


def main():    
    with open("hash.txt", "r") as f1, open("hash_.txt", "r") as f2:
        h_arr1 = [line.strip()[:-3] for line in f1.readlines()]
        h_arr2 = [line.strip()[:-3] for line in f2.readlines()]
    
    with open("diff.txt", "w") as f:
        for idx, line1 in enumerate(h_arr1):
            line2 = h_arr2[idx]
            f.write(f"{HASH_SUMS[idx]}\n")
            f.write(f"{line1}\n")
            f.write(f"{line2}\n")
            all_bits = 0
            diff_bits = 0
            for pos in range(len(line1)):
                diff_bits += bin(int(line1[pos], 16) ^ int(line2[pos], 16)).count('1')
                all_bits += 4
            f.write(f"Liczba rozniacych sie bitow: {diff_bits} z {all_bits}, procentowo: {round(diff_bits / all_bits * 100, 2)}%\n\n")
    
    

if __name__ == '__main__':
    main()