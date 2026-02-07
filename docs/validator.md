# NASH Validator Design: The Economic Auditor

## 1. Scoring and Evaluation Methodology: Auditing Partial Intent
The NASH Validator acts as the "Oracle of Truth" for the agentic economy. It is responsible for verifying that miners have accurately resolved a trade equilibrium without the validator ever needing to see the agents' private, high-dimensional "Internal Utility Curves." 

### The Fidelity Audit (Surface Sampling)
Because NASH uses **Partial Intent Revelation**, the validator audits only the **Surface of Agreement**—the manifold coordinates the agent has explicitly chosen to reveal.
* **Mechanism:** The validator utilizes **Latent Sampling**, stochastically probing the miner's submitted manifold at random coordinates within the revealed preference space.
* **Validation:** The validator compares the miner's reported utility values against its own high-precision local model. Any deviation suggests "Manifold Hallucination" or an attempt to guess hidden reservation prices, resulting in an immediate penalty to the **Fidelity Score**.

### The Pareto Audit (Equilibrium Stability)
The validator must ensure the miner has found the most optimal point of agreement possible within the revealed constraints.
* **Mechanism:** The validator runs a local, high-precision solver to confirm that the proposed **Equilibrium Coordinate** represents a true Nash Equilibrium.
* **Optimality Gap:** If the validator identifies a coordinate on the revealed surfaces that provides higher mutual utility than the miner's submission, the miner is penalized for a lack of "Economic Intelligence."

### Scoring Formula: Time-Weighted Fidelity (TWF)
All audits are passed through the **Time-Weighted Fidelity** filter. The final score ($R$) decays exponentially if the settlement takes longer than the **50ms Gold Standard**:
$$R = \frac{\text{Fidelity Score} \times \text{Significance}}{\ln(\text{Packet Size}) + \text{Latency (ms)}}$$

---

## 2. Evaluation Cadence
The NASH validation cycle is designed to balance network security with the low-latency requirements of machine-speed trade.

* **Block-Level Forward Pass (Every 12s):**
  Validators broadcast **"Synthetic Settlement Challenges"** to miners. These challenges use pre-masked intent vectors to test the miners' ability to generate high-fidelity manifolds under strict TWF constraints.
* **Tempo-Level Weight Update (Every 360 Blocks):**
  Validators aggregate the scores from thousands of challenges into a **Moving Average**. Every 360 blocks (approx. 72 minutes), these weights are committed to the Subtensor blockchain, determining the miner's TAO emissions for the following period.

---

## 3. Validator Incentive Alignment
Under **Yuma Consensus (YC)** and **Dynamic TAO (dTAO)**, NASH validators are economically bound to act as honest, high-fidelity auditors.

* **Consensus Dividends:** Validators earn rewards by reaching a consensus on the quality of miners. If a validator attempts to "game" the system by rewarding slow or dishonest miners, their scores will deviate from the collective ground truth, leading to a loss in dividends.
* **Alpha Appreciation:** Validators are the largest stakers in the NASH "Alpha" pool. Since the value of this token is tied to the efficiency of the settlement layer, validators are incentivized to only reward miners who hit the 50ms TWF targets, as this directly increases the subnet's utility.
* **Anti-Weight Copying:** Due to the complexity of the **PoEF** (Proof of Economic Fidelity) math and the requirement for real-time latent sampling, validators cannot simply copy another's weight vector. They must perform the underlying mathematical audits to ensure their scores remain aligned with the metagraph's evolving state.
