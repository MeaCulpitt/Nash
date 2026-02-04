# Nash: Incentive & Mechanism Design

### Emission and Reward Logic
The Nash Subnet utilizes a dual-objective emission model designed to maximize both **Economic Fidelity** and **Discovery Speed**. Total emissions ($E$) allocated to the subnet are distributed based on a miner’s ability to minimize the "Utility Gap"—the difference between an agent's raw intent and the manifold's compressed representation.

* **Fidelity Score ($S_f$):** Accounts for 60% of the reward. It measures how accurately the miner’s manifold represents the agent's complex utility function.
* **Equilibrium Efficiency ($S_e$):** Accounts for 40% of the reward. It measures the speed and precision with which a miner identifies the Pareto-optimal intersection between two manifolds.

The final reward $R$ for a miner is calculated as:
$$R = \alpha(S_f) + \beta(S_e) - \text{Latency Penalty}$$
where $\alpha$ and $\beta$ are weights adjusted by the validator network to prioritize accuracy or throughput based on current market demand.

### Incentive Alignment for Miners and Validators
The Nash mechanism creates a symbiotic "Check-and-Balance" relationship:

* **Miners:** Incentivized to invest in high-performance Hypernetworks. Because the "Utility Surface" is high-dimensional, miners who use more sophisticated AI models to find better "deal coordinates" (Equilibria) earn exponentially higher rewards than those providing sub-optimal solutions.
* **Validators:** Incentivized to be rigorous auditors. Validators earn dividends by correctly ranking miners. If a validator accepts a low-fidelity manifold that is later "challenged" by the network, the validator’s weight-setting authority (and thus their earnings) is reduced via the Yuma Consensus mechanism.

### Mechanisms to Discourage Low-Quality or Adversarial Behavior
Nash implements three layers of defense against bad actors:
1.  **Latent Sampling:** Validators do not check the whole manifold (which is computationally expensive). Instead, they perform "stochastic probes" at random coordinates. If the miner's manifold value at a probe point deviates from the ground truth by $> \epsilon$, the entire submission is discarded.
2.  **Commit-Reveal Cycles:** To prevent "Miner Plagiarism" (where one miner copies another’s manifold), miners must submit a hash of their solution before revealing the full data.
3.  **Collusion Slashing:** If a validator consistently favors a specific set of miners regardless of their mathematical accuracy, the anomalous weight distribution is flagged by other validators, leading to a "Consensus Penalty" that diverts emissions away from the colluding cluster.

### Proof of Intelligence and Proof of Effort
Nash qualifies as a **Genuine Proof of Intelligence** because the task—compressing high-dimensional economic intent into a 3D manifold—cannot be solved by brute force. It requires a "world model" of utility. 
* **Proof of Intelligence:** Miners must use neural architectures to generalize an agent's preferences across unseen coordinates. This is a task of synthesis and prediction, not just computation.
* **Proof of Effort:** The high-frequency nature of the "Equilibrium Race" requires miners to maintain 99.9% uptime and low-latency hardware. The computational cost of running gradient descent to find the Pareto-frontier acts as a physical stake in the network’s success.

### High-Level Algorithm: The Nash Cycle
The following cycle occurs within the timeframe of a few blocks:

1.  **Task Assignment:** The Validator broadcasts a "Request for Equilibrium" (RFE) containing two distinct sets of raw agent requirements (e.g., Buyer A vs. Seller B).
2.  **Submission:** Miners process the RFE through their local models, generating a compact Manifold and a proposed Equilibrium Coordinate. They submit a `Commit` hash to the chain.
3.  **Validation:** Once the `Reveal` phase begins, Validators pull the full manifold data. They run **Latent Sampling** to verify fidelity and **Gradient Descent** to ensure the proposed coordinate is a true Nash Equilibrium.
4.  **Scoring:** The Validator assigns a score based on the **Nash Efficiency Ratio**:
    * *Accuracy:* How close is the manifold to the ground truth?
    * *Optimality:* Is there a better deal coordinate the miner missed?
    * *Latency:* How fast was the response?
5.  **Reward Allocation:** Scores are aggregated via Yuma Consensus, and TAO emissions are distributed to the miners' hotkeys proportionally to their performance.
