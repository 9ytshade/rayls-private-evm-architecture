#!/usr/bin/env python3
"""
Generate Cover Image for Week 6:
"What Is a Private EVM and Why Would a Financial Institution Need One?"
Canvas: 1600x900px (16:9)
Theme: Light Signature Rayls Noir Ventures Gradient (#B49AFF to #ECFB3E)
Official Untouched Black Logo: Rayls_Logo_Black.png
Clean Institutional Typography: Zero '//' slop, crisp badges, and generous safe zones.
"""

import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
LOGO_BLACK_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "Brand_Guide", "Rayls_Logo_Pack", "PNG", "Rayls_Logo_Black.png"
)
OUTPUT_PATH = os.path.join(ASSETS_DIR, "cover_image_private_evm.png")

# Brand Color Palette
C_PURPLE = (180, 154, 255, 255)      # #B49AFF
C_YELLOW = (236, 251, 62, 255)       # #ECFB3E
C_GREEN = (140, 247, 139, 255)       # #8CF78B
C_BLACK = (17, 17, 20, 255)          # #111114 Deep Institutional Black
C_CHARCOAL = (35, 35, 42, 255)       # #23232A
C_CARD_BG = (24, 24, 28, 255)        # #18181C Dark Card BG
C_CARD_BORDER = (55, 55, 65, 255)    # #373741
C_TEXT_WHITE = (255, 255, 255, 255)
C_TEXT_MUTED = (165, 165, 175, 255)

def get_font(name, size):
    font_path = os.path.join("C:\\Windows\\Fonts", name)
    try:
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

