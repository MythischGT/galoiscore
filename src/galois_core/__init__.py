"""
GaloisCore: A pure Python implementation of ECC primitives.

This package exposes the foundational mathematical structures:
1. FieldElement: Modular arithmetic in GF(p).
2. Point: Elliptic Curve arithmetic over GF(p).
"""

# We import these classes here to flatten the namespace for the user.
# Note: These imports will fail until we create field.py and ecc.py.
from .field import FieldElement
from .ecc import Point

# We do NOT expose 'utils' or 'xgcd' here. 
# Those are internal implementation details.

__all__ = [
    "FieldElement",
    "Point",
]

__version__ = "0.1.0"