# What Is a Private EVM and Why Would a Financial Institution Need One?

[![Foundry Tests](https://img.shields.io/badge/Foundry-7%20Passed-brightgreen)](test/PrivateEVMInstitutionalGate.t.sol)
[![Solidity](https://img.shields.io/badge/Solidity-0.8.24-blue)](contracts/PrivateEVMInstitutionalGate.sol)
[![Rayls Chain ID](https://img.shields.io/badge/Rayls%20L1-72957%20(0x11cfd)-yellow)](https://mainnet-rpc.rayls.com)
[![Reth Version](https://img.shields.io/badge/Reth%20Node-1.4.2%20(b19896a1)-purple)](data/rayls_reth_node_telemetry.json)
[![CI Status](https://img.shields.io/badge/CI-Passing-brightgreen)](.github/workflows/verify.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An institutional research deep dive and empirical verification test suite deconstructing why regulated financial institutions require **Private EVMs**—specifically analyzing **Rayls Sovereign Subnets** powered by **Paradigm's Reth in Rust**, embedded **MDBX** state storage, and **private local transaction priority queues**.

---

## 🏛️ Executive Architecture Overview

```
+---------------------------------------------------------------------------------------------------------+
|                                    RAYLS SOVEREIGN PRIVATE EVM TOPOLOGY                                 |
+---------------------------------------------------------------------------------------------------------+
|                                                                                                         |
|   +-------------------------------------------------------------------------------+                     |
|   |                       INSTITUTIONAL PERIMETER (FIREWALL)                      |                     |
|   |                                                                               |                     |
|   |   +-----------------------+               +-------------------------------+   |                     |
|   |   | Direct TLS RPC Ingress|               | KYC / LEI Institutional Gate  |   |                     |
|   |   | (Zero Public Gossip)  |               | (Active / Suspended Status)   |   |                     |
|   |   +-----------+-----------+               +---------------+---------------+   |                     |
|   |               │                                           │                   |                     |
|   |               ▼                                           ▼                   |                     |
|   |   +---------------------------------------------------------------+           |                     |
|   |   |            PRIVATE SEQUENCER LOCAL PRIORITY QUEUE             |           |                     |
|   |   |            • Exposure Window: 0.00s (Zero Mempool Leakage)    |           |                     |
|   |   |            • Strict Monotonic Sequence Nonce Monotonicity     |           |                     |
|   |   +-------------------------------+-------------------------------+           |                     |
|   |                                   │                                           |                     |
|   |                                   ▼                                           |                     |
|   |   +---------------------------------------------------------------+           |                     |
|   |   |            PARADIGM'S RETH EXECUTION ENGINE (RUST)            |           |                     |
|   |   |            • Zero Garbage Collection (Compile-Time RAII)      |           |                     |
|   |   |            • p99 Tail Latency: 1.56ms (0% SLA Breaches)       |           |                     |
|   |   +-------------------------------+-------------------------------+           |                     |
|   |                                   │                                           |                     |
|   |                                   ▼                                           |                     |
|   |   +---------------------------------------------------------------+           |                     |
|   |   |            EMBEDDED MDBX KEY-VALUE STORAGE ENGINE             |           |                     |
|   |   |            • Memory-Mapped Files (Zero-Copy Reads)            |           |                     |
|   |   |            • Zero LSM-Tree Compaction Lock Contention         |           |                     |
|   |   +---------------------------------------------------------------+           |                     |
|   |                                                                               |                     |
|   +---------------------------------------+---------------------------------------+                     |
|                                           │                                                             |
|                                           │ Periodic ZK State Root Commitments                          |
|                                           ▼                                                             |
|   +-------------------------------------------------------------------------------+                     |
|   |                           RAYLS PUBLIC CHAIN (L1)                             |                     |
|   |                  Chain ID: 72957  |  Reth Node 1.4.2 (b19896a1)               |                     |
|   |                                                                               |                     |
|   |   * Decentralized Validator Set & 500M Block Gas Ceiling                      |                     |
|   |   * Public Secondary Market Liquidity & Canonical Asset Bridging              |                     |
|   +-------------------------------------------------------------------------------+                     |
+---------------------------------------------------------------------------------------------------------+
```

---

## ⚡ Quick Start & Verification

### Prerequisites
- [Foundry](https://getfoundry.sh/) (`forge`, `cast`)
- Python 3.10+ (with `Pillow`)

### 1. Run Complete Demonstration Suite
```bash
./run_all_week6_demonstrations.sh
```

### 2. Run Foundry Test Suite
```bash
forge test -vvv
```

Expected Output:
```
Ran 7 tests for test/PrivateEVMInstitutionalGate.t.sol:PrivateEVMInstitutionalGateTest
[PASS] test_DeterministicGasProfiling() (gas: 959515)
[PASS] test_RevertIf_CollateralInsufficient() (gas: 67580)
[PASS] test_RevertIf_InstitutionalLaneSuspended() (gas: 71467)
[PASS] test_RevertIf_NonceReplayed() (gas: 261922)
[PASS] test_RevertIf_SequenceTampered() (gas: 44634)
[PASS] test_RevertIf_UnauthorizedCaller() (gas: 39457)
[PASS] test_ValidInstitutionalPrivateExecution() (gas: 259546)
Suite result: ok. 7 passed; 0 failed; 0 skipped; finished in 40.65ms
```

### 3. Query Live Rayls Public L1 Telemetry
```bash
python scripts/rayls_node_telemetry_audit.py
```

### 4. Run Controlled Engine Latency & Mempool Benchmark
```bash
python scripts/private_evm_engine_benchmark.py
```

---

## 📜 Complete 4-Category Evidence Boundary Matrix

| Row | Tested Property | Epistemic Boundary | Exact Artifact / Source | Result |
|:---:|:---|:---|:---|:---|
| **1** | Client Version | **[Category 1: Live On-Chain]** | `web3_clientVersion` RPC | `1.4.2 (b19896a12cfc1f1f775c33196c940f3345c00ede)` [Rust Reth] |
| **2** | Canonical Head Block | **[Category 1: Live On-Chain]** | `eth_blockNumber` | `#13,817,772+` (Live mainnet state) |
| **3** | Protocol Gas Ceiling | **[Category 1: Live On-Chain]** | `eth_getBlockByNumber` | `500,000,000 gas` (Computational execution headroom) |
| **4** | Median Block Cadence | **[Category 1: Live On-Chain]** | Sampled 500 blocks | `1.30s median cadence` (1.34s mean) |
| **5** | Base Gas Price | **[Category 1: Live On-Chain]** | `eth_gasPrice` RPC query | `48.00 gwei` (`48,000,000,000 wei`) |
| **6** | Private State Settlement | **[Category 2: Local Test]** | `test_ValidInstitutionalPrivate` | **PASS** (Gas: `259,546`, atomic debit/credit) |
| **7** | Unauthorized Caller Gate | **[Category 2: Local Test]** | `test_RevertIf_Unauthorized` | **REVERT:** `UnauthorizedInstitutionalCaller` |
| **8** | Monotonic Sequence Gate | **[Category 2: Local Test]** | `test_RevertIf_SequenceTampered` | **REVERT:** `InvalidExecutionSequence(0, 5)` |
| **9** | Nonce Replay Protection | **[Category 2: Local Test]** | `test_RevertIf_NonceReplayed` | **REVERT:** `InvalidExecutionSequence(1, 0)` |
| **10** | Collateral Overspend Gate | **[Category 2: Local Test]** | `test_RevertIf_Collateral` | **REVERT:** `InsufficientInstitutionalCollateral` |
| **11** | Regulatory Suspension | **[Category 2: Local Test]** | `test_RevertIf_Suspended` | **REVERT:** `InstitutionalLaneSuspended` |
| **12** | Gas Determinism Invariant | **[Category 2: Local Test]** | `test_DeterministicGasProfiling` | **PASS** (Steady-state variance $\le 4$ gas units) |
| **13** | Public Mempool Exposure | **[Category 3: Controlled Sim]**| Geth P2P model ($N=1\text{k}$) | `13.42s` mean pending exposure (100% node visibility) |
| **14** | Rayls Private Queue Exposure | **[Category 3: Controlled Sim]**| Sovereign TLS RPC ($N=1\text{k}$) | `0.00s` exposure (0.0% visibility; zero P2P gossip) |
| **15** | Go Geth Tail Latency ($p99$) | **[Category 3: Controlled Sim]**| Go runtime GC model ($N=1\text{k}$)| $p99 = 73.20\text{ms}$ (GC mark-sweep pauses) |
| **16** | Rust Reth Tail Latency ($p99$) | **[Category 3: Controlled Sim]**| Rust revm trace ($N=1\text{k}$) | $p99 = 1.56\text{ms}$ (Deterministic RAII memory safety) |
| **17** | Interbank DvP SLA Breaches | **[Category 3: Controlled Sim]**| Evaluated vs $>25\text{ms}$ SLA | Geth: **2.7% breach rate** vs. Rayls Reth: **0.0%** |
| **18** | MDBX State Storage Engine | **[Category 4: Documented Spec]**| Reth MDBX architecture | Memory-mapped B+ tree with zero-copy reads |
| **19** | Tooling Interoperability | **[Category 4: Documented Spec]**| Solidity & Foundry standard | 100% EVM bytecode compatibility; 0 niche DSLs |
| **20** | Wholesale CBDC Settlement | **[Category 4: Primary Alignment]**| Central Bank of Brazil (Drex) | 1:1 Real Digital reserve backing on Private Subnets |

---

## 📁 Repository Structure

```
├── .github/
│   └── workflows/
│       └── verify.yml                        # Automated GitHub Actions cloud CI
├── contracts/
│   ├── interfaces/
│   │   └── IPrivateEVMInstitutionalGate.sol  # Gateway interface, structs, & custom errors
│   └── PrivateEVMInstitutionalGate.sol       # Reference private EVM gate contract
├── test/
│   └── PrivateEVMInstitutionalGate.t.sol     # 7-test Foundry invariant suite
├── scripts/
│   ├── rayls_node_telemetry_audit.py         # Live Rayls L1 RPC auditor (500-block sample)
│   ├── private_evm_engine_benchmark.py       # Controlled latency & mempool benchmark (N=1k)
│   ├── generate_cover_image.py               # 1600x900 Twitter-safe cover generator
│   ├── generate_diagram_1.py                 # 1600x900 3-Eras DLT evolution diagram
│   ├── generate_diagram_2.py                 # 1600x900 Execution engine pipeline diagram
│   └── generate_matrix_table.py              # 1920x1800 4-Category evidence table
├── data/
│   ├── rayls_reth_node_telemetry.json        # Live RPC capture (Chain 72957, Reth 1.4.2)
│   ├── evm_engine_benchmark_results.json     # N=1,000 execution & mempool latency metrics
│   └── foundry_test_results.json             # Machine-readable test traces & gas profiles
├── assets/
│   ├── cover_image_private_evm.png           # Master cover asset
│   ├── diagram_1_enterprise_dlt_evolution.png# Figure 1: The Three Eras of DLT
│   ├── diagram_2_reth_mdbx_architecture.png  # Figure 2: Geth vs. Reth Execution Pipeline
│   ├── evidence_boundary_matrix_table.png    # Figure 3: Complete 4-Category Matrix
│   └── final cut.mp4                         # Narrated terminal screen recording demonstration
├── WHAT_IS_A_PRIVATE_EVM_AND_WHY_BANKS_NEED_ONE.md # Master 3,500+ Word Research Article
├── CROSS_POST_SUMMARY.md                     # Executive Short-Form Cross-Post Package
├── run_all_week6_demonstrations.sh           # Master one-line reproduction runner
└── foundry.toml                              # Foundry project configuration
```

---

## ⚖️ License & Attribution
Distributed under the MIT License. Developed for The Rail Research Labs.  
Visual assets adhere strictly to the **Noir Ventures Rayls Brand System**.
