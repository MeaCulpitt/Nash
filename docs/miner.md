# NASH Miner Design: High-Fidelity Manifold Generation

## 1. Miner Tasks
The NASH miner acts as the computational engine of the "Economic Molt," transforming abstract agentic intent into actionable mathematical geometry. The process is engineered to ensure high-speed resolution while maintaining the privacy of the participants.

### Phase I: Encrypted Intent Encoding
Miners receive "Intent Vectors" that have been pre-processed via the NASH SDK's Differential Privacy layer. The miner's task is to map these high-dimensional requirements into a compact **Nash Manifold**. 

Crucially, the miner only generates the **Surface of Agreement**—the boundary representing acceptable trade conditions. The agent's **Internal Utility Curve** (absolute reservation prices and private strategic constraints) remains hidden within the high-dimensional latent space of the agent’s private model, never reaching the miner.

### Phase II: Geometric Equilibrium Discovery
Once manifolds are generated, the miner must solve for the "Overlapping Manifold"—the intersection of the buyer's and seller's geometric surfaces. The miner runs optimization algorithms (e.g., Gradient-Play Dynamics) to identify the **Nash Equilibrium Coordinate**. This coordinate represents the unique point of mutual agreement where neither agent can improve their outcome by deviating, resolved without the miner ever seeing the agents' raw database or full intent history.

---

## 2. Expected Input → Output Format
NASH utilizes a high-density binary serialization format to ensure sub-100ms compatibility across the metagraph.

### Expected Input (The Synapse)
* **Encrypted Intent Vector (`Tensor[N, D]`):** A differentially private representation of agent preferences.
* **Context Header (`JSON/Bytes`):** Meta-constraints including transaction deadlines and priority weights.
* **Partial Manifold ID:** The specific counter-party surface to be resolved against.

### Expected Output (The Submission)
* **Nash Manifold Surface (`Compressed Tensor`):** A 128–512 byte representation of the "Surface of Agreement."
* **Equilibrium Point (`Vector[D]`):** The final negotiated coordinates for the trade.
* **Commitment Hash:** A cryptographic signature ensuring the manifold was generated honestly from the provided inputs.

---

## 3. Performance Dimensions
Miner performance is evaluated through **Time-Weighted Fidelity (TWF)**, balancing technical precision with the speed of the agentic economy.

### Quality & Structural Fidelity (Partial Revelation)
Miners must ensure the generated manifold surface is a precise reflection of the revealed intent.
* **Metric:** Mean Squared Error (MSE) on sampled surface points.
* **Target:** MSE < 0.001.
* **Privacy Guard:** Any miner attempt to "probe" beyond the revealed surface results in a Fidelity mismatch, leading to immediate reward slashing.

### Speed & Latency (The TWF Core)
Speed is the primary denominator in the Nash Efficiency Ratio ($R$). 
* **Gold Standard:** <50ms. 
* **The Reward Cliff:** Due to TWF logic, rewards decay exponentially beyond 100ms. This incentivizes miners to optimize CUDA kernels for the geometric intersection math, ensuring settlement happens at machine-speed.

### Accuracy (Equilibrium Stability)
The proposed Equilibrium must be mathematically stable. If a validator finds a more optimal coordinate (an "Optimality Gap") that was visible on the revealed manifold surfaces, the miner is penalized.
* **Target:** Pareto Optimality. 
* **Verification:** Validators utilize latent sampling to verify that the proposed point sits at the exact intersection of the submitted surfaces.
