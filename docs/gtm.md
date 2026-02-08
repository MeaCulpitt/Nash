# NASH: Go-To-Market Strategy

NASH launches as the settlement layer for Bittensor's internal economy, then expands to the broader agentic ecosystem. This document outlines the path from first integration to network-scale adoption.

---

## Phase 1: Anchor Subnet Partnerships

### Target: Prove value with 3 committed subnet integrations

The goal is not broad adoption — it's deep integration with subnets that have real, recurring settlement needs.

### Primary Targets

| Subnet | Why | Use Case | Integration Path |
|--------|-----|----------|------------------|
| **SN64 (Chutes)** | High inference volume, variable demand | GPU capacity sourcing, job routing | SDK integration into orchestrator |
| **SN27 (Nodexo)** | Large compute capacity, needs buyers | Selling idle GPU hours | SDK integration into allocation logic |
| **SN12 (Compute Horde)** | Batch workloads, timing flexibility | Deferral agreements, capacity sharing | SDK integration into scheduler |

### Why These Three?

They form a natural triangle:
- Chutes needs compute → Nodexo has compute
- Nodexo has excess capacity → Compute Horde can absorb or defer
- Compute Horde's batch jobs are flexible → creates optimization opportunities

Three-party trades become possible immediately.

### Integration Approach

**Step 1: SDK delivery**
- Python library, Synapse-compatible
- Drop-in integration for existing subnet code
- <100 lines of code to integrate

**Step 2: Pilot period**
- Run alongside existing settlement methods
- Compare outcomes (price, speed, success rate)
- No commitment required

**Step 3: Production rollout**
- Subnet switches primary settlement to NASH
- Fallback to direct bilateral if NASH unavailable
- Metrics dashboard for subnet operators

### Success Criteria (Phase 1)

| Metric | Target | Timeline |
|--------|--------|----------|
| Integrations signed | 3 subnets | Month 1-2 |
| Daily settlements | 100+ | Month 3 |
| Avg savings vs bilateral | >10% | Month 3 |
| Settlement success rate | >99% | Month 3 |

---

## Phase 2: Subnet Expansion

### Target: 10+ subnet integrations, network effect begins

Once the anchor triangle proves value, expand to adjacent subnets.

### Expansion Targets

| Category | Subnets | Use Case |
|----------|---------|----------|
| **Compute** | Additional GPU/inference subnets | Capacity balancing |
| **Data** | Training data subnets | Data-for-compute swaps |
| **Infrastructure** | Storage, bandwidth subnets | Resource triangulation |
| **Application** | End-user facing subnets | Backend resource sourcing |

### Network Effects

Each new subnet integration:
- Adds liquidity (more potential counterparties)
- Enables new trade patterns (more multi-party combinations)
- Increases PMU opportunities (more complex challenges)

At 10 subnets, the combinatorial space explodes:
- 2 subnets: 1 trading pair
- 5 subnets: 10 trading pairs
- 10 subnets: 45 trading pairs
- Plus multi-party combinations

### Miner Growth Strategy

More volume = more miner interest. Target:

| Phase | Active Miners | Rationale |
|-------|---------------|-----------|
| Launch | 20-50 | Early adopters, high PMU |
| Phase 1 | 50-100 | Anchor volume supports more miners |
| Phase 2 | 100-200 | Network effects attract specialists |

Miner diversity matters:
- Generalists handle commodity trades
- Specialists handle complex multi-party optimization
- Geographic distribution reduces latency variance

### Success Criteria (Phase 2)

| Metric | Target | Timeline |
|--------|--------|----------|
| Integrations | 10+ subnets | Month 6 |
| Daily settlements | 10,000+ | Month 6 |
| Multi-party settlements | 20%+ of volume | Month 6 |
| Daily volume | 1,000+ TAO equivalent | Month 6 |

---

## Phase 3: External Expansion

### Target: Settlement layer for the broader agentic ecosystem

With Bittensor-native settlement proven, expand to external integrations.

### External Integration Targets

| Category | Examples | Use Case |
|----------|----------|----------|
| **Agent frameworks** | AutoGPT, CrewAI, LangChain agents | Agent-to-agent resource trading |
| **Compute marketplaces** | Akash, Render, Golem | Cross-network settlement |
| **AI infrastructure** | Inference APIs, model hosting | Automated capacity agreements |
| **DeFi** | Cross-chain bridges, DEXs | TAO liquidity integration |

### The Agentic Economy Thesis

