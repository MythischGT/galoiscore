from __future__ import annotations


class PrimeFieldElement:
    """An element of GF(p)."""

    __slots__ = ("num", "prime")

    def __init__(self, num: int, prime: int) -> None:
        object.__setattr__(self, "num", num)
        object.__setattr__(self, "prime", prime)

    def __setattr__(self, name, value):
        raise AttributeError("PrimeFieldElement is immutable.")

    def __repr__(self):
        return f"FieldElement_GFp({self.num}, p={self.prime})"

    def __hash__(self):
        return hash((self.num, self.prime))

    def _check_same_field(self, other):
        if not hasattr(other, "num") or not hasattr(other, "prime"):
            raise TypeError(
                f"Cannot operate on PrimeFieldElement and {type(other).__name__}."
            )
        if self.prime != other.prime:
            raise TypeError(
                f"Field mismatch: GF({self.prime}) vs GF({other.prime})."
            )
        return other

    def __add__(self, other):
        other = self._check_same_field(other)
        return PrimeFieldElement((self.num + other.num) % self.prime, self.prime)

    def __sub__(self, other):
        other = self._check_same_field(other)
        return PrimeFieldElement((self.num - other.num) % self.prime, self.prime)

    def __neg__(self):
        return PrimeFieldElement((-self.num) % self.prime, self.prime)

    def __mul__(self, other):
        other = self._check_same_field(other)
        return PrimeFieldElement((self.num * other.num) % self.prime, self.prime)

    def __pow__(self, exponent: int):
        if not isinstance(exponent, int):
            raise TypeError("Exponent must be an integer.")
        if exponent < 0:
            return self.inverse() ** (-exponent)
        reduced = exponent % (self.prime - 1)
        return PrimeFieldElement(pow(self.num, reduced, self.prime), self.prime)

    def __truediv__(self, other):
        other = self._check_same_field(other)
        return self * other.inverse()

    def inverse(self):
        if self.num == 0:
            raise ValueError("Zero element has no multiplicative inverse.")
        return PrimeFieldElement(pow(self.num, self.prime - 2, self.prime), self.prime)

    def is_zero(self):
        return self.num == 0

    def __bool__(self):
        return not self.is_zero()

    @property
    def field_order(self):
        return self.prime

    def __eq__(self, other):
        if not hasattr(other, "num") or not hasattr(other, "prime"):
            return False
        return self.num == other.num and self.prime == other.prime

    def __ne__(self, other):
        return not self.__eq__(other)


class PrimeField:
    """Factory for GF(p) elements."""

    def __init__(self, p: int, verify_prime: bool = False) -> None:
        if p < 2:
            raise ValueError(f"Field characteristic must be >= 2, got {p}.")
        if verify_prime:
            from utils.primes import is_prime
            if not is_prime(p):
                raise ValueError(f"{p} is not prime.")
        self.prime = p

    def __call__(self, num: int) -> PrimeFieldElement:
        if num >= self.prime or num < -(self.prime - 1):
            raise ValueError(f"{num} is out of range for GF({self.prime})")
        num = num % self.prime
        return PrimeFieldElement(num, self.prime)

    def zero(self):
        return PrimeFieldElement(0, self.prime)

    def one(self):
        return PrimeFieldElement(1, self.prime)

    def __repr__(self):
        return f"PrimeField(p={self.prime})"

    def __eq__(self, other):
        return isinstance(other, PrimeField) and self.prime == other.prime