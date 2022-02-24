from io import BytesIO
from base64 import decodebytes
import argparse

import colorama
from PIL import Image
from colorama import Fore, Back, Style

colorama.init()

colors_dict = {"BLACK": (0, 0, 0),
               "RED": (255, 0, 0),
               "GREEN": (0, 255, 0),
               "YELLOW": (255, 255, 0),
               "BLUE": (0, 0, 255),
               "MAGENTA": (255, 0, 255),
               "CYAN": (0, 255, 255),
               "WHITE": (255, 255, 255)}


def read_img(source, base64=False):
    if base64:
        source = BytesIO(decodebytes(source.encode()))
    return Image.open(source)


def resize(img, width=None, height=None, ar_coef=2.4):
    if width or height:
        if height is None:
            w, h = img.size
            height = int(h/w*width/ar_coef)
        elif width is None:
            w, h = img.size
            width = int(w*ar_coef/h * height)
        return img.resize((width, height))
    return img


def pick_color(r, g, b, bg_color=None):
    m, s = "BLACK", 255**2*3
    for color, (cr, cg, cb) in colors_dict.items():
        score = ((cr-r)**2+(cg-g)**2+(cb-b)**2)
        if color != bg_color and score < s:
            m = color
            s = score
    return m


def get_pixel(pixel, chars, colorful=False, bg_color=None):
    if colorful:
        r, g, b = pixel
        color = pick_color(r, g, b, bg_color)
        color = vars(Fore)[color]
        return color + chars[int((0.2989 * r + 0.5870 * g + 0.1140 * b) * len(chars) / 256)] + Fore.RESET
    else:
        return chars[pixel * len(chars) // 256]


def to_ascii(img, width=None, height=None, colorful=False, chars=None, reverse=False,
             bg_color=None, bright=False, ar_coef=2.4):
    img = resize(img, width, height, ar_coef)
    if colorful:
        img = img.convert('RGB')
    else:
        img = img.convert('L')

    if bg_color:
        bg_color = vars(Back)[bg_color.upper()]

    chars = chars or r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]
    if reverse:
        chars = list(reversed(chars))

    pixels = img.load()
    text_img = [Style.BRIGHT] if bright else []
    w, h = img.size
    for i in range(h):
        line = bg_color if bg_color else ""
        for j in range(w):
            line += get_pixel(pixels[j, i], chars, colorful, bg_color)
        line += Back.RESET if bg_color else ""
        text_img.append(line)
    if bright:
        text_img.append(Style.RESET_ALL)
    return '\n'.join(text_img)


def img_to_ascii(source, width=None, height=None, colorful=False,
                 chars=None, reverse=False, bg_color=None, bright=False, ar_coef=2.4, base64=False):

    img = read_img(source, base64=base64)

    ascii_img = to_ascii(
        img,
        width=width,
        height=height,
        colorful=colorful,
        chars=chars,
        reverse=reverse,
        bg_color=bg_color,
        bright=bright,
        ar_coef=ar_coef,
    )
    img.close()

    return ascii_img


def main():
    parser = argparse.ArgumentParser(description='read image as ascii text')
    parser.add_argument('source', metavar='source', type=str, help='path to image file')
    parser.add_argument('-w', '--width', dest='width', type=int, default=None,
                        help='number of columns/characters to use in the generated ascii image')
    parser.add_argument('--height', dest='height', type=int, default=None,
                        help='number of lines to use in the generated ascii image')
    parser.add_argument('-c', '--colorful', dest='colorful', default=False, action='store_true',
                        help='get ascii image with colors')
    parser.add_argument('--bg', dest='bg_color', default=None, help='Background color')
    parser.add_argument('-b', '--bright', dest='bright', default=False, action='store_true', help='enable bright mode')
    parser.add_argument('-r', '--reverse', dest='reverse', default=False, action='store_true',
                        help='inverse brightness')
    parser.add_argument('--ar', '--aspect-ratio', dest='ar_coef', type=float, default=2.4,
                        help='set aspect ratio coefficient')
    parser.add_argument('--chars', dest='chars', type=str, default=None,
                        help='ascii chars to use for picture generation')
    parser.add_argument('-o', '--output', dest='output', type=str, default=None,
                        help='output the result to a file')

    args = parser.parse_args()

    result = img_to_ascii(
        args.source,
        width=args.width,
        height=args.height,
        colorful=args.colorful,
        chars=args.chars,
        bg_color=args.bg_color,
        bright=args.bright,
        ar_coef=args.ar_coef,
        reverse=args.reverse,
    )

    if args.output is None:
        print(result)
    else:
        with open(args.output, 'w') as f:
            f.write(result + '\n')


if __name__ == '__main__':
    main()
