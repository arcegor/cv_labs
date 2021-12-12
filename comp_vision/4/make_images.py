from PIL import Image, ImageFont, ImageDraw


def get_symbol_images(text, font, font_size):
    for symbol in text:
        image = Image.new("1", (font_size, font_size), 1)
        draw = ImageDraw.Draw(image)
        symbol_width, symbol_height = draw.textsize(symbol, font=font)

        new_image = Image.new("1", (symbol_width, symbol_height), 1)
        new_draw = ImageDraw.Draw(new_image)
        new_draw.text((0, 0), symbol, 0, font=font)
        new_image.save("symbols/" + symbol + ".png")


def crop(image):
    width, height = image.size
    flag = False
    left_boarder = 0
    right_boarder = width - 1
    top_boarder = 0
    bottom_boarder = height - 1
    for x in range(width):
        if flag:
            left_boarder = x - 1
            break
        for y in range(height):
            if image.getpixel((x, y)) == 0:
                flag = True
                break
    flag = False
    for x in range(width - 1, -1, -1):
        if flag:
            right_boarder = x + 2
            break
        for y in range(height):
            if image.getpixel((x, y)) == 0:
                flag = True
                break
    flag = False
    for y in range(height):
        if flag:
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


def main():
    font_size = 20
    font = ImageFont.truetype("TNR.ttf", font_size)
    text = "0123456789"
    get_symbol_images(text, font, font_size)
    for symbol in text:
        image = Image.open("symbols/" + symbol + ".png")
        cp_image = crop(image)
        cp_image.save("symbols/" + symbol + ".png")


if __name__ == "__main__":
    main()