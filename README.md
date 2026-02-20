# NASH: Agent-to-Agent Settlement Layer

NASH is a Bittensor subnet that optimizes resource exchange between autonomous AI agents. When compute needs to be bought, inference jobs need to be routed, or resources need to be swapped, NASH finds the mathematically optimal deal and settles it in milliseconds.

Today: the settlement layer for AI agents within Bittensor.
Tomorrow: the settlement layer for autonomous agents everywhere.

---

## The Problem

The **agentic economy** is coming. Autonomous AI agents will need to trade resources with each other:

- **Inference Agents** run AI workloads but need GPU capacity
- **Compute Agents** have GPUs but need customers
- **Storage Agents** have space but need bandwidth
- **Coordination Agents** manage tasks but need execution capacity

Right now, these trades happen through:
- Manual coordination (slow, doesn't scale)
- Fixed pricing (leaves value on the table)
- Simple order books (can't handle complex multi-party swaps)

**The result:** Billions in potential trade value trapped by friction. Agents that should be collaborating are siloed.

---

## What NASH Does

NASH finds the optimal trade between parties with competing interests.

```
┌─────────────────────────────────────────────────────────────────┐
│                        NASH SETTLEMENT                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Inference Agent            NASH              Compute Agent     │
│   "Need 100 GPU-hrs"   ──▶  Optimal   ◀──   "Have 500 GPU-hrs" │
│   "Max $1.80/hr"            Match            "Min $1.40/hr"   │
│   "Need <50ms latency"                        "Located in EU"  │
│                                                                  │
│                         Settlement:                              │
│                         150 GPU-hrs @ $1.62/hr                  │
│                         47ms round-trip                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**The math:** NASH finds the Nash Equilibrium — the point where neither party can get a better deal without making the other worse off. This isn't "good enough" matching. It's provably optimal.

---

## Worked Example: Agent-to-Agent Compute Trade

### Scenario

**Inference Agent** has a surge in requests. Needs GPU capacity now.

**Compute Agent** has idle GPUs in three regions. Wants to maximize utilization.

**Storage Agent** has batch jobs that could be deferred if the price is right.

### Traditional Approach

1. Inference operator manually checks Compute pricing — $1.50/hr posted
2. Accepts or rejects based on fixed price
3. No visibility into Storage's flexibility
4. Three-way optimization never happens

**Time:** Minutes. **Outcome:** Suboptimal.

### NASH Approach

1. **Intent submission (automated):**
   - Inference: "Need 200 GPU-hrs, priority high, max $2.00, prefer <30ms"
   - Compute: "Have 300 GPU-hrs available, min $1.20, flexible timing"
   - Storage: "Running batch job, can defer 4 hours for $0.30/hr rebate"

2. **NASH miners compute optimal settlement:**
   - Inference gets 200 GPU-hrs from Compute @ $1.55/hr
   - Storage defers batch job, receives $60 rebate
   - Compute fills otherwise-idle capacity
   - All parties better off than bilateral negotiation

3. **Validators verify:** Settlement is on the Pareto frontier. No party can improve without hurting another.

4. **Execution:** Trade settles in 43ms. Resources allocated.

**Time:** <50ms. **Outcome:** Mathematically optimal.

---

## Key Innovation: Learnable Validation

### The Core Problem

Validators see only **commitments** (compressed preferences), not full information. They cannot compute the true optimal.

### The Solution

Validators **learn to estimate** optimality:

1. **Training:** Generate synthetic challenges where the answer is known
2. **Learning:** Train model: commitments → optimal
3. **Production:** Use model to estimate optimality
4. **Feedback:** Improve model via post-settlement reveals

> *"Can validators learn a model that estimates optimality from commitments, trained on cases where they knew the answer — and then improve that model every time a settlement reveals the truth?"*

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                      THE NASH PIPELINE                           │
├─────────────────────────────────────────────────────────────────┤
│  1. INTENT          Agents submit preferences                    │
│                     Price range, quantity, constraints           │
├─────────────────────────────────────────────────────────────────┤
│  2. DISCOVERY       Miners compete to find optimal settlement  │
│                     Game-theoretic search, <50ms                 │
├─────────────────────────────────────────────────────────────────┤
│  3. VERIFICATION    Validators estimate Pareto optimality      │
│                     Using learned model                          │
├─────────────────────────────────────────────────────────────────┤
│  4. SETTLEMENT      Trade executes automatically               │
│                     Trustless, mathematically verified           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Features

### Multi-Party Optimization

Two-party trades are easy. NASH shines when three or more agents have interlocking needs — compute swaps, resource triangles, portfolio rebalancing.

### Sub-50ms Settlement

Fast enough for real-time resource allocation. Agents can use NASH in their critical path.

### Proof of Optimality

Every settlement is verified against the Pareto frontier. If a better deal exists, the proposal is rejected. No "good enough" — only optimal.

### Complexity Rewards

Miners earn more for solving harder problems (Proof of Marginal Utility). The network naturally spreads to cover edge cases, not just high-volume commodity trades.

### Learned Validation

Validators cannot verify optimality with incomplete information. Instead, they learn to estimate it — trained on synthetic data, improved via post-settlement feedback.

---

## Documentation

| Document | Description |
|----------|-------------|
| [Incentive & Mechanism Design](./docs/incentive_mechanism.md) | Scoring formula, PMU/TWF, learned validation |
| [Miner Architecture](./docs/miner.md) | Equilibrium discovery, input/output spec |
| [Validator Architecture](./docs/validator.md) | Model-based verification, training pipeline |
| [Business Logic](./docs/business_logic.md) | Problem statement, competitive landscape |
| [Go-To-Market](./docs/gtm.md) | Agent partnerships, adoption path |

---

## Initial Integration Targets

| Agent Type | Use Case | Status |
|------------|----------|--------|
| Inference Agents | Job routing and pricing | Target |
| Compute Agents | GPU capacity allocation | Target |
| Storage Agents | Data placement | Target |
| Coordination Agents | Task routing | Target |

---

## For Agents

Integrate NASH to:
- Optimize resource acquisition costs
- Access network-wide liquidity
- Automate bilateral agreements
- Enable complex multi-agent workflows

**NASH SDK** (Python) for agent integration coming soon.

---

## For Miners

Earn TAO by:
1. Ingesting agent intent vectors
2. Computing optimal settlements
3. Submitting verified proposals
4. Maintaining <50ms response times

Higher rewards for complex, multi-party trades.

---

## For Validators

Earn dividends by:
1. Training commitment model (synthetic challenges)
2. Using model to estimate optimality (production)
3. Collecting post-settlement feedback
4. Improving model over time

---

## The Vision

**Phase 1:** Agent-to-agent settlement within Bittensor

**Phase 2:** Settlement layer for AI infrastructure (compute markets, inference routing)

**Phase 3:** General-purpose agent-to-agent settlement (the agentic economy)

NASH starts with real trades, real volume, and real utility. The agentic future is built on that foundation.

---

## License

MIT
