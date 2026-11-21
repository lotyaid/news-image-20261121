#!/usr/bin/env python3
"""Compose entry.png for news-image-20261121: the whole world of
Saturday 21 November 2026 on one dense front page.

Revision 2 (champion-pattern densification). The page now carries 42
stories from the day's One Turn edition (49 stories and 14 in brief,
drawn from 849 headlines): one illustrated lead, four illustrated
features, a consensus band of the five most widely reported stories
with their outlets named, a numbers strip of the day's hard figures,
and 32 one-line briefs in three ruled columns. Every fact below is
taken from that edition; nothing is invented to fill space.

The five illustrations live in assets/; every word is typeset here
with PIL so no text can come out garbled. The page is 1024x1024 and
is saved as JPEG bytes under the name entry.png (the gate tells PNG
from JPEG by first bytes), kept under 1 MiB. Same inputs, same bytes,
every run.
"""
import os

from PIL import Image, ImageDraw, ImageFont

from typeset import columns, double_rule, fit_size

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")
SIZE = 1024
MARGIN = 26
WIDTH = SIZE - 2 * MARGIN

PAPER = (243, 237, 226)
NAVY = (22, 36, 60)
INK = (28, 28, 32)
RED = (164, 36, 30)
GREY = (88, 88, 92)
GOLD = (238, 216, 152)
WHITE = (236, 236, 236)
RULE = (150, 142, 126)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def crop_to(img, w, h, focus_y=0.5):
    """Scale img to cover a w x h box, then crop, centred horizontally
    and at focus_y vertically (0 = top, 1 = bottom)."""
    img = img.convert("RGB")
    scale = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)),
                   Image.LANCZOS)
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

