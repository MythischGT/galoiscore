from __future__ import annotations
from .utils import modular_inverse

class FieldElement:
    """
    Represents an element in a Finite Field GF(p).
    """

    def __init__(self, num: int, prime: int):
        if num >= prime or num < 0:
            error_msg = f"Num {num} not in field range 0 to {prime - 1}"
            raise ValueError(error_msg)
        self.num = num
        self.prime = prime

    def __repr__(self):
        return f"FieldElement_{self.prime}({self.num})"

    def __eq__(self, other: object) -> bool:
        if other is None:
            return False
        if not isinstance(other, FieldElement):
            return False
        return self.num == other.num and self.prime == other.prime

    def __ne__(self, other: object) -> bool:
        return not (self == other)

    def _check_field(self, other: FieldElement):
        """Ensure the other element belongs to the same field."""
        if not isinstance(other, FieldElement):
             raise TypeError(f"Cannot operate on FieldElement and {type(other).__name__}")
        if self.prime != other.prime:
            raise TypeError(f"Cannot operate on numbers from different fields: {self.prime} vs {other.prime}")

    def __add__(self, other: FieldElement) -> FieldElement:
        self._check_field(other)
        num = (self.num + other.num) % self.prime
        return self.__class__(num, self.prime)

    def __sub__(self, other: FieldElement) -> FieldElement:
        self._check_field(other)
        num = (self.num - other.num) % self.prime
        return self.__class__(num, self.prime)

    def __mul__(self, other: FieldElement) -> FieldElement:
        self._check_field(other)
        num = (self.num * other.num) % self.prime
        return self.__class__(num, self.prime)

    def __pow__(self, exponent: int) -> FieldElement:
        # Note: Exponent is a regular integer, not a FieldElement!
        n = exponent % (self.prime - 1)  # Fermat's Little Theorem Optimization
        num = pow(self.num, n, self.prime)
        return self.__class__(num, self.prime)

    def __truediv__(self, other: FieldElement) -> FieldElement:
        """
        Modular Division: self / other
        Implemented as: self * inverse(other)
        """
        self._check_field(other)
        
        # Use our custom utility to find the inverse
        inv = modular_inverse(other.num, self.prime)
        
        num = (self.num * inv) % self.prime
        return self.__class__(num, self.prime)