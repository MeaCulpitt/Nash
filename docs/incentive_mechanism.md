# 1. Incentive & Mechanism Design

## Emission and Reward Logic

NASH uses **dual emission pools** to balance reliability with market discovery:

| Pool | Allocation | Purpose |
|------|------------|---------|
| **Stability Layer** | 40% | Rewards consistent, long-term participants via Time-Weighted Fidelity (TWF) |
| **Discovery Layer** | 60% | Rewards solving hard problems via Proof of Marginal Utility (PMU) |

### Time-Weighted Fidelity (TWF)

```python
TWF = rolling_average(accuracy, uptime, latency, last_1000_challenges)
```

| Factor | Weight | What It Measures |
|--------|--------|------------------|
| Accuracy | 50% | % of proposals on Pareto frontier |
| Uptime | 20% | % of challenges responded to |
| Latency | 30% | Response time vs. 50ms threshold |

### Proof of Marginal Utility (PMU)

```python
PMU = base_reward × (1 / √solver_count) × complexity_multiplier × uniqueness_bonus
```

| Trade Type | Base PMU | Complexity Multiplier |
|------------|----------|----------------------|
| Simple two-party swap | 0.3x | 1.0x |
| Two-party with constraints | 0.7x | 1.2x |
| Three-party optimization | 1.8x | 2.5x |
| Multi-subnet resource triangle | 3.0x | 4.0x |

## Scoring Formula

```
S = Q × PMU × TWF × SPF

Where:
  Q   = Quality (0.0 - 1.0) — accuracy of equilibrium proposal
  PMU = Proof of Marginal Utility (0.1 - 5.0) — difficulty multiplier
  TWF = Time-Weighted Fidelity (0.5 - 1.5) — reputation multiplier
  SPF = Subnet Priority Factor (0.8 - 1.2) — priority-weighted satisfaction
```

### Quality Score (Q)

| Result | Q Score |
|--------|---------|
| On Pareto frontier (optimal) | 1.0 |
| Within 0.1% of optimal | 0.95 |
| Within 1% of optimal | 0.80 |
| Within 5% of optimal | 0.60 |
| Dominated by another solution | 0.0 |

## Incentive Alignment for Miners

Optimal miner strategy:
1. **Target complex trades** — Multi-party, multi-constraint = high PMU
2. **Maintain accuracy** — Quality score multiplies everything
3. **Build reputation** — TWF compounds over time
4. **Optimize infrastructure** — Latency affects TWF decay
5. **Aim for uniqueness** — Being the first to solve = bonus

## Incentive Alignment for Validators

Optimal validator strategy:
1. **Accurate verification** — V-Trust determines dividend share
2. **Consensus alignment** — Outlier scores get penalized
3. **Challenge diversity** — Novel challenge types = new PMU opportunities
4. **Fast baseline simulation** — Required to judge 50ms window accurately
5. **Stake up** — Higher stake = more voting power in consensus

## Mechanisms to Discourage Low-Quality or Adversarial Behavior

### 1. Fidelity Slash
```python
def apply_fidelity_slash(miner, quality):
    if quality < 0.3:
        miner.TWF *= 0.6  # 40% decay
    elif quality < 0.5:
        miner.TWF *= 0.8  # 20% decay
```
Recovery: 200-800 challenges depending on stratum.

### 2. Anti-Sybil PMU Collapse
```python
def detect_sybil_attack(miner_solutions):
    clusters = cluster_solutions_by_similarity(miner_solutions)
    if len(cluster) > 1:
        return 0.1  # Minimum PMU for everyone
```
IP and key reputation tracking.

### 3. Saturation Cap
```python
if solver_count > 100 and complexity < 2.0:
    effective_pmu = min(0.2, calculated_pmu)
```

### 4. Salted Challenges
Validators issue challenges with known solutions at random intervals. Pre-computed responses detectable via response time fingerprinting.

## Proof of Intelligence

Finding Nash Equilibria is computationally non-trivial:

| Problem Class | Complexity | NASH Application |
|---------------|------------|------------------|
| Two-player zero-sum | Polynomial | Simple swaps |
| Multi-player general | PPAD-complete | NASH settlements |
| Coalition formation | NP-hard | Multi-subnet trades |

This ensures the network requires genuine computation, not database lookups.

## High-Level Algorithm

```
1. INTENT     → Subnets submit preference vectors
2. DISCOVERY  → Miners compete to find optimal settlement
3. VERIFY     → Validators confirm Pareto optimality (stake-weighted)
4. SETTLE     → Trade executes automatically
5. SCORE      → Q × PMU × TWF × SPF → emissions distributed
```
