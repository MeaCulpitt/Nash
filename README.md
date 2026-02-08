# NASH: Inter-Subnet Settlement Layer

NASH is a Bittensor subnet that optimizes resource exchange between subnets. When compute needs to be bought, inference jobs need to be routed, or resources need to be swapped, NASH finds the mathematically optimal deal and settles it in milliseconds.

Today: the settlement layer for Bittensor's internal economy.
Tomorrow: the settlement layer for autonomous agents everywhere.

---

## The Problem

Bittensor subnets increasingly need to trade with each other:

- **SN64 (Chutes)** runs inference jobs but needs to source GPU capacity
- **SN27 (Compute)** has GPU capacity but needs customers
- **SN12 (ComputeHorde)** has batch compute but needs to price it dynamically
- Validators stake across subnets and need to rebalance positions

Right now, these trades happen through:
- Manual coordination (slow, doesn't scale)
- Fixed pricing (leaves value on the table)
- Simple order books (can't handle complex multi-party swaps)

**The result:** Billions in potential trade value trapped by friction. Subnets that should be collaborating are siloed.

---

## What NASH Does

NASH finds the optimal trade between parties with competing interests.

```
┌─────────────────────────────────────────────────────────────────┐
│                        NASH SETTLEMENT                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   SN64 (Chutes)              NASH               SN27 (Compute)  │
│   "Need 100 GPU-hrs"   ──▶  Optimal   ◀──   "Have 500 GPU-hrs"  │
│   "Max $1.80/hr"            Match            "Min $1.40/hr"     │
│   "Need <50ms latency"                       "Located in EU"    │
│                                                                  │
│                         Settlement:                              │
│                         150 GPU-hrs @ $1.62/hr                  │
│                         47ms round-trip                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**The math:** NASH finds the Nash Equilibrium — the point where neither party can get a better deal without making the other worse off. This isn't "good enough" matching. It's provably optimal.

---

## Worked Example: Cross-Subnet Compute Trade

### Scenario

**SN64 (Chutes)** has a surge in inference requests. Needs GPU capacity now.

**SN27 (Compute)** has idle GPUs in three regions. Wants to maximize utilization.

**SN12 (ComputeHorde)** has batch jobs that could be delayed if the price is right.

### Traditional Approach

1. Chutes operator manually checks Compute pricing — $1.50/hr posted
2. Accepts or rejects based on fixed price
3. No visibility into ComputeHorde's flexibility
4. Three-way optimization never happens

**Time:** Minutes. **Outcome:** Suboptimal.

### NASH Approach

1. **Intent submission (automated):**
   - Chutes: "Need 200 GPU-hrs, priority high, max $2.00, prefer <30ms"
   - Compute: "Have 300 GPU-hrs available, min $1.20, flexible timing"
   - ComputeHorde: "Running batch job, can defer 4 hours for $0.30/hr rebate"

2. **NASH miners compute optimal settlement:**
   - Chutes gets 200 GPU-hrs from Compute @ $1.55/hr
   - ComputeHorde defers batch job, receives $60 rebate
   - Compute fills otherwise-idle capacity
   - All parties better off than bilateral negotiation

3. **Validators verify:** Settlement is on the Pareto frontier. No party can improve without hurting another.

4. **Execution:** Trade settles in 43ms. Resources allocated.

**Time:** <50ms. **Outcome:** Mathematically optimal.

---

## Why This Matters for Bittensor

### Today: Internal Liquidity

Bittensor is becoming an economy, not just a network. Subnets are:
- Buying compute from each other
- Routing jobs based on capacity and pricing
- Staking and rebalancing across the metagraph

This happens inefficiently today. NASH makes it efficient.

### Tomorrow: External Liquidity

Once NASH proves itself on Bittensor-native trades, it becomes the natural settlement layer for:
- AI agents trading resources
- Autonomous systems negotiating contracts
- Any multi-party optimization problem

The "agentic economy" is coming. NASH will be ready because it's battle-tested on real volume.

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                      THE NASH PIPELINE                           │
├─────────────────────────────────────────────────────────────────┤
│  1. INTENT          Subnets/agents submit preferences           │
│                     Price range, quantity, constraints          │
├─────────────────────────────────────────────────────────────────┤
│  2. DISCOVERY       Miners compete to find optimal settlement   │
│                     Game-theoretic search, <50ms                │
├─────────────────────────────────────────────────────────────────┤
│  3. VERIFICATION    Validators confirm Pareto optimality        │
│                     No better deal exists                       │
├─────────────────────────────────────────────────────────────────┤
│  4. SETTLEMENT      Trade executes automatically                │
│                     Trustless, mathematically verified          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Features

### Multi-Party Optimization

Two-party trades are easy. NASH shines when three or more parties have interlocking needs — compute swaps, resource triangles, portfolio rebalancing.

### Sub-50ms Settlement

Fast enough for real-time resource allocation. Validators and subnet orchestrators can use NASH in their critical path.

### Proof of Optimality

Every settlement is verified against the Pareto frontier. If a better deal exists, the proposal is rejected. No "good enough" — only optimal.

### Complexity Rewards

Miners earn more for solving harder problems (Proof of Marginal Utility). The network naturally spreads to cover edge cases, not just high-volume commodity trades.

---

## Documentation

| Document | Description |
|----------|-------------|
| [Incentive & Mechanism Design](./docs/incentive_mechanism.md) | Scoring formula, PMU/TWF multipliers, anti-gaming |
| [Miner Architecture](./docs/miner.md) | Equilibrium discovery, input/output spec |
| [Validator Architecture](./docs/validator.md) | Pareto audits, verification methodology |
| [Business Logic](./docs/business_logic.md) | Problem statement, competitive landscape |
| [Go-To-Market](./docs/gtm.md) | Subnet partnerships, adoption path |

---

## Initial Integration Targets

| Subnet | Use Case | Status |
|--------|----------|--------|
| SN64 (Chutes) | Inference job routing and pricing | Target |
| SN27 (Nodexo) | GPU capacity allocation | Target |
| SN12 (Compute Horde) | Batch job scheduling | Target |
| SN62 (Ridges) | Task routing and settlement | Target |
| Cross-validator | Stake rebalancing | Future |

---

## For Subnet Owners

Integrate NASH to:
- Optimize resource acquisition costs
- Access network-wide liquidity
- Automate bilateral agreements
- Enable complex multi-subnet workflows

**NASH SDK** (Python) for Synapse integration coming soon.

---

## For Miners

Earn TAO by:
1. Ingesting subnet intent vectors
2. Computing optimal settlements
3. Submitting verified proposals
4. Maintaining <50ms response times

Higher rewards for complex, multi-party trades.

---

## For Validators

Earn dividends by:
1. Generating economic challenges
2. Verifying Pareto optimality
3. Maintaining consensus accuracy
4. Running anti-gaming audits

---

## The Vision

**Phase 1:** Inter-subnet settlement for Bittensor (the internal economy)

**Phase 2:** Settlement layer for Bittensor-adjacent AI infrastructure (compute markets, inference routing)

**Phase 3:** General-purpose agent-to-agent settlement (the agentic economy)

NASH starts with real trades, real volume, and real utility. The agentic future is built on that foundation.

---

## License

MIT

---