def create_horizontal_gradient(width, height, color_left, color_right):
    """Draws a smooth horizontal gradient base."""
    base = Image.new("RGBA", (width, height), color_left)
    top = Image.new("RGBA", (width, height), color_right)
    mask = Image.new("L", (width, height))
    mask_data = []
    for y in range(height):
        for x in range(width):
            mask_data.append(int(255 * (x / width)))
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def main():
    w, h = 1600, 900
    # 1. Base Signature Gradient (Purple to Yellow)
    img = create_horizontal_gradient(w, h, C_PURPLE, C_YELLOW)
    draw = ImageDraw.Draw(img)

    # 2. Official Black Logo in Top Right
    if os.path.exists(LOGO_BLACK_PATH):
        logo = Image.open(LOGO_BLACK_PATH).convert("RGBA")
        aspect = logo.width / logo.height
        logo_h = 44
        logo_w = int(logo_h * aspect)
        logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        img.paste(logo, (w - logo_w - 80, 48), logo)

    # 3. Category Pill (Top Left, Clean, No '//')
    font_pill = get_font("segoeuib.ttf", 15)
    draw.rounded_rectangle([80, 46, 360, 88], radius=8, fill=C_BLACK)
    draw.text((105, 56), "INSTITUTIONAL RESEARCH", font=font_pill, fill=C_YELLOW)

    # 4. Main Titles in Deep Crisp Black
    font_title = get_font("segoeuib.ttf", 44)
    font_sub = get_font("segoeui.ttf", 20)

    draw.text((80, 106), "What Is a Private EVM and Why Would a", font=font_title, fill=C_BLACK)
    draw.text((80, 162), "Financial Institution Need One?", font=font_title, fill=C_BLACK)
    
    sub_text = "An empirical systems investigation into Paradigm's Reth in Rust, MDBX storage, and zero-exposure mempool queues."
    draw.text((80, 226), sub_text, font=font_sub, fill=C_CHARCOAL)

    # 5. Four High-Contrast Cards Floating Over the Gradient
    card_y = 275
    card_h = 240
    card_w = 335
    gap = 35
    start_x = 80

    cards_data = [
        {
            "tag": "PARADIGM'S RETH",
            "val": "Reth 1.4.2",
            "sub": "Rust Native Core",
            "desc": "Verified live on Rayls L1 (72957). Compile-time RAII eliminates Go GC latency spikes.",
            "color": C_PURPLE
        },
        {
            "tag": "MEMPOOL PRIVACY",
            "val": "0.00 sec",
            "sub": "Zero P2P Gossip",
            "desc": "Direct authenticated TLS RPC ingress protects order flow and enforces banking secrecy.",
            "color": C_YELLOW
        },
        {
            "tag": "TAIL LATENCY (p99)",
            "val": "1.56 ms",
            "sub": "0% SLA Breaches",
            "desc": "MDBX zero-copy storage vs. Geth 73.2ms p99 spikes (>25ms institutional SLA ceiling).",
            "color": C_GREEN
        },
        {
            "tag": "TOOLING INTEROP",
            "val": "100% EVM",
            "sub": "Solidity & Foundry",
            "desc": "Eliminates proprietary enterprise DSLs (Corda/Fabric). Uses battle-tested tooling.",
            "color": C_TEXT_WHITE
        }
    ]

    font_card_tag = get_font("segoeuib.ttf", 12)
    font_card_val = get_font("segoeuib.ttf", 32)
    font_card_sub = get_font("segoeuib.ttf", 14)
    font_card_desc = get_font("segoeui.ttf", 13)

    for i, c in enumerate(cards_data):
        x0 = start_x + i * (card_w + gap)
        x1 = x0 + card_w
        y0 = card_y
        y1 = y0 + card_h

        # Card container
        draw.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=C_CARD_BG, outline=C_CARD_BORDER, width=2)

        # Tag
        draw.text((x0 + 22, y0 + 20), c["tag"], font=font_card_tag, fill=c["color"])

        # Value
        draw.text((x0 + 22, y0 + 46), c["val"], font=font_card_val, fill=C_TEXT_WHITE)

        # Subtitle
        draw.text((x0 + 22, y0 + 90), c["sub"], font=font_card_sub, fill=c["color"])

        # Inner divider line
        draw.line([x0 + 22, y0 + 116, x1 - 22, y0 + 116], fill=(45, 45, 55, 255), width=1)

        # Description text wrapped
        words = c["desc"].split()
        lines = []
        curr = ""
        for w_word in words:
            if len(curr + " " + w_word) < 35:
                curr = (curr + " " + w_word).strip()
            else:
                lines.append(curr)
                curr = w_word
        if curr:
            lines.append(curr)

        for l_idx, line in enumerate(lines[:4]):
            draw.text((x0 + 22, y0 + 128 + l_idx * 19), line, font=font_card_desc, fill=C_TEXT_MUTED)

    # 6. Inverted Horizontal Gradient Band (Yellow to Purple)
    band_y = 540
    band_h = 95
    band = create_horizontal_gradient(w - 160, band_h, C_YELLOW, C_PURPLE)
    img.paste(band, (80, band_y))

    # Inner border for band
    draw.rounded_rectangle([80, band_y, w - 80, band_y + band_h], radius=10, fill=None, outline=C_BLACK, width=2)

    font_band_title = get_font("segoeuib.ttf", 18)
    font_band_sub = get_font("segoeui.ttf", 15)

    draw.text((110, band_y + 22), "EMPIRICAL SCOPE: RAYLS PUBLIC L1 (#13,817,772+) • CONTROLLED N=1,000 ENGINE TRACE", font=font_band_title, fill=C_BLACK)
    draw.text((110, band_y + 54), "7/7 Passing Foundry Invariant & Unit Tests • Mathematical Steady-State Gas Determinism (±4 Gas Units)", font=font_band_sub, fill=C_BLACK)

    # 7. Bottom Footnote & Attribution (Ends well above y=760px safe margin)
    font_foot = get_font("segoeui.ttf", 14)
    font_foot_bold = get_font("segoeuib.ttf", 14)

    draw.text((80, 660), "The Rail Research Labs", font=font_foot_bold, fill=C_BLACK)
    draw.text((255, 660), "• Axyl BFT Consensus (1.30s Cadence) • 500M Block Gas Ceiling • CPMI-IOSCO Principle 8 Alignment", font=font_foot, fill=C_BLACK)
    draw.text((80, 688), "Zero Assumptions Standard • Source Code & Verifiable Datasets: github.com/9ytshade/rayls-private-evm-architecture", font=font_foot, fill=C_BLACK)

    # Save output
    os.makedirs(ASSETS_DIR, exist_ok=True)
    img.save(OUTPUT_PATH, "PNG")
    print(f"[OK] Cover image generated at: {OUTPUT_PATH}")
    print(f"     Lowest element at y=710px (Safe clearance: {900 - 710}px)")

if __name__ == "__main__":
    main()
