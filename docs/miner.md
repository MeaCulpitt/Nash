# NASH Miner Design: Economic Equilibrium Discovery

## 1. Miner Tasks: The PoEF Pipeline
Miners on the NASH subnet act as decentralized game-theoretic solvers. Their primary function is to resolve the "Surface of Agreement" between competing economic intents (Buyer vs. Seller) and pinpoint the optimal coordinate for trade settlement.

### Task 1: Encrypted Intent Decoding & Manifold Generation
Miners receive high-dimensional, encrypted intent vectors from validators. The first task is to project these vectors into a local simulation environment to generate a **Nash Manifold Surface**—a mathematical representation of all possible points of agreement where the utility for both parties is non-zero.

### Task 2: Geometric Equilibrium Discovery
Once the manifold is generated, the miner must execute a high-speed search for the **Global Nash Equilibrium**. This is the specific coordinate on the surface where no party can improve their utility without diminishing the other's. This task is NP-hard in multi-modal environments and requires sophisticated neural-heuristic hybrid models.

### Task 3: Commitment & Proof Generation
To prevent "copy-cat" mining (weight copying), miners must generate a commitment hash of their manifold before submitting the final result. They also produce a cryptographic **Proof-of-Computation** that validates the model utilized to find the equilibrium was not pre-computed or cached.

---

## 2. Expected Input → Output Format
Miners interact with the Validator through the `NashIntentSynapse`.

### Input Format (Validator → Miner)
The miner receives a challenge packet containing encrypted intent data and environmental constraints:
* **challenge_id**: HEX-512
* **intent_vector**: ENCRYPTED_BLOB
* **utility_weights**: {"buyer": 0.5, "seller": 0.5}
* **market_constraints**: ["non-negative-spread", "max-slippage-2%"]
* **validator_timestamp**: Unix epoch

### Output Format (Miner → Validator)
The miner returns a compressed tensor representing the manifold and the proposed equilibrium:
* **manifold_tensor**: COMPRESSED_FLOAT_32_ARRAY
* **equilibrium_coordinate**: [x, y] coordinates
* **utility_score**: Float (0-1)
* **commitment_hash**: SHA256_HASH
* **compute_proof**: ZK_PROOF_OR_COMMITMENT

---

## 3. Performance Dimensions
NASH miners are evaluated across three core dimensions, prioritized by the **Nash Efficiency Ratio (NER)**.

### **A. Quality: Economic Fidelity (Weight: 60%)**
* **Metric:** Mean Squared Error (MSE) < 0.001 against the ground-truth Pareto Frontier.
* **Goal:** The miner must find the true global maximum of the manifold. Finding a "local" peak or a sub-optimal trade point results in a non-linear decay of the score.

### **B. Speed: Settlement Latency (Weight: 30%)**
* **Metric:** Round-trip response time < 50ms.
* **Logic:** NASH is a real-time marketplace. Even a perfect mathematical solution is useless if it arrives late. The **TWF (Time-Weighted Fidelity)** multiplier punishes jitter and high-latency responses, favoring miners with optimized network stacks and edge-compute hardware.

### **C. Accuracy: Equilibrium Stability (Weight: 10%)**
* **Metric:** Variance of the solution across multiple identical challenges.
* **Goal:** A miner's model must be deterministic and stable. If the same intent is provided twice (with slight noise), the miner's output must remain within a tight confidence interval to ensure market reliability.
