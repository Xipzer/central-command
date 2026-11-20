#!/usr/bin/env python3
"""Draws the Central Command tray icon: a C around a centre point (Pillow).

  tools/make_icon.py <out.ico> [dark]     white, for a dark taskbar; with "dark" the dark one for a light taskbar
  tools/make_icon.py --sheet <out.png>    both at 16, 20, 24 and 32 px on both taskbar colours, for review

The same mark is drawn in the panel header (mark() in src/panel.c).
"""
import math
import sys

from PIL import Image, ImageDraw

SIZES = [16, 20, 24, 32, 40, 48, 64]
WHITE, DARK = (255, 255, 255), (27, 27, 31)
RED = (229, 72, 77)  # the app's accent: the centre point, on either taskbar colour


def parts(n):
    """Outer radius, ring width and centre radius in pixels. Ring, gap and centre are each a third of the radius,
    on whole pixels so the small sizes stay sharp. At 16 px there is no room for thirds and the centre gives way."""
    if n < 20:
        return n / 2, 3, 2
    r = n // 6 * 3
    return r, r / 3, r / 3


def mask(n, centre):
    """The C, or only its centre point when centre is set, as an alpha mask."""
    s = 16
    r, w, c = (v * s for v in parts(n))
    img = Image.new("L", (n * s, n * s), 0)
    d = ImageDraw.Draw(img)
    mid = n * s / 2
    # The C: a ring open to the right by 45 degrees each way, with round ends.
    if centre:
        d.ellipse([mid - c, mid - c, mid + c, mid + c], fill=255)
        return img.resize((n, n), Image.LANCZOS)
    d.arc([mid - r, mid - r, mid + r, mid + r], 45, 315, fill=255, width=round(w))
    for a in (45, -45):
        x, y = mid + (r - w / 2) * math.cos(math.radians(a)), mid + (r - w / 2) * math.sin(math.radians(a))
        d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=255)
    return img.resize((n, n), Image.LANCZOS)


def draw(n, rgb):
    img = Image.new("RGBA", (n, n), rgb + (0,))
    img.putalpha(mask(n, False))
    dot = Image.new("RGBA", (n, n), RED + (0,))
    dot.putalpha(mask(n, True))
    return Image.alpha_composite(img, dot)


def sheet(out):
    zoom, sizes = 6, [16, 20, 24, 32]
    row = sum(sizes) + sum(n * zoom for n in sizes) + 22 * len(sizes) + 16
    img = Image.new("RGB", (row + 24, 2 * (32 * zoom + 24) + 36), (58, 62, 66))
    for k, (bar, rgb) in enumerate((((28, 30, 32), WHITE), ((238, 238, 240), DARK))):
        y = 12 + k * (32 * zoom + 36)
        ImageDraw.Draw(img).rectangle([12, y, 12 + row, y + 32 * zoom + 24], fill=bar)
        x = 24
        for n in sizes:  # as the taskbar shows them
            icon = draw(n, rgb)
            img.paste(icon, (x, y + 12 + (32 - n) // 2), icon)
            x += n + 10
        for n in sizes:  # the same pixels, enlarged
            tile = Image.new("RGB", (n, n), bar)
            icon = draw(n, rgb)
            tile.paste(icon, (0, 0), icon)
            img.paste(tile.resize((n * zoom, n * zoom), Image.NEAREST), (x, y + 12 + (32 - n) * zoom // 2))
            x += n * zoom + 12
    img.save(out)


if __name__ == "__main__":
    if "--sheet" in sys.argv:
        sheet(sys.argv[sys.argv.index("--sheet") + 1])
    else:
        imgs = [draw(n, DARK if "dark" in sys.argv[2:] else WHITE) for n in SIZES]
        out = sys.argv[1] if len(sys.argv) > 1 else "central-command.ico"
        imgs[-1].save(out, sizes=[(n, n) for n in SIZES], append_images=imgs[:-1])
