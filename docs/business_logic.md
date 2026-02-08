# NASH: Business Logic & Market Rationale

NASH solves the coordination problem between Bittensor subnets. Today, subnets that need to trade resources — compute, inference capacity, data — do so inefficiently through manual coordination or fixed pricing. NASH replaces that with automated, optimal settlement.

---

## The Problem

Bittensor is becoming an internal economy. Subnets buy and sell:

| Resource | Sellers | Buyers |
|----------|---------|--------|
| GPU compute | SN27 (Nodexo), SN12 (Compute Horde) | SN64 (Chutes), inference subnets |
| Inference capacity | SN64 (Chutes) | Application subnets, external users |
| Data | Data subnets | Training subnets |
| Bandwidth | Infrastructure subnets | High-throughput subnets |

**Current state:** These trades happen through:
- Discord DMs between subnet operators
- Fixed posted prices (no negotiation)
- Manual bilateral agreements
- No visibility into network-wide supply/demand

**The result:**
- Subnets overpay for resources
- Capacity sits idle while buyers search
- Multi-party optimizations never happen
- No price discovery mechanism

---

## Worked Example: The Coordination Failure

### Scenario

**Monday morning:**
- SN64 (Chutes) has a spike in inference requests. Needs 300 GPU-hours urgently.
- SN27 (Nodexo) has 200 GPU-hours idle in EU region.
- SN12 (Compute Horde) is running a batch job that could be deferred.

**What happens today:**

1. Chutes operator checks Nodexo's posted price: $1.70/hr
2. Only 200 hours available — not enough
3. Operator doesn't know Compute Horde could free up capacity
4. Chutes provisions from external cloud at $2.40/hr for the remaining 100 hours
5. Total cost: (200 × $1.70) + (100 × $2.40) = **$580**

**What happens with NASH:**

1. All three subnets have standing intents registered
2. NASH sees the opportunity for three-way optimization
3. Settlement computed:
   - Chutes gets 300 GPU-hours total
   - Nodexo provides 200 hours @ $1.55/hr
   - Compute Horde defers batch job, frees 100 hours @ $1.40/hr + $30 deferral fee
4. Total cost: (200 × $1.55) + (100 × $1.40) + $30 = **$480**

**Savings:** $100 (17%) on a single trade. Multiply across thousands of daily inter-subnet transactions.

---

## Why This Matters Now

### Bittensor's Growth Creates Friction

As the network grows:
- More subnets = more potential trading pairs
- More specialization = more interdependence
- More value flowing = higher stakes for efficiency

The coordination problem scales quadratically. Manual solutions don't.

### Subnet Interdependence is Increasing

| Pattern | Example | Frequency |
|---------|---------|-----------|
| Compute sourcing | Inference subnet buys GPU hours | Daily |
| Capacity balancing | High-load subnet offloads to low-load | Hourly |
| Resource triangulation | Three subnets with interlocking needs | Weekly |
| Cross-stake optimization | Validators rebalancing positions | Continuous |

These patterns exist today. They're just handled inefficiently.

### The Agentic Future Starts Here

If NASH works for subnet-to-subnet trades, it becomes the natural layer for:
- Agent-to-agent transactions (as AI agents become economic actors)
- Cross-chain settlement (as Bittensor integrates with other networks)
- External liquidity (as traditional finance connects to decentralized compute)

Starting with concrete, measurable subnet trades builds the foundation.

---

## Competitive Landscape

### Why Not Simple Order Books?

Order books work for:
- Fungible assets (one GPU-hour = another GPU-hour)
- Two-party trades (buyer meets seller)
- Price-only matching (no complex constraints)

Order books fail for:
- Differentiated resources (EU GPU ≠ US GPU)
- Multi-party optimization (three subnets with interlocking needs)
- Constraint satisfaction (latency requirements, timing preferences)

NASH handles the complex cases that order books can't.

### Why Not Request-for-Quote (RFQ)?

RFQ systems work for:
- Low-frequency, high-value trades
- Human-in-the-loop negotiation
- Known counterparties

RFQ fails for:
- High-frequency resource allocation
- Automated subnet operations
- Network-wide price discovery

NASH operates at machine speed with no human bottleneck.

### Why Not Centralized Matching?

