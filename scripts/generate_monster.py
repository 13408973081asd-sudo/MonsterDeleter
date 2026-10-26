#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_monster.py —— 程序化生成 MonsterDeleter 的怪兽动画素材 monster.gif
=========================================================================
用纯代码绘制一个“吞文件”的大将怪兽动画（透明背景），
这样工程完全自包含、无版权问题、可复现。

依赖： Pillow  (pip install Pillow)
输出： ../assets/monster.gif   （约 20 帧，透明背景，循环播放）

你可以修改下面参数来换怪兽颜色、体型，或整体重绘。
"""

import os
import math
from PIL import Image, ImageDraw

SIZE = 340              # 画布边长
FRAMES = 24             # 总帧数
FPS = 12                # 每秒帧数（GIF 延迟 = 1000//FPS 毫秒）

BODY = (93, 173, 76)          # 身体主色（绿）
BODY_DARK = (56, 118, 44)     # 描边深色
BELLY = (200, 235, 170)       # 肚皮
MOUTH_IN = (150, 28, 28)      # 口腔内部
TEETH = (255, 255, 255)       # 牙齿
EYE_WHITE = (255, 255, 255)
PUPIL = (30, 30, 30)


def draw_frame(open_ratio: float, bounce: float, eye_angry: float,
               mouth_wobble: float) -> Image.Image:
    """
    open_ratio  : 0~1，嘴张开的程度
    bounce      : 0~1，身体上下弹跳幅度（吞咽抖动）
    eye_angry   : 0~1，眼睛眯起/瞪大的程度
    mouth_wobble: 0~1，下颚左右摇晃
    """
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    cx = SIZE // 2
    body_top = 60 + bounce * 8
    body_bottom = 250 - bounce * 8
    body_w = 190
    body_left = cx - body_w // 2
    body_right = cx + body_w // 2

    m = open_ratio
    mouth_cx = cx + mouth_wobble * 14
    mouth_w = int(70 + 60 * m)
    mouth_h = int(24 + 92 * m)
    mouth_top = body_top + int(150 - 20 * m)
    mouth_bottom = mouth_top + mouth_h

    d.ellipse([body_left, body_top, body_right, body_bottom],
              fill=BODY, outline=BODY_DARK, width=6)
    d.ellipse([body_left + 26, body_top + 40, body_right - 26, body_bottom - 14],
              fill=BELLY)

    foot_y = body_bottom - 10
    d.ellipse([body_left + 8, foot_y - 14, body_left + 52, foot_y + 16],
              fill=BODY_DARK)
    d.ellipse([body_right - 52, foot_y - 14, body_right - 8, foot_y + 16],
              fill=BODY_DARK)

    horn_top = body_top - 26
    d.polygon([(cx - 46, body_top - 6), (cx - 58, horn_top + 4), (cx - 30, body_top - 6)],
              fill=BODY_DARK)
    d.polygon([(cx + 46, body_top - 6), (cx + 58, horn_top + 4), (cx + 30, body_top - 6)],
              fill=BODY_DARK)

    if m > 0.02:
        d.ellipse([mouth_cx - mouth_w // 2, mouth_top,
                   mouth_cx + mouth_w // 2, mouth_bottom],
                  fill=MOUTH_IN)
        teeth_n = 5
        tw = mouth_w // teeth_n
        for i in range(teeth_n):
            x0 = mouth_cx - mouth_w // 2 + i * tw
            tri_top = mouth_top + 2
            tri_bottom = tri_top + 16 + int(8 * m)
            d.polygon([(x0 + 3, tri_top), (x0 + tw - 3, tri_top),
                       (x0 + tw // 2, tri_bottom)],
                      fill=TEETH)
        for i in range(teeth_n):
            x0 = mouth_cx - mouth_w // 2 + i * tw
            tri_bottom = mouth_bottom - 2
            tri_top = tri_bottom - 16 - int(8 * m)
            d.polygon([(x0 + 3, tri_bottom), (x0 + tw - 3, tri_bottom),
                       (x0 + tw // 2, tri_top)],
                      fill=TEETH)
    else:
        d.line([mouth_cx - 20, mouth_top + 10, mouth_cx + 20, mouth_top + 10],
               fill=BODY_DARK, width=3)

    angry_shift = eye_angry * 10
    for ex in (cx - 44, cx + 44):
        ey = body_top + 58 - angry_shift * 0.4
        r = int(22 - eye_angry * 4)
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=EYE_WHITE, outline=BODY_DARK, width=3)
        pr = max(5, int(9 + 4 * m))
        d.ellipse([ex - pr, ey - pr, ex + pr, ey + pr], fill=PUPIL)
        d.ellipse([ex - pr + 3, ey - pr + 3, ex - pr + 8, ey - pr + 8], fill=(255, 255, 255))
        brow_y = ey - r - 8 - int(4 * eye_angry)
        d.line([ex - r, brow_y + 8, ex + r, brow_y], fill=BODY_DARK, width=5)

    return img


def build() -> None:
    frames: list[Image.Image] = []
    for f in range(FRAMES):
        t = f / FRAMES
        if t < 0.34:
            open_r = t / 0.34
            bounce = 0.0
            angry = open_r
            wobble = 0.0
        elif t < 0.5:
            open_r = 1.0
            bounce = 0.25 + 0.15 * math.sin((t - 0.34) / 0.16 * math.pi * 3)
            angry = 1.0
            wobble = 0.05 * math.sin((t - 0.34) / 0.16 * math.pi * 4)
        elif t < 0.75:
            k = (t - 0.5) / 0.25
            open_r = max(0.12, abs(math.sin(k * math.pi * 3.0)))
            bounce = 0.3 + 0.25 * math.sin(k * math.pi * 6)
            angry = 0.6 + 0.4 * math.cos(k * math.pi * 3)
            wobble = 0.1 * math.sin(k * math.pi * 5)
        else:
            open_r = max(0.05, 0.2 - (t - 0.75) / 0.25 * 0.15)
            bounce = 0.1 * math.sin((t - 0.75) / 0.25 * math.pi * 2)
            angry = 0.5 - (t - 0.75) / 0.25 * 0.5
            wobble = 0.0
        frames.append(draw_frame(open_r, bounce, angry, wobble))

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
    out_path = os.path.normpath(os.path.join(out_dir, "monster.gif"))
    os.makedirs(out_dir, exist_ok=True)

    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=1000 // FPS,
        loop=0,
        disposal=2,
        transparency=0,
    )
    print(f"OK -> {out_path}  ({len(frames)} 帧, {FPS} fps, {SIZE}x{SIZE})")


if __name__ == "__main__":
    build()
