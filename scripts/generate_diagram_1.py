#!/usr/bin/env python3
"""
Generate Diagram 1 for Week 6:
"The Three Eras of Enterprise Blockchain: Evolution toward Private EVM"
Canvas: 1600x900px
Brand Palette: Noir Ventures Dark #18181C, Purple #B49AFF, Yellow #ECFB3E, Crisp White #FFFFFF
Typography: High legibility (Headers 24-32pt, Body 14-16pt), 40px card padding, zero overflow.
"""

import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
LOGO_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "Brand_Guide", "Rayls_Logo_Pack", "PNG", "Rayls_Logo_White.png"
)
OUTPUT_PATH = os.path.join(ASSETS_DIR, "diagram_1_enterprise_dlt_evolution.png")

def get_font(name, size):
    font_path = os.path.join("C:\\Windows\\Fonts", name)
    try:
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

def wrap_text(text, max_len):
    words = text.split()
    lines = []
    curr = ""
    for w in words:
        if len(curr + " " + w) <= max_len:
            curr = (curr + " " + w).strip()
        else:
            lines.append(curr)
            curr = w
    if curr:
        lines.append(curr)
    return lines

def main():
    width, height = 1600, 900
    img = Image.new("RGBA", (width, height), (24, 24, 28, 255))
    draw = ImageDraw.Draw(img)

    # 1. Header with Logo & Title
    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH).convert("RGBA")
        aspect = logo.width / logo.height
        logo_w, logo_h = int(38 * aspect), 38
        logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        img.paste(logo, (80, 50), logo)
    else:
        draw.text((80, 50), "Rayls", font=get_font("segoeuib.ttf", 30), fill=(255, 255, 255, 255))

    font_header_pill = get_font("segoeuib.ttf", 13)
    draw.rounded_rectangle([1050, 55, 1520, 88], radius=8, fill=(35, 35, 42, 255), outline=(65, 65, 75, 255), width=1)
    draw.text((1075, 64), "ARCHITECTURAL TOPOLOGY BENCHMARK // FIGURE 1", font=font_header_pill, fill=(180, 154, 255, 255))

    # Titles
    font_main_title = get_font("segoeuib.ttf", 32)
    font_sub_title = get_font("segoeui.ttf", 17)
    draw.text((80, 105), "The Evolution of Institutional DLT: Why Private EVM Wins", font=font_main_title, fill=(255, 255, 255, 255))
    draw.text((80, 148), "Comparing ten years of enterprise blockchain paradigms against real institutional requirements.", font=font_sub_title, fill=(160, 160, 170, 255))

    draw.line([80, 185, 1520, 185], fill=(45, 45, 55, 255), width=1)

    # 2. Three Cards Across Width
    card_w = 450
    card_gap = 45
    card_x_start = 80
    card_y = 215
    card_h = 620

    columns = [
        {
            "era": "ERA 1 (2015 - 2020)",
            "title": "Niche Enterprise DLTs",
            "subtitle": "Fabric, Corda, Quorum, Daml",
            "badge": "ISOLATED SILOS",
            "badge_color": (255, 105, 97, 255),  # Muted Red
            "sections": [
                ("Architecture", "Proprietary, non-EVM domain-specific languages (Go chaincode, Kotlin on Corda, Daml). Zero EVM composability."),
                ("Execution & State", "Custom transaction endorsement pipelines. High maintenance overhead requiring bespoke infrastructure."),
                ("Mempool & Privacy", "Private data collections within consortium, but completely walled off from secondary markets."),
                ("Fatal Limitation", "The 'Intranet of Value' trap: Zero interoperability with public DeFi liquidity. High developer acquisition cost.")
            ]
        },
        {
            "era": "ERA 2 (2020 - 2023)",
            "title": "Public EVM & Geth",
            "subtitle": "Ethereum, Standard Geth Private Forks",
            "badge": "METADATA LEAKAGE",
            "badge_color": (255, 180, 80, 255),  # Orange
            "sections": [
                ("Architecture", "Standard Solidity tooling, but built on Go-Ethereum (Geth) designed for decentralized P2P networks."),
                ("Execution & State", "Go runtime Garbage Collection (GC) triggers stop-the-world pauses (p99 latency spikes up to 73.2ms)."),
                ("Mempool & Privacy", "P2P gossiped mempools broadcast transactions to all peers 12-15s before mining, exposing order flow to MEV bots."),
                ("Fatal Limitation", "Violates statutory banking secrecy (Brazil LC 105/2001, GLBA, GDPR). Gas price volatility causes settlement stalls.")
            ]
        },
        {
            "era": "ERA 3 (2024 - PRESENT)",
            "title": "Rayls Sovereign Private EVM",
            "subtitle": "Paradigm Reth in Rust + MDBX",
            "badge": "INSTITUTIONAL APEX",
            "badge_color": (236, 251, 62, 255),  # Rayls Yellow
            "sections": [
                ("Architecture", "100% Solidity & Foundry compatibility. Standard ERC standards and audited contracts without niche DSLs."),
                ("Execution & State", "Reth in Rust with zero garbage collection. Deterministic sub-millisecond execution (p99 = 1.56ms, 0% SLA breaches)."),
                ("Mempool & Privacy", "Private Local Priority Queue: Direct authenticated TLS RPC ingress. Zero public P2P mempool gossip (0.0s exposure)."),
                ("Institutional Advantage", "Wholesale CBDC reserve anchoring (Drex model). Regulatory KYC/LEI gates & deterministic zero/fixed gas pricing.")
            ]
        }
    ]

    for idx, col in enumerate(columns):
        cx0 = card_x_start + idx * (card_w + card_gap)
        cx1 = cx0 + card_w
        cy0 = card_y
        cy1 = cy0 + card_h

        # Card body
        card_fill = (28, 28, 34, 255) if idx < 2 else (32, 30, 42, 255)  # Slightly highlighted for Rayls
        border_col = (50, 50, 60, 255) if idx < 2 else (180, 154, 255, 255)
        border_w = 1 if idx < 2 else 2
        
        draw.rounded_rectangle([cx0, cy0, cx1, cy1], radius=14, fill=card_fill, outline=border_col, width=border_w)

        # Era Tag
        font_era = get_font("segoeuib.ttf", 12)
        draw.text((cx0 + 25, cy0 + 25), col["era"], font=font_era, fill=(160, 160, 175, 255))

        # Status Badge
        badge_w = 140
        draw.rounded_rectangle([cx1 - badge_w - 20, cy0 + 20, cx1 - 20, cy0 + 44], radius=6, fill=(38, 38, 46, 255), outline=col["badge_color"], width=1)
        font_badge = get_font("segoeuib.ttf", 10)
        draw.text((cx1 - badge_w - 10, cy0 + 26), col["badge"], font=font_badge, fill=col["badge_color"])

        # Card Title & Subtitle
        font_ctitle = get_font("segoeuib.ttf", 22)
        font_csub = get_font("segoeui.ttf", 13)
        draw.text((cx0 + 25, cy0 + 52), col["title"], font=font_ctitle, fill=(255, 255, 255, 255))
        draw.text((cx0 + 25, cy0 + 82), col["subtitle"], font=font_csub, fill=(180, 154, 255, 255) if idx == 2 else (180, 180, 190, 255))

        # Horizontal divider inside card
        draw.line([cx0 + 25, cy0 + 108, cx1 - 25, cy0 + 108], fill=(50, 50, 60, 255), width=1)

        # 4 Sections inside card
        sec_y = cy0 + 124
        for s_title, s_desc in col["sections"]:
            font_stitle = get_font("segoeuib.ttf", 14)
            stitle_color = (236, 251, 62, 255) if idx == 2 and s_title == "Institutional Advantage" else (220, 220, 230, 255)
            draw.text((cx0 + 25, sec_y), s_title, font=font_stitle, fill=stitle_color)
            
            font_sdesc = get_font("segoeui.ttf", 13)
            lines = wrap_text(s_desc, 44)
            for l_idx, l in enumerate(lines[:3]):
                draw.text((cx0 + 25, sec_y + 22 + l_idx * 18), l, font=font_sdesc, fill=(150, 150, 160, 255))
            
            sec_y += 118

    # Save output
    os.makedirs(ASSETS_DIR, exist_ok=True)
    img.save(OUTPUT_PATH, "PNG")
    print(f"[OK] Diagram 1 generated at: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
