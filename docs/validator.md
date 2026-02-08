# NASH: Validator Architecture & Audit Logic

NASH validators ensure that miner proposals are genuinely optimal — not just feasible, but the best possible settlement for all parties. They generate trade challenges, verify Pareto optimality, and maintain consensus on miner performance.

---

## What Validators Do

Validators serve three functions:

1. **Challenge generation:** Create realistic trade scenarios from subnet intents
2. **Optimality verification:** Confirm proposals are on the Pareto frontier
3. **Consensus maintenance:** Agree with other validators on miner rankings

A validator isn't checking if a trade *can* happen — they're checking if it's the *best* trade possible.

---

## Worked Example: Verifying a Three-Party Settlement

### Challenge Issued

Validator generates challenge from real or synthetic subnet intents:

```json
{
  "challenge_id": "0x7a3f...",
  "parties": [
    {"id": "sn64_chutes", "intent": "buy", "resource": "gpu_hours", ...},
    {"id": "sn27_nodexo", "intent": "sell", "resource": "gpu_hours", ...},
    {"id": "sn12_compute_horde", "intent": "defer", "resource": "gpu_hours", ...}
  ]
}
```

### Proposals Received

Within 200ms window, validator receives 47 proposals from miners.

### Verification Process

**Step 1: Constraint Check**

For each proposal, verify all hard constraints are satisfied:
- Chutes: latency < 50ms? ✓
- Nodexo: price >= $1.30? ✓
- Compute Horde: defer <= 8 hours? ✓

Proposals violating constraints → disqualified.

**Step 2: Pareto Frontier Analysis**

Validator runs baseline simulation to construct the true Pareto frontier.

```python
def is_pareto_optimal(proposal, all_proposals):
    for other in all_proposals:
        if dominates(other, proposal):
            # Other proposal is strictly better for at least one party
            # and no worse for any party
            return False
    return True
```

Results:
- 31 proposals: Pareto dominated (another proposal is strictly better)
- 12 proposals: On the Pareto frontier
- 4 proposals: Constraint violations

**Step 3: Nash Stability Check**

For frontier proposals, verify Nash stability — no party has incentive to deviate.

```python
def is_nash_stable(proposal):
    for party in proposal.parties:
        # If this party could do better by changing their action
        # (given other parties stay fixed), it's not stable
        if has_profitable_deviation(party, proposal):
            return False
    return True
```

Results:
- 8 proposals: Nash stable
- 4 proposals: On frontier but not stable (party could deviate profitably)

**Step 4: Scoring**

| Miner | Constraint | Pareto | Nash | Q Score |
|-------|------------|--------|------|---------|
| Miner A | ✓ | ✓ | ✓ | 1.0 |
| Miner B | ✓ | ✓ | ✓ | 1.0 |
| Miner C | ✓ | ✓ | ✗ | 0.85 |
| Miner D | ✓ | ✗ | — | 0.0 |
| Miner E | ✗ | — | — | 0.0 |

**Step 5: PMU and TWF Application**

For miners with Q > 0:
```
Final Score = Q × PMU × TWF
```

- Miner A: 1.0 × 2.2 × 1.15 = **2.53**
- Miner B: 1.0 × 2.2 × 0.95 = **2.09**
- Miner C: 0.85 × 2.2 × 1.10 = **2.06**

---

## The Verification Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                    VERIFICATION STACK                            │
├─────────────────────────────────────────────────────────────────┤
│  Layer 1: CONSTRAINT VALIDATION                                  │
│           All hard constraints satisfied?                        │
│           Immediate disqualification if not                      │
├─────────────────────────────────────────────────────────────────┤
│  Layer 2: PARETO ANALYSIS                                        │
│           Is proposal on the efficiency frontier?                │
│           Dominated proposals score zero                         │
├─────────────────────────────────────────────────────────────────┤
│  Layer 3: NASH STABILITY                                         │
│           Does any party have incentive to deviate?              │
│           Unstable proposals receive penalty                     │
├─────────────────────────────────────────────────────────────────┤
│  Layer 4: PMU WEIGHTING                                          │
│           How difficult was this challenge?                      │
│           How many miners solved it?                             │
├─────────────────────────────────────────────────────────────────┤
│  Layer 5: TWF APPLICATION                                        │
│           Miner's historical accuracy and latency                │
│           Reputation multiplier                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Pareto Frontier Verification

The core validator task: determining if a proposal is truly optimal.

### What is Pareto Optimality?

A settlement is Pareto optimal if you cannot make any party better off without making another party worse off.

```
Proposal A: Chutes pays $1.52/hr, Nodexo earns $304
Proposal B: Chutes pays $1.48/hr, Nodexo earns $296

B is better for Chutes, worse for Nodexo.
Neither dominates the other — both could be on the frontier.

Proposal C: Chutes pays $1.55/hr, Nodexo earns $290

C is worse for both parties compared to A.
A dominates C. C is not Pareto optimal.
```

### Baseline Simulation

Validators run their own equilibrium search to establish ground truth:

1. Parse the same intent vectors miners receive
2. Run local optimization algorithm
3. Construct the Pareto frontier
4. Compare miner proposals against frontier

This requires validators to have competitive solving capability — not as fast as miners, but accurate enough to verify.

### Dominance Testing

For each proposal, check against all other proposals:

```python
def dominates(a, b):
    """Does proposal A dominate proposal B?"""
    dominated = False
    for party in parties:
        utility_a = calculate_utility(party, a)
        utility_b = calculate_utility(party, b)
        
        if utility_a < utility_b:
            return False  # B is better for this party
        if utility_a > utility_b:
            dominated = True  # A is better for at least one party
    
    return dominated  # A is at least as good for all, better for one
```

