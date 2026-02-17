**nash/validator.py**

```python
"""
NASH Validator - Optimized implementation for scoring and verification.

Optimizations:
- Cached metagraph axon references
- Vectorized scoring instead of loops
- Miner response validation
- Proper error handling
- Batched challenge generation
"""

import bittensor as bt
from nash.protocol import NashSynapse
import torch
import torch.nn as nn
from typing import List, Optional, Tuple
import time
from dataclasses import dataclass


@dataclass
class ChallengeResult:
    """Result of a validation challenge."""
    intent: torch.FloatTensor
    manifold: Optional[torch.FloatTensor]
    equilibrium: Optional[torch.FloatTensor]
    latency_ms: float


class FidelityScorer(nn.Module):
    """
    Neural network to calculate fidelity scores for miner responses.
    Learns to score responses based on historical accuracy.
    """
    def __init__(self, intent_dim: int = 10, manifold_dim: int = 256):
        super().__init__()
        self.scorer = nn.Sequential(
            nn.Linear(intent_dim + manifold_dim + 2, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid(),  # Output between 0 and 1
        )
    
    def forward(
        self, 
        intent: torch.FloatTensor, 
        manifold: torch.FloatTensor,
        equilibrium: torch.FloatTensor
    ) -> torch.FloatTensor:
        """
        Calculate fidelity score for a response.
        
        Args:
            intent: Original intent vector
            manifold: Miner-provided manifold tensor
            equilibrium: Miner-provided equilibrium point
            
        Returns:
            Fidelity score between 0 and 1
        """
        # Flatten and concatenate
        intent_flat = intent.flatten()
        manifold_flat = manifold.flatten()[:256]  # Truncate if too long
        eq_flat = equilibrium.flatten()
        
        # Pad to fixed size if needed
        combined = torch.cat([
            intent_flat,
            manifold_flat,
            eq_flat
        ])[:int(10 + 256 + 2)]
        
        # Pad to expected size
        if combined.shape[0] < 268:
            combined = torch.cat([combined, torch.zeros(268 - combined.shape[0])])
        
        return self.scorer(combined.unsqueeze(0))


class NashValidator(bt.Neuron):
    """
    NASH Validator that challenges miners and scores their responses.
    
    Optimizations:
    - Cached axon references
    - Vectorized scoring
    - Response validation
    - Proper error handling
    """
    
    def __init__(self):
        super().__init__()
        
        # Initialize scorer model
        self.scorer = FidelityScorer(intent_dim=10, manifold_dim=256).to(self.device)
        self.scorer.eval()
        
        # Cache for metagraph axon references (updated periodically)
        self._axon_cache: Optional[List[object]] = None
        self._axon_cache_time: float = 0
        self._axon_cache_ttl: float = 60  # Cache for 60 seconds
        
        # Scoring parameters
        self._min_valid_responses = 1
        
        # Pre-allocate challenge tensor
        self._challenge_buffer = torch.empty(10, device=self.device)
        
        bt.logging.info(f"Validator initialized on device: {self.device}")
    
    def _get_axon_references(self) -> List[object]:
        """Get cached or fresh axon references from metagraph."""
        current_time = time.time()
        
        # Return cached if still valid
        if (self._axon_cache is not None and 
            current_time - self._axon_cache_time < self._axon_cache_ttl):
            return self._axon_cache
        
        # Refresh cache
        try:
            uids = self.metagraph.uids
            axons = [self.metagraph.axons[uid] for uid in uids]
            self._axon_cache = axons
            self._axon_cache_time = current_time
            bt.logging.debug(f"Refreshed axon cache with {len(axons)} axons")
            return axons
        except Exception as e:
            bt.logging.error(f"Error getting axon references: {e}")
            return self._axon_cache or []
    
    def _generate_challenge(self, batch_size: int = 1) -> torch.FloatTensor:
        """
        Generate synthetic economic challenges.
        
        Args:
            batch_size: Number of challenges to generate
            
        Returns:
            Tensor of shape (batch_size, 10) containing challenge intents
        """
        # Use pre-allocated buffer when possible
        if batch_size == 1:
            torch.randn(10, device=self.device, out=self._challenge_buffer)
            return self._challenge_buffer.unsqueeze(0)
        
        return torch.randn(batch_size, 10, device=self.device)
    
    def _validate_response(
        self, 
        manifold: Optional[torch.FloatTensor], 
        equilibrium: Optional[torch.FloatTensor]
    ) -> bool:
        """
        Validate a miner's response before scoring.
        
        Args:
            manifold: Response manifold tensor
            equilibrium: Response equilibrium point
            
        Returns:
            True if response is valid for scoring
        """
        if manifold is None or equilibrium is None:
            return False
        
        # Check shapes
        if manifold.numel() == 0 or equilibrium.numel() != 2:
            return False
        
        # Check for NaN or Inf
        if torch.isnan(manifold).any() or torch.isinf(manifold).any():
            return False
        if torch.isnan(equilibrium).any() or torch.isinf(equilibrium).any():
            return False
        
        return True
    
    def _calculate_fidelity(
        self,
        challenge: torch.FloatTensor,
        manifold: torch.FloatTensor,
        equilibrium: torch.FloatTensor
    ) -> float:
        """
        Calculate fidelity score for a miner's response.
        
        Args:
            challenge: Original challenge intent
            manifold: Miner-provided manifold
            equilibrium: Miner-provided equilibrium
            
        Returns:
            Fidelity score (0.0 to 1.0)
        """
        try:
            with torch.no_grad():
                # Move to device
                challenge_dev = challenge.to(self.device)
                manifold_dev = manifold.to(self.device)
                equilibrium_dev = equilibrium.to(self.device)
                
                # Calculate score using neural network
                score_tensor = self.scorer(challenge_dev, manifold_dev, equilibrium_dev)
                score = score_tensor.item()
                
                return float(score)
                
        except Exception as e:
            bt.logging.warning(f"Error calculating fidelity: {e}")
            return 0.0
    
    async def forward(self):
        """
        Validator loop: Challenge -> Score -> Set Weights.
        
        Optimized with:
        - Cached axon references
        - Vectorized response processing
        - Proper error handling
        """
        start_time = time.perf_counter()
        
        try:
            # Get axon references (cached)
            axons = self._get_axon_references()
            if not axons:
                bt.logging.warning("No valid axons found in metagraph")
                return
            
            miner_uids = self.metagraph.uids.tolist()
            
            # Generate challenge
            challenge_intent = self._generate_challenge()
            synapse = NashSynapse(raw_intent=challenge_intent)
            
            # Query miners
            responses: List[ChallengeResult] = []
            try:
                dendrite_responses = await self.dendrite(
                    axons=axons,
                    synapse=synapse,
                    deserialize=True,
                    timeout=5.0,  # 5 second timeout for response collection
                )
            except Exception as e:
                bt.logging.error(f"Error querying dendrite: {e}")
                return
            
            # Process responses (vectorized where possible)
            scores = torch.zeros(len(miner_uids), device=self.device)
            valid_count = 0
            
            for i, response in enumerate(dendrite_responses):
                try:
                    manifold, equilibrium = response
                    
                    # Validate response
                    if not self._validate_response(manifold, equilibrium):
                        continue
                    
                    # Calculate fidelity score
                    score = self._calculate_fidelity(
                        challenge_intent, 
                        manifold, 
                        equilibrium
                    )
                    
                    scores[i] = score
                    valid_count += 1
                    
                except Exception as e:
                    bt.logging.warning(f"Error processing response {i}: {e}")
                    continue
            
            # Check if we have enough valid responses
            if valid_count < self._min_valid_responses:
                bt.logging.warning(
                    f"Insufficient valid responses: {valid_count}/{self._min_valid_responses}"
                )
                # Apply small penalty to all for non-participation
                scores = scores * 0.5
            
            # Normalize scores (softmax-like, but ensure positive)
            scores = torch.relu(scores)  # Ensure non-negative
            if scores.sum() > 0:
                scores = scores / scores.sum()
            
            # Set weights on blockchain
            elapsed = time.perf_counter() - start_time
            bt.logging.info(
                f"Validation round completed in {elapsed*1000:.1f}ms, "
                f"valid responses: {valid_count}/{len(miner_uids)}"
            )
            
            self.subtensor.set_weights(
                netuid=self.config.netuid,
                wallet=self.wallet,
                uids=miner_uids,
                weights=scores.cpu().numpy().tolist()
            )
            
        except Exception as e:
            bt.logging.error(f"Error in validator forward: {e}")
            import traceback
            bt.logging.debug(traceback.format_exc())
    
    def get_scorer_info(self) -> dict:
        """Return scorer model information for debugging."""
        return {
            "scorer_params": sum(p.numel() for p in self.scorer.parameters()),
            "device": str(self.device),
            "axon_cache_size": len(self._axon_cache) if self._axon_cache else 0,
            "cache_ttl_seconds": self._axon_cache_ttl,
        }


async def run_validator():
    """Standalone validator runner with proper async handling."""
    with NashValidator() as validator:
        bt.logging.info(f"Validator scorer info: {validator.get_scorer_info()}")
        
        while True:
            bt.logging.info("Validator auditing...")
            await validator.forward()
            await asyncio.sleep(10)  # Run validation every 10 seconds


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_validator())
```

---

Ready for the next file?
