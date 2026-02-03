# Nash Validator Design: The Economic Oracle

Validators in Nash ensure that the decentralized marketplace remains honest and efficient. They do not just "check" data; they actively probe manifolds to ensure mathematical soundness.

## 1. Scoring and Evaluation Methodology

### A. The Fidelity Audit (Primary Metric)
The validator deconstructs the miner’s Nash Manifold using Latent Sampling.
* **The Process:** The validator takes raw intent ($I_{raw}$) and the manifold ($M$) and selects $K$ random coordinates.
* **Scoring:** The Fidelity Score ($F$) is derived from:
  $$F = \exp(-\text{MSE}(U_r, U_m))$$

### B. Equilibrium Validation (The Pareto Test)
The validator checks if the miner's proposed Equilibrium Point is truly optimal.
* **The Penalty:** If the validator finds a different point that offers higher mutual utility, the miner’s score is slashed.

### C. Speed & Size Multipliers
* **Latency Multiplier:** Responses slower than the 50ms "Gold Standard" face exponential decay.
* **Compression Bonus:** Miners who represent complex intent in smaller packets receive a bonus.

## 2. Evaluation Cadence
* **Block-Level Sampling:** Validators query a random subset of miners every block (12 seconds) with "Synthetic Challenges."
* **Epoch-Level Weight Setting:** Every 360 blocks, validators aggregate rolling averages to set weights.

## 3. Validator Incentive Alignment

### A. VTrust (Validation Trust)
A validator's dividends depend on their VTrust score. If their rankings deviate from the Stake-Weighted Median of the network, rewards are clipped.

### B. The Discovery Bounty
To encourage "Active Auditing," Nash rewards validators who are the first to detect a "Cheat Point" (intentional dishonesty in a manifold) with higher Incentive Weight.
