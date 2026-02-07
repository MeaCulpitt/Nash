# NASH Incentive & Mechanism Design: Proof of Economic Fidelity (PoEF)

## 1. Emission and Reward Logic: The Dual-Layer Yield
NASH operates on a **Synthetic-Equilibrium Model** where emissions are governed by the **Nash Efficiency Ratio (NER)**. Unlike simple compute subnets, NASH splits its reward potential into two distinct dimensions to balance stability with market discovery.

### Pool A: The Stability Layer (Reputation Weighted)
Utilizes **Time-Weighted Fidelity (TWF)** to reward the "Trust Moat" of a neuron.
* **Logic:** Emissions are multiplied by a rolling average of the miner's historical accuracy and uptime.
* **Impact:** This rewards long-term participants, making "flash-mining" or seasonal participation economically inefficient.

### Pool B: The Discovery Layer (Utility Weighted)
Utilizes **Proof of Marginal Utility (PMU)** to reward "Economic Alpha."
* **Logic:** Rewards scale based on the scarcity of the trade resolution. If 200 miners solve a simple USD-BTC pair, the individual reward is minimal. If a single miner resolves a complex, multi-leg industrial asset trade, the PMU multiplier triggers a significant emission spike.
* **Impact:** Forces the network's intelligence to spread across the entire economic landscape, ensuring no trade intent goes unserved.

---

## 2. Incentive Alignment for Miners and Validators
* **Miners:** Positioned as **Economic Arbitrageurs**. They are incentivized to find the "hardest" problems (High PMU) while maintaining a flawless performance record (High TWF). Their goal is to find the point of maximum economic efficiency—the Nash Equilibrium—where no party can improve their position without making another worse off.
* **Validators:** Positioned as **Equilibrium Auditors**. They do not just verify if a trade *can* happen; they verify if the miner's proposal is the *most* efficient possible resolution. Validators are aligned through V-Trust, earning higher dividends by maintaining strict consensus on what constitutes a "high-fidelity" settlement.

---

## 3. Mechanisms to Discourage Low-Quality or Adversarial Behavior
* **The Fidelity Slash:** Any miner submitting a mathematically impossible or "hallucinated" equilibrium suffers an immediate, non-linear decay of their **TWF** multiplier. This forces them to spend weeks re-earning the network's trust.
* **Anti-Sybil PMU Decay:** If multiple keys are used to submit identical solutions for the same task, the PMU score for that specific task collapses, rendering the Sybil attack cost-prohibitive.
* **Complexity Buffering:** Simple tasks are subject to a "Saturation Cap." This prevents high-performance miners from "bullying" the network by only solving easy tasks, as their rewards will eventually hit a ceiling that only complex, marginal utility tasks can break.

---

## 4. Proof of Intelligence and Proof of Effort
* **Proof of Intelligence:** Finding a Nash Equilibrium in a multi-modal, multi-currency environment is an **NP-hard** problem. It requires the miner to synthesize disparate economic intents into a single, unified settlement manifold. This cannot be solved with brute-force compute; it requires a sophisticated understanding of game theory and economic heuristic modeling.
* **Proof of Effort:** Maintaining a top-tier **TWF** score requires relentless infrastructure maintenance and 24/7 connectivity. Because the scoring includes a **Latency Penalty**, miners must exert significant "effort" in optimizing their network stacks to ensure their intelligence is delivered in real-time.

---

## 5. High-Level Algorithm: The PoEF Pipeline
The NASH subnet operates on a continuous, high-frequency cycle:

1.  **Task Assignment:** The Validator generates an **Economic Challenge Pair** (Buyer Intent vs. Seller Intent) with specific utility constraints and broadcasts it to the metagraph.
2.  **Equilibrium Proposal (Submission):** Miners ingest the intent data and utilize local game-theoretic models to generate a **Trade Manifold**. They submit their proposed equilibrium along with a cryptographic "Proof-of-Computation."
3.  **The Pareto Audit (Validation):** The Validator checks the submission against the **Pareto Frontier**. If a proposal is found to be mathematically inefficient compared to the validator’s own baseline or the best-performing miner's solution, it is discarded.
4.  **NER Scoring:** The Validator calculates the **Nash Efficiency Ratio ($R$)** based on accuracy, latency, and the PMU/TWF multipliers.
5.  **Reward Allocation:** Scores are normalized across the epoch and submitted to the Subtensor. Emissions are then distributed via Yuma Consensus to the miners based on their final $S$ score ($S = (R \times PMU) \times TWF$).
