# NASH Miner Design: Economic Equilibrium Discovery

## 1. Miner Tasks: The PoEF Pipeline
Miners on the NASH subnet act as decentralized game-theoretic solvers. Their primary function is to resolve the "Surface of Agreement" between competing economic intents (Buyer vs. Seller) and pinpoint the optimal coordinate for trade settlement.

### Task 1: Encrypted Intent Decoding & Manifold Generation
Miners project high-dimensional, encrypted intent vectors into a local simulation environment to generate a **Nash Manifold Surface**—a mathematical representation of all possible points of agreement where utility for all parties is non-zero.

### Task 2: Geometric Equilibrium Discovery (The PMU Hunt)
Miners must execute a high-speed search for the **Global Nash Equilibrium**. To maximize rewards, miners must strategically target underserved or complex "Marginal" intents. Solving for niche economic pairs triggers a higher **Proof of Marginal Utility (PMU)** multiplier, rewarding discovery over commodity farming.

### Task 3: Commitment & Proof Generation
To prevent weight copying, miners generate a commitment hash and a cryptographic **Proof-of-Computation** to validate that the equilibrium was found via active inference rather than a pre-computed cache.

---

## 2. Expected Input → Output Format
### Input Format (Validator → Miner)
* **challenge_id**: HEX-512
* **intent_vector**: ENCRYPTED_BLOB
* **utility_weights**: {"buyer": 0.5, "seller": 0.5}
* **market_constraints**: ["non-negative-spread", "max-slippage-2%"]

### Output Format (Miner → Validator)
* **manifold_tensor**: COMPRESSED_FLOAT_32_ARRAY
* **equilibrium_coordinate**: [x, y]
* **utility_score**: Float (0-1)
* **commitment_hash**: SHA256_HASH
* **compute_proof**: ZK_PROOF_OR_COMMITMENT

---

## 3. Performance Dimensions
NASH miners are evaluated via the **Nash Efficiency Ratio (NER)**, which incorporates both stability and utility discovery.

### **A. Quality: Economic Fidelity (Weight: 50%)**
* **Metric:** MSE < 0.001 against the ground-truth Pareto Frontier.
* **Goal:** Finding the global maximum of the manifold. Finding sub-optimal points results in a non-linear decay of the score.

### **B. Utility: Marginal Discovery (Weight: 20%)**
* **Metric:** **PMU Multiplier.**
* **Logic:** If a miner solves a "crowded" trade (many other miners submitting), the score is diluted. If the miner identifies and solves a unique, complex intent, the **PMU** multiplier boosts the final reward.

### **C. Speed: Settlement Latency (Weight: 20%)**
* **Metric:** Round-trip response time < 50ms.
* **Logic:** The **TWF (Time-Weighted Fidelity)** multiplier punishes jitter, favoring miners with optimized network stacks.

### **D. Accuracy: Equilibrium Stability (Weight: 10%)**
* **Metric:** Solution variance across identical challenges.
* **Goal:** Models must be deterministic and stable to ensure long-term market reliability.