---

## PMU Weighting

Validators calculate the Proof of Marginal Utility multiplier per challenge.

### Factors

| Factor | Impact |
|--------|--------|
| Party count | More parties = higher complexity |
| Constraint count | More constraints = harder optimization |
| Solver count | Fewer solvers = higher individual reward |
| Novelty | Unseen trade patterns = bonus |

### Calculation

```python
def calculate_pmu(challenge, valid_solutions):
    # Base complexity from problem structure
    party_factor = challenge.party_count ** 1.5
    constraint_factor = log2(challenge.constraint_count + 1)
    complexity = party_factor * constraint_factor
    
    # Dilution from competition
    solver_count = len(valid_solutions)
    dilution = 1.0 / sqrt(solver_count)
    
    # Novelty bonus for rare trade types
    novelty = 1.5 if is_novel(challenge.type) else 1.0
    
    return complexity * dilution * novelty
```

### Typical PMU Values

| Challenge Type | Solvers | PMU |
|----------------|---------|-----|
| Two-party token swap | 150 | 0.3x |
| Two-party with 5 constraints | 80 | 0.7x |
| Three-party resource trade | 25 | 2.0x |
| Four-party with timing constraints | 8 | 3.5x |

---

## TWF Tracking

Validators maintain a Time-Weighted Fidelity score for each miner UID.

### Rolling Average

```python
def update_twf(miner, challenge_result):
    # Decay factor for older results
    decay = 0.995  # Per challenge
    
    # Update accuracy component
    miner.accuracy_sum = miner.accuracy_sum * decay + challenge_result.quality
    miner.accuracy_count = miner.accuracy_count * decay + 1
    
    # Update latency component
    miner.latency_sum = miner.latency_sum * decay + challenge_result.response_time
    miner.latency_count = miner.latency_count * decay + 1
    
    # Calculate TWF
    avg_accuracy = miner.accuracy_sum / miner.accuracy_count
    avg_latency = miner.latency_sum / miner.latency_count
    
    miner.TWF = (avg_accuracy * 0.7) + (latency_score(avg_latency) * 0.3)
```

### TWF Impact

| TWF Score | Interpretation | Multiplier |
|-----------|----------------|------------|
| 0.95+ | Elite performer | 1.4x - 1.5x |
| 0.85 - 0.95 | Strong | 1.1x - 1.4x |
| 0.70 - 0.85 | Average | 0.9x - 1.1x |
| 0.50 - 0.70 | Below average | 0.6x - 0.9x |
| < 0.50 | Poor / new | 0.5x - 0.7x |

---

## Evaluation Cadence

### Per-Challenge (Real-Time)

- Challenge broadcast: Every block (~12 seconds)
- Response window: 200ms
- Immediate verification: Constraint + Pareto check
- Score calculation: Q × PMU × TWF

### Per-Epoch (Hourly)

- Aggregate scores across all challenges
- Normalize across miner population
- Commit weight matrix to Subtensor
- Yuma Consensus determines final emissions

### Periodic Audits

- **Salted challenges:** Known solutions to detect pre-computation
- **Replay challenges:** Identical problems to check consistency
- **Cross-validator comparison:** Detect scoring anomalies

---

## Validator Incentive Alignment

### V-Trust and Dividends

Validators earn based on consensus alignment:

```python
def validator_dividend(validator, epoch_scores):
    # How close is this validator's scoring to the consensus?
    consensus = stake_weighted_median(all_validator_scores)
    deviation = mean_absolute_error(validator.scores, consensus)
    
    # Higher deviation = lower trust = lower dividends
    v_trust = 1.0 - (deviation * penalty_factor)
    
    return base_dividend * v_trust
```

Validators who score miners differently from consensus see reduced earnings.

### Infrastructure Requirements

To verify effectively, validators need:
- Fast enough compute to run baseline simulations
- Low-latency connections to measure miner response times
- Sufficient stake to influence consensus

### Anti-Collusion

Collusion is detectable because:

1. **Pareto verification is deterministic:** A dominated solution is mathematically dominated — no room for subjective scoring
2. **Cross-validator checks:** Outlier scoring patterns are flagged
3. **Stake economics:** Colluding validators lose dividends when they deviate from honest validators

---

## Challenge Generation

Validators generate challenges from:

### Real Subnet Intents

When integrated with partner subnets (SN64, SN27, etc.), validators can pull actual pending trade requests:

```python
def generate_real_challenge():
    intents = fetch_pending_intents([SN64, SN27, SN12])
    if len(intents) >= 2:
        return package_as_challenge(intents)
    else:
        return generate_synthetic_challenge()
```

### Synthetic Challenges

For training and benchmarking, validators generate realistic synthetic scenarios:

```python
def generate_synthetic_challenge():
    party_count = weighted_random([2, 3, 4], [0.6, 0.3, 0.1])
    parties = [generate_random_intent() for _ in range(party_count)]
    constraints = generate_realistic_constraints(parties)
    
    return Challenge(parties, constraints)
```

Synthetic challenges ensure miners are tested on edge cases that may not appear in real traffic.

---

## Validator Infrastructure

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| CPU | 16-core, 3.5GHz+ |
| RAM | 64GB |
| Network | 1Gbps, low latency |
| Storage | 500GB SSD |

### Recommended

| Component | Recommendation |
|-----------|----------------|
| CPU | 32-core, 4.0GHz+ |
| RAM | 128GB |
| Network | 10Gbps, <5ms to major nodes |

### Why Higher Specs Than Miners?

Validators must:
- Run baseline simulations for every challenge
- Verify all miner proposals (potentially 256)
- Maintain TWF state for all miners
- Process in real-time without becoming a bottleneck

---
