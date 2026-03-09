from __future__ import annotations
from typing import Union
from .base import FieldElementBase

class PrimeFieldElement(FieldElementBase):
    __slots__ = ("num", "prime")

    def __init__(self, num: int, prime: int) -> None:
        if not 0 <= num < prime:
            raise ValueError(
                f"Num {num} not in field range 0 to {prime - 1}"
            )
        
        object.__setattr__(self, "num", num)
        object.__setattr__(self, "prime", prime)

    def __setattr__(self, name: str, value: object) -> None:
        raise AttributeError("FieldElement instances are immutable")
    
    # Representation
    def __repr__(self) -> str:
        return f"FieldElement_GFp{self.prime}({self.num})"