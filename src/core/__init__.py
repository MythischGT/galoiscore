"""
GaloisCore: A pure Python finite field arithmetic library.

Phase 1 exposes:
    - PrimeField       : GF(p) field factory
    - PrimeFieldElement: Elements of GF(p)
    - Point            : Elliptic curve points over GF(p)
    - curves           : Named curve constants (secp256k1, P-256, P-384)
"""

from .core.prime import PrimeField, PrimeFieldElement
from .crypto.ecc.point import Point
from .crypto.ecc import curves

__version__ = "0.2.0"

__all__ = [
    "PrimeField",
    "PrimeFieldElement",
    "Point",
    "curves",
]
