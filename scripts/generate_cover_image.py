#!/usr/bin/env python3
"""
Generate Cover Image for Week 6:
"What Is a Private EVM and Why Would a Financial Institution Need One?"
Canvas: 1600x900px
Safe Zone: Content ends by y=760px (140px bottom margin for Twitter mobile preview)
Palette: Noir Ventures Dark #18181C, Purple #B49AFF, Yellow #ECFB3E, Crisp White #FFFFFF
"""

import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
LOGO_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "Brand_Guide", "Rayls_Logo_Pack", "PNG", "Rayls_Logo_White.png"
)
OUTPUT_PATH = os.path.join(ASSETS_DIR, "cover_image_private_evm.png")

def get_font(name, size):
    font_path = os.path.join("C:\\Windows\\Fonts", name)
    try:
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

def main():
    width, height = 1600, 900
    # Clean Noir Ventures dark background #18181C
    img = Image.new("RGBA", (width, height), (24, 24, 28, 255))
    
    # Subtle purple glow layer using proper alpha composite
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    for r in range(500, 100, -25):
        alpha = int(4 * (1 - r / 500))
        glow_draw.ellipse([800 - r, 300 - int(r*0.6), 800 + r, 300 + int(r*0.6)], fill=(180, 154, 255, alpha))
    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)

    # 2. Header: Official Logo + Institutional Research Pill
    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH).convert("RGBA")
        # Resize logo maintaining aspect ratio (approx height 48px)
        aspect = logo.width / logo.height
        logo_w, logo_h = int(48 * aspect), 48
        logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        img.paste(logo, (90, 75), logo)
    else:
        font_logo = get_font("segoeuib.ttf", 36)
        draw.text((90, 75), "Rayls", font=font_logo, fill=(255, 255, 255, 255))

    # Research pill
    font_pill = get_font("segoeuib.ttf", 15)
    pill_text = "INSTITUTIONAL EVM ARCHITECTURE // EMPIRICAL BENCHMARK"
    draw.rounded_rectangle([900, 80, 1510, 120], radius=12, fill=(34, 34, 40, 255), outline=(60, 60, 72, 255), width=1)
    draw.text((930, 91), pill_text, font=font_pill, fill=(180, 154, 255, 255))

    # Divider line
    draw.line([90, 145, 1510, 145], fill=(45, 45, 55, 255), width=1)

    # 3. Main Title
    font_title = get_font("segoeuib.ttf", 46)
    title_line1 = "What Is a Private EVM and Why Would a"
    title_line2 = "Financial Institution Need One?"
    
    draw.text((90, 185), title_line1, font=font_title, fill=(255, 255, 255, 255))
    draw.text((90, 245), title_line2, font=font_title, fill=(236, 251, 62, 255))  # Rayls Yellow accent

    # 4. Subtitle
    font_sub = get_font("segoeui.ttf", 22)
    sub_text = "An empirical study of Paradigm's Reth in Rust, MDBX zero-copy storage, and private non-gossiped mempool queues."
    draw.text((90, 320), sub_text, font=font_sub, fill=(160, 160, 170, 255))

    # 5. Core Metric Cards (4 cards across width, ending well above y=760px)
    card_y = 390
    card_h = 240
    cards_data = [
        {
            "tag": "LIVE NODE RUNTIME",
            "val": "Reth 1.4.2",
            "sub": "Rust Native Core",
            "desc": "Verified live on Rayls Public Chain (72957). Zero garbage-collection latency spikes.",
            "color": (180, 154, 255, 255)
        },
        {
            "tag": "MEMPOOL EXPOSURE",
            "val": "0.00 sec",
            "sub": "Zero P2P Gossip",
            "desc": "Direct authenticated RPC ingress eliminates mempool front-running & protects bank secrecy.",
            "color": (236, 251, 62, 255)
        },
        {
            "tag": "TAIL LATENCY (p99)",
            "val": "1.56 ms",
            "sub": "0% SLA Breaches",
            "desc": "MDBX memory-mapped storage vs. Go Geth 73.2ms p99 spikes (>25ms DvP SLA threshold).",
            "color": (120, 220, 160, 255)
        },
        {
            "tag": "TOOLING ECOSYSTEM",
            "val": "100% EVM",
            "sub": "Solidity & Foundry",
            "desc": "Eliminates proprietary enterprise DSLs (Corda/Fabric). Uses standard battle-tested tooling.",
            "color": (255, 255, 255, 255)
        }
    ]

    card_w = 330
    gap = 33
    start_x = 90

    for i, c in enumerate(cards_data):
        x0 = start_x + i * (card_w + gap)
        x1 = x0 + card_w
        y0 = card_y
        y1 = y0 + card_h

        # Card background
        draw.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=(30, 30, 36, 255), outline=(50, 50, 60, 255), width=1)
        
        # Tag pill
        font_tag = get_font("segoeuib.ttf", 11)
        draw.text((x0 + 20, y0 + 22), c["tag"], font=font_tag, fill=c["color"])

        # Value
        font_val = get_font("segoeuib.ttf", 32)
        draw.text((x0 + 20, y0 + 48), c["val"], font=font_val, fill=(255, 255, 255, 255))

        # Subtitle
        font_subcard = get_font("segoeuib.ttf", 14)
        draw.text((x0 + 20, y0 + 92), c["sub"], font=font_subcard, fill=c["color"])

        # Divider inside card
        draw.line([x0 + 20, y0 + 120, x1 - 20, y0 + 120], fill=(45, 45, 55, 255), width=1)

        # Description text (wrapped)
        font_desc = get_font("segoeui.ttf", 13)
        words = c["desc"].split()
        lines = []
        curr = ""
        for w in words:
            if len(curr + " " + w) < 36:
                curr = (curr + " " + w).strip()
            else:
                lines.append(curr)
                curr = w
        if curr:
            lines.append(curr)

        for l_idx, line in enumerate(lines[:4]):
            draw.text((x0 + 20, y0 + 132 + l_idx * 19), line, font=font_desc, fill=(150, 150, 160, 255))

    # 6. Lower Summary Banner (Ends at y=740px, safe from Twitter crop at y=760px)
    banner_y = 660
    draw.rounded_rectangle([90, banner_y, 1510, banner_y + 75], radius=12, fill=(24, 24, 30, 255), outline=(60, 50, 85, 255), width=1)
    
    font_bar_bold = get_font("segoeuib.ttf", 16)
    font_bar_text = get_font("segoeui.ttf", 15)
    
    draw.text((115, banner_y + 26), "EMPIRICAL SCOPE:", font=font_bar_bold, fill=(236, 251, 62, 255))
    scope_str = "Verified on Rayls Public L1 (#13,779,415+) & Controlled N=1,000 Engine Trace Latency Benchmark. Foundry Suite 7/7 Passing."
    draw.text((280, banner_y + 27), scope_str, font=font_bar_text, fill=(210, 210, 220, 255))

    # Save output
    os.makedirs(ASSETS_DIR, exist_ok=True)
    img.save(OUTPUT_PATH, "PNG")
    print(f"[OK] Cover image generated at: {OUTPUT_PATH}")
    print(f"     Lowest element at y={banner_y + 75}px (Safe clearance: {900 - (banner_y + 75)}px)")

if __name__ == "__main__":
    main()
