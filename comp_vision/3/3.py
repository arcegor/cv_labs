from PIL import Image
import numpy as np
from math import *


def change_to_semitone(image):
    width, height = image.size
    newImage = Image.new('P', (width, height))
    for x in range(width):
        for y in range(height):
            color = image.getpixel((x, y))
            bright = floor(0.3 * color[0] + 0.59 * color[1] + 0.11 * color[2])
            newImage.putpixel((x, y), bright)
    return newImage


def get_Gx(image):
    width, height = image.size
    Gx = np.zeros((height, width))
    max_x = 0
    src = np.pad(image, ((2, 2), (2, 2)), 'constant')
    for x in range(2, 2 + height):
        for y in range(2, 2 + width):
            z1 = src[x - 2][y - 2]
            z2 = src[x - 2][y - 1]
            z3 = src[x - 2][y]
            z4 = src[x - 2][y + 1]
            z5 = src[x - 2][y + 2]
            z21 = src[x + 2][y - 2]
            z22 = src[x + 2][y - 1]
            z23 = src[x + 2][y]
            z24 = src[x + 2][y + 1]
            z25 = src[x + 2][y + 2]
            bright_x = -z1 - z2 - z3 - z4 - z5 + z21 + z22 + z23 + z24 + z25
            Gx[x-2][y-2] = bright_x
            if max_x < bright_x:
                max_x = bright_x
    return Gx, max_x


def get_Gy(image):
    width, height = image.size
    Gy = np.zeros((height, width))
    max_y = 0
    src = np.pad(image, ((2, 2), (2, 2)), 'constant')
    for x in range(2, 2 + height):
        for y in range(2, 2 + width):
            z1 = src[x - 2][y - 2]
            z2 = src[x - 1][y - 2]
            z3 = src[x][y - 2]
            z4 = src[x + 1][y - 2]
            z5 = src[x + 2][y - 2]
            z21 = src[x - 2][y + 2]
            z22 = src[x - 1][y + 2]
            z23 = src[x][y + 2]
            z24 = src[x + 1][y + 2]
            z25 = src[x + 2][y + 2]
            bright_y = -z1 - z2 - z3 - z4 - z5 + z21 + z22 + z23 + z24 + z25
            Gy[x-2][y-2] = bright_y
            if max_y < bright_y:
                max_y = bright_y
    return Gy, max_y


def get_gradient(Gx, Gy):
    height,  width = Gx.shape
    G = np.zeros((height, width))
    max_g = 0
    for x in range(height):
        for y in range(width):
            G[x][y] = sqrt(Gy[x][y]**2 + Gx[x][y]**2)
            if max_g < G[x][y]:
                max_g = G[x][y]
    return G, max_g


def get_normalize(matrix, max_value):
    height,  width = matrix.shape
    new_image = Image.new('P', (width, height))
    for x in range(height):
        for y in range(width):
            value = floor(matrix[x][y] * 255 / max_value)
            new_image.putpixel((y, x), value)
    return new_image


def binary(image, threshold):
    width, height = image.size
    binary_image = Image.new('1', (width, height))
    for x in range(width):
        for y in range(height):
            if image.getpixel((x, y)) < threshold:
                binary_image.putpixel((x, y), 0)
            else:
                binary_image.putpixel((x, y), 1)
    return binary_image


def main():
    # dart_image = change_to_semitone(Image.open("dart.jpg"))
    # dart_image.save("dart.jpg_semitone.png")
    # Gx, max_x = get_Gx(dart_image)
    # Gy, max_y = get_Gy(dart_image)
    # G, max_g = get_gradient(Gx, Gy)
    #
    # Gx_image = get_normalize(Gx, max_x)
    # Gy_image = get_normalize(Gy, max_y)
    # G_image = get_normalize(G, max_g)
    #
    # binary_gradient_image = binary(G_image, 1)
    #
    # Gx_image.save("dart_Gx.png")
    # Gy_image.save("dart_Gy.png")
    # G_image.save("dart_G.png")
    # binary_gradient_image.save("dart_binary_gradient.png")
    olaf_image = change_to_semitone(Image.open("olaf.png"))
    olaf_image.save("1.png")
    Gx, max_x = get_Gx(olaf_image)
    Gy, max_y = get_Gy(olaf_image)
    G, max_g = get_gradient(Gx, Gy)

    Gx_image = get_normalize(Gx, max_x)
    Gy_image = get_normalize(Gy, max_y)
    G_image = get_normalize(G, max_g)

    binary_gradient_image = binary(G_image, 20)

    Gx_image.save("1_Gx.png")
    Gy_image.save("1_Gy.png")
    G_image.save("1_G.png")
    binary_gradient_image.save("1_gradient.png")

if __name__ == "__main__":
    main()
