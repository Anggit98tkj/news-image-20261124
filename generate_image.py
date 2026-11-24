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
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (250, 246, 236)
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


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, max_w, lines, fnt, fill, leading=1.25):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


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

LEAD = ("GAZA  |  MIDDLE EAST", "AIRSTRIKE KILLS AT LEAST THREE IN GAZA",
        "Five more were wounded near a police post in Khan Younis, medics say.",
        "pin", CRIMSON)

STORIES = [
    ("MARKETS  |  ASIA", "ASIA RALLIES AS HUANG RETURN REVIVES AI TRADE",
     "Nikkei up 4.5%, Kospi up 7.5% and Taiwan up 9.1% after Nvidia jumped 31% on Monday.",
     "chart", NAVY),
    ("ECONOMY  |  JAPAN", "JAPAN FACTORIES PICK UP SPEED",
     "Manufacturing PMI rises to 53.7 in November, up from 53.3, on chip and electronics demand.",
     "factory", TEAL),
    ("SECURITY  |  IRAN", "IRAN CLAIMS MISSILES CAN NOW REACH EUROPE",
     "A lawmaker says the range grew to 4,500 km, up from 2,000 km. The claim is unverified.",
     "rocket", CRIMSON),
    ("CHINA", "CHINA OFFICIAL SENTENCED TO DEATH FOR SPYING",
     "Official known only as Ma accused of passing 35 state secrets to a foreign agency.",
     "scales", NAVY),
]

LAST = ("MEXICO  |  CRIME", "EL CHAPO ISIDRO TO FACE TRIAL IN MEXICO",
        "Attorney general says Mexico will try him at home, not extradite him.",
        "court", TEAL)


def card(d, x, y, w, h, kicker, head, sub, icon, color, head_size=25):
    d.rectangle([x, y, x + w, y + h], outline=FAINT, width=2)
    d.rectangle([x, y, x + w, y + 6], fill=color)
    d.text((x + 16, y + 18), kicker, font=font(SANS_B, 17), fill=color)
    ICONS[icon](d, x + w - 58, y + 56, 0.58, color)
    hl = wrap(d, head, font(SERIF_B, head_size), w - 148)
    yy = block(d, x + 16, y + 46, w - 148, hl, font(SERIF_B, head_size), INK, 1.18)
    sl = wrap(d, sub, font(SANS, 18), w - 32)
    block(d, x + 16, yy + 8, w - 32, sl, font(SANS, 18), BODY, 1.3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 34
    # ---- masthead ----
    d.text((m, 22), "THE WORLD TODAY", font=font(SERIF_B, 60), fill=INK)
    d.text((W - m - d.textlength("No. 24", font=font(SANS_B, 20)), 40),
           "No. 24", font=font(SANS_B, 20), fill=GREY)
    d.rectangle([m, 100, W - m, 104], fill=CRIMSON)
    d.text((m, 114), "TUESDAY, 24 NOVEMBER 2026", font=font(SANS_B, 30), fill=CRIMSON)
    tag = "SIX STORIES IN ONE IMAGE"
    d.text((W - m - d.textlength(tag, font=font(SANS_B, 18)), 122),
           tag, font=font(SANS_B, 18), fill=GREY)
    d.rectangle([m, 156, W - m, 160], fill=INK)

    # ---- lead story, full width ----
    lx, ly, lw, lh = m, 172, W - 2 * m, 196
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=(255, 252, 244),
                outline=FAINT, width=2)
    d.rectangle([lx, ly, lx + lw, ly + 6], fill=LEAD[4])
    d.text((lx + 18, ly + 20), LEAD[0], font=font(SANS_B, 20), fill=LEAD[4])
    ICONS[LEAD[3]](d, lx + lw - 78, ly + 92, 0.85, LEAD[4])
    hl = wrap(d, LEAD[1], font(SERIF_B, 38), lw - 220)
    yy = block(d, lx + 18, ly + 52, lw - 220, hl, font(SERIF_B, 38), INK, 1.15)
    sl = wrap(d, LEAD[2], font(SANS, 20), lw - 220)
    block(d, lx + 18, yy + 12, lw - 220, sl, font(SANS, 20), BODY, 1.3)

    # ---- middle grid: 2 columns x 2 rows ----
    gx, gy = m, 382
    cw = (W - 2 * m - 20) // 2
    ch = 196
    for i, (kicker, head, sub, icon, color) in enumerate(STORIES):
        x = gx + (i % 2) * (cw + 20)
        y = gy + (i // 2) * (ch + 14)
        card(d, x, y, cw, ch, kicker, head, sub, icon, color)

    # ---- bottom strip: sixth story, horizontal ----
    bx, by, bw, bh = m, 800, W - 2 * m, 150
    d.rectangle([bx, by, bx + bw, by + bh], fill=(255, 252, 244),
                outline=FAINT, width=2)
    d.rectangle([bx, by, bx + bw, by + 6], fill=LAST[4])
    d.text((bx + 150, by + 18), LAST[0], font=font(SANS_B, 18), fill=LAST[4])
    ICONS[LAST[3]](d, bx + 78, by + 76, 0.72, LAST[4])
    hl = wrap(d, LAST[1], font(SERIF_B, 28), bw - 190)
    yy = block(d, bx + 150, by + 46, bw - 190, hl, font(SERIF_B, 28), INK, 1.15)
    sl = wrap(d, LAST[2], font(SANS, 19), bw - 190)
    block(d, bx + 150, yy + 8, bw - 190, sl, font(SANS, 19), BODY, 1.3)

    # ---- footer ----
    fy = 962
    d.rectangle([m, fy, W - m, fy + 2], fill=INK)
    d.text((m, fy + 10), "Sources: Reuters, Iran International",
           font=font(SANS, 17), fill=GREY)
    d.text((m, fy + 34), "Headlines drawn from reports in the Tuesday 24 November 2026 news cycle.",
           font=font(SANS, 17), fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
