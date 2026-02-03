import bittensor as bt
import typing
import torch

class NashSynapse(bt.Synapse):
    """
    The Nash Synapse protocol for high-frequency economic negotiation.
    """
    # --- Input (Filled by Validator) ---
    # raw_intent: N-dimensional vector of requirements [Price, Latency, Reliability, etc.]
    raw_intent: torch.FloatTensor = None
    
    # context: Additional metadata (e.g. "Hardware: H100", "Region: US-East")
    context: typing.Optional[dict] = None

    # --- Output (Filled by Miner) ---
    # manifold_tensor: Compressed hypernetwork weights (The Nash Manifold)
    manifold_tensor: typing.Optional[torch.FloatTensor] = None

    # equilibrium_point: The proposed (x, y) coordinates for the transaction
    equilibrium_point: typing.Optional[torch.FloatTensor] = None

    def deserialize(self) -> typing.Tuple[torch.FloatTensor, torch.FloatTensor]:
        """
        Returns a tuple of (manifold, equilibrium)
        """
        return self.manifold_tensor, self.equilibrium_point
