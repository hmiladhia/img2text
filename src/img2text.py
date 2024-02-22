from __future__ import annotations

import argparse
from base64 import decodebytes
from io import BytesIO

import colorama
from PIL import Image

colorama.init()

_COLORS_DICT: dict[str, tuple[int, int, int]] = {
    "BLACK": (0, 0, 0),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "YELLOW": (255, 255, 0),
    "BLUE": (0, 0, 255),
    "MAGENTA": (255, 0, 255),
    "CYAN": (0, 255, 255),
    "WHITE": (255, 255, 255),
}

_BACKGROUND_DICT: dict[str, str] = {
    "BLACK": "\x1b[40m",
    "BLUE": "\x1b[44m",
    "CYAN": "\x1b[46m",
    "GREEN": "\x1b[42m",
    "LIGHTBLACK_EX": "\x1b[100m",
    "LIGHTBLUE_EX": "\x1b[104m",
    "LIGHTCYAN_EX": "\x1b[106m",
    "LIGHTGREEN_EX": "\x1b[102m",
    "LIGHTMAGENTA_EX": "\x1b[105m",
    "LIGHTRED_EX": "\x1b[101m",
    "LIGHTWHITE_EX": "\x1b[107m",
    "LIGHTYELLOW_EX": "\x1b[103m",
    "MAGENTA": "\x1b[45m",
    "RED": "\x1b[41m",
    "RESET": "\x1b[49m",
    "WHITE": "\x1b[47m",
    "YELLOW": "\x1b[43m",
}
_FOREGROUND_DICT: dict[str, str] = {
    "BLACK": "\x1b[30m",
    "BLUE": "\x1b[34m",
    "CYAN": "\x1b[36m",
    "GREEN": "\x1b[32m",
    "LIGHTBLACK_EX": "\x1b[90m",
    "LIGHTBLUE_EX": "\x1b[94m",
    "LIGHTCYAN_EX": "\x1b[96m",
    "LIGHTGREEN_EX": "\x1b[92m",
    "LIGHTMAGENTA_EX": "\x1b[95m",
    "LIGHTRED_EX": "\x1b[91m",
    "LIGHTWHITE_EX": "\x1b[97m",
    "LIGHTYELLOW_EX": "\x1b[93m",
    "MAGENTA": "\x1b[35m",
    "RED": "\x1b[31m",
    "RESET": "\x1b[39m",
    "WHITE": "\x1b[37m",
    "YELLOW": "\x1b[33m",
}
_BACKGROUND_RESET: str = "\x1b[49m"
_FOREGROUND_RESET: str = "\x1b[39m"
_BRIGHT_STYLE: str = "\x1b[1m"
_STYLE_RESET_ALL: str = "\x1b[0m"

_DEFAULT_CHARS = (
    r" .'`^\"\,:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
)

__author__ = "Dhia Hmila"
__version__ = "0.1.1"
__all__ = ["img_to_ascii", "to_ascii", "__version__", "__author__"]


def to_ascii(
    img: Image.Image,
    width: int | None = None,
    height: int | None = None,
    colorful: bool = False,
    chars: str | None = None,
    reverse: bool = False,
    bg_color: str | None = None,
    bright: bool = False,
    ar_coef: float = 2.4,
) -> str:
    img = _resize(img, width, height, ar_coef)
    img = img.convert("RGB" if colorful else "L")

    if bg_color:
        bg_color = _BACKGROUND_DICT[bg_color.upper()]

    chars = chars or _DEFAULT_CHARS
    if reverse:
        chars = chars[::-1]

    pixels = img.load()
    text_img = [_BRIGHT_STYLE] if bright else []
    w, h = img.size
    for i in range(h):
        line = bg_color if bg_color else ""
        for j in range(w):
            line += _get_pixel(pixels[j, i], chars, bg_color)
        line += _BACKGROUND_RESET if bg_color else ""
        text_img.append(line)
    if bright:
        text_img.append(_STYLE_RESET_ALL)
    return "\n".join(text_img)


def img_to_ascii(
    source: str,
    width: int | None = None,
    height: int | None = None,
    colorful: bool = False,
    chars: str | None = None,
    reverse: bool = False,
    bg_color: str | None = None,
    bright: bool = False,
    ar_coef: float = 2.4,
    base64: bool = False,
) -> str:
    with _read_img(source, base64=base64) as img:
        return to_ascii(
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


def main() -> None:
    args = _get_parser().parse_args()

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
        with open(args.output, "w") as f:
            f.write(result + "\n")


def _get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="read image as ascii text")
    parser.add_argument("source", metavar="source", type=str, help="path to image file")
    parser.add_argument(
        "-w",
        "--width",
        dest="width",
        type=int,
        default=None,
        help="number of columns/characters to use in the generated ascii image",
    )
    parser.add_argument(
        "--height",
        dest="height",
        type=int,
        default=None,
        help="number of lines to use in the generated ascii image",
    )
    parser.add_argument(
        "-c",
        "--colorful",
        dest="colorful",
        default=False,
        action="store_true",
        help="get ascii image with colors",
    )
    parser.add_argument("--bg", dest="bg_color", default=None, help="Background color")
    parser.add_argument(
        "-b",
        "--bright",
        dest="bright",
        default=False,
        action="store_true",
        help="enable bright mode",
    )
    parser.add_argument(
        "-r",
        "--reverse",
        dest="reverse",
        default=False,
        action="store_true",
        help="inverse brightness",
    )
    parser.add_argument(
        "--ar",
        "--aspect-ratio",
        dest="ar_coef",
        type=float,
        default=2.4,
        help="set aspect ratio coefficient",
    )
    parser.add_argument(
        "--chars",
        dest="chars",
        type=str,
        default=None,
        help="ascii chars to use for picture generation",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        type=str,
        default=None,
        help="output the result to a file",
    )

    return parser


def _read_img(source: str, base64: bool = False) -> Image.Image:
    if not base64:
        return Image.open(source)

    source_io = BytesIO(decodebytes(source.encode()))
    return Image.open(source_io)


def _resize(
    img: Image.Image,
    width: int | None = None,
    height: int | None = None,
    ar_coef: float = 2.4,
) -> Image.Image:
    if width:
        w, h = img.size
        height = int(h / w * width / ar_coef)
        img = img.resize((width, height))
    elif height:
        w, h = img.size
        width = int(w * ar_coef / h * height)
        img = img.resize((width, height))
    return img


def _pick_color(r: int, g: int, b: int, bg_color: str | None = None) -> str:
    m, s = "BLACK", 255**2 * 3
    for color, (cr, cg, cb) in _COLORS_DICT.items():
        score = (cr - r) ** 2 + (cg - g) ** 2 + (cb - b) ** 2
        if color != bg_color and score < s:
            m = color
            s = score
    return m


def _get_pixel(
    pixel: tuple[int, int, int] | int,
    chars: str,
    bg_color: str | None = None,
) -> str:
    if not isinstance(pixel, tuple):
        return chars[pixel * len(chars) // 256]

    r, g, b = pixel
    color = _pick_color(r, g, b, bg_color)
    color = _FOREGROUND_DICT[color]
    grayscale = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return color + chars[int(grayscale * len(chars) / 256)] + _FOREGROUND_RESET


if __name__ == "__main__":
    main()
