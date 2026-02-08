# NASH: Incentive & Mechanism Design

NASH incentivizes miners to find optimal trade settlements between Bittensor subnets. The mechanism rewards both **accuracy** (finding the true equilibrium) and **difficulty** (solving complex, multi-party trades). This creates a network that handles everything from simple swaps to complex resource triangulations.

---

## Worked Example: Cross-Subnet Compute Settlement

### Scenario: Three-Subnet Resource Optimization

**Participants:**
- **SN64 (Chutes):** Needs 200 GPU-hours for inference surge, max $1.80/hr, requires <40ms latency
- **SN27 (Nodexo):** Has 500 GPU-hours available, min $1.30/hr, EU and US regions
- **SN12 (ComputeHorde):** Running batch job using 150 GPU-hours, could defer 6 hours for compensation

**Traditional bilateral approach:**
- Chutes checks Nodexo pricing, accepts posted rate of $1.60/hr
- ComputeHorde unaware of the opportunity
- No optimization across the three parties
- Total value captured: suboptimal

**NASH settlement:**

1. **Intent submission:** All three subnets submit preference vectors
2. **Miners compute:** 180 miners attempt to find optimal three-way settlement
3. **Winning solution:**
   - Chutes gets 200 GPU-hours from Nodexo @ $1.52/hr (EU region, 35ms)
   - ComputeHorde defers batch job, receives $45 rebate from Nodexo
   - Nodexo fills 350 GPU-hours total (200 to Chutes + retained 150 from ComputeHorde deferral)
   - All parties better off than bilateral trades

4. **Scoring the winning miner:**
   - Quality: Solution on Pareto frontier → Q = 0.98
   - Complexity: Three-party trade, uncommon → PMU = 2.2x
   - Speed: Response in 41ms → No penalty
   - Reputation: 94% historical accuracy → TWF = 1.15x
   - **Final score:** 0.98 × 2.2 × 1.15 = **2.48**

5. **Comparison — simple two-party swap:**
   - Miner solving Chutes↔Nodexo direct trade
   - Q = 0.99 × PMU = 0.5x × TWF = 1.0x = **0.50**
   - Three-party solution earns 5x more

---

## Emission and Reward Logic

NASH uses dual emission pools to balance reliability with market discovery.

### Pool A: Stability Layer (40% of emissions)

Rewards consistent, long-term participants via **Time-Weighted Fidelity (TWF)**.

```python
TWF = rolling_average(accuracy, uptime, latency, last_1000_challenges)
```

| Factor | Weight | What It Measures |
|--------|--------|------------------|
| Accuracy | 50% | % of proposals on Pareto frontier |
| Uptime | 20% | % of challenges responded to |
| Latency | 30% | Response time vs. 50ms threshold |

**Why it matters:** Subnet operators need reliability. TWF ensures that high-volume settlement flows through battle-tested miners, not newcomers with no track record.

### Pool B: Discovery Layer (60% of emissions)

Rewards solving hard problems via **Proof of Marginal Utility (PMU)**.

```python
PMU = base_reward × (1 / sqrt(solver_count)) × complexity_multiplier
```

| Trade Type | Typical Solver Count | PMU Multiplier |
|------------|---------------------|----------------|
| Simple two-party swap | 150+ miners | 0.3x - 0.5x |
| Two-party with constraints | 50-100 miners | 0.7x - 1.0x |
| Three-party optimization | 10-30 miners | 1.5x - 2.5x |
| Multi-subnet resource triangle | 3-10 miners | 3.0x - 4.0x |

**Why it matters:** Without PMU, miners would only solve easy trades. PMU pushes the network to handle complex inter-subnet workflows that create the most value.

---

## The Scoring Formula

```
S = Q × PMU × TWF

Where:
  Q   = Quality (0.0 - 1.0) — accuracy of equilibrium proposal
  PMU = Proof of Marginal Utility (0.1 - 5.0) — difficulty multiplier
  TWF = Time-Weighted Fidelity (0.5 - 1.5) — reputation multiplier
```

### Quality Score (Q)

Measures proposal accuracy against the true Pareto frontier.

| Result | Q Score |
|--------|---------|
| On Pareto frontier (optimal) | 1.0 |
| Within 0.1% of optimal | 0.95 |
| Within 1% of optimal | 0.80 |
| Dominated by another solution | 0.0 |

Validators run baseline simulations. If any miner finds a better solution, inferior proposals score zero.

### PMU Calculation

Per-challenge, based on:

1. **Solver density:** Fewer solvers = higher PMU
2. **Party count:** More parties = higher complexity multiplier
3. **Constraint count:** More constraints = harder optimization

