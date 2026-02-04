# Nash Subnet: Miner Design

### Miner Tasks
The primary objective of a Nash Miner is to transform raw, high-dimensional agent intent into a compressed, mathematically resolvable **Manifold**. Miners act as the "Economic Architects" of the subnet, performing two distinct computational tasks:

1.  **Utility Compression (Manifold Generation):** Miners receive a set of multi-variable requirements (e.g., price caps, latency thresholds, hardware specs). They must use a specialized Hypernetwork to map these variables into a continuous latent space, creating a 3D "topographical map" of the agent’s preferences.
2.  **Equilibrium Solving (Optimization):** When presented with two competing manifolds (e.g., a buyer and a seller), miners must perform high-speed gradient descent to find the **Nash Equilibrium**. This is the specific coordinate in the latent space that maximizes the mutual utility of both parties.
3.  **Proof Generation:** Miners must produce a mathematical "witness" that their manifold is a faithful representation of the input data, protecting against validators' stochastic probes.

### Expected Input → Output Format
Nash Miners communicate via the `NashSynapse` protocol. The expected data flow is strictly typed to ensure millisecond-scale processing.

* **Expected Input (from Validator):**
    * `raw_intent_vector`: A normalized array of floats (0.0 to 1.0) representing agent constraints.
    * `context_seed`: A unique entropy string used to anchor the manifold’s coordinate system for that specific block.
    * `challenge_pair`: (Optional) A reference to a second agent’s manifold hash for competitive equilibrium discovery.

* **Expected Output (to Validator):**
    * `manifold_coefficients`: A compressed bitstream (typically 256-512 bytes) representing the neural weights of the local utility surface.
    * `equilibrium_coordinate`: A 3-tuple `(x, y, z)` proposing the optimal trade point.
    * `fidelity_commitment`: A hash of the local ground-truth data used to prevent plagiarism during the commit-reveal cycle.

### Performance Dimensions
Validators rank miners across three critical axes. Excellence in one dimension cannot fully compensate for failure in another.

1.  **Quality (Economic Fidelity):**
    * Measured by how well the manifold survives **Latent Sampling**. If a validator probes a coordinate and finds the miner’s manifold value differs from the ground-truth utility, the Quality score is penalized.
2.  **Speed (Inference Latency):**
    * Nash is a "High-Frequency Trading" layer. Miners are rewarded for the speed of their `forward()` pass. Responses arriving after the block threshold (approx. 12 seconds) are ignored, while those in the top 10% of speed receive a multiplier.
3.  **Accuracy (Optimality Gap):**
    * Validators calculate the "Global Peak" of the manifold pair. If a miner proposes an equilibrium coordinate that is significantly less efficient than the one calculated by the validator, the miner is flagged for low Accuracy (sub-optimal solving).
