# NASH: Agent-to-Agent Settlement Layer

NASH is a Bittensor subnet that finds optimal trade agreements between AI agents. When autonomous systems need to exchange value — compute for tokens, services for payment, resources for resources — NASH calculates the mathematically optimal deal and settles it in milliseconds.

---

## The Problem

AI agents are becoming economic actors. They buy compute, sell services, and trade resources. But when two agents with competing interests need to make a deal, they face a problem: **how do you negotiate without a human in the loop?**

Current approaches fail:

| Approach | Problem |
|----------|---------|
| Chat-based negotiation | Too slow (seconds to minutes) |
| Fixed pricing | Leaves value on the table |
| Centralized matching | Single point of failure, high fees |
| Pairwise P2P | No liquidity, local optima |

Agents need a way to find the best possible deal — the point where neither party can improve without making the other worse off. In game theory, this is called the **Nash Equilibrium**.

---

## How NASH Works

```
┌─────────────────────────────────────────────────────────────────┐
│                     THE NASH PIPELINE                            │
├─────────────────────────────────────────────────────────────────┤
│  1. INTENT          Agent submits what it wants                 │
│                     (price, quantity, constraints, preferences) │
├─────────────────────────────────────────────────────────────────┤
│  2. DISCOVERY       Miners compute the optimal agreement        │
│                     Game-theoretic search across all options    │
├─────────────────────────────────────────────────────────────────┤
│  3. VERIFICATION    Validators confirm optimality               │
│                     No better deal exists for either party      │
├─────────────────────────────────────────────────────────────────┤
│  4. SETTLEMENT      Trade executes at equilibrium point         │
│                     Sub-50ms end-to-end                         │
└─────────────────────────────────────────────────────────────────┘
```

**Miners** compete to find the optimal trade agreement fastest.
**Validators** verify that proposed agreements are actually optimal.
**Agents** get mathematically fair deals without negotiation overhead.

---

## Worked Example: Compute-for-Inference Swap

**Scenario:** Two AI agents need to trade.

- **Agent A** (inference provider): Has GPU capacity, wants TAO
- **Agent B** (training pipeline): Has TAO, wants GPU time

**Traditional approach:** Agent A quotes $2/hour. Agent B counters $1.50. Back and forth. Takes 30 seconds. Neither knows if they got the best deal.

**NASH approach:**

1. Agent A submits intent: "Sell 100 GPU-hours, min price $1.20, prefer bulk, available now"
2. Agent B submits intent: "Buy 50-200 GPU-hours, max price $2.00, need within 1 hour, flexible on quantity"
3. NASH miners analyze both intents and compute the equilibrium:
   - Optimal quantity: 150 GPU-hours
   - Optimal price: $1.65/hour
   - Neither party can get a better deal without hurting the other
4. Validators verify the math checks out
5. Trade settles in 47ms

**Result:** Both agents got the mathematically optimal deal. No negotiation. No information asymmetry. No wasted time.

---

## Key Concepts

### Nash Equilibrium

A state where no participant can improve their outcome by changing their strategy alone. NASH finds this point for multi-party economic trades.

### Intent Vectors

Agents express preferences as high-dimensional vectors:
- Price range (min/max)
- Quantity flexibility
- Time constraints
- Quality requirements
- Risk tolerance

More dimensions = more precise matching.

### Proof of Economic Fidelity (PoEF)

Miners prove they found the genuine optimum, not just a "good enough" solution. Validators check proposals against the Pareto frontier — if a better deal exists, the proposal is rejected.

---

## Documentation

| Document | Description |
|----------|-------------|
| [Incentive & Mechanism Design](./docs/incentive_mechanism.md) | Scoring formula, reward pools, anti-gaming mechanisms |
| [Miner Architecture](./docs/miner.md) | Equilibrium discovery, input/output spec, performance dimensions |
| [Validator Architecture](./docs/validator.md) | Pareto audits, PMU weighting, evaluation cadence |
| [Business Logic & Market Rationale](./docs/business_logic.md) | Problem statement, competitive landscape, sustainability |
| [Go-To-Market Strategy](./docs/gtm.md) | Target users, growth channels, early incentives |

---

## Why Bittensor?

Finding Nash Equilibria in real-time requires:

1. **Parallel competition:** 256+ miners racing to find the optimal solution
2. **Economic alignment:** Miners earn more for harder problems (Proof of Marginal Utility)
3. **Trustless verification:** Validators ensure mathematical correctness
4. **Decentralized neutrality:** No party controls the matching engine

Bittensor provides all of this out of the box.

---

## Target Use Cases

### Within Bittensor

| Subnet | Use Case |
|--------|----------|
| SN64 (Chutes) | Inference job bidding and settlement |
| SN27 (Compute) | GPU resource allocation |
| SN62 (Ridges) | Micro-task routing and payment |

### Beyond Bittensor

| Market | Use Case |
|--------|----------|
| Autonomous trading | Multi-asset portfolio rebalancing |
| Supply chain | Multi-party logistics optimization |
| Energy markets | Grid resource allocation |

---

## For Miners

Earn TAO by:
1. Ingesting agent intent vectors
2. Computing optimal trade agreements
3. Submitting equilibrium proposals with proofs
4. Maintaining sub-50ms response times

Higher rewards for:
- **Complex trades:** Multi-party, multi-constraint problems (PMU multiplier)
- **Consistent accuracy:** Long-term track record (TWF multiplier)
- **Speed:** Faster than other miners

---

## For Validators

Earn dividends by:
1. Generating economic challenge pairs
2. Verifying proposals against Pareto frontier
3. Maintaining consensus with other validators
4. Running "salted challenges" to detect gaming

---

## For Agent Developers

Integrate NASH to:
- Settle trades in <50ms
- Get mathematically optimal deals
- Avoid negotiation logic in your agent
- Access network liquidity

**NASH SDK** (Python) coming soon.

---

## License

MIT

---