As AI agents become autonomous economic actors, they need:
- Fast settlement (can't wait for human approval)
- Optimal pricing (maximize utility automatically)
- Trustless execution (no counterparty risk)
- Multi-party coordination (complex supply chains)

NASH provides all of this, battle-tested on Bittensor volume.

### Positioning

**Not "the future of agent commerce"** (too speculative)

**Instead: "The settlement layer that works, today"**

- Proven on X thousand daily settlements
- Sub-50ms latency, verified
- Multi-party optimization, demonstrated
- Bittensor-native, TAO-denominated

External adopters get infrastructure that's already working, not vaporware.

### Success Criteria (Phase 3)

| Metric | Target | Timeline |
|--------|--------|----------|
| External integrations | 5+ | Month 12 |
| Non-Bittensor volume | 20%+ of total | Month 12 |
| Daily settlements | 100,000+ | Month 12 |
| Self-sustaining fees | Optional, not required | Month 12 |

---

## Miner Incentives by Phase

### Phase 1: Early Adopter Advantage

| Incentive | Mechanism |
|-----------|-----------|
| High PMU | Low solver count = concentrated rewards |
| TWF head start | Early miners build reputation moat |
| Emission share | Fewer miners splitting emissions |

**Message to miners:** Get in early, build TWF, dominate when volume scales.

### Phase 2: Specialization Rewards

| Incentive | Mechanism |
|-----------|-----------|
| Complexity premiums | Multi-party trades pay 3-5x |
| Niche discovery | Underserved trade types = high PMU |
| Infrastructure ROI | Better hardware = better TWF |

**Message to miners:** Find your niche. Generalists compete on volume; specialists compete on capability.

### Phase 3: Scale Economics

| Incentive | Mechanism |
|-----------|-----------|
| Volume rewards | More settlements = more total earnings |
| External demand | Non-Bittensor trades add volume |
| Fee revenue | Transaction fees supplement emissions |

**Message to miners:** NASH becomes critical infrastructure. Mining it is mining the backbone of agent commerce.

---

## Validator Incentives by Phase

### Phase 1: Foundation Building

| Incentive | Mechanism |
|-----------|-----------|
| Early V-Trust | Establish consensus position |
| Emission share | High per-validator dividends |
| Challenge design | Shape the problem space |

### Phase 2: Consensus Importance

| Incentive | Mechanism |
|-----------|-----------|
| V-Trust compounding | Consistent validators dominate |
| Stake growth | Successful subnet attracts delegation |
| Governance influence | Shape PMU parameters, thresholds |

### Phase 3: Infrastructure Returns

| Incentive | Mechanism |
|-----------|-----------|
| Fee share | Transaction fees to validators |
| External credibility | "NASH validator" as credential |
| Network criticality | Essential infrastructure role |

---

## SDK and Developer Experience

### SDK Features

```python
from nash import NashClient, Intent

# Initialize
client = NashClient(subnet_id="sn64", hotkey=hotkey)

# Register standing intent
intent = Intent(
    action="buy",
    resource="gpu_hours",
    quantity={"min": 50, "max": 200},
    price={"max": 1.80},
    constraints=["latency_ms < 40"]
)
client.register_intent(intent)

# Receive settlements via callback
@client.on_settlement
def handle_settlement(settlement):
    # Execute the trade
    allocate_resources(settlement.terms)
```

### Integration Complexity

| Integration Level | Effort | Capability |
|-------------------|--------|------------|
| Basic (standing intents) | 1 day | Passive settlement |
| Standard (callbacks) | 1 week | Automated execution |
| Advanced (dynamic intents) | 2 weeks | Real-time adjustment |

### Documentation

- Quick start guide (30 min to first settlement)
- API reference (full specification)
- Example integrations (reference implementations)
- Troubleshooting guide (common issues)

---

## Marketing and Communications

### Phase 1: Technical Credibility

| Channel | Content |
|---------|---------|
| GitHub | Open source, documented code |
| Bittensor Discord | Technical deep-dives, AMA |
| Subnet operator outreach | Direct partnership discussions |

**No hype.** Let the technology and results speak.

### Phase 2: Case Studies

| Content | Purpose |
|---------|---------|
| Integration case studies | "SN64 saved 17% on compute costs" |
| Performance benchmarks | Settlement times, success rates |
| Miner economics | "Top miners earning X TAO/month" |

**Proof over promises.**

### Phase 3: Ecosystem Positioning

| Channel | Content |
|---------|---------|
| Agent framework docs | "How to integrate NASH" |
| Conference talks | Technical architecture |
| Research papers | Game-theoretic foundations |

**Infrastructure credibility.** NASH as the serious settlement layer.

---

## Risk Mitigation

### Integration Risk

**Risk:** Subnet operators don't integrate.

**Mitigation:**
- Start with warm relationships (operators already trading manually)
- SDK makes integration trivial
- Pilot period with no commitment
- Clear ROI case with worked examples

### Volume Risk

**Risk:** Not enough trades to attract miners.

**Mitigation:**
- Synthetic challenges during low volume
- Concentrated emissions attract early miners
- PMU rewards any valid solution, even low volume

### Technical Risk

**Risk:** Settlement quality doesn't meet promises.

**Mitigation:**
- Conservative latency targets (50ms is achievable)
- Thorough testing before mainnet
- Gradual complexity ramp (two-party first)

### Competition Risk

**Risk:** Another solution captures the market.

**Mitigation:**
- First-mover advantage on liquidity
- Multi-party optimization is genuinely hard
- Network effects compound quickly

---

## Timeline Summary

| Month | Milestone |
|-------|-----------|
| 1-2 | Anchor partnerships signed (SN64, SN27, SN12) |
| 3 | SDK released, pilot settlements begin |
| 4-5 | Production rollout, 100+ daily settlements |
| 6 | 10+ subnet integrations, 10K daily settlements |
| 9 | External integrations begin |
| 12 | 100K daily settlements, self-sustaining optional |

---