# ---------------- masthead ----------------
pen.text((SIZE // 2, 8), "T H E   W O R L D   T O D A Y",
         font=F(SERIF_BOLD, 37), fill=NAVY, anchor="ma")
pen.text((SIZE // 2, 52), "SATURDAY, 21 NOVEMBER 2026",
         font=F(SANS_BOLD, 21), fill=RED, anchor="ma")
pen.text((SIZE - MARGIN, 56), "42 STORIES · 849 HEADLINES READ",
         font=F(SANS_BOLD, 13), fill=GREY, anchor="ra")
pen.text((MARGIN, 56), "ONE PAGE · THE WHOLE DAY",
         font=F(SANS_BOLD, 13), fill=GREY, anchor="la")
double_rule(pen, MARGIN, SIZE - MARGIN, 80, NAVY)

# ---------------- numbers strip ----------------
NUMBERS = [
    ("400+", "DRONES FIRED"),
    ("110", "MISSILES"),
    ("-3.7%", "S&P 500"),
    ("-5.1%", "NIKKEI 225"),
    ("-4.6%", "GOLD"),
    ("$57,850", "BITCOIN"),
    ("$89.95", "BRENT CRUDE"),
    ("+2.3%", "SENSEX"),
]
pen.rectangle([0, 90, SIZE, 143], fill=NAVY)
pen.text((MARGIN, 96), "THE DAY IN NUMBERS", font=F(SANS_BOLD, 11),
         fill=GOLD)
cell = WIDTH // len(NUMBERS)
for i, (figure, label) in enumerate(NUMBERS):
    cx = MARGIN + i * cell + cell // 2
    pen.text((cx, 105), figure, font=F(SANS_BOLD, 21), fill=WHITE,
             anchor="ma")
    pen.text((cx, 130), label, font=F(SANS_BOLD, 9), fill=GOLD,
             anchor="ma")

# ---------------- lead story ----------------
LEAD_IMG = "media-generation-panel-ukraine-0-117789b3-eec4-48e3-9f7a-0839bdfab6a6.webp"
art = Image.open(os.path.join(ASSETS, LEAD_IMG))
page.paste(crop_to(art, WIDTH, 158, 0.45), (MARGIN, 148))
pen.rectangle([MARGIN, 148, MARGIN + WIDTH, 148 + 158], outline=NAVY,
              width=2)
ty = 314
pen.text((MARGIN + 2, ty), "WAR  ·  UKRAINE & POLAND  ·  REPORTED BY 12 OUTLETS",
         font=F(SANS_BOLD, 15), fill=RED)
ty += 21
lead_head = "RUSSIA FIRES 400 DRONES AND 110 MISSILES; MISSILES LAND IN POLAND"
lead_size = fit_size(pen, lead_head, SANS_BOLD, WIDTH - 4, 2, 30)
for line in wrap(pen, lead_head, F(SANS_BOLD, lead_size), WIDTH - 4):
    pen.text((MARGIN + 2, ty), line, font=F(SANS_BOLD, lead_size), fill=INK)
    ty += lead_size + 3
lead_sub = ("Eight killed in Kyiv as bridges, rail stations and power "
            "sites were hit; two missiles and a suspected drone came "
            "down in eastern Poland. NATO called it a grave violation "
            "of its airspace; Prime Minister Tusk: a deliberate "
            "provocation.")
for line in wrap(pen, lead_sub, F(SANS, 15), WIDTH - 4):
    pen.text((MARGIN + 2, ty), line, font=F(SANS, 15), fill=GREY)
    ty += 19
pen.text((MARGIN + 2, ty + 2),
         "Sources: BBC News · PBS NewsHour · France 24",
         font=F(SANS_BOLD, 12), fill=NAVY)
LEAD_END = ty + 18

# ---------------- four illustrated features ----------------
FEATURES = [
    ("media-generation-panel-markets-0-ac9d7ffb-058c-459c-afd1-061557ef1f5a.webp",
     0.40, "MARKETS  ·  AI SELL-OFF", "AI ROUT: S&P IN CORRECTION",
     "Chip shares plunged; the Nasdaq erased its 2026 gains; "
     "Anthropic fell 10% after its record debut"),
    ("media-generation-panel-court-0-76f5fbb2-2826-42cb-97c2-239c4abc0116.webp",
     0.35, "JUSTICE  ·  WORLD COURT", "GUILTY OF GENOCIDE",
     "Myanmar held responsible for the Rohingya genocide; "
     "reparations ordered — a first for the court"),
    ("media-generation-panel-pill-0-7376fe15-437c-4398-962a-db4693b8f612.webp",
     0.45, "HEALTH  ·  MEDICINE", "CANCER PILL STUNS TRIAL",
     "Daraxonrasib left pancreatic tumours undetectable in "
     "1 in 12 patients on trial"),
    ("media-generation-panel-summit-0-c98a186a-5c9f-403c-8a0f-3f95146ffc25.webp",
     0.40, "POLITICS  ·  SHENZHEN SUMMIT", "TRUMP DEFENDS PUTIN & XI",
     "Friendship defended after the trilateral; Zelensky "
     "answers: 'He's a killer'"),
]
FEAT_Y = LEAD_END + 10
pen.line([(MARGIN, FEAT_Y - 6), (SIZE - MARGIN, FEAT_Y - 6)],
         fill=RULE, width=1)
FCOLS = columns(SIZE, MARGIN, 14, 4)
feat_bottom = FEAT_Y
for (img_name, focus, kicker, head, sub), (fx, fw) in zip(FEATURES, FCOLS):
    art = Image.open(os.path.join(ASSETS, img_name))
    page.paste(crop_to(art, fw, 74, focus), (fx, FEAT_Y))
    pen.rectangle([fx, FEAT_Y, fx + fw, FEAT_Y + 74], outline=NAVY,
                  width=2)
    fy = FEAT_Y + 80
    pen.text((fx + 1, fy), kicker, font=F(SANS_BOLD, 11), fill=RED)
    fy += 15
    hs = fit_size(pen, head, SANS_BOLD, fw - 2, 2, 17)
    for line in wrap(pen, head, F(SANS_BOLD, hs), fw - 2):
        pen.text((fx + 1, fy), line, font=F(SANS_BOLD, hs), fill=INK)
        fy += hs + 2
    for line in wrap(pen, sub, F(SANS, 12), fw - 2):
        pen.text((fx + 1, fy), line, font=F(SANS, 12), fill=GREY)
        fy += 15
    feat_bottom = max(feat_bottom, fy)

# ---------------- consensus band ----------------
CONSENSUS = [
    ("Hormuz tanker attacks as US-Iran talks stall",
     "AL JAZEERA · STRAITS TIMES · THE HINDU"),
    ("Houthi missiles aim at Riyadh; coalition strikes Yemen",
     "AL JAZEERA · FRANCE 24"),
    ("UK and EU sign three post-Brexit agreements",
     "BRUSSELS SUMMIT"),
    ("COP31 runs past deadline over fossil fuels",
     "ANTALYA, TURKEY"),
    ("FBI criminal database reportedly hacked",
     "US MEDIA REPORTS"),
]
CONS_Y = feat_bottom + 8
pen.rectangle([MARGIN, CONS_Y, SIZE - MARGIN, CONS_Y + 62], fill=NAVY)
pen.text((MARGIN + 10, CONS_Y + 6),
         "CONSENSUS — THE STORIES EVERY OUTLET CARRIED",
         font=F(SANS_BOLD, 12), fill=GOLD)
CCOLS = columns(SIZE, MARGIN + 10, 10, 5)
for (head, src), (cx, cw) in zip(CONSENSUS, CCOLS):
    lines = wrap(pen, head, F(SANS_BOLD, 12), cw - 4)[:2]
    cy = CONS_Y + 23
    for line in lines:
        pen.text((cx, cy), line, font=F(SANS_BOLD, 12), fill=WHITE)
        cy += 14
    pen.text((cx, CONS_Y + 52), src, font=F(SANS_BOLD, 8), fill=GOLD)
CONS_END = CONS_Y + 62

# ---------------- briefs: 32 one-liners in three columns ----------------
BRIEFS = [
    ("WORLD", [
        ("LOS ANGELES", "Palisades fire starter convicted"),
        ("HAITI", "Salvadoran troops lose men to gangs"),
        ("GAZA", "Israeli fire kills Palestinians"),
        ("NIGERIA", "Funeral boat sinks: 30 dead, 300 lost"),
        ("BASRA", "Power-station fire kills four"),
        ("PERU · TIMOR", "Quakes of 6.7 and 6.8 shake both"),
        ("MADRID", "Spain heads to Nov 29 election"),
        ("NEW YORK", "19 years for Sikh-leader murder plot"),
        ("PARIS", "Police sentenced over racist beating"),
        ("COPENHAGEN", "Russian diplomat expelled"),
        ("NARVA", "Estonia to shut Russian border posts"),
    ]),
    ("SOCIETY, SCIENCE & SPACE", [
        ("EUROPE", "Living-cost protests in 25 countries"),
        ("TOKYO", "Japan sidelined as China ties hit low"),
        ("BRASÍLIA", "Bolsonaro hospitalised, gut blocked"),
        ("CAPE TOWN", "Mlambo-Ngcuka dies aged 71"),
        ("AMAZON", "Isolated Awá approach Brazil outpost"),
        ("KAMPALA", "Uganda curbs gatherings over Ebola"),
        ("WASHINGTON", "US loses measles-free status"),
        ("GENEVA", "CERN spots ultra-rare particle decay"),
        ("SAN FRANCISCO", "Claim of AI-assisted Riemann proof"),
        ("DEEP SPACE", "Voyager 1, 24 light-hours out"),
        ("MERCURY", "BepiColombo in orbit after 8 years"),
    ]),
    ("ECONOMY, CULTURE & SPORT", [
        ("BUENOS AIRES", "Argentina risk tops 1,000 pts"),
        ("TURKANA", "Kenya starts onshore oil drilling"),
        ("RIYADH", "Saudi-Japan oil stockpile deal"),
        ("JAPAN", "Pilotless air taxi carries passenger"),
        ("ANTARCTICA", "Lost ranges found under the ice"),
        ("LAS VEGAS", "Verstappen on pole for the GP"),
        ("CLEVELAND", "Harden passes Kobe 50-point mark"),
        ("OSAKA", "BTS wins five MAMA awards"),
        ("MUNICH", "Kane out months with ankle injury"),
        ("HOUSTON", "Texans rout Colts 26-3"),
    ]),
]
BRIEF_Y = CONS_END + 10
BCOLS = columns(SIZE, MARGIN, 18, 3)
for ci, ((section, items), (bx, bw)) in enumerate(zip(BRIEFS, BCOLS)):
    if ci:
        pen.line([(bx - 9, BRIEF_Y), (bx - 9, 966)], fill=RULE, width=1)
    pen.text((bx, BRIEF_Y), section, font=F(SANS_BOLD, 13), fill=NAVY)
    pen.line([(bx, BRIEF_Y + 19), (bx + bw, BRIEF_Y + 19)], fill=NAVY,
             width=2)
    by = BRIEF_Y + 27
    for place, head in items:
        prefix = place + " — "
        size = 12
        while size > 9 and pen.textlength(prefix + head,
                                          font=F(SANS_BOLD, size)) > bw:
            size -= 1
        fnt = F(SANS_BOLD, size)
        pen.text((bx, by), prefix, font=fnt, fill=RED)
        pen.text((bx + pen.textlength(prefix, font=fnt), by), head,
                 font=fnt, fill=INK)
        by += 19
BRIEF_END = by

# ---------------- footer ----------------
pen.rectangle([0, 976, SIZE, SIZE], fill=NAVY)
pen.text((MARGIN, 984),
         "SOURCE: ONE TURN DAILY EDITION — 49 STORIES & 14 IN BRIEF "
         "FROM 849 HEADLINES",
         font=F(SANS_BOLD, 12), fill=GOLD)
pen.text((MARGIN, 1004),
         "World Mood: UNEASY · The full edition, on a living globe: "
         "oneturn.news",
         font=F(SANS, 12), fill=WHITE)

target = os.path.join(ROOT, "entry.png")
page.save(target, format="JPEG", quality=92, subsampling=0)
print("wrote", target, os.path.getsize(target), "bytes", page.size,
      "| lead_end", LEAD_END, "cons_end", CONS_END, "brief_end",
      BRIEF_END)
