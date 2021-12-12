import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def dilate(src, n):
    m = n // 2
    src = np.pad(src, ((m, m), (m, m)), 'constant')
    arr = []
    c = len(src)
    l = len(src[0])
    for j in range(m, c - m):
        arr.append([])
        for i in range(m, l - m):
            img = src[j - m:j + m + 1, i - m:i + m + 1]
            min = 255
            for a in range(len(img)):
                for b in range(len(img[0])):
                    if img[a][b] <= min:
                        min = img[a][b]
            arr[j - m].append(min)
    return Image.fromarray(np.array(arr))


def different(image, new_image):
    width, height = image.size
    dif_image = Image.new('P', (width, height))
    for x in range(width):
        for y in range(height):
            dif_image.putpixel((x, y), abs(image.getpixel((x,y)) - new_image.getpixel((x,y))))
    return dif_image


if __name__ == '__main__':
    image = Image.open("woman_picture.bmp")
    print(np.asarray(image).shape)
    print(np.asarray(image))
    image1 = dilate(image, 5)
    image1.save("dilate_woman_picture.bmp")
    dif = different(image, image1)
    dif.save("dif_woman_picture.bmp")
    image2 = Image.open("new_text.bmp")
    print(np.asarray(image2).shape)
    image3 = dilate(image2, 5)
    image3.save("dilate_new_text.bmp")
    dif1 = different(image2, image3)
    dif1.save("dif_new_text.bmp")


