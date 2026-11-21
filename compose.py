#!/usr/bin/env python3
"""Compose entry.png for news-image-20261121: the world news of
Saturday 21 November 2026 as a one-page illustrated newspaper.

Layout: masthead naming the day, one lead panel, a 2x2 grid of four
more stories, and an "also today" ticker along the bottom. The five
illustrations live in assets/; every word is typeset here with PIL so
no text can come out garbled. The page is 1024x1024 and is saved as
JPEG bytes under the name entry.png (the gate tells PNG from JPEG by
first bytes), kept under 1 MiB. Same inputs, same bytes, every run.
"""
import os

from PIL import Image, ImageDraw, ImageFont

from typeset import columns, double_rule, fit_size

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")
SIZE = 1024
MARGIN = 26

PAPER = (244, 239, 228)
NAVY = (24, 38, 63)
INK = (30, 30, 34)
RED = (166, 38, 32)
GREY = (92, 92, 96)
GOLD = (240, 220, 160)
WHITE = (238, 238, 238)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def crop_to(img, w, h, focus_y=0.5):
    """Scale img to cover a w x h box, then crop, centred horizontally
    and at focus_y vertically (0 = top, 1 = bottom)."""
    img = img.convert("RGB")
    scale = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    left = (img.width - w) // 2
    top = int((img.height - h) * focus_y)
    return img.crop((left, top, left + w, top + h))


def wrap(draw, text, fnt, max_w):
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


page = Image.new("RGB", (SIZE, SIZE), PAPER)
pen = ImageDraw.Draw(page)


def story(x, y, w, image, kicker, headline, sub, img_h, focus_y=0.5,
          head_size=33, sub_size=23):
    """Draw one story: framed illustration, kicker, headline, sub-line.
    Returns the y just past the sub-line."""
    art = Image.open(os.path.join(ASSETS, image))
    page.paste(crop_to(art, w, img_h, focus_y), (x, y))
    pen.rectangle([x, y, x + w, y + img_h], outline=NAVY, width=2)
    ty = y + img_h + 8
    pen.text((x + 2, ty), kicker, font=F(SANS_BOLD, 19), fill=RED)
    ty += 26
    head_size = fit_size(pen, headline, SANS_BOLD, w - 4, 2, head_size)
    for line in wrap(pen, headline, F(SANS_BOLD, head_size), w - 4):
        pen.text((x + 2, ty), line, font=F(SANS_BOLD, head_size), fill=INK)
        ty += head_size + 4
    for line in wrap(pen, sub, F(SANS, sub_size), w - 4):
        pen.text((x + 2, ty), line, font=F(SANS, sub_size), fill=GREY)
        ty += sub_size + 3
    return ty


# ---------------- masthead ----------------
pen.text((SIZE // 2, 16), "T H E   W O R L D   T O D A Y",
         font=F(SERIF_BOLD, 40), fill=NAVY, anchor="ma")
double_rule(pen, MARGIN, SIZE - MARGIN, 72, NAVY)
pen.text((SIZE // 2, 84), "SATURDAY, 21 NOVEMBER 2026",
         font=F(SANS_BOLD, 55), fill=RED, anchor="ma")
double_rule(pen, MARGIN, SIZE - MARGIN, 150, NAVY)

# ---------------- lead story ----------------
story(MARGIN, 166, SIZE - 2 * MARGIN,
      "media-generation-panel-ukraine-0-117789b3-eec4-48e3-9f7a-0839bdfab6a6.webp",
      "WAR  ·  UKRAINE & POLAND",
      "RUSSIA FIRES 400 DRONES AND 110 MISSILES",
      "Eight killed in Kyiv; two missiles down in Poland — NATO: a grave violation",
      img_h=200, focus_y=0.45, head_size=36, sub_size=23)

# ---------------- 2x2 grid ----------------
GRID = columns(SIZE, MARGIN, 18, 2)
COL = GRID[0][1]
RIGHT = GRID[1][0]
story(MARGIN, 492, COL,
      "media-generation-panel-markets-0-ac9d7ffb-058c-459c-afd1-061557ef1f5a.webp",
      "MARKETS  ·  AI SELL-OFF",
      "AI ROUT: S&P IN CORRECTION",
      "US stocks fall 3.7%; the Nasdaq erases its 2026 gains; "
      "the Nikkei drops 5%",
      img_h=100, focus_y=0.40, head_size=30, sub_size=21)
story(RIGHT, 492, COL,
      "media-generation-panel-court-0-76f5fbb2-2826-42cb-97c2-239c4abc0116.webp",
      "JUSTICE  ·  WORLD COURT",
      "GUILTY OF GENOCIDE",
      "Myanmar must let the Rohingya return and pay reparations, "
      "the court rules",
      img_h=100, focus_y=0.35, head_size=30, sub_size=21)
story(MARGIN, 724, COL,
      "media-generation-panel-pill-0-7376fe15-437c-4398-962a-db4693b8f612.webp",
      "HEALTH  ·  MEDICINE",
      "CANCER PILL STUNS TRIAL",
      "Daraxonrasib left tumours undetectable in 1 in 12 patients "
      "on trial",
      img_h=100, focus_y=0.45, head_size=30, sub_size=21)
story(RIGHT, 724, COL,
      "media-generation-panel-summit-0-c98a186a-5c9f-403c-8a0f-3f95146ffc25.webp",
      "POLITICS  ·  SHENZHEN SUMMIT",
      "TRUMP DEFENDS PUTIN & XI",
      "Calls Putin a friend after the trilateral; Zelensky answers: "
      "'He's a killer'",
      img_h=100, focus_y=0.40, head_size=30, sub_size=21)

# ---------------- ticker ----------------
pen.rectangle([0, 956, SIZE, SIZE], fill=NAVY)
pen.text((MARGIN, 974), "ALSO TODAY:", font=F(SANS_BOLD, 20), fill=GOLD)
ticker = ("COP31 talks run past deadline over fossil fuels  ·  "
          "Peru quake 6.8 shakes the Andes  ·  "
          "GTA VI earns $3.8B on day one  ·  "
          "BepiColombo orbits Mercury")
tx = MARGIN + 152
ty = 972
tick_size = fit_size(pen, ticker, SANS, SIZE - tx - MARGIN, 2, 19)
for line in wrap(pen, ticker, F(SANS, tick_size), SIZE - tx - MARGIN)[:2]:
    pen.text((tx, ty), line, font=F(SANS, tick_size), fill=WHITE)
    ty += 25

target = os.path.join(ROOT, "entry.png")
page.save(target, format="JPEG", quality=88)
print("wrote", target, os.path.getsize(target), "bytes", page.size)
