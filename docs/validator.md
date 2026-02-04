# Nash Subnet: Validator Design

### Scoring and Evaluation Methodology
The Nash Validator employs a multi-stage, asymmetric evaluation process to ensure that miners are providing genuine "Economic Intelligence" rather than static or cached data.

1.  **Fidelity Audit (Latent Sampling):** Instead of evaluating the entire manifold (which is computationally prohibitive), validators perform stochastic probes at random coordinates $(x, y, z)$. They compare the miner's reported utility value against the "Ground Truth" calculated locally by the validator. The accuracy score ($S_a$) is derived using Mean Squared Error (MSE):
    $$S_a = 1 - \text{min}(1, \frac{MSE}{\text{threshold}})$$
2.  **Optimality Verification:** Validators run a high-precision gradient descent pass to identify the true global Nash Equilibrium for a given manifold pair. They then measure the "Optimality Gap" ($G_o$)—the distance between the miner's proposed coordinate and the validator's ground-truth coordinate. 
3.  **Efficiency Scoring:** To prevent "lazy mining," validators incorporate a time-decay multiplier ($T$). Responses that arrive earlier in the block cycle receive a higher weight, ensuring the network remains capable of instant settlement.

The final weight $W$ set on-chain for a miner is a moving average of these components:
$$W_{t+1} = (1 - \rho)W_t + \rho(\text{Fidelity} \times \text{Optimality} \times \text{Speed})$$

### Evaluation Cadence
The validation cycle is synchronized with the Bittensor block clock to ensure network-wide consistency:

* **Step-Level (Every Block ~12s):** Validators broadcast RFEs (Requests for Equilibrium) to a randomized subset of the metagraph to ensure constant coverage without overwhelming network bandwidth.
* **Epoch-Level (Every 360 Blocks / 1 Tempo):** Validators aggregate their internal scores, normalize them across the current active miner set, and submit the final weight vector to the Subtensor blockchain.
* **Sync-Level:** Validators continuously synchronize their local metagraph state to track new registrations and deregistered UIDs, ensuring that only "Immune" and "Top-Performing" miners are evaluated for rewards.

### Validator Incentive Alignment
Nash aligns validator incentives with the health of the broader ecosystem through three pillars:

1.  **VTrust (Validator Trust):** Under Yuma Consensus, validators earn rewards (Dividends) based on how well their weight assignments align with the stake-weighted majority. This discourages "lonely" or idiosyncratic scoring and forces validators to be mathematically objective.
2.  **Market-Maker Rewards:** Validators act as the primary gateways for external agents to access the subnet. By providing high-fidelity validation, they increase the "Utility Value" of the Nash subnet, which attracts more delegated stake from TAO holders and increases the validator's own emission share.
3.  **Anti-Plagiarism Checks:** Validators are incentivized to use unique, randomized entropy seeds in their challenges. If a validator uses predictable tasks, they risk their miners being "copied" by others, which lowers the consensus score and reduces the validator's performance metrics.
