#!/usr/bin/env python3
"""生成站点根目录 favicon.ico（主题绿 + 字母 S）。修改后重新运行本脚本即可。"""
from __future__ import annotations

import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("需要 Pillow: pip install Pillow", file=sys.stderr)
    sys.exit(1)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "favicon.ico")

# 与 index.html 中 theme-color / 主色一致
BG = "#6c8d71"
FG = "#ffffff"
ACCENT = "#4d6a53"


def find_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for path in candidates:
        if os.path.isfile(path):
            try:
                return ImageFont.truetype(path, size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def render(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    pad = max(1, size // 14)
    r = max(2, size // 5)
    draw.rounded_rectangle(
        [pad, pad, size - pad - 1, size - pad - 1],
        radius=r,
        fill=BG,
        outline=ACCENT,
        width=max(1, size // 32),
    )
    font_size = max(8, int(size * 0.58))
    font = find_font(font_size)
    ch = "S"
    bbox = draw.textbbox((0, 0), ch, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (size - tw) // 2 - bbox[0]
    y = (size - th) // 2 - bbox[1]
    draw.text((x, y), ch, font=font, fill=FG)
    return img


def main() -> None:
    sizes = (16, 32, 48)
    icons = [render(s) for s in sizes]
    icons[0].save(OUT, format="ICO", sizes=[(s, s) for s in sizes], append_images=icons[1:])
    print("wrote", OUT, "sizes=", sizes)


if __name__ == "__main__":
    main()
