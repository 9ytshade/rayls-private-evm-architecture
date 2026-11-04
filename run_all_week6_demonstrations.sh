#!/usr/bin/env bash
# ==============================================================================
# Master Demonstration Runner: Week 6 Private EVM Architecture Investigation
# ==============================================================================
set -e
export PATH="$HOME/.foundry/bin:$PATH"

echo "======================================================================"
echo " [1/3] Querying Live Rayls Public L1 (Chain ID 72957, Reth 1.4.2)..."
echo "======================================================================"
python3 -u scripts/rayls_node_telemetry_audit.py

echo ""
echo "======================================================================"
echo " [2/3] Running Controlled Private EVM Engine Benchmark (N=1,000)..."
echo "======================================================================"
python3 -u scripts/private_evm_engine_benchmark.py

echo ""
echo "======================================================================"
echo " [3/3] Running Foundry Invariant & Identity Gate Test Suite..."
echo "======================================================================"
forge test -vvv

echo ""
echo "======================================================================"
echo " [✓] All Demonstrations Completed Successfully!"
echo " Results stored in data/ directory."
echo "======================================================================"
