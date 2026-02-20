# Incentive & Mechanism Design

## Overview

NASH incentivizes miners to find optimal trade settlements between Bittensor subnets. The mechanism rewards both **accuracy** (finding the true equilibrium) and **difficulty** (solving complex, multi-party trades).

The core innovation: Validators cannot verify optimality with incomplete information (commitments only). Instead, they **learn to estimate** optimality via a model trained on synthetic challenges where the answer is known.

---

## 1. Emission and Reward Logic

### Dual Emission Pools

NASH uses **dual emission pools** to balance reliability with market discovery:

| Pool | Allocation | Purpose |
|------|------------|---------|
| **Stability Layer** | 40% | Rewards consistent, long-term participants via Time-Weighted Fidelity (TWF) |
| **Discovery Layer** | 60% | Rewards solving hard problems via Proof of Marginal Utility (PMU) |

This dual-pool design prevents two failure modes:
- If only Stability existed, miners would do the minimum to maintain reputation
- If only Discovery existed, newcomers could outcompete proven miners on hard problems

### Time-Weighted Fidelity (TWF)

TWF rewards consistent performance over time:

```python
TWF = rolling_average(accuracy, uptime, latency, last_1000_challenges)
```

| Factor | Weight | What It Measures |
|--------|--------|------------------|
| Accuracy | 50% | % of proposals on Pareto frontier |
| Uptime | 20% | % of challenges responded to |
| Latency | 30% | Response time vs. 50ms threshold |

TWF ranges from **0.5 to 1.5x**, creating stickiness for established miners while allowing newcomers to compete.

### Proof of Marginal Utility (PMU)

PMU rewards miners for solving hard problems that few others can solve:

```python
PMU = base_reward × (1 / √solver_count) × complexity_multiplier × uniqueness_bonus
```

| Trade Type | Typical Solvers | Base PMU | Complexity Multiplier |
|------------|-----------------|----------|----------------------|
| Simple two-party swap | 150+ | 0.3x | 1.0x |
| Two-party with constraints | 50-100 | 0.7x | 1.2x |
| Three-party optimization | 10-30 | 1.8x | 2.5x |
| Multi-subnet resource triangle | 3-10 | 3.0x | 4.0x |

PMU ranges from **0.1 to 5.0x**.

### Scoring Formula

```
S = Q × PMU × TWF × SPF

Where:
  Q   = Quality (0.0 - 1.0) — accuracy of equilibrium proposal
  PMU = Proof of Marginal Utility (0.1 - 5.0) — difficulty multiplier
  TWF = Time-Weighted Fidelity (0.5 - 1.5) — reputation multiplier
  SPF = Subnet Priority Factor (0.8 - 1.2) — priority-weighted satisfaction
```

---

## 2. Incentive Alignment for Miners and Validators

### For Miners

Optimal miner strategy:

1. **Target complex trades** — Multi-party, multi-constraint = high PMU
2. **Maintain accuracy** — Quality score multiplies everything
3. **Build reputation** — TWF compounds over time
4. **Optimize infrastructure** — Latency affects TWF decay
5. **Aim for uniqueness** — Being first to solve = bonus

### Stratum System

| Stratum | Requirement | TWF Floor | Recovery Rate |
|---------|-------------|-----------|---------------|
| Platinum | Top 1% by stake, 5000+ challenges | 1.3x | Fastest |
| Gold | Top 10%, 5000+ challenges, >95% accuracy | 1.2x | Fast |
| Silver | 1000+ challenges, >80% accuracy | 1.0x | Normal |
| Bronze | Newcomer (<1000 challenges) | 0.7x | Slowest |

### For Validators

Optimal validator strategy:

1. **Accurate verification** — V-Trust determines dividend share
2. **Consensus alignment** — Outlier scores penalized
3. **Challenge diversity** — Novel challenge types = PMU + V-Trust boost
4. **Train the model** — Generate synthetic challenges to build commitment model
5. **Stake up** — More stake = more voting power in consensus

### V-Trust (Validator Reputation)

```python
def calculate_v_trust(validator):
    V_TRUST = (
        0.4 * consensus_accuracy +   # Agrees with majority
        0.3 * speed_score +          # Verification speed
        0.3 * challenge_diversity     # Novel challenge types
    )
    return V_TRUST

# Quadratic voting power
validator.voting_power = validator.stake ** 0.5 * V_TRUST
```

### Validator Training Pipeline (Key Innovation)

**The Problem:** Validators see only commitments, not full preferences. They cannot compute the true optimal.

**The Solution:** Train a model to estimate optimality.

```
TRAINING PHASE (synthetic):
 1. Generate challenges where we know the answer (full preferences)
 2. Validators see both commitments AND ground truth
 3. Train model: commitments → optimal
 4. After N samples, model is ready

PRODUCTION PHASE (real):
 1. Validators see only commitments (like miners)
 2. Use trained model to estimate optimality
 3. Score miners based on model's estimate
```

This is the **core insight**: validation becomes estimation, not computation.

---

## 3. Mechanisms to Discourage Low-Quality or Adversarial Behavior

### 1. Fidelity Slash

**Attack:** Submit random proposals hoping for lucky matches.

**Defense:** Failed proposals trigger tiered TWF decay:

```python
def apply_fidelity_slash(miner, quality):
    if quality < 0.3:
        miner.TWF *= 0.6  # 40% decay
    elif quality < 0.5:
        miner.TWF *= 0.8  # 20% decay
```

Recovery: 200-800 challenges depending on stratum.

### 2. Anti-Sybil PMU Collapse

**Attack:** Run multiple miners to capture PMU on same challenge.

**Defense:** Identical/near-identical solutions from different UIDs collapse PMU:

