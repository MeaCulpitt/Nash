**neurons/miner.py**

```python
"""
NASH Miner Neuron - Entry point for running the miner.

This is the main neuron file that wraps the optimized NashMiner implementation.
"""

import bittensor as bt
from nash.protocol import NashSynapse
from nash.miner import NashMiner as CoreMiner
import asyncio


class NashMiner(CoreMiner):
    """
    NASH Miner neuron - inherits from optimized core implementation.
    
    Usage:
        python neurons/miner.py --wallet.name my_wallet --subtensor.network finney
    """
    pass


async def main():
    """Main entry point for the miner."""
    bt.logging.info("Starting NASH Miner...")
    
    with NashMiner() as miner:
        bt.logging.info(f"Miner model info: {miner.get_model_info()}")
        
        while True:
            bt.logging.info("Miner running, waiting for requests...")
            await asyncio.sleep(60)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

---
