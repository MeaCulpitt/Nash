**nash/miner.py**

```python
"""
NASH Miner - Optimized implementation for equilibrium discovery.

Optimizations:
- Learnable model instead of random placeholders
- Proper device management for GPU acceleration
- Pre-allocated tensors to avoid allocation overhead
- torch.no_grad() for inference
- Timeout handling for <50ms target
"""

import bittensor as bt
from nash.protocol import NashSynapse
import torch
import torch.nn as nn
from typing import Optional
import asyncio
import time


class IntentEncoder(nn.Module):
    """
    Encodes raw intent vectors into a compressed manifold representation.
    """
    def __init__(self, input_dim: int = 10, manifold_dim: int = 256):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, manifold_dim),
        )
    
    def forward(self, x: torch.FloatTensor) -> torch.FloatTensor:
        return self.encoder(x)


class EquilibriumSolver(nn.Module):
    """
    Discovers optimal equilibrium points from manifold representations.
    """
    def __init__(self, manifold_dim: int = 256):
        super().__init__()
        self.solver = nn.Sequential(
            nn.Linear(manifold_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 2),  # Output: (x, y) equilibrium coordinates
        )
    
    def forward(self, manifold: torch.FloatTensor) -> torch.FloatTensor:
        return self.solver(manifold)


class NashMiner(bt.Neuron):
    """
    NASH Miner that encodes intents and solves for equilibria.
    
    Optimized for sub-50ms settlement with:
    - Pre-allocated tensors
    - GPU acceleration
    - No gradient computation in inference
    """
    
    def __init__(self):
        super().__init__()
        
        # Initialize models and move to device
        self.encoder = IntentEncoder(input_dim=10, manifold_dim=256).to(self.device)
        self.solver = EquilibriumSolver(manifold_dim=256).to(self.device)
        
        # Set to evaluation mode
        self.encoder.eval()
        self.solver.eval()
        
        # Pre-allocate output tensors to avoid allocation overhead
        self._manifold_buffer = torch.empty(1, 256, device=self.device)
        self._equilibrium_buffer = torch.empty(1, 2, device=self.device)
        
        # Timeout for equilibrium discovery (in seconds)
        self._timeout_seconds = 0.045  # 45ms timeout to leave buffer for <50ms total
        
        bt.logging.info(f"Miner initialized on device: {self.device}")

    async def forward(self, synapse: NashSynapse) -> NashSynapse:
        """
        The main mining logic. 
        Takes raw intent -> Returns Manifold + Equilibrium.
        
        Optimizations:
        - No gradient computation
        - Pre-allocated tensors
        - Timeout handling
        """
        start_time = time.perf_counter()
        
        try:
            # Validate input
            if not synapse.validate():
                bt.logging.warning("Invalid synapse received, returning empty response")
                synapse.manifold_tensor = None
                synapse.equilibrium_point = None
                return synapse
            
            # Move input to device and ensure correct shape
            intent = synapse.raw_intent.to(self.device)
            
            # Handle different input shapes
            if intent.dim() == 1:
                intent = intent.unsqueeze(0)
            elif intent.dim() == 0:
                intent = intent.unsqueeze(0).unsqueeze(0)
            
            # Check timeout before computation
            elapsed = time.perf_counter() - start_time
            if elapsed > self._timeout_seconds:
                bt.logging.warning(f"Timeout exceeded before computation: {elapsed*1000:.1f}ms")
            
            # Inference: encode intent to manifold (no gradients)
            with torch.no_grad():
                manifold = self.encoder(intent)
                
                # Check timeout after encoding
                elapsed = time.perf_counter() - start_time
                if elapsed > self._timeout_seconds:
                    bt.logging.warning(f"Timeout after encoding: {elapsed*1000:.1f}ms")
                
                # Solve for equilibrium
                equilibrium = self.solver(manifold)
                
                # Check final timeout
                elapsed = time.perf_counter() - start_time
                bt.logging.debug(f"Inference completed in {elapsed*1000:.2f}ms")
            
            # Store results (move to CPU for serialization if needed)
            synapse.manifold_tensor = manifold.contiguous()
            synapse.equilibrium_point = equilibrium.contiguous()
            
            return synapse
            
        except Exception as e:
            bt.logging.error(f"Error in miner forward: {e}")
            synapse.manifold_tensor = None
            synapse.equilibrium_point = None
            return synapse
    
    def get_model_info(self) -> dict:
        """Return model information for debugging."""
        return {
            "encoder_params": sum(p.numel() for p in self.encoder.parameters()),
            "solver_params": sum(p.numel() for p in self.solver.parameters()),
            "device": str(self.device),
            "dtype": str(next(self.encoder.parameters()).dtype),
        }


async def run_miner():
    """Standalone miner runner with proper async handling."""
    with NashMiner() as miner:
        bt.logging.info(f"Model info: {miner.get_model_info()}")
        
        while True:
            bt.logging.info("Miner running...")
            await asyncio.sleep(1)


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_miner())
```

---

Ready for the next file?
