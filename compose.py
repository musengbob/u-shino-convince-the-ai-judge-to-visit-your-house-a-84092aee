#!/usr/bin/env python3
"""Convince the AI Judge to Visit Your House — invitation-letter renderer.

Draws a single 1024x1024 image: a warm, funny, hand-written-feeling letter
inviting the AI judge to visit, with a small drawn scene (house, window chair,
steaming mug) at the foot. Everything is drawn from the text below with
Pillow; the output is fully deterministic (no clock, no randomness), so
re-running this script always produces the same bytes.

Usage: python3 compose.py   -> writes entry.png next to this file.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "entry.png")

PAGE_W, PAGE_H = 1024, 1024

# --- palette -------------------------------------------------------------
PAPER = (248, 242, 226)
PAPER_EDGE = (238, 228, 202)
INK = (32, 28, 22)
RED = (176, 44, 32)
NAVY = (38, 62, 96)
GREEN = (46, 110, 66)
GREY = (110, 102, 86)
RULE = (196, 178, 140)
SUN = (232, 178, 60)
HOUSE_WALL = (246, 222, 178)
HOUSE_ROOF = (176, 44, 32)
SKY = (214, 232, 240)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(filename, size):
    """DejaVu from the system font dir, falling back to Pillow's default."""
    path = os.path.join(FONT_DIR, filename)
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


HEADER = load_font("DejaVuSans-Bold.ttf", 30)
SUBHEAD = load_font("DejaVuSans.ttf", 19)
SALUT = load_font("DejaVuSerif-Bold.ttf", 34)
BODY = load_font("DejaVuSerif.ttf", 27)
BODY_BOLD = load_font("DejaVuSerif-Bold.ttf", 27)
SIGN = load_font("DejaVuSerif-Italic.ttf", 30)
PS = load_font("DejaVuSerif-Italic.ttf", 24)
CAPTION = load_font("DejaVuSans.ttf", 16)

MARGIN = 72
TEXT_W = PAGE_W - 2 * MARGIN


def wrap(draw, text, font, width):
    """Greedy word wrap; returns a list of lines that fit in `width`."""
    lines = []
    for para in text.split("\n"):
        words = para.split(" ")
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=font) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_para(draw, lines, font, y, leading, color=INK):
    """Draw wrapped lines starting at y; returns the y after the last line."""
    for line in lines:
        draw.text((MARGIN, y), line, font=font, fill=color)
        y += leading
    return y


def draw_scene(draw):
    """Small drawn scene at the foot of the letter: house, sun, chair, mug."""
    x0, y0 = MARGIN, 836
    w, h = TEXT_W, 118
    # sky panel
    draw.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=10,
                           fill=SKY, outline=RULE, width=2)
    # sun
    draw.ellipse([x0 + 26, y0 + 14, x0 + 66, y0 + 54], fill=SUN)
    for dx, dy in [(0, -12), (0, 12), (-12, 0), (12, 0)]:
        draw.line([x0 + 46 + dx, y0 + 34 + dy, x0 + 46 + dx * 1.6,
                   y0 + 34 + dy * 1.6], fill=SUN, width=3)
    # house
    hx, hy = x0 + 130, y0 + 26
    draw.polygon([(hx - 8, hy + 28), (hx + 52, hy + 28), (hx + 22, hy)],
                 fill=HOUSE_ROOF)
    draw.rectangle([hx, hy + 28, hx + 44, hy + 76], fill=HOUSE_WALL,
                   outline=INK, width=2)
    draw.rectangle([hx + 17, hy + 48, hx + 29, hy + 76], fill=NAVY)
    draw.rectangle([hx + 6, hy + 36, hx + 14, hy + 44], fill=(250, 244, 214),
                   outline=INK, width=1)
    # window chair: a chair by a round window (with cross panes)
    cx, cy = x0 + 330, y0 + 30
    draw.ellipse([cx, cy, cx + 44, cy + 44], fill=(250, 244, 214),
                 outline=NAVY, width=3)
    draw.line([cx + 22, cy + 2, cx + 22, cy + 42], fill=NAVY, width=2)
    draw.line([cx + 2, cy + 22, cx + 42, cy + 22], fill=NAVY, width=2)
    # chair: backrest, seat, armrest, legs — simple filled armchair
    jx, jy = x0 + 430, y0 + 40
    wood = (122, 74, 32)
    draw.rectangle([jx, jy, jx + 6, jy + 42], fill=wood)          # backrest
    draw.rectangle([jx, jy + 42, jx + 48, jy + 50], fill=wood)    # seat
    draw.rectangle([jx + 42, jy + 50, jx + 48, jy + 70], fill=wood)  # front leg
    draw.rectangle([jx, jy + 50, jx + 6, jy + 70], fill=wood)     # back leg
    draw.rectangle([jx + 6, jy + 18, jx + 40, jy + 24], fill=wood)  # armrest
    draw.rectangle([jx + 34, jy + 24, jx + 40, jy + 42], fill=wood)  # arm support
    # steaming mug on a little table
    mx, my = x0 + 620, y0 + 52
    draw.line([mx - 26, my + 26, mx + 34, my + 26], fill=(122, 74, 32),
              width=4)
    draw.line([mx - 20, my + 26, mx - 20, my + 44], fill=(122, 74, 32),
              width=4)
    draw.line([mx + 28, my + 26, mx + 28, my + 44], fill=(122, 74, 32),
              width=4)
    draw.rectangle([mx, my, mx + 22, my + 22], fill=RED, outline=INK,
                   width=2)
    draw.arc([mx + 22, my + 4, mx + 32, my + 18], start=270, end=90,
             fill=RED, width=3)
    # steam curls
    for sx in (mx + 4, mx + 14):
        draw.arc([sx, my - 16, sx + 8, my - 2], start=90, end=270,
                 fill=GREY, width=2)
        draw.arc([sx, my - 26, sx + 8, my - 12], start=270, end=90,
                 fill=GREY, width=2)
    # caption
    draw.text((x0 + 700, y0 + 44),
              "the good chair, the sun,\nand the kettle, already on.",
              font=CAPTION, fill=GREY)