Centralized matching (like a traditional exchange) works but introduces:
- Single point of failure
- Trust requirements
- Rent extraction (exchange fees)
- Opacity (matching logic is a black box)

NASH is decentralized, trustless, and transparent. Matching logic is verified by validators.

---

## The NASH Advantage

### Multi-Party Optimization

Most settlement systems handle bilateral trades. NASH finds optimal settlements across 2, 3, 4+ parties simultaneously.

**Value unlocked:** Trades that couldn't happen bilaterally become possible. The three-party compute example above saves 17% — that value was previously stranded.

### Proof of Optimality

Every NASH settlement is verified against the Pareto frontier. If a better deal exists, validators reject the proposal.

**Value unlocked:** Participants know they got the best possible deal. No information asymmetry, no wondering if they left money on the table.

### Latency

Sub-50ms settlement enables real-time resource allocation.

**Value unlocked:** Subnets can use NASH in their critical path. "I need compute now" gets answered now.

### Complexity Rewards

PMU incentivizes miners to solve hard problems, not just farm easy trades.

**Value unlocked:** Edge cases get covered. The network handles the full spectrum of trade complexity.

---

## Sustainability Model

### Phase 1: Emission-Funded (Current)

Miners and validators earn through Bittensor emissions. No transaction fees required.

**Sustainability:** Works as long as NASH provides value to the network (measured by root network support).

### Phase 2: Hybrid (Growth)

As transaction volume grows, introduce optional priority fees:
- Subnets can pay for faster settlement
- Complex trades can pay for guaranteed solver attention
- Fees distributed to miners proportional to work

**Sustainability:** Transaction fees supplement emissions. Network becomes self-sustaining.

### Phase 3: Fee-Funded (Maturity)

At scale, transaction fees alone could sustain the network:
- 0.1% settlement fee on trade value
- At $10M daily volume = $10K daily fees
- Distributed to miners and validators

**Sustainability:** NASH operates independently of emission subsidies.

---

## Risk Analysis

### Bootstrapping Risk

**Risk:** Not enough transaction volume to attract miners.

**Mitigation:**
- Start with guaranteed subnet partnerships (SN64, SN27, SN12)
- Use synthetic challenges for miner training during low-volume periods
- PMU rewards for solving any challenge, even synthetic

### Complexity Risk

**Risk:** Multi-party optimization is hard. Miners can't solve it fast enough.

**Mitigation:**
- Start with two-party trades, scale complexity gradually
- 200ms response window is generous for well-implemented solvers
- TWF rewards consistency over heroics

### Adoption Risk

**Risk:** Subnet operators don't integrate.

**Mitigation:**
- SDK makes integration trivial (Python library, Synapse-compatible)
- Clear ROI case (17% savings in worked example)
- Start with willing partners, prove value, expand

### Competition Risk

**Risk:** Another subnet builds a simpler solution.

**Mitigation:**
- NASH's multi-party optimization is genuinely hard to replicate
- First-mover advantage in liquidity
- Network effects compound (more participants = better matching)

---

## Why Bittensor?

NASH requires:

| Requirement | Bittensor Solution |
|-------------|-------------------|
| Competitive solving | 256 miners racing for optimal solution |
| Trustless verification | Validators confirm Pareto optimality |
| Economic alignment | Miners earn more for harder problems |
| Decentralized neutrality | No party controls the matching engine |
| Native liquidity | TAO-denominated, subnet-native trades |

Bittensor provides all of this. Building NASH elsewhere would require recreating the entire infrastructure.

---

## Success Metrics

### Phase 1: Proof of Concept

| Metric | Target |
|--------|--------|
| Subnet integrations | 3+ (SN64, SN27, SN12) |
| Daily settlements | 100+ |
| Average settlement time | <50ms |
| Miner participation | 50+ active |

### Phase 2: Growth

| Metric | Target |
|--------|--------|
| Subnet integrations | 10+ |
| Daily settlements | 10,000+ |
| Daily volume (TAO equivalent) | 1,000+ TAO |
| Multi-party settlements | 20%+ of volume |

### Phase 3: Scale

| Metric | Target |
|--------|--------|
| Daily settlements | 1M+ |
| Daily volume | $1M+ |
| External integrations | Agent frameworks, cross-chain |
| Self-sustaining fees | Emissions optional |

---
