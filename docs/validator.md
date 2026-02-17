# Validator Design

## What Validators Do

Validators are the **orchestrators** of the NASH network. They don't find equilibria — they **verify** that miners did, and ensure the incentive mechanism runs fairly.

### The Core Task

```
INPUT:  Miner settlement proposals
        (from multiple miners)

OUTPUT: Weighted scores for each miner
        (submitted to blockchain)
```

Validators run the incentive mechanism — generating challenges, scoring responses, and maintaining network integrity.

---

## Validator Tasks

### 1. Intent Collection
- Receive intents from subnets via API/SDK
- Aggregate preferences into challenges
- Format for miner consumption

### 2. Challenge Generation
- Create synthetic economic challenges (before real subnets join)
- Mix synthetic + real intents
- Ensure challenge diversity

### 3. Miner Querying
- Broadcast challenges to all active miners
- Collect responses within time window
- Handle timeouts gracefully

### 4. Response Validation
- Check for NaN/Inf values
- Verify valid shapes
- Detect suspicious patterns (pre-computed, etc.)

### 5. Quality Scoring
- Run baseline simulations
- Compare miner solutions to ground truth
- Calculate fidelity scores

### 6. Consensus & Weight Setting
- Aggregate scores across validators (stake-weighted)
- Submit final weights to blockchain

---

## The Validator Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    VALIDATOR PIPELINE                            │
├─────────────────────────────────────────────────────────────────┤
│  1. INTENT        Collect intents from subnets                │
│     COLLECTION     Aggregate into challenges                    │
├─────────────────────────────────────────────────────────────────┤
│  2. CHALLENGE     Generate synthetic challenges               │
│     GENERATION     Mix real + synthetic intents                │
│                   Ensure diversity                              │
├─────────────────────────────────────────────────────────────────┤
│  3. QUERY         Broadcast to all active miners              │
│                   Collect responses                            │
│                   Handle timeouts                              │
├─────────────────────────────────────────────────────────────────┤
│  4. VALIDATION    Check for NaN/Inf                           │
│                   Verify shapes                                 │
│                   Detect suspicious patterns                   │
├─────────────────────────────────────────────────────────────────┤
│  5. SCORING       Run baseline simulations                    │
│                   Compare to ground truth                      │
│                   Calculate fidelity scores                    │
├─────────────────────────────────────────────────────────────────┤
│  6. CONSENSUS     Aggregate (stake-weighted)                  │
│                   Set weights on blockchain                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Scoring and Evaluation Methodology

### Step 1: Generate Challenge
Validator creates a challenge representing a potential settlement scenario.

```json
{
  "challenge_id": "0xabc123",
  "parties": [...],
  "expected_optimal": {...},  // Known for synthetic challenges
  "difficulty": "medium"
}
```

### Step 2: Query Miners
Broadcast to all active miner axons, collect responses within 5-second window.

### Step 3: Validate Responses
```python
def validate_response(response):
    if response.manifold is None:
        return False
    if torch.isnan(response.manifold).any():
        return False
    if torch.isinf(response.manifold).any():
        return False
    if response.equilibrium.numel() != 2:
        return False
    return True
```

### Step 4: Calculate Fidelity
Run baseline simulation to determine ground truth, compare miner solutions.

```python
def calculate_fidelity(miner_solution, ground_truth):
    mse = ((miner_solution - ground_truth) ** 2).mean()
    fidelity = 1.0 - mse  # Higher is better
    return fidelity
```

### Step 5: Compute Consensus
Stake-weighted average across all validators.

```python
def weighted_consensus(miner_scores, validators):
    weighted_scores = []
    for v in validators:
        weight = v.stake * v.v_trust
        for miner, score in v.scores.items():
            weighted_scores.append((miner, score * weight))
    
    # Aggregate by miner
    final = {}
    for miner, weighted in weighted_scores:
        if miner not in final:
            final[miner] = []
        final[miner].append(weighted)
    
    return {m: sum(s)/len(s) for m, s in final.items()}
```

### Step 6: Set Weights
Submit to blockchain.

---

## V-Trust (Validator Reputation)

Validators have their own reputation system:

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

| Factor | Weight | Description |
|--------|--------|-------------|
| Consensus Accuracy | 40% | How often validator agrees with majority |
| Speed | 30% | Verification time vs. threshold |
| Diversity | 30% | Novel challenge types introduced |

### Why V-Trust Matters

- **Higher dividends** — Quadratic bonus for proven validators
- **More voting power** — Stake × V-Trust in consensus
- **Network quality** — Rewards accurate, fast, diverse verification

---

## Validator Dividends

Validators earn from network emissions:

```python
def calculate_validator_dividends(validator):
    base = validator.stake / total_network_stake
    trust_bonus = validator.v_trust ** 2      # Quadratic!
    diversity_bonus = 1.0 + (validator.unique_challenges / 10)
    return base * trust_bonus * diversity_bonus
```

---

## Evaluation Cadence

| Metric | Value |
|--------|-------|
| Challenge frequency | Every 10 seconds |
| Response window | 5 seconds |
| Weight updates | Every 100 blocks (~20 min) |
| Consensus calculation | Real-time aggregation |

---

## Validator Incentive Alignment

Optimal validator strategy:

1. **Accurate verification** — V-Trust determines dividend share
2. **Consensus alignment** — Outlier scores penalized
3. **Challenge diversity** — Novel challenge types = new PMU opportunities + V-Trust boost
4. **Fast baseline simulation** — Required to judge within time window
5. **Stake up** — Higher stake = more voting power in consensus

---

## Requirements for Validators

| Requirement | Value |
|-------------|-------|
| Minimum stake | 1000 τ (including delegated) |
| Permit | Must be in top 64 by emissions |
| Hardware | Standard Bittensor validator specs |

---