```python
def calculate_pmu(challenge, valid_solutions):
    solver_count = len(valid_solutions)
    complexity = challenge.party_count * log2(challenge.constraint_count + 1)
    
    base_pmu = 1.0 / sqrt(solver_count)
    return base_pmu * complexity
```

### TWF Calculation

Rolling reputation over last 1,000 challenges:

| Performance Tier | TWF Range |
|------------------|-----------|
| Elite (top 10%, <30ms avg) | 1.3x - 1.5x |
| Strong (top 30%) | 1.1x - 1.3x |
| Average | 0.9x - 1.1x |
| Below average | 0.6x - 0.9x |
| New miner | 0.7x (starting point) |

TWF creates stickiness — established miners have an edge, but not an insurmountable one.

---

## Incentive Alignment

### For Miners

Optimal strategy:
1. **Target complex trades:** Multi-party, multi-constraint = high PMU
2. **Maintain accuracy:** Quality score multiplies everything
3. **Build reputation:** TWF compounds over time
4. **Optimize infrastructure:** Latency affects TWF decay

The equilibrium: Miners specialize in different complexity tiers based on their capabilities.

### For Validators

Optimal strategy:
1. **Accurate verification:** V-Trust determines dividend share
2. **Consensus alignment:** Outlier scores get penalized
3. **Challenge diversity:** Novel challenge types = new PMU opportunities
4. **Fast baseline simulation:** Required to judge 50ms window accurately

### For Subnet Operators

NASH aligns subnet interests by:
- Finding better deals than they'd find bilaterally
- Enabling multi-party optimizations they couldn't coordinate manually
- Providing settlement guarantees via Pareto verification

---

## Anti-Gaming Mechanisms

### Fidelity Slash

**Attack:** Submit random proposals hoping for lucky matches.

**Defense:** Failed proposals trigger non-linear TWF decay.

```python
if proposal.quality < 0.5:
    miner.TWF *= 0.7  # 30% immediate decay
    miner.recovery_period = 500  # challenges to recover
```

One bad week can take a month to recover from.

### Anti-Sybil PMU Collapse

**Attack:** Run multiple miners to capture PMU on same challenge.

**Defense:** Identical solutions from different UIDs collapse PMU for all.

```python
if solutions_match(uid_a, uid_b):
    challenge.pmu = 0.1  # Minimum for everyone
```

Sybil attacks become unprofitable.

### Saturation Cap

**Attack:** High-performance miners farm only easy trades.

**Defense:** Low-complexity trades have emission ceiling.

```python
if solver_count > 100 and complexity < 2.0:
    effective_pmu = min(0.2, calculated_pmu)
```

Easy trades hit diminishing returns quickly.

### Salted Challenges

**Attack:** Pre-compute solutions for common trade patterns.

**Defense:** Validators issue challenges with known solutions at random intervals. Pre-computed responses are detectable.

---

## Proof of Intelligence

Finding Nash Equilibria is computationally non-trivial:

| Problem Class | Complexity | NASH Application |
|---------------|------------|------------------|
| Two-player zero-sum | Polynomial | Simple swaps (low PMU) |
| Multi-player general-sum | PPAD-complete | Multi-subnet trades (high PMU) |
| Continuous preferences | NP-hard | Real resource constraints |

**Why this qualifies as intelligence:**
- Brute-force fails for complex trades
- Requires game-theoretic reasoning
- Heuristic development differentiates miners
- Real-world constraints add dimensionality

---

## Algorithm Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│  1. CHALLENGE        Validator generates trade scenario         │
│     GENERATION       Subnet intents + constraints + seed        │
├─────────────────────────────────────────────────────────────────┤
│  2. BROADCAST        Challenge to top 256 miners                │
│                      200ms response window                      │
├─────────────────────────────────────────────────────────────────┤
│  3. DISCOVERY        Miners compute equilibrium proposals       │
│                      Submit: solution + hash + proof            │
├─────────────────────────────────────────────────────────────────┤
│  4. PARETO           Validator simulates baseline               │
│     AUDIT            Compares all proposals to frontier         │
│                      Dominated solutions → Q = 0                │
├─────────────────────────────────────────────────────────────────┤
│  5. SCORING          S = Q × PMU × TWF per valid submission     │
│                      Normalize across epoch                     │
├─────────────────────────────────────────────────────────────────┤
│  6. SETTLEMENT       Weights committed to Subtensor             │
│                      Yuma Consensus distributes emissions       │
└─────────────────────────────────────────────────────────────────┘
```

**Timing:**
- Challenge frequency: Every block (~12 seconds)
- Response window: 200ms
- Epoch settlement: 360 blocks (~1 hour)

---
