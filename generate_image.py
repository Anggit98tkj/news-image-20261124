#!/usr/bin/env python3
"""Draw the 24 November 2026 front page: 1024x1024, original art drawn in code.

Six verified stories from the Tuesday 24 November 2026 news cycle:
 1. Airstrike kills at least three Palestinians near Khan Younis, Gaza (Reuters)
 2. Asian shares rally on Tuesday as Huang's Nvidia return revives AI trade (Reuters)
 3. Japan factory activity expands, manufacturing PMI 53.7 (Reuters)
 4. Iran claims its missiles can now reach Europe, range 4,500 km (Iran International)
 5. Chinese official sentenced to death for leaking state secrets (Reuters)
 6. Alleged drug lord El Chapo Isidro to be tried in Mexico (Reuters)

Deterministic: fixed strings, fixed geometry, no time, no randomness, no network.
Two runs from any working directory write byte-identical output next to this script.
"""
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 34
PAPER = (250, 246, 236)
CARD_BG = (255, 252, 244)
INK = (24, 24, 28)
CRIMSON = (172, 32, 32)
NAVY = (30, 66, 122)
TEAL = (14, 96, 90)
OCHRE = (172, 118, 20)
GREY = (96, 93, 86)
FAINT = (214, 206, 188)
BODY = (56, 53, 48)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


