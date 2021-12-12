from PIL import Image
import pandas as pd


def foo(item):
    if (item == 255):
        return 1
    return 0


def weight_of_black(symbol):
    image = Image.open("symbols/" + symbol + ".png")
    width, height = image.size
    sum_ = 0
    for x in range(width):
        for y in range(height):
            sum_ += foo(image.getpixel((x, y)))
    return width * height - sum_, (width * height - sum_) / (width * height)


def coords_of_center_of_gravity(symbol):
    image = Image.open("symbols/" + symbol + ".png")
    width, height = image.size
    sum1 = 0
    sum2 = 0
    for x in range(width):
        for y in range(height):
            sum1 += (x + 1) * (1 - foo(image.getpixel((x, y))))
    for x in range(width):
        for y in range(height):
            sum2 += (y + 1) * (1 - foo(image.getpixel((x, y))))
    weight = weight_of_black(symbol)
    return sum1 / weight[0], sum2 / weight[0]


def norm_coords_of_center_of_gravity(symbol):
    image = Image.open("symbols/" + symbol + ".png")
    width, height = image.size
    sum1 = 0
    sum2 = 0
    for x in range(width):
        for y in range(height):
            sum1 += (x + 1) * (1 - foo(image.getpixel((x, y))))
    for x in range(width):
        for y in range(height):
            sum2 += (y + 1) * (1 - foo(image.getpixel((x, y))))
    weight = weight_of_black(symbol)[0]
    return ((sum1 / weight) - 1) / (width - 1), ((sum2 / weight) - 1) / (height - 1)


def axial_moments_of_inertia(symbol):
    image = Image.open("symbols/" + symbol + ".png")
    width, height = image.size
    sum1 = 0
    sum2 = 0
    center = coords_of_center_of_gravity(symbol)
    for x in range(width):
        for y in range(height):
            sum1 += (1 - foo(image.getpixel((x, y)))) * (y + 1 - center[1]) ** 2
    for x in range(width):
        for y in range(height):
            sum2 += (1 - foo(image.getpixel((x, y)))) * (x + 1 - center[0]) ** 2
    return sum1, sum2


def norm_axial_moments_of_inertia(symbol):
    image = Image.open("symbols/" + symbol + ".png")
    width, height = image.size
    sum1 = 0
    sum2 = 0
    center = coords_of_center_of_gravity(symbol)
    for x in range(width):
        for y in range(height):
            sum1 += (1 - foo(image.getpixel((x, y)))) * (y + 1 - center[1]) ** 2
    for x in range(width):
        for y in range(height):
            sum2 += (1 - foo(image.getpixel((x, y)))) * (x + 1 - center[0]) ** 2
    return sum1 / (width ** 2 + height ** 2), sum2 / (width ** 2 + height ** 2)


def main():
    text = "0123456789"
    df = pd.DataFrame({'symbol': list(text),
                       'weight_of_black': [weight_of_black(symbol)[0] for symbol in text],
                       'specific_weight_of_black': [weight_of_black(symbol)[1] for symbol in text],
                       'center_of_gravity': [coords_of_center_of_gravity(symbol) for symbol in text],
                       'norm_center_of_gravity': [norm_coords_of_center_of_gravity(symbol) for symbol in text],
                       'axial_moments_of_inertia': [axial_moments_of_inertia(symbol) for symbol in text],
                       'norm_axial_moments_of_inertia': [norm_axial_moments_of_inertia(symbol) for symbol in text]})
    df.to_csv("signs.csv", sep=";")


if __name__ == "__main__":
    main()
