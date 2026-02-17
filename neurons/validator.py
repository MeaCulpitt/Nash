**neurons/validator.py**

```python
"""
NASH Validator Neuron - Entry point for running the validator.

This is the main neuron file that wraps the optimized NashValidator implementation.
"""

import bittensor as bt
from nash.protocol import NashSynapse
from nash.validator import NashValidator as CoreValidator
import asyncio


class NashValidator(CoreValidator):
    """
    NASH Validator neuron - inherits from optimized core implementation.
    
    Usage:
        python neurons/validator.py --wallet.name my_wallet --subtensor.network finney
    """
    pass


async def main():
    """Main entry point for the validator."""
    bt.logging.info("Starting NASH Validator...")
    
    with NashValidator() as validator:
        bt.logging.info(f"Validator scorer info: {validator.get_scorer_info()}")
        
        while True:
            bt.logging.info("Running validation round...")
            await validator.forward()
            await asyncio.sleep(10)


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_validator())
```

---
