#!/usr/bin/env python3
"""
Generate Diagram 2 for Week 6:
"Execution Engine Architecture: Go-Geth vs. Rayls Sovereign (Rust Reth + MDBX)"
Canvas: 1600x900px
Brand Palette: Noir Ventures Dark #18181C, Purple #B49AFF, Yellow #ECFB3E, Crisp White #FFFFFF
Typography: High legibility (Headers 24-32pt, Body 14-15pt), 40px card padding, zero overflow.
"""

import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
LOGO_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "Brand_Guide", "Rayls_Logo_Pack", "PNG", "Rayls_Logo_White.png"
)
OUTPUT_PATH = os.path.join(ASSETS_DIR, "diagram_2_reth_mdbx_architecture.png")

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
    draw.rounded_rectangle([1170, 55, 1520, 88], radius=8, fill=(35, 35, 42, 255), outline=(65, 65, 75, 255), width=1)
    draw.text((1195, 64), "FIGURE 2: EXECUTION PIPELINE", font=font_header_pill, fill=(180, 154, 255, 255))

    # Titles
    font_main_title = get_font("segoeuib.ttf", 32)
    font_sub_title = get_font("segoeui.ttf", 17)
    draw.text((80, 105), "EVM Execution Pipeline: Standard Geth vs. Rayls Sovereign Reth", font=font_main_title, fill=(255, 255, 255, 255))
    draw.text((80, 148), "Comparing memory management, mempool ingress, and state storage engines under institutional workloads.", font=font_sub_title, fill=(160, 160, 170, 255))

    draw.line([80, 185, 1520, 185], fill=(45, 45, 55, 255), width=1)

    # 2. Two Large Comparison Containers
    cont_w = 690
    cont_gap = 60
    c_x1 = 80
    c_x2 = c_x1 + cont_w + cont_gap
    c_y = 215
    c_h = 635

    # Container 1: Go-Geth
    draw.rounded_rectangle([c_x1, c_y, c_x1 + cont_w, c_y + c_h], radius=16, fill=(28, 28, 34, 255), outline=(55, 55, 65, 255), width=1)
    
    # Header 1
    font_col_title = get_font("segoeuib.ttf", 22)
    font_col_sub = get_font("segoeui.ttf", 13)
    draw.text((c_x1 + 30, c_y + 25), "Standard Go-Ethereum (Geth) Model", font=font_col_title, fill=(255, 255, 255, 255))
    draw.text((c_x1 + 30, c_y + 55), "Traditional Public EVM Architecture (Decentralized Default)", font=font_col_sub, fill=(255, 180, 80, 255))
    
    draw.line([c_x1 + 30, c_y + 80, c_x1 + cont_w - 30, c_y + 80], fill=(45, 45, 55, 255), width=1)

    # Container 2: Rayls Sovereign Reth
    draw.rounded_rectangle([c_x2, c_y, c_x2 + cont_w, c_y + c_h], radius=16, fill=(32, 30, 44, 255), outline=(180, 154, 255, 255), width=2)
    
    # Header 2
    draw.text((c_x2 + 30, c_y + 25), "Rayls Sovereign (Reth + MDBX) Model", font=font_col_title, fill=(255, 255, 255, 255))
    draw.text((c_x2 + 30, c_y + 55), "Purpose-Built Institutional Private EVM Architecture", font=font_col_sub, fill=(236, 251, 62, 255))
    
    draw.line([c_x2 + 30, c_y + 80, c_x2 + cont_w - 30, c_y + 80], fill=(60, 50, 85, 255), width=1)

    # 4 Pipeline Stages per container
    stages_geth = [
        ("1. Transaction Ingress", "P2P Gossiped Mempool", "Broadcasts pending transactions to all network peers. Sits in mempool 12-15s, exposing trade size, calldata, and counterparties to MEV front-runners.", (255, 105, 97, 255)),
        ("2. Memory & Execution", "Go Runtime (Garbage Collected)", "Concurrent GC mark-sweep triggers non-deterministic Stop-The-World latency spikes (p99 = 73.2ms; 2.7% of txs breach the 25ms institutional SLA).", (255, 180, 80, 255)),
        ("3. State Storage Engine", "LevelDB / PebbleDB (LSM-Tree)", "Log-structured merge-tree write amplification. Periodic background compaction cycles cause I/O lock contention during high-velocity bursts.", (255, 180, 80, 255)),
        ("4. Economic Model", "EIP-1559 Dynamic Gas Bidding", "Gas prices fluctuate unpredictably with external network congestion (15 to 150+ gwei), threatening automated banking settlement pipelines.", (255, 105, 97, 255))
    ]

    stages_reth = [
        ("1. Transaction Ingress", "Private Local Priority Queue", "Authenticated TLS RPC direct to sovereign sequencer. Zero public P2P mempool gossip (0.0s exposure). Total protection of banking secrecy.", (236, 251, 62, 255)),
        ("2. Memory & Execution", "Rust Reth (revm Zero-GC)", "Deterministic compile-time memory management (RAII). Predictable sub-millisecond execution (p99 = 1.56ms; 0.0% SLA breaches across 1,000 txs).", (180, 154, 255, 255)),
        ("3. State Storage Engine", "Embedded MDBX (Memory-Mapped)", "B+ tree with memory-mapped zero-copy reads. ACID-compliant crash-proof transactional storage with zero compaction latency jitter.", (120, 220, 160, 255)),
        ("4. Economic Model", "Zero-Gas / Fixed Institutional Settlement", "Configurable zero-gas internal accounting or fixed token fee settlement (USDr / BRL1) via FeeAggregator, eliminating gas bidding.", (236, 251, 62, 255))
    ]

    stage_y_start = c_y + 100
    stage_gap = 126

    # Draw Geth stages
    for i, (num, tag, desc, col) in enumerate(stages_geth):
        sy = stage_y_start + i * stage_gap
        # Inner card
        draw.rounded_rectangle([c_x1 + 25, sy, c_x1 + cont_w - 25, sy + 112], radius=10, fill=(22, 22, 26, 255), outline=(45, 45, 55, 255), width=1)
        
        font_num = get_font("segoeuib.ttf", 13)
        font_tag = get_font("segoeuib.ttf", 15)
        font_desc = get_font("segoeui.ttf", 13)
        
        draw.text((c_x1 + 42, sy + 14), num, font=font_num, fill=(160, 160, 170, 255))
        draw.text((c_x1 + 210, sy + 14), tag, font=font_tag, fill=col)
        
        lines = wrap_text(desc, 68)
        for l_idx, l in enumerate(lines[:3]):
            draw.text((c_x1 + 42, sy + 40 + l_idx * 18), l, font=font_desc, fill=(145, 145, 155, 255))

    # Draw Reth stages
    for i, (num, tag, desc, col) in enumerate(stages_reth):
        sy = stage_y_start + i * stage_gap
        # Inner card
        draw.rounded_rectangle([c_x2 + 25, sy, c_x2 + cont_w - 25, sy + 112], radius=10, fill=(24, 22, 34, 255), outline=(70, 60, 95, 255), width=1)
        
        font_num = get_font("segoeuib.ttf", 13)
        font_tag = get_font("segoeuib.ttf", 15)
        font_desc = get_font("segoeui.ttf", 13)
        
        draw.text((c_x2 + 42, sy + 14), num, font=font_num, fill=(180, 154, 255, 255))
        draw.text((c_x2 + 210, sy + 14), tag, font=font_tag, fill=col)
        
        lines = wrap_text(desc, 68)
        for l_idx, l in enumerate(lines[:3]):
            draw.text((c_x2 + 42, sy + 40 + l_idx * 18), l, font=font_desc, fill=(165, 165, 180, 255))

    # Save output
    os.makedirs(ASSETS_DIR, exist_ok=True)
    img.save(OUTPUT_PATH, "PNG")
    print(f"[OK] Diagram 2 generated at: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
