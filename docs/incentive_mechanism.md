# Incentive & Mechanism Design

## Overview

NASH incentivizes miners to find optimal trade settlements between Bittensor subnets. The mechanism rewards both **accuracy** (finding the true equilibrium) and **difficulty** (solving complex, multi-party trades). This creates a network that handles everything from simple swaps to complex resource triangulations.

The core insight: Finding Nash Equilibria is computationally non-trivial (PPAD-complete for multi-player games), so the network naturally requires genuine computation — not database lookups or simple matching.

---

## The Manifold: Compressed Intent Representation

A key component of NASH is the **Nash Manifold** — a compressed representation of subnet intent used by miners to find equilibria.

### What is the Manifold?

The manifold is a **fixed-dimension encoding** (256 dimensions) that standardizes input format for miners:

1. **Neural network compatibility** — Fixed input size for ML-based solvers
2. **Faster computation** — Compressed representation processes faster
3. **Standardization** — All miners receive the same input format

**Important:** Miners see the full intent to find equilibria. Privacy comes from **what gets published on-chain** (just settlement terms), not from hiding data from miners.

### Where Do Intents Come From?

The **subnets themselves** submit their intents — not the validator.

```
SN64 (Chutes)     SN27 (Nodexo)     SN12 (ComputeHorde)
      │                   │                    │
      │ "I need 200      │ "I have 500       │ "I could defer
      │  GPU-hrs,        │  GPU-hrs,         │  my batch job
      │  max $1.80/hr"   │  min $1.30/hr"    │  for $X/hr"
      │                   │                    │
      └───────────────────┼────────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │    VALIDATOR       │
              │  Collects intents  │
              │  Broadcasts to miners│
              └─────────────────────┘
                         │
                         ▼
                   MINERS solve
                         │
                         ▼
              ┌─────────────────────┐
              │    SETTLEMENT       │
              │  200 hrs @ $1.52   │
              │  (on-chain)        │
              └─────────────────────┘
```

The validator is the **orchestrator** — receives intents from subnets, broadcasts challenges, verifies solutions, publishes settlement.

### Bootstrapping: Training Miners Initially

**Phase 1: Synthetic Training**
- Validator generates fake intents simulating subnet preferences
- Miners practice finding equilibria on these problems
- Builds initial TWF/reputation scores

**Phase 2: Real Subnets Join**
- Subnets begin submitting real intents
- Validators mix synthetic + real challenges

**Phase 3: Full Production**
- Real intents dominate
- Optional: Anonymized historical data for fine-tuning
- Subnets control their data (voluntary sharing)

---

## Emission and Reward Logic

NASH uses **dual emission pools**:

| Pool | Allocation | Purpose |
|------|------------|---------|
| **Stability Layer** | 40% | Rewards consistent participants via TWF |
| **Discovery Layer** | 60% | Rewards solving hard problems via PMU |

---

## Time-Weighted Fidelity (TWF)

```python
TWF = rolling_average(accuracy, uptime, latency, last_1000_challenges)
```

| Factor | Weight | What It Measures |
|--------|--------|------------------|
| Accuracy | 50% | % of proposals on Pareto frontier |
| Uptime | 20% | % of challenges responded to |
| Latency | 30% | Response time vs. 50ms threshold |

---

## Proof of Marginal Utility (PMU)

```python
PMU = base_reward × (1 / √solver_count) × complexity_multiplier × uniqueness_bonus
```

| Trade Type | Typical Solvers | Base PMU | Complexity |
|------------|-----------------|----------|------------|
| Simple two-party swap | 150+ | 0.3x | 1.0x |
| Two-party with constraints | 50-100 | 0.7x | 1.2x |
| Three-party optimization | 10-30 | 1.8x | 2.5x |
| Multi-subnet resource triangle | 3-10 | 3.0x | 4.0x |

---

## Scoring Formula

```
S = Q × PMU × TWF × SPF

Q   = Quality (0.0 - 1.0)
PMU = Proof of Marginal Utility (0.1 - 5.0)
TWF = Time-Weighted Fidelity (0.5 - 1.5)
SPF = Subnet Priority Factor (0.8 - 1.2)
```

---

## Incentive Alignment for Miners

1. Target complex trades — high PMU
2. Maintain accuracy — Q multiplies everything
3. Build reputation — TWF compounds
4. Optimize infrastructure — latency affects TWF
5. Aim for uniqueness — bonus for first to solve

### Stratum System

| Stratum | Requirement | TWF Floor |
|---------|-------------|-----------|
| Platinum | Top 1%, 5000+ challenges | 1.3x |
| Gold | Top 10%, 5000+ challenges | 1.2x |
| Silver | 1000+ challenges | 1.0x |
| Bronze | Newcomer | 0.7x |

---

## Incentive Alignment for Validators

1. Accurate verification — V-Trust determines dividends
2. Consensus alignment — Outlier scores penalized
3. Challenge diversity — Novel challenges = PMU + V-Trust boost
4. Fast baseline simulation
5. Stake up — More stake = more voting power

---

## Anti-Gaming Mechanisms

1. **Fidelity Slash** — Tiered TWF decay for low-quality proposals
2. **Anti-Sybil** — Similar solutions collapse PMU
3. **Saturation Cap** — Easy trades capped
4. **Salted Challenges** — Detect pre-computation
5. **Validator Collusion Prevention** — Random score publishing + outlier penalization

---

## Proof of Intelligence

| Problem Class | Complexity |
|---------------|------------|
| Two-player zero-sum | Polynomial |
| Multi-player general | PPAD-complete |
| Coalition formation | NP-hard |

---

## High-Level Algorithm

```
1. INTENT     → Subnets submit preference vectors
2. MANIFOLD   → Compress to standardized encoding
3. DISCOVERY  → Miners compete to find optimal settlement
4. VERIFY     → Validators confirm Pareto optimality
5. SETTLE     → Trade executes automatically
6. SCORE      → Q × PMU × TWF × SPF → emissions distributed
```

---
