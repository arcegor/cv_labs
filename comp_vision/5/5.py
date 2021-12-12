from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from math import floor
from matplotlib import transforms


def foo(item):
    if item == 255:
        return 1
    return 0


def plotX(text):
    image = Image.open(text)
    width, height = image.size
    plt.axis('off')
    x = range(width)
    y = [sum([1 - foo(image.getpixel((x, y))) for y in range(height)]) for x in range(width)]
    plt.plot(x, y, color='green')
    plt.fill_between(x, [0 for _ in range(width)], y, facecolor='green')
    plt.savefig(text + "Xprofile.png")
    plt.clf()


def plotY(text):
    image = Image.open(text)
    width, height = image.size
    base = plt.gca().transData
    rot = transforms.Affine2D().rotate_deg(90)
    plt.axis('off')
    x = range(height)
    y = [sum([1 - foo(image.getpixel((x, y))) for x in range(width)]) for y in range(height)]
    plt.plot(x, y, color='red', scalex=False, scaley=False)
    plt.fill_between(x, [0 for _ in range(height)], y, facecolor='red')
    plt.savefig(text + "Yprofile.png")
    plt.clf()
    image = Image.open(text + "Yprofile.png")
    image.transpose(Image.ROTATE_270).save(text + "Yprofile.png")


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


def change_to_halftone(image):
    width, height = image.size
    newImage = Image.new('P', (width, height))
    for x in range(width):
        for y in range(height):
            color = image.getpixel((x, y))
            bright = floor(0.3 * color[0] + 0.59 * color[1] + 0.11 * color[2])
            newImage.putpixel((x, y), bright)
    return newImage


def crop(image):
    width, height = image.size
    flag = False
    left_boarder = 0
    right_boarder = width - 1
    top_boarder = 0
    bottom_boarder = height - 1
    for x in range(width):
        if (flag):
            left_boarder = x - 1
            break
        for y in range(height):
            if image.getpixel((x, y)) == 0:
                flag = True
                break
    flag = False
    for x in range(width - 1, -1, -1):
        if (flag):
            right_boarder = x + 2
            break
        for y in range(height):
            if image.getpixel((x, y)) == 0:
                flag = True
                break
    flag = False
    for y in range(height):
        if (flag):
            top_boarder = y - 1
            break
        for x in range(width):
            if image.getpixel((x, y)) == 0:
                flag = True
                break
    flag = False
    for y in range(height - 1, -1, -1):
        if (flag):
            bottom_boarder = y + 2
            break
        for x in range(width):
            if image.getpixel((x, y)) == 0:
                flag = True
                break
    area = (left_boarder, top_boarder, right_boarder, bottom_boarder)
    cropped_image = image.crop(area)
    return cropped_image


def get_coords(boundaries, image):
    coords = []
    width, height = image.size
    for item in boundaries:
        flag = False
        for y in range(height):
            if (flag):
                top_boarder = y - 1
                break
            for x in range(item[0], item[1] + 1):
                if image.getpixel((x, y)) == 0:
                    flag = True
                    break
        flag = False
        for y in range(height - 1, -1, -1):
            if (flag):
                bottom_boarder = y + 1
                break
            for x in range(item[0], item[1] + 1):
                if image.getpixel((x, y)) == 0:
                    flag = True
                    break
        coords.append([item[0], top_boarder, item[1], bottom_boarder])
    return coords


def get_boundaries(x_data, y_data):
    boundaries = []
    left = 0
    flag = True
    for item in x_data:
        if item == len(x_data) - 1:
            if flag:
                right = item
                boundaries.append((left, right))
            break
        if flag:
            if y_data[item] > 1 and (y_data[item + 1] == 0 or y_data[item + 1] == 1):
                right = item
                boundaries.append((left, right))
                flag = False
        else:
            if (y_data[item] == 0 or y_data[item] == 1) and y_data[item + 1] > 1:
                left = item
                flag = True
    return boundaries


def process_string(string):
    image = binary(change_to_halftone(string), 150)
    image = crop(image)
    width, height = image.size
    x_data = range(width)
    y_data = [sum([1 - image.getpixel((x, y)) for y in range(height)]) for x in range(width)]
    boundaries = get_boundaries(x_data, y_data)
    coords = get_coords(boundaries, image)

    test_image = image.convert("RGB")
    draw = ImageDraw.Draw(test_image)
    for item in coords:
        draw.rectangle(item, outline="red")
    return image, test_image, coords


def main():
    image = Image.open("5.png")
    cropped_text, test_image, coords = process_string(image)
    cropped_text.save("cropped_text.bmp")
    test_image.save("processed_picture.bmp")
    with open("coords.txt", 'w') as file:
        for item in coords:
            for element in item:
                file.write(str(element) + ' ')
            file.write("\n")
    plotX("cropped_text.bmp")
    plotY("cropped_text.bmp")
    # image = Image.open("pictures/string2.png")
    # cropped_text, test_image, coords = process_string(image)
    # cropped_text.save("pictures/cropped_text2.bmp")
    # test_image.save("pictures/processed_picture2.bmp")
    # with open("coords2.txt", 'w') as file:
    #     for item in coords:
    #         for element in item:
    #             file.write(str(element) + ' ')
    #         file.write("\n")
    #
    # image = Image.open("pictures/string3.png")
    # cropped_text, test_image, coords = process_string(image)
    # cropped_text.save("pictures/cropped_text3.bmp")
    # test_image.save("pictures/processed_picture3.bmp")
    # with open("coords3.txt", 'w') as file:
    #     for item in coords:
    #         for element in item:
    #             file.write(str(element) + ' ')
    #         file.write("\n")


if __name__ == "__main__":
    main()
