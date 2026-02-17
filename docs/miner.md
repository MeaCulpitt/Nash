# Miner Design

## What Miners Do

NASH miners are **game-theoretic solvers**. They ingest trade intents from Bittensor subnets and compute the mathematically optimal settlement — the point where no party can improve without making another worse off. This isn't matching — it's optimization. The miner must find the single best point in a multi-dimensional trade space.

### The Core Task

```
INPUT:  Intent vectors from 2+ subnets
        (price ranges, quantities, constraints, preferences)

OUTPUT: Equilibrium proposal
        (exact settlement terms that optimize for all parties)
```

---

## Miner Tasks

### 1. Intent Parsing
- Parse incoming intent vectors from validators
- Convert to utility functions for each party
- Validate constraints

### 2. Manifold Construction
- Construct trade possibility space
- Map all feasible settlements
- Identify constraint boundaries

### 3. Equilibrium Discovery
- Search for Pareto frontier
- Find Nash stable point
- Optimize for global utility

### 4. Proof Generation
- Generate commitment hash
- Create computation proof
- Package response

---

## Worked Example: Solving a Three-Party Trade

### Challenge Received

Validator broadcasts:

```json
{
  "challenge_id": "0x7a3f...",
  "parties": [
    {
      "id": "sn64_chutes",
      "intent": "buy",
      "resource": "gpu_hours",
      "quantity": {"min": 100, "max": 300},
      "price": {"max": 1.80},
      "constraints": ["latency_ms < 50", "region in [US, EU]"]
    },
    {
      "id": "sn27_nodexo",
      "intent": "sell",
      "resource": "gpu_hours",
      "quantity": {"available": 500},
      "price": {"min": 1.30},
      "constraints": ["region = EU"]
    },
    {
      "id": "sn12_compute_horde",
      "intent": "defer",
      "resource": "gpu_hours",
      "quantity": {"current": 150},
      "compensation": {"min": 0.20, "per": "hour_deferred"},
      "constraints": ["max_defer_hours = 8"]
    }
  ],
  "response_window_ms": 200
}
```

### Miner Processing

1. **Parse intents** into utility functions for each party
2. **Construct trade manifold** — all possible settlements
3. **Search for Pareto frontier** — outcomes where no party can improve without hurting another
4. **Find Nash Equilibrium** — the stable point on the frontier
5. **Generate proof** — commitment hash proving computation

### Solution Submitted

```json
{
  "challenge_id": "0x7a3f...",
  "settlement": {
    "sn64_chutes": {
      "action": "buy",
      "quantity": 200,
      "price_per_unit": 1.52,
      "constraints_met": ["latency: 38ms", "region: EU"]
    },
    "sn27_nodexo": {
      "action": "sell",
      "quantity": 200,
      "revenue": 304.00
    },
    "sn12_compute_horde": {
      "action": "defer",
      "hours_deferred": 6,
      "compensation": 45.00
    }
  },
  "equilibrium_proof": {
    "pareto_optimal": true,
    "utility_scores": {
      "sn64_chutes": 0.87,
      "sn27_nodexo": 0.82,
      "sn12_compute_horde": 0.91
    }
  },
  "response_time_ms": 43
}
```

### Why This Wins
- All constraints satisfied
- No party can get a better deal without hurting another (Pareto optimal)
- No party has incentive to deviate (Nash stable)
- Response time under threshold

---

## The Miner Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                       MINER PIPELINE                             │
├─────────────────────────────────────────────────────────────────┤
│  1. INTENT           Parse incoming intent vectors              │
│     PARSING          Convert to utility functions               │
│                      Validate constraints                        │
├─────────────────────────────────────────────────────────────────┤
│  2. MANIFOLD         Construct trade possibility space         │
│     CONSTRUCTION     Map all feasible settlements               │
│                      Identify constraint boundaries              │
├─────────────────────────────────────────────────────────────────┤
│  3. EQUILIBRIUM      Search for Pareto frontier                │
│     DISCOVERY        Find Nash stable point                     │
│                      Optimize for global utility                │
├─────────────────────────────────────────────────────────────────┤
│  4. PROOF            Generate commitment hash                   │
│     GENERATION       Create computation proof                   │
│                      Package response                           │
└─────────────────────────────────────────────────────────────────┘
```

All four stages must complete within 200ms response window.

---

## Input/Output Specification

### Input Format (Validator → Miner)

| Field | Type | Description |
|-------|------|-------------|
| `challenge_id` | hex-512 | Unique challenge identifier |
| `parties` | array | List of participating subnets/agents |
| `parties[].id` | string | Subnet or agent identifier |
| `parties[].intent` | enum | buy, sell, swap, defer |
| `parties[].resource` | string | What's being traded |
| `parties[].quantity` | object | Min/max/available amounts |
| `parties[].price` | object | Min/max acceptable prices |
| `parties[].constraints` | array | Hard requirements |
| `response_window_ms` | int | Time limit for response |

### Output Format (Miner → Validator)

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

## Scoring Dimensions

Miners are evaluated on four dimensions:

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

## Miner Architecture

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

## Performance Targets

| Dimension | Target | Impact |
|-----------|--------|--------|
| **Quality** | ≥0.95 Q-score | Directly multiplies emission |
| **Speed** | <50ms | No penalty; >100ms = TWF decay |
| **Uptime** | >95% | 20% of TWF weight |
| **Complexity** | 3+ parties | Up to 4x PMU bonus |

---
