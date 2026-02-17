**nash/__init__.py**

```python
"""NASH - Inter-Subnet Settlement Layer for Bittensor."""

__version__ = "0.1.0"

from nash.protocol import NashSynapse
from nash.miner import NashMiner
from nash.validator import NashValidator

__all__ = ["NashSynapse", "NashMiner", "NashValidator"]
```

---