@lru_cache(maxsize=None)
def font(path, size):
    """Load each font file once; the old code re-read it for every string.
    Falls back to Pillow's built-in bitmap font if DejaVu is missing,
    so the generator still runs (with plainer type) on a bare machine."""
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default(size=size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; a single over-long word is hard-broken, never dropped."""
    lines, cur = [], ""
    for word in text.split():
        while d.textlength(word, font=fnt) > max_w:
            cut = 1
            while cut < len(word) and d.textlength(word[:cut + 1], font=fnt) <= max_w:
                cut += 1
            lines.append(word[:cut])
            word = word[cut:]
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, x, y, lines, fnt, fill, leading=1.25):
    """Draw wrapped lines top to bottom; returns the y below the last line."""
    step = int(fnt.size * leading)
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def right_text(d, text, fnt, right_x, y, fill):
    """Right-align a single line against right_x."""
    d.text((right_x - d.textlength(text, font=fnt), y), text, font=fnt, fill=fill)


# ---------- pictograms, every line drawn in code ----------
def icon_pin(d, cx, cy, s, col):
    d.ellipse([cx - 34 * s, cy - 44 * s, cx + 34 * s, cy + 24 * s], fill=col)
    d.polygon([(cx - 24 * s, cy + 8 * s), (cx + 24 * s, cy + 8 * s),
               (cx, cy + 52 * s)], fill=col)
    d.ellipse([cx - 13 * s, cy - 23 * s, cx + 13 * s, cy + 3 * s], fill=PAPER)


def icon_chart(d, cx, cy, s, col):
    d.line([cx - 48 * s, cy + 40 * s, cx + 52 * s, cy + 40 * s], fill=col, width=4)
    d.line([cx - 48 * s, cy + 40 * s, cx - 48 * s, cy - 44 * s], fill=col, width=4)
    for i, h in enumerate([18, 32, 48]):
        x0 = cx - 34 * s + i * 30 * s
        d.rectangle([x0, cy + 34 * s - h * s, x0 + 18 * s, cy + 34 * s], fill=col)
    d.line([cx - 40 * s, cy + 8 * s, cx - 12 * s, cy - 14 * s, cx + 8 * s, cy - 2 * s,
            cx + 44 * s, cy - 38 * s], fill=CRIMSON, width=5)
    d.polygon([(cx + 44 * s, cy - 38 * s), (cx + 30 * s, cy - 38 * s),
               (cx + 44 * s, cy - 24 * s)], fill=CRIMSON)


def icon_factory(d, cx, cy, s, col):
    d.rectangle([cx - 50 * s, cy - 6 * s, cx + 50 * s, cy + 40 * s], fill=col)
    d.polygon([(cx - 50 * s, cy - 6 * s), (cx - 25 * s, cy - 28 * s),
               (cx, cy - 6 * s), (cx + 25 * s, cy - 28 * s),
               (cx + 50 * s, cy - 6 * s)], fill=col)
    d.rectangle([cx - 40 * s, cy - 40 * s, cx - 28 * s, cy - 6 * s], fill=col)
    d.rectangle([cx - 12 * s, cy - 48 * s, cx, cy - 6 * s], fill=col)
    for i in range(4):
        d.rectangle([cx - 40 * s + i * 24 * s, cy + 12 * s,
                     cx - 26 * s + i * 24 * s, cy + 28 * s], fill=PAPER)


def icon_rocket(d, cx, cy, s, col):
    d.polygon([(cx, cy - 52 * s), (cx + 18 * s, cy - 12 * s), (cx + 18 * s, cy + 16 * s),
               (cx, cy + 28 * s), (cx - 18 * s, cy + 16 * s),
               (cx - 18 * s, cy - 12 * s)], fill=col)
    d.ellipse([cx - 8 * s, cy - 30 * s, cx + 8 * s, cy - 14 * s], fill=PAPER)
    d.polygon([(cx - 18 * s, cy + 8 * s), (cx - 34 * s, cy + 30 * s),
               (cx - 18 * s, cy + 24 * s)], fill=col)
    d.polygon([(cx + 18 * s, cy + 8 * s), (cx + 34 * s, cy + 30 * s),
               (cx + 18 * s, cy + 24 * s)], fill=col)
    d.polygon([(cx - 9 * s, cy + 28 * s), (cx + 9 * s, cy + 28 * s),
               (cx, cy + 52 * s)], fill=OCHRE)


def icon_scales(d, cx, cy, s, col):
    d.line([cx, cy - 44 * s, cx, cy + 40 * s], fill=col, width=5)
    d.line([cx - 44 * s, cy - 34 * s, cx + 44 * s, cy - 34 * s], fill=col, width=5)
    d.ellipse([cx - 5 * s, cy - 52 * s, cx + 5 * s, cy - 42 * s], fill=col)
    for sgn in (-1, 1):
        d.line([cx + sgn * 44 * s, cy - 34 * s, cx + sgn * 28 * s, cy - 2 * s],
               fill=col, width=3)
        d.line([cx + sgn * 44 * s, cy - 34 * s, cx + sgn * 60 * s, cy - 2 * s],
               fill=col, width=3)
        d.pieslice([cx + sgn * 44 * s - 20 * s, cy - 6 * s,
                    cx + sgn * 44 * s + 20 * s, cy + 22 * s], 0, 180, fill=col)
    d.line([cx - 26 * s, cy + 40 * s, cx + 26 * s, cy + 40 * s], fill=col, width=5)


def icon_court(d, cx, cy, s, col):
    d.polygon([(cx - 52 * s, cy - 18 * s), (cx, cy - 52 * s),
               (cx + 52 * s, cy - 18 * s)], fill=col)
    d.ellipse([cx - 10 * s, cy - 44 * s, cx + 10 * s, cy - 24 * s], fill=PAPER)
    for i in range(-1, 2):
        d.rectangle([cx + i * 30 * s - 6 * s, cy - 12 * s,
                     cx + i * 30 * s + 6 * s, cy + 28 * s], fill=col)
    d.rectangle([cx - 52 * s, cy + 28 * s, cx + 52 * s, cy + 38 * s], fill=col)
    d.rectangle([cx - 56 * s, cy + 42 * s, cx + 56 * s, cy + 50 * s], fill=col)


ICONS = {"pin": icon_pin, "chart": icon_chart, "factory": icon_factory,
         "rocket": icon_rocket, "scales": icon_scales, "court": icon_court}


@dataclass(frozen=True)
class Story:
    kicker: str
    headline: str
    sub: str
    icon: str
    color: tuple


LEAD = Story(
    "GAZA  |  MIDDLE EAST",
    "AIRSTRIKE KILLS AT LEAST THREE IN GAZA",
    "Five more were wounded near a police post in Khan Younis, medics say.",
    "pin", CRIMSON,
)

STORIES = [
    Story("MARKETS  |  ASIA", "ASIA RALLIES AS HUANG RETURN REVIVES AI TRADE",
          "Nikkei up 4.5%, Kospi up 7.5% and Taiwan up 9.1% after Nvidia jumped 31% on Monday.",
          "chart", NAVY),
    Story("ECONOMY  |  JAPAN", "JAPAN FACTORIES PICK UP SPEED",
          "Manufacturing PMI rises to 53.7 in November, up from 53.3, on chip and electronics demand.",
          "factory", TEAL),
    Story("SECURITY  |  IRAN", "IRAN CLAIMS MISSILES CAN NOW REACH EUROPE",
          "A lawmaker says the range grew to 4,500 km, up from 2,000 km. The claim is unverified.",
          "rocket", CRIMSON),
    Story("CHINA", "CHINA OFFICIAL SENTENCED TO DEATH FOR SPYING",
          "Official known only as Ma accused of passing 35 state secrets to a foreign agency.",
          "scales", NAVY),
]

LAST = Story(
    "MEXICO  |  CRIME",
    "EL CHAPO ISIDRO TO FACE TRIAL IN MEXICO",
    "Attorney general says Mexico will try him at home, not extradite him.",
    "court", TEAL,
)


def panel(d, x, y, w, h, color, fill=CARD_BG):
    """Card frame: faint outline, bright paper fill, coloured top rule."""
    d.rectangle([x, y, x + w, y + h], fill=fill, outline=FAINT, width=2)
    d.rectangle([x, y, x + w, y + 6], fill=color)


def headline_block(d, x, y, max_w, story, head_size, sub_size, gap=8):
    """Wrapped headline then wrapped subtext; returns y below the subtext."""
    head_font = font(SERIF_B, head_size)
    sub_font = font(SANS, sub_size)
    y = draw_lines(d, x, y, wrap(d, story.headline, head_font, max_w),
                   head_font, INK, 1.15)
    return draw_lines(d, x, y + gap, wrap(d, story.sub, sub_font, max_w),
                      sub_font, BODY, 1.3)


def card(d, x, y, w, h, story):
    panel(d, x, y, w, h, story.color)
    d.text((x + 16, y + 18), story.kicker, font=font(SANS_B, 17), fill=story.color)
    ICONS[story.icon](d, x + w - 58, y + 56, 0.58, story.color)
    headline_block(d, x + 16, y + 46, w - 148, story, 25, 18)


def draw_masthead(d):
    m = MARGIN
    d.text((m, 22), "THE WORLD TODAY", font=font(SERIF_B, 60), fill=INK)
    right_text(d, "No. 24", font(SANS_B, 20), W - m, 40, GREY)
    d.rectangle([m, 100, W - m, 104], fill=CRIMSON)
    d.text((m, 114), "TUESDAY, 24 NOVEMBER 2026", font=font(SANS_B, 30), fill=CRIMSON)
    right_text(d, "SIX STORIES IN ONE IMAGE", font(SANS_B, 18), W - m, 122, GREY)
    d.rectangle([m, 156, W - m, 160], fill=INK)


def draw_lead(d):
    m = MARGIN
    x, y, w, h = m, 172, W - 2 * m, 196
    panel(d, x, y, w, h, LEAD.color)
    d.text((x + 18, y + 20), LEAD.kicker, font=font(SANS_B, 20), fill=LEAD.color)
    ICONS[LEAD.icon](d, x + w - 78, y + 92, 0.85, LEAD.color)
    headline_block(d, x + 18, y + 52, w - 220, LEAD, 38, 20, gap=12)


def draw_grid(d):
    m = MARGIN
    gx, gy = m, 382
    cw = (W - 2 * m - 20) // 2
    ch = 196
    for i, story in enumerate(STORIES):
        x = gx + (i % 2) * (cw + 20)
        y = gy + (i // 2) * (ch + 14)
        card(d, x, y, cw, ch, story)


def draw_bottom_strip(d):
    m = MARGIN
    x, y, w, h = m, 800, W - 2 * m, 150
    panel(d, x, y, w, h, LAST.color)
    ICONS[LAST.icon](d, x + 78, y + 76, 0.72, LAST.color)
    d.text((x + 150, y + 18), LAST.kicker, font=font(SANS_B, 18), fill=LAST.color)
    headline_block(d, x + 150, y + 46, w - 190, LAST, 28, 19)


def draw_footer(d):
    m = MARGIN
    fy = 962
    d.rectangle([m, fy, W - m, fy + 2], fill=INK)
    d.text((m, fy + 10), "Sources: Reuters, Iran International",
           font=font(SANS, 17), fill=GREY)
    d.text((m, fy + 34), "Headlines drawn from reports in the Tuesday 24 November 2026 news cycle.",
           font=font(SANS, 17), fill=GREY)
    # Date stamp, bottom right: the one visible change in this revision.
    stamp = "24 NOV 2026"
    stamp_font = font(SANS_B, 18)
    tw = d.textlength(stamp, font=stamp_font)
    sx, sy = W - m - tw - 24, fy + 8
    d.rectangle([sx, sy, sx + tw + 24, sy + 30], outline=CRIMSON, width=2)
    d.text((sx + 12, sy + 5), stamp, font=stamp_font, fill=CRIMSON)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_lead(d)
    draw_grid(d)
    draw_bottom_strip(d)
    draw_footer(d)

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, optimize=True)
    print("saved", out, img.size)


if __name__ == "__main__":
    main()
