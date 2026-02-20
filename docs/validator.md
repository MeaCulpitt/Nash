# Validator Design

## Overview

Validators are the **orchestrators** of the NASH network. They don't find equilibria — they **verify** that miners did, and ensure the incentive mechanism runs fairly.

The key innovation: Validators cannot verify optimality with incomplete information. Instead, they **learn to estimate** optimality via a model trained on synthetic data, then improve via post-settlement feedback.

---

## 1. Validator Tasks

### Core Responsibilities

1. **Intent Collection**
   - Receive intents from agents via API/SDK
   - Aggregate preferences into challenges
   - Format for miner consumption

2. **Challenge Generation**
   - Create synthetic economic challenges (before real agents join)
   - Mix synthetic + real intents
   - Ensure challenge diversity

3. **Miner Querying**
   - Broadcast challenges to all active miners
   - Collect responses within time window
   - Handle timeouts gracefully

4. **Response Validation**
   - Check for NaN/Inf values
   - Verify valid shapes
   - Detect suspicious patterns (pre-computed, etc.)

5. **Quality Scoring**
   - Run baseline simulations (training phase)
   - Compare miner solutions to model estimates (production)
   - Calculate fidelity scores

6. **Consensus & Weight Setting**
   - Aggregate scores across validators (stake-weighted)
   - Submit final weights to blockchain

7. **Post-Settlement Verification**
   - Collect agent feedback after settlement
   - Compare estimates to revealed outcomes
   - Update model based on ground truth

---

## 2. Scoring and Evaluation Methodology

### The Core Challenge

Validators see only **commitments**, not full preferences. They cannot compute the true optimal.

**Solution:** Train a model to estimate optimality, then improve via feedback.

### Step 1: Training Phase (Synthetic Challenges)

```python
def validate_training(settlement, commitments, full_preferences):
    # Validator knows the answer
    true_optimal = solve_with_full_info(full_preferences)
    distance = compute_distance(settlement, true_optimal)
    
    # Train model: commitment → optimal
    model.train(commitments, true_optimal)
    
    return distance < threshold
```

### Step 2: Production Phase (Real Challenges)

```python
def validate_production(settlement, commitments):
    # Use trained model to estimate optimality
    estimated_optimal = model.predict(commitments)
    
    # Compare miner solution to estimate
    distance = compute_distance(settlement, estimated_optimal)
    
    return distance < threshold
```

### Step 3: Post-Settlement Feedback

```python
def verify_post_settlement(settlement, revealed_outcomes):
    # Agents reveal actual results
    for agent, revealed in revealed_outcomes.items():
        accuracy = compute_accuracy(validator.estimate[agent], revealed)
        validator.update_model(accuracy)
```

---

## 3. Validator Emissions

Validators earn from network emissions based on their **stake only**:

```python
def calculate_validator_dividends(validator):
    # Emissions determined by stake (Bittensor consensus)
    base = validator.stake / total_network_stake
    return base
```

Note: Validator emissions are fixed by Bittensor consensus. No additional bonuses or multipliers apply.

---

## 4. Evaluation Cadence

| Metric | Value |
|--------|-------|
| Challenge frequency | Every 10 seconds |
| Response window | 5 seconds |
| Weight updates | Every 100 blocks (~20 min) |
| Consensus calculation | Real-time aggregation |
| Post-settlement feedback | After each settlement |

---

## 5. Validator Incentive Alignment

Optimal validator strategy:

1. **Train the model** — Generate synthetic challenges to build commitment model
2. **Collect feedback** — Learn from post-settlement reveals
3. **Stake up** — More stake = more emissions

---

## 6. Requirements for Validators

| Requirement | Value |
|-------------|-------|
| Minimum stake | 1000 τ (including delegated) |
| Permit | Must be in top 64 by emissions |
| Hardware | Standard Bittensor validator specs |
| Model training | Must train commitment model before production |

---

## 7. The Validator Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    VALIDATOR PIPELINE                            │
├─────────────────────────────────────────────────────────────────┤
│  1. INTENT        Collect intents from agents                 │
│     COLLECTION     Aggregate into challenges                    │
├─────────────────────────────────────────────────────────────────┤
│  2. CHALLENGE     Generate synthetic challenges               │
│     GENERATION     Mix real + synthetic intents                │
│                   Ensure diversity                             │
├─────────────────────────────────────────────────────────────────┤
│  3. QUERY         Broadcast to all active miners              │
│                   Collect responses                            │
│                   Handle timeouts                             │
├─────────────────────────────────────────────────────────────────┤
│  4. VALIDATION    Check for NaN/Inf                          │
│                   Verify shapes                                │
│                   Detect suspicious patterns                   │
├─────────────────────────────────────────────────────────────────┤
│  5. SCORING       Use model to estimate optimality           │
│                   Compare miner solutions to estimate          │
│                   Calculate fidelity scores                   │
├─────────────────────────────────────────────────────────────────┤
│  6. CONSENSUS     Aggregate (stake-weighted)                  │
│                   Set weights on blockchain                    │
├─────────────────────────────────────────────────────────────────┤
│  7. FEEDBACK      Collect post-settlement reveals             │
│                   Update model with ground truth               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. Key Innovation: Learnable Validation

### The Problem
- Validators see only commitments (compressed preferences)
- Cannot compute true optimal without full information
- Traditional verification fails

### The Solution
1. **Training:** Generate synthetic challenges where answer is known
2. **Learning:** Train model: commitments → optimal
3. **Production:** Use model to estimate optimality
4. **Feedback:** Improve model via post-settlement reveals

### The Kernel
> *"Can validators learn a model that estimates optimality from commitments, trained on cases where they knew the answer — and then improve that model every time a settlement reveals the truth?"*
