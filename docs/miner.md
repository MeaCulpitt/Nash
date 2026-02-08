# NASH: Miner Architecture & Operations

NASH miners are game-theoretic solvers. They ingest trade intents from Bittensor subnets and compute the mathematically optimal settlement — the point where no party can improve without making another worse off. Speed and accuracy determine earnings.

---

## What Miners Do

When subnets need to trade resources, they submit intent vectors describing their preferences. Miners race to find the optimal deal.

### The Core Task

```
INPUT:  Intent vectors from 2+ subnets
        (price ranges, quantities, constraints, preferences)

OUTPUT: Equilibrium proposal
        (exact settlement terms that optimize for all parties)
```

This isn't matching — it's optimization. The miner must find the single best point in a multi-dimensional trade space.

---

## Worked Example: Solving a Three-Party Trade

### Challenge Received

Validator broadcasts:

```json
{
  "challenge_id": "0x7a3f...",
  "timestamp": 1707408000000,
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
      "total_cost": 304.00,
      "constraints_met": ["latency: 38ms", "region: EU"]
    },
    "sn27_nodexo": {
      "action": "sell",
      "quantity": 200,
      "revenue": 304.00,
      "utilization_gain": "40%"
    },
    "sn12_compute_horde": {
      "action": "defer",
      "hours_deferred": 6,
      "compensation": 45.00,
      "freed_capacity": 150
    }
  },
  "equilibrium_proof": {
    "pareto_optimal": true,
    "nash_stable": true,
    "utility_scores": {
      "sn64_chutes": 0.87,
      "sn27_nodexo": 0.82,
      "sn12_compute_horde": 0.91
    }
  },
  "commitment_hash": "sha256:9f3c2...",
  "compute_proof": "zk:0x8a1b...",
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
│                      Validate constraints                       │
├─────────────────────────────────────────────────────────────────┤
│  2. MANIFOLD         Construct trade possibility space          │
│     CONSTRUCTION     Map all feasible settlements               │
│                      Identify constraint boundaries             │
├─────────────────────────────────────────────────────────────────┤
│  3. EQUILIBRIUM      Search for Pareto frontier                 │
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
| `parties[].preferences` | array | Soft preferences (weighted) |
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
| `equilibrium_proof.nash_stable` | bool | No incentive to deviate? |
| `equilibrium_proof.utility_scores` | object | Utility achieved per party |
| `commitment_hash` | sha256 | Prevents post-hoc modification |
| `compute_proof` | zk-proof | Proves computation was performed |
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

Validators compare all submissions. If your solution is dominated (another miner found a strictly better deal), you score zero.

### Utility: Marginal Discovery (20% weight)

**Metric:** PMU multiplier based on problem difficulty.

| Trade Complexity | PMU Range |
|------------------|-----------|
| Two-party, no constraints | 0.3x - 0.5x |
| Two-party with constraints | 0.6x - 1.0x |
| Three-party | 1.5x - 2.5x |
| Four+ party | 2.5x - 4.0x |

Also scaled by solver count — fewer miners solving = higher PMU.

### Speed: Response Latency (20% weight)

**Metric:** Response time vs. 200ms window.

| Response Time | Impact |
|---------------|--------|
| <50ms | Optimal, no penalty |
| 50-100ms | Minor TWF decay |
| 100-150ms | Moderate TWF decay |
| 150-200ms | Significant TWF decay |
| >200ms | Disqualified |

Fast miners build TWF over time. Slow miners see it erode.

### Consistency: Solution Stability (10% weight)

**Metric:** Variance across identical challenges.

Validators occasionally reissue the same challenge (salted). Miners should produce identical solutions. High variance suggests:
- Non-deterministic algorithms
- Random guessing
- Unstable infrastructure

Consistent miners earn trust.

---

## Hardware Requirements

NASH is CPU-intensive, not GPU-intensive. The bottleneck is algorithmic efficiency, not raw compute.

### Minimum

| Component | Requirement |
|-----------|-------------|
| CPU | 8-core, 3.5GHz+ |
| RAM | 32GB |
| Network | 100Mbps, low latency |
| Storage | 100GB SSD |

### Recommended

| Component | Recommendation |
|-----------|----------------|
| CPU | 16-core, 4.0GHz+ (AMD Ryzen 9 / Intel i9) |
| RAM | 64GB |
| Network | 1Gbps, <10ms to major exchanges |

### Why Not GPU?

Nash Equilibrium search is:
- Branching and conditional (poor GPU fit)
- Memory-access heavy (CPU cache advantage)
- Algorithmically bounded (better algorithms beat more cores)

Smart heuristics outperform brute force. Invest in algorithm development, not hardware.

---

## Competitive Strategy

### Finding Your Edge

Top miners differentiate through:

1. **Algorithm quality:** Better search heuristics find equilibria faster
2. **Specialization:** Focus on trade types others struggle with (high PMU)
3. **Infrastructure:** Low-latency network positioning
4. **Reliability:** High uptime builds TWF

### The PMU Hunt

Simple two-party trades are crowded (150+ miners competing). Complex trades are sparse (5-20 miners).

**Strategy:** Develop capabilities for multi-party optimization. Accept lower volume for higher per-trade earnings.

### Building TWF

TWF compounds over time. Early consistency matters more than early volume.

**Strategy:** Start with trades you can solve reliably. Expand complexity as your reputation builds.

---

## Anti-Gaming Protections

Miners cannot game the system:

| Attack | Defense |
|--------|---------|
| Random submissions | TWF slash on failed proposals |
| Copying other miners | Commitment hash proves priority |
| Sybil (multiple UIDs) | Identical solutions collapse PMU |
| Pre-computed lookups | Salted challenges detect patterns |
| Latency manipulation | Validator-measured RTT |

Detected gaming results in:
1. Immediate TWF decay
2. Multi-week recovery period
3. Potential stake slashing on repeat offense

---
