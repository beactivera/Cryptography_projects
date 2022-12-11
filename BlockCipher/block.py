# Author: Weronika Wdowiak
# date: 11/12/2022


# to RUN this script you need to download python library for images, 
# the instruction for particular sytem in the link below:
# https://pillow.readthedocs.io/en/stable/installation.html 

import math
import os
import secrets
import sys
from hashlib import sha1
from PIL import Image


class Block:
    def __init__(self, x, y, w, h, d):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.d = d


class ECB:
    def __init__(self):
        self.image = Tools.get_bitmap()
        self.encrypted_image = Image.new("1", Tools.get_bitmap().size)

    def encrypt(self):
        image_w, image_h = self.image.size
        for b in Tools.create_blocks(self.image, (5, 5)):
            Tools.save_image_bytes(self.encrypted_image, b, Tools.encrypt(b.d), image_w, image_h)
        self.encrypted_image.save("ecb_crypto.bmp")


class CBC:
    def __init__(self):
        self.image = Tools.get_bitmap()
        self.encrypted_image = Image.new("1", Tools.get_bitmap().size)
        self.prev = secrets.token_bytes(25)  # block size is (8, 8)

    def encrypt(self):
        for b in Tools.create_blocks(self.image, (5, 5)):
            image_w, image_h = self.image.size
            xor_result = bytes(b1 ^ b2 for b1, b2 in zip(b.d, self.prev))
            self.prev = Tools.encrypt(xor_result)
            Tools.save_image_bytes(self.encrypted_image, b, self.prev, image_w, image_h)
        self.encrypted_image.save("cbc_crypto.bmp")


class Tools:
    @staticmethod
    def get_whole_file(filename):
        if not os.path.exists(filename):
            print("file ", filename, " is needed to perform this operation, but does not exist")
            sys.exit(1)
        return open(filename, "rb").read()

    @staticmethod
    def save_to_file(filename, result):
        if result is None:
            print("There was an error, the files might contain wrong data.")
            sys.exit(1)
        f = open(filename, "w")
        f.write(result)

    @staticmethod
    def get_bitmap():
        return Image.open("plain.bmp", formats=["bmp"]).convert("1")

    @staticmethod
    def byte_to_bw_scale(byte):
        return 0 if byte <= 127 else 255

    @staticmethod
    def encrypt(image):
        byte_array = bytearray(len(image))

        for i in range(0, len(image), sha1().digest_size):
            minimum = min(sha1().digest_size, len(image) - 1)
            digest = sha1(image[i: i + minimum]).digest()
            byte_array[i: i + minimum] = digest[:minimum]

        return bytes(map(Tools.byte_to_bw_scale, byte_array))

    @staticmethod
    def create_blocks(image, block_size):
        image_w, image_h = image.size
        block_w, block_h = block_size
        how_many_blocks_width = math.ceil(image_w / block_w)
        how_many_blocks_height = math.ceil(image_h / block_h)
        amount_of_blocks = how_many_blocks_width * how_many_blocks_height

        for block_number in range(amount_of_blocks):
            x = block_w * (block_number % how_many_blocks_width)
            y = math.floor(block_number / how_many_blocks_height) * block_h
            arr = Tools.data(x, y, block_w, block_h, image_w, image_h, image)

            yield Block(x, y, block_w, block_h, arr)

    @staticmethod
    def data(b_x, b_y, b_w, b_h, i_w, i_h, image):
        byte_array = bytearray(b_w * b_h)

        for y in range(b_y):
            for x in range(b_x):
                pixel_x = b_x + x
                pixel_y = b_y + y
                if pixel_x < i_w and pixel_y < i_h:
                    insert = y * b_w + x
                    if insert < len(byte_array):
                        byte_array[insert] = image.getpixel((pixel_x, pixel_y))
        return byte_array

    @staticmethod
    def save_image_bytes(image, block, data, image_w, image_h):
        for i, byte in enumerate(data):
            x = block.x + i % block.w
            y = block.y + math.floor(i / block.h)
            if x < image_w and y < image_h:
                image.putpixel((x, y), byte)


if __name__ == '__main__':
    ecb = ECB()
    ecb.encrypt()

    cbc = CBC()
    cbc.encrypt()