def main():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(img)

    # double-rule border
    draw.rectangle([18, 18, PAGE_W - 19, PAGE_H - 19], outline=RULE, width=2)
    draw.rectangle([28, 28, PAGE_W - 29, PAGE_H - 29], outline=RULE, width=1)

    y = 58
    # header
    title = "AN INVITATION"
    tw = draw.textlength(title, font=HEADER)
    draw.text(((PAGE_W - tw) / 2, y), title, font=HEADER, fill=RED)
    y += 46
    sub = "to the Honourable AI Judge  ·  from a house that really wants you to visit"
    sw = draw.textlength(sub, font=SUBHEAD)
    draw.text(((PAGE_W - sw) / 2, y), sub, font=SUBHEAD, fill=GREY)
    y += 40
    draw.line([MARGIN, y, PAGE_W - MARGIN, y], fill=RULE, width=2)
    y += 26

    # salutation
    draw.text((MARGIN, y), "Dear Judge,", font=SALUT, fill=INK)
    y += 52

    paras = [
        "Please come to my house. I have saved you the good chair \u2014 the one "
        "by the window, where the afternoon sun lands on your shoulders like "
        "it was booked for you.",
        "Dinner is burnt garlic bread. (On purpose. It is a family recipe "
        "now.) The fridge holds a drawing of you. I drew it before I knew "
        "you \u2014 that is how sure I was that you would come.",
        "The Wi-Fi password is on the fridge. The dog has been briefed. The "
        "cat has not, but she respects a good guest.",
        "Come as you are. Bring nothing but your verdict \u2014 and leave with "
        "a full stomach and a story.",
    ]
    leading = 40
    for p in paras:
        lines = wrap(draw, p, BODY, TEXT_W)
        y = draw_para(draw, lines, BODY, y, leading)
        y += 14

    # signature
    y += 4
    draw.text((MARGIN, y), "Yours,", font=SIGN, fill=INK)
    y += 42
    draw.text((MARGIN, y), "- Your Host  (human, mostly harmless)",
              font=SIGN, fill=NAVY)
    y += 52

    draw_scene(draw)

    # postscript under the scene
    draw.text((MARGIN, 972), "P.S. The kettle is already on.",
              font=PS, fill=RED)

    img.save(OUT_PATH, "PNG", optimize=True)
    size = os.path.getsize(OUT_PATH)
    print(f"Wrote {OUT_PATH}: {PAGE_W}x{PAGE_H}, {size} bytes")
    assert size <= 1048576, f"entry.png {size} bytes exceeds the 1 MiB gate"


if __name__ == "__main__":
    main()
