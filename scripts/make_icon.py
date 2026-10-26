#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_icon.py —— 从 monster.gif 首帧生成应用图标 monster.ico（含多尺寸）
依赖： Pillow
输出： ../assets/monster.ico
"""

import os
from PIL import Image, ImageSequence

HERE = os.path.dirname(os.path.abspath(__file__))
GIF = os.path.normpath(os.path.join(HERE, "..", "assets", "monster.gif"))
ICO = os.path.normpath(os.path.join(HERE, "..", "assets", "monster.ico"))


def build() -> None:
    img = Image.open(GIF)
    frame = next(iter(ImageSequence.Iterator(img))).convert("RGBA")
    canvas = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    f = frame.resize((256, 256), Image.LANCZOS)
    canvas.paste(f, (0, 0), f)
    canvas.save(ICO, sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print(f"OK -> {ICO}")


if __name__ == "__main__":
    build()
