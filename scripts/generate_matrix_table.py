#!/usr/bin/env python3
"""
Generate Diagram 3 for Week 6:
"The 4-Category Evidence Boundary Matrix: Complete Research & Invariant Mapping"
Canvas: 1920x1800px
Brand Palette: Noir Ventures Dark #18181C, Purple #B49AFF, Yellow #ECFB3E, Crisp White #FFFFFF
Typography: High legibility (Headers 24-34pt, Table text 14-16pt), crisp contrast.
Strictly maps all 20 empirical claims to their four verified categories.
"""

import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
LOGO_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "Brand_Guide", "Rayls_Logo_Pack", "PNG", "Rayls_Logo_White.png"
)
OUTPUT_PATH = os.path.join(ASSETS_DIR, "evidence_boundary_matrix_table.png")

def get_font(name, size):
    font_path = os.path.join("C:\\Windows\\Fonts", name)
    try:
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

def main():
    width, height = 1920, 1800
    img = Image.new("RGBA", (width, height), (24, 24, 28, 255))
    draw = ImageDraw.Draw(img)

    # 1. Header with Logo & Title
    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH).convert("RGBA")
        aspect = logo.width / logo.height
        logo_w, logo_h = int(42 * aspect), 42
        logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        img.paste(logo, (90, 45), logo)
    else:
        draw.text((90, 45), "Rayls", font=get_font("segoeuib.ttf", 32), fill=(255, 255, 255, 255))

    font_header_pill = get_font("segoeuib.ttf", 13)
    draw.rounded_rectangle([1320, 50, 1830, 85], radius=8, fill=(35, 35, 42, 255), outline=(65, 65, 75, 255), width=1)
    draw.text((1345, 59), "SCIENTIFIC RIGOR & EPISTEMIC BOUNDARIES", font=font_header_pill, fill=(180, 154, 255, 255))

    font_main_title = get_font("segoeuib.ttf", 34)
    font_sub_title = get_font("segoeui.ttf", 17)
    draw.text((90, 100), "The 4-Category Evidence Boundary Matrix", font=font_main_title, fill=(255, 255, 255, 255))
    draw.text((90, 145), "Explicitly separating live on-chain observations, local invariant tests, empirical simulations, and documented architecture.", font=font_sub_title, fill=(160, 160, 170, 255))

    draw.line([90, 180, 1830, 180], fill=(45, 45, 55, 255), width=1)

    # 2. Table Column Headers
    table_y = 205
    col_x = [90, 150, 560, 920, 1420, 1830]
    col_titles = ["#", "Tested Property / Invariant", "Epistemic Boundary Category", "Artifact / Test Method", "Observed Empirical Result"]

    # Table Header row
    draw.rounded_rectangle([col_x[0], table_y, col_x[-1], table_y + 45], radius=6, fill=(32, 32, 38, 255), outline=(55, 55, 65, 255), width=1)
    font_th = get_font("segoeuib.ttf", 15)
    for i, title in enumerate(col_titles):
        draw.text((col_x[i] + 12, table_y + 12), title, font=font_th, fill=(236, 251, 62, 255))

    # 3. Table Rows (20 rows grouped into 4 categories)
    rows_data = [
        # CATEGORY 1: Live On-Chain Checks
        ("1", "Client Version", "Category 1: Live On-Chain", "web3_clientVersion via JSON-RPC", "1.4.2 (b19896a12cfc1f1f775c33196c940f3345c00ede) [Rust Reth]", (120, 220, 160, 255)),
        ("2", "Canonical Head Block", "Category 1: Live On-Chain", "eth_blockNumber (Rayls L1: 72957)", "#13,817,772+ (Captured 2026-11-04)", (120, 220, 160, 255)),
        ("3", "Protocol Gas Ceiling", "Category 1: Live On-Chain", "eth_getBlockByNumber (500 blocks)", "500,000,000 gas limit (Protocol execution headroom)", (120, 220, 160, 255)),
        ("4", "Median Block Cadence", "Category 1: Live On-Chain", "Sampled 500 consecutive blocks", "1.30s median cadence (1.34s mean)", (120, 220, 160, 255)),
        ("5", "Base Gas Price", "Category 1: Live On-Chain", "eth_gasPrice RPC query", "48.00 gwei (48,000,000,000 wei)", (120, 220, 160, 255)),

        # CATEGORY 2: Local Invariant & Access Control Tests
        ("6", "Private State Settlement", "Category 2: Local Prototype Test", "test_ValidInstitutionalPrivateExecution", "PASS (259,546 gas, balance debit/credit atomic)", (180, 154, 255, 255)),
        ("7", "Unauthorized Caller Gate", "Category 2: Local Prototype Test", "test_RevertIf_UnauthorizedCaller", "REVERT: UnauthorizedInstitutionalCaller(address)", (180, 154, 255, 255)),
        ("8", "Monotonic Sequence Gate", "Category 2: Local Prototype Test", "test_RevertIf_SequenceTampered", "REVERT: InvalidExecutionSequence(expected, actual)", (180, 154, 255, 255)),
        ("9", "Nonce Replay Protection", "Category 2: Local Prototype Test", "test_RevertIf_NonceReplayed", "REVERT: InvalidExecutionSequence (Replay blocked)", (180, 154, 255, 255)),
        ("10", "Collateral Overspend Gate", "Category 2: Local Prototype Test", "test_RevertIf_CollateralInsufficient", "REVERT: InsufficientInstitutionalCollateral", (180, 154, 255, 255)),
        ("11", "Regulatory Suspension", "Category 2: Local Prototype Test", "test_RevertIf_InstitutionalLaneSuspended", "REVERT: InstitutionalLaneSuspended (Instant freeze)", (180, 154, 255, 255)),
        ("12", "Gas Determinism Invariant", "Category 2: Local Prototype Test", "test_DeterministicGasProfiling", "PASS (Steady-state variance <= 4 gas units across txs)", (180, 154, 255, 255)),

        # CATEGORY 3: Controlled Empirical Simulations
        ("13", "Public Mempool Exposure", "Category 3: Controlled Simulation", "Geth P2P gossiped mempool (N=1,000)", "13.42s mean pending exposure (100% node visibility)", (255, 180, 80, 255)),
        ("14", "Rayls Private Queue Exposure", "Category 3: Controlled Simulation", "Sovereign direct TLS RPC (N=1,000)", "0.00s exposure (0.0% visibility; zero P2P gossip)", (255, 180, 80, 255)),
        ("15", "Go Geth Tail Latency (p99)", "Category 3: Controlled Simulation", "Go runtime GC trace simulation (N=1k)", "p99 = 73.20ms (Stop-The-World mark-sweep pauses)", (255, 180, 80, 255)),
        ("16", "Rust Reth Tail Latency (p99)", "Category 3: Controlled Simulation", "Rust revm zero-GC trace (N=1,000)", "p99 = 1.56ms (Deterministic RAII memory safety)", (255, 180, 80, 255)),
        ("17", "Interbank DvP SLA Breaches", "Category 3: Controlled Simulation", "Evaluated against >25ms SLA target", "Geth: 2.7% SLA breach rate vs. Rayls Reth: 0.0%", (255, 180, 80, 255)),

        # CATEGORY 4: Architectural & Primary Specifications
        ("18", "MDBX State Storage Engine", "Category 4: Documented Spec", "Reth MDBX embedded architecture", "Memory-mapped B+ tree with zero-copy reads", (210, 210, 220, 255)),
        ("19", "Tooling Interoperability", "Category 4: Documented Spec", "Solidity & Foundry compatibility", "100% EVM bytecode compatibility; 0 niche DSLs", (210, 210, 220, 255)),
        ("20", "Wholesale CBDC Settlement", "Category 4: Primary Alignment", "Central Bank of Brazil (Drex pilot)", "1:1 Real Digital reserve backing on Private Subnets", (210, 210, 220, 255))
    ]

    row_y = table_y + 55
    row_h = 70

    font_cell_num = get_font("segoeuib.ttf", 14)
    font_cell_prop = get_font("segoeuib.ttf", 14)
    font_cell_cat = get_font("segoeui.ttf", 13)
    font_cell_art = get_font("segoeui.ttf", 13)
    font_cell_res = get_font("segoeuib.ttf", 13)

    for i, r in enumerate(rows_data):
        bg_col = (28, 28, 34, 255) if i % 2 == 0 else (24, 24, 28, 255)
        draw.rounded_rectangle([col_x[0], row_y, col_x[-1], row_y + row_h - 6], radius=4, fill=bg_col, outline=(40, 40, 48, 255), width=1)

        # Draw left indicator bar by category color
        draw.rectangle([col_x[0], row_y, col_x[0] + 5, row_y + row_h - 6], fill=r[5])

        draw.text((col_x[0] + 18, row_y + 24), r[0], font=font_cell_num, fill=(200, 200, 210, 255))
        draw.text((col_x[1] + 12, row_y + 24), r[1], font=font_cell_prop, fill=(255, 255, 255, 255))
        draw.text((col_x[2] + 12, row_y + 25), r[2], font=font_cell_cat, fill=r[5])
        draw.text((col_x[3] + 12, row_y + 25), r[3], font=font_cell_art, fill=(170, 170, 180, 255))
        draw.text((col_x[4] + 12, row_y + 24), r[4], font=font_cell_res, fill=r[5] if "REVERT" in r[4] or "PASS" in r[4] or "0.0%" in r[4] else (230, 230, 240, 255))

        row_y += row_h

    # 4. Bottom Category Legend (Safe from bottom cutoff)
    legend_y = row_y + 20
    draw.rounded_rectangle([col_x[0], legend_y, col_x[-1], legend_y + 55], radius=8, fill=(30, 30, 38, 255), outline=(55, 55, 70, 255), width=1)
    
    font_leg_bold = get_font("segoeuib.ttf", 13)
    font_leg = get_font("segoeui.ttf", 13)

    draw.text((120, legend_y + 18), "EPISTEMIC TAXONOMY:", font=font_leg_bold, fill=(255, 255, 255, 255))
    
    # Legend items
    draw.rectangle([320, legend_y + 22, 332, legend_y + 34], fill=(120, 220, 160, 255))
    draw.text((340, legend_y + 18), "Cat 1: Live On-Chain", font=font_leg, fill=(200, 200, 210, 255))

    draw.rectangle([540, legend_y + 22, 552, legend_y + 34], fill=(180, 154, 255, 255))
    draw.text((560, legend_y + 18), "Cat 2: Local Invariant Test", font=font_leg, fill=(200, 200, 210, 255))

    draw.rectangle([800, legend_y + 22, 812, legend_y + 34], fill=(255, 180, 80, 255))
    draw.text((820, legend_y + 18), "Cat 3: Empirical Simulation", font=font_leg, fill=(200, 200, 210, 255))

    draw.rectangle([1060, legend_y + 22, 1072, legend_y + 34], fill=(210, 210, 220, 255))
    draw.text((1080, legend_y + 18), "Cat 4: Documented Spec", font=font_leg, fill=(200, 200, 210, 255))

    # Save output
    os.makedirs(ASSETS_DIR, exist_ok=True)
    img.save(OUTPUT_PATH, "PNG")
    print(f"[OK] Diagram 3 (Evidence Matrix Table) generated at: {OUTPUT_PATH}")
    print(f"     Total canvas height: {height}px, Lowest element at y={legend_y + 55}px (Safe clearance: {height - (legend_y + 55)}px)")

if __name__ == "__main__":
    main()
