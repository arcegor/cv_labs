import matplotlib.pyplot as plt
from matplotlib import transforms
from PIL import Image


def foo(item):
    if (item == 255):
        return 1
    return 0


def plotX(symbol):
    image = Image.open("symbols/" + symbol + ".png")
    width, height = image.size
    plt.axis('off')
    x = range(width)
    y = [sum([1 - foo(image.getpixel((x, y))) for y in range(height)]) for x in range(width)]
    plt.plot(x, y, color='green')
    plt.fill_between(x, [0 for _ in range(width)], y, facecolor='green')
    plt.savefig("Xprofiles/" + symbol + "profile.png")
    plt.clf()


def plotY(symbol):
    image = Image.open("symbols/" + symbol + ".png")
    width, height = image.size
    base = plt.gca().transData
    rot = transforms.Affine2D().rotate_deg(90)
    plt.axis('off')
    x = range(height)
    y = [sum([1 - foo(image.getpixel((x, y))) for x in range(width)]) for y in range(height)]
    plt.plot(x, y, color='red', scalex=False, scaley=False)
    plt.fill_between(x, [0 for _ in range(height)], y, facecolor='red')
    plt.savefig("Yprofiles/" + symbol + "profile.png")
    plt.clf()
    image = Image.open("Yprofiles/" + symbol + "profile.png")
    image.transpose(Image.ROTATE_270).save("Yprofiles/" + symbol + "profile.png")


def main():
    text = "0123456789"
    for symbol in text:
        plotX(symbol)

    for symbol in text:
        plotY(symbol)


if __name__ == "__main__":
    main()
