#!/usr/bin/env python3
"""Draw the catalog logo (256 x 256 PNG): a plain map mark, a grid of blocks with one highlighted
object on a rounded square, no text, so it stays legible at icon size.

  <python with Pillow> logo.py <output png>
"""

import sys

from PIL import Image, ImageDraw

S = 4  # supersampling
N = 256 * S
BG = "#1d5f6b"
BLOCK = "#9cc9c2"
ACCENT = "#f2b134"


def main(out):
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, N - 1, N - 1), radius=44 * S, fill=BG)
    m, gap = 40 * S, 14 * S
    cell = (N - 2 * m - 2 * gap) / 3
    for i in range(3):
        for j in range(3):
            x0, y0 = m + i * (cell + gap), m + j * (cell + gap)
            fill = ACCENT if (i, j) == (1, 1) else BLOCK
            d.rounded_rectangle((x0, y0, x0 + cell, y0 + cell), radius=8 * S, fill=fill)
    im.resize((256, 256), Image.LANCZOS).save(out)


if __name__ == "__main__":
    main(sys.argv[1])