```python
def detect_sybil_attack(miner_solutions):
    clusters = cluster_solutions_by_similarity(miner_solutions)
    if len(cluster) > 1:
        return 0.1  # Minimum PMU for everyone
```

IP and key reputation tracking.

### 3. Saturation Cap

**Attack:** High-performance miners farm only easy trades.

**Defense:** Low-complexity trades have emission ceiling:

```python
if solver_count > 100 and complexity < 2.0:
    effective_pmu = min(0.2, calculated_pmu)
```

### 4. Salted Challenges

**Attack:** Pre-compute responses to known challenge patterns.

**Defense:** Validators issue challenges with known solutions at random intervals. Pre-computed responses detectable via response time fingerprinting (too fast = pre-computed).

### 5. Validator Collusion Prevention

- Random subset of validator scores published before consensus
- Outlier validators lose V-Trust
- Stake-weighted voting makes colluding expensive (need majority stake)

---

## 4. Proof of Intelligence / Proof of Effort

### The Computational Hardness Argument

Finding Nash Equilibria is computationally non-trivial:

| Problem Class | Complexity | NASH Application |
|---------------|------------|------------------|
| Two-player zero-sum | Polynomial | Simple swaps |
| Multi-player general | **PPAD-complete** | NASH settlements |
| Coalition formation | **NP-hard** | Multi-subnet trades |

This ensures the network requires **genuine computation**, not database lookups or simple matching.

### Why This Is Proof of Intelligence

1. **NP-Hard Problem:** Finding optimal settlements in multi-party trades is computationally intractable. Miners must use sophisticated algorithms, not brute force.

2. **Learned Estimation:** Validators cannot compute optimality—they must learn to estimate it. This requires:
   - Generating diverse synthetic challenges
   - Training a model on known answers
   - Generalizing to unseen commitment patterns

3. **Game-Theoretic Reasoning:** Miners must understand incentive structures, not just optimize a function. They reason about what each party wants and find mutually optimal outcomes.

4. **Adaptive Strategy:** The optimal approach varies by:
   - Number of parties (2, 3, 4+)
   - Constraint types (latency, region, time horizon)
   - Resource being traded (GPU-hours, TAO, storage)

### Why This Is Proof of Effort

1. **Time-Weighted Fidelity:** Reputation compounds with consistent participation. Short-term exploitation is penalized.

2. **Infrastructure Investment:** Sub-50ms settlement requires optimized hardware and low-latency networks.

3. **Continuous Learning:** Miners must improve solvers to handle harder problems. Validators must generate diverse challenges.

4. **Skin in the Game:** Both miners and validators stake TAO. Misbehavior results in economic loss.

---

## 5. High-Level Algorithm

### The Complete Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           NASH SETTLEMENT PIPELINE                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   1. INTENT  │───▶│  2. CHALLENGE│───▶│  3. DISCOVERY│───▶│  4. VERIFY  │
│   Collection │    │  Generation  │    │    (Miners)  │    │(Validators) │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
                           │                                       │
                           │                                       ▼
                    ┌──────┴──────┐                        ┌──────────────┐
                    │   Real or   │                        │   Estimate   │
                    │  Synthetic  │                        │  Optimality  │
                    └─────────────┘                        │ via Model    │
                                                          └──────────────┘
                                                                 │
                                                                 ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  7. EMIT     │◀───│  6. SCORE   │◀───│  5. SETTLE   │◀───│ 4b. CONSENSUS│
│  Rewards     │    │  Q×PMU×TWF  │    │ On-Chain     │    │(Stake-Weight)│
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

### Step-by-Step Description

#### Step 1: Intent Collection
- Subnets submit preferences via SDK/API
- Validator aggregates into challenge format
- **Training mode:** Also generates synthetic challenges with known answers

#### Step 2: Challenge Generation
- Validator creates challenge from intents
- Includes: party info, constraints, time limits
- **Training:** Validators generate challenges where they know the optimal solution

#### Step 3: Discovery (Miners)
- Validator broadcasts challenge to all active miners
- Miners compute equilibrium (Nash solver)
- Response window: 50-200ms depending on complexity

#### Step 4: Verification (Validators)

**Training Phase:**
1. Validator has full preferences (ground truth)
2. Run Nash solver to get true optimal
3. Train model: commitments → optimal

**Production Phase:**
1. Validator sees only commitments (like miners)
2. Use trained model to estimate optimality
3. Compare miner response to estimate
4. Assign score

#### Step 4b: Consensus
- Validators aggregate scores (stake-weighted)
- Outliers penalized
- Final weights submitted to blockchain

#### Step 5: Settlement
- Winning settlement published on-chain
- Trade executes automatically
- Subnets reveal preferences post-settlement (can reject if worse off)

#### Step 6: Scoring
```
final_score = Q × PMU × TWF × SPF
```

- **Q:** Quality (accuracy vs. estimated optimal)
- **PMU:** Difficulty multiplier
- **TWF:** Reputation multiplier
- **SPF:** Subnet priority factor

#### Step 7: Emission
- TAO distributed proportionally to scores
- Validators earn dividends from network emissions

### Task Assignment Summary

| Role | Task | Input | Output |
|------|------|-------|--------|
| **Subnet** | Submit intent | Preferences | Commitment vector |
| **Validator** | Orchestrate | Commitments | Weights |
| **Miner** | Solve | Challenge | Equilibrium proposal |

---

## Summary

| Component | Value |
|-----------|-------|
| Settlement time | <50ms |
| Max PMU | 5.0x |
| TWF range | 0.5 - 1.5x |
| Validator stake | ≥1000 τ |
| Subnet capacity | 256 UIDs (64V + 192M) |
| Proof type | PPAD-complete + learned estimation
