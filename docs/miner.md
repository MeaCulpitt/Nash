# Miner Design

## Overview

NASH miners are **game-theoretic solvers**. They ingest trade intents from Bittensor agents and compute the mathematically optimal settlement — the point where no party can improve without making another worse off.

---

## 1. Miner Tasks

### Core Responsibilities

1. **Intent Parsing**
   - Parse incoming intent vectors from validators
   - Convert to utility functions for each party
   - Validate constraints

2. **Manifold Construction**
   - Construct trade possibility space
   - Map all feasible settlements
   - Identify constraint boundaries

3. **Equilibrium Discovery**
   - Search for Pareto frontier
   - Find Nash stable point
   - Optimize for global utility

4. **Proof Generation**
   - Generate commitment hash
   - Create computation proof
   - Package response

---

## 2. Expected Input → Output Format

### Input (from Validator)

| Field | Type | Description |
|-------|------|-------------|
| `challenge_id` | hex-512 | Unique challenge identifier |
| `parties` | array | List of participating agents |
| `parties[].id` | string | Agent identifier |
| `parties[].intent` | enum | buy, sell, swap, defer |
| `parties[].resource` | string | What's being traded |
| `parties[].quantity` | object | Min/max/available amounts |
| `parties[].price` | object | Min/max acceptable prices |
| `parties[].constraints` | array | Hard requirements |
| `response_window_ms` | int | Time limit for response |

### Output (to Validator)

| Field | Type | Description |
|-------|------|-------------|
| `challenge_id` | hex-512 | Echo back for matching |
| `settlement` | object | Proposed terms for each party |
| `settlement[party].action` | enum | What this party does |
| `settlement[party].quantity` | float | Amount traded |
| `settlement[party].price_per_unit` | float | Settlement price |
| `settlement[party].constraints_met` | array | Proof of constraint satisfaction |
| `equilibrium_proof` | object | Mathematical verification |
| `equilibrium_proof.pareto_optimal` | bool | On the Pareto frontier? |
| `equilibrium_proof.utility_scores` | object | Utility achieved per party |
| `commitment_hash` | sha256 | Prevents post-hoc modification |
| `response_time_ms` | int | Self-reported latency |

---

## 3. Performance Dimensions

### Quality: Equilibrium Accuracy (50% weight)

**Metric:** Is the proposal on the Pareto frontier?

| Result | Q Score |
|--------|---------|
| Pareto optimal, Nash stable | 1.0 |
| Pareto optimal, not Nash stable | 0.85 |
| Within 0.1% of frontier | 0.90 |
| Within 1% of frontier | 0.70 |
| Dominated by another solution | 0.0 |

### Utility: Marginal Discovery (PMU)

**Metric:** PMU multiplier based on problem difficulty.

| Trade Complexity | PMU Range |
|------------------|-----------|
| Two-party, no constraints | 0.3x - 0.5x |
| Two-party with constraints | 0.6x - 1.0x |
| Three-party | 1.5x - 2.5x |
| Four+ party | 2.5x - 4.0x |

Also scaled by solver count — fewer miners solving = higher PMU.

### Speed: Response Latency

**Metric:** Response time vs. 200ms window.

| Response Time | Impact |
|---------------|--------|
| <50ms | Optimal, no penalty |
| 50-100ms | Minor penalty |
| >100ms | Major TWF decay |

### Uptime: Participation

**Metric:** % of challenges responded to. Part of TWF calculation (20% weight).

---

## 4. Architecture

```python
class NashMiner(bt.Neuron):
    def __init__(self):
        self.encoder = IntentEncoder(input_dim=10, manifold_dim=256)
        self.solver = EquilibriumSolver(manifold_dim=256)
    
    async def forward(self, synapse: NashSynapse) -> NashSynapse:
        manifold = self.encoder(synapse.raw_intent)
        equilibrium = self.solver(manifold)
        return synapse
```

---

## 5. Performance Targets

| Dimension | Target | Impact |
|-----------|--------|--------|
| **Quality** | ≥0.95 Q-score | Directly multiplies emission |
| **Speed** | <50ms | No penalty; >100ms = TWF decay |
| **Uptime** | >95% | 20% of TWF weight |
| **Complexity** | 3+ parties | Up to 4x PMU bonus |
