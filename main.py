#!/usr/bin/env python3
"""The World Today — Saturday 21 November 2026.

Draws a newspaper front page summing up the day's world news with
PIL shapes and text only (no network, no external assets) and writes
it to $MAKEFUN_OUTPUT_DIR/entry.png, or /output/entry.png by default.
The output is deterministic: the same bytes every run.
"""

import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import draw_frontpage as fp

W, H = fp.W, fp.H
M = 24                      # page margin
CW = W - 2 * M              # content width: 976


def build_page():
    img = Image.new("RGB", (W, H), fp.PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ---------------------------------------------------
    title_f = fp.font(fp.SERIF_B, 58)
    title = "THE WORLD TODAY"
    tw = title_f.getlength(title)
    d.text(((W - tw) / 2, 14), title, font=title_f, fill=fp.INK)

    fp.double_rule(d, M, W - M, 84)
    date_f = fp.font(fp.SANS_B, 27)
    date = "SATURDAY 21 NOVEMBER 2026"
    dw = date_f.getlength(date)
    d.text(((W - dw) / 2, 98), date, font=date_f, fill=fp.RED)
    side_f = fp.font(fp.SANS, 14)
    d.text((M, 106), "WORLD EDITION", font=side_f, fill=fp.GREY)
    right = "ONE DAY  •  ONE PAGE"
    d.text((W - M - side_f.getlength(right), 106), right, font=side_f,
           fill=fp.GREY)
    fp.rule(d, M, W - M, 132, weight=2)

    # ---- lead kicker + headline -------------------------------------
    kick_f = fp.font(fp.SANS_B, 19)
    d.text((M, 144), "WAR IN UKRAINE  —  RUSSIA'S RETALIATION",
           font=kick_f, fill=fp.RED)
    head_f = fp.font(fp.SERIF_B, 44)
    d.text((M, 170), "MISSILES RAIN ON KYIV", font=head_f, fill=fp.INK)
    d.text((M, 218), "AND KRYVYI RIH", font=head_f, fill=fp.INK)

    # ---- lead illustration + lead text ------------------------------
    ix, iy, iw, ih = M, 276, 560, 204
    fp.draw_lead_illustration(img, ix, iy, iw, ih)
    tx, tw2 = 608, W - M - 608
    body_f = fp.font(fp.SERIF, 18)
    lead = ("A Russian strike on Kryvyi Rih killed two people and "
            "injured 42, including four children. Kyiv's bridges were "
            "hit, with at least nine dead. A missile crashed in "
            "Poland — Warsaw called it a provocation.")
    y = fp.draw_wrapped(d, tx, iy + 2, lead, body_f, tw2, fill=fp.INK,
                        leading=24)
    # casualty box
    box_y = 404
    d.rectangle([tx, box_y, W - M, box_y + 76], fill=fp.LIGHT,
                outline=fp.RED, width=2)
    stat_f = fp.font(fp.SANS_B, 16)
    d.text((tx + 12, box_y + 8), "KRYVYI RIH: 2 killed, 42 injured",
           font=stat_f, fill=fp.DARKRED)
    d.text((tx + 12, box_y + 31), "KYIV: at least 9 dead",
           font=stat_f, fill=fp.DARKRED)
    d.text((tx + 12, box_y + 54), "POLAND: missile crash",
           font=stat_f, fill=fp.DARKRED)

    # ---- divider -----------------------------------------------------
    fp.double_rule(d, M, W - M, 500)

    # ---- three secondary stories -------------------------------------
    cards = [
        ("DENMARK: PLOT TO KILL ON DANISH SOIL",
         "Copenhagen accuses Russian intelligence of plotting to kill "
         "an American Ukrainian in Denmark.",
         fp.draw_denmark),
        ("TRUMP FLOATS CHIEF OF STAFF FOR 2028",
         "\u201cDo you wanna run for president?\u201d — asked after the "
         "Shenzhen summit with Xi and Putin.",
         fp.draw_summit),
        ("19\u00bd YEARS FOR PANNUN MURDER PLOT",
         "A US court sentences Indian national Nikhil Gupta to 235 "
         "months in the murder-for-hire case.",
         fp.draw_courtroom),
    ]
    card_w = 312
    card_x = [M, M + 332, M + 664]
    card_y = 516
    illo_h = 104
    for (headline, body, draw_fn), cx in zip(cards, card_x):
        draw_fn(img, cx, card_y, card_w, illo_h)
        hy = card_y + illo_h + 10
        h_f = fp.font(fp.SERIF_B, 20)
        hy = fp.draw_wrapped(d, cx, hy, headline, h_f, card_w, fill=fp.INK,
                             leading=25)
        b_f = fp.font(fp.SANS, 15)
        fp.draw_wrapped(d, cx, hy + 6, body, b_f, card_w, fill=fp.INK,
                        leading=20)

    # ---- divider -----------------------------------------------------
    fp.rule(d, M, W - M, 756, weight=2)

    # ---- bottom row: three small stories ------------------------------
    small = [
        ("BOLSONARO IN HOSPITAL",
         "Brazil's former president Jair Bolsonaro hospitalised with "
         "abdominal pain.",
         fp.draw_hospital_icon),
        ("COP31: CRUNCH TIME, NO DEAL",
         "Climate talks enter their final stretch with no agreement "
         "in sight.",
         fp.draw_globe_icon),
        ("EUROPE'S PROTESTS JOIN FORCES",
         "Cost-of-living protesters join forces, with actions planned "
         "across Europe on 21\u201322 November.",
         fp.draw_crowd_icon),
    ]
    row_y = 772
    icon_s = 62
    for (headline, body, draw_fn), cx in zip(small, card_x):
        draw_fn(img, cx, row_y, icon_s)
        hx = cx + icon_s + 10
        hw = card_w - icon_s - 10
        h_f = fp.font(fp.SERIF_B, 19)
        hy = fp.draw_wrapped(d, hx, row_y, headline, h_f, hw, fill=fp.INK,
                             leading=23)
        b_f = fp.font(fp.SANS, 15)
        fp.draw_wrapped(d, cx, row_y + icon_s + 8, body, b_f, card_w,
                        fill=fp.INK, leading=20)

    # ---- briefs strip --------------------------------------------------
    by = 928
    d.rectangle([0, by, W, H], fill=fp.NAVY)
    brief_f = fp.font(fp.SANS, 15)
    brief_b = fp.font(fp.SANS_B, 15)
    d.text((M, by + 12), "IN BRIEF", font=brief_b, fill=(255, 196, 66))
    line1 = ("Bangladesh: fresh arson attacks amid political unrest.   "
             "Myanmar calls the ICJ genocide ruling unfair.")
    line2 = ("Malaysia plans to resettle 10,000 Rohingya in Turkey.   "
             "Researcher says Claude proved the Riemann Hypothesis.")
    d.text((M + 96, by + 12), line1, font=brief_f, fill=(240, 240, 235))
    d.text((M + 96, by + 38), line2, font=brief_f, fill=(240, 240, 235))
    d.text((M + 96, by + 64), "All stories as reported on 21 November 2026.",
           font=brief_f, fill=(170, 175, 190))

    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img = build_page()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG")
    print("wrote", path, img.size)


if __name__ == "__main__":
    main()
