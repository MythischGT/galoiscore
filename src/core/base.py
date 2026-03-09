from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TypeVar

# Generic type variable bound to FieldElementBase, used for return type hints
# so that subclass methods can declare they return their own type, not the base.
F = TypeVar("F", bound="FieldElementBase")

class FieldElementBase(ABC):
    """Abstract base class for field elements. Subclasses must implement the
    arithmetic operations and ensure that all elements belong to the same field.
    """

    @abstractmethod
    def __add__(self, other: F) -> F:
        pass

    @abstractmethod
    def __sub__(self, other: F) -> F:
        pass

    @abstractmethod
    def __mul__(self, other: F) -> F:
        pass

    @abstractmethod
    def __pow__(self, exponent: int) -> F:
        pass

    @abstractmethod
    def __truediv__(self, other: F) -> F:
        pass

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        pass

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    @abstractmethod
    def inverse(self) -> F:
        """Return the multiplicative inverse of this field element."""
        pass

    @classmethod
    @abstractmethod
    def is_zero(self) -> bool:
        """Return True if this field element is the additive identity (zero)."""
        pass

    @classmethod
    @abstractmethod
    def zero(cls: type[F]) -> F:
        """Return the additive identity (zero) of the field."""
        pass

    @classmethod
    @abstractmethod
    def one(cls: type[F]) -> F:
        """Return the multiplicative identity (one) of the field."""
        pass

    @property
    @abstractmethod
    def field_order(self) -> int:
        """Return the order of the field (e.g., prime p for GF(p))."""
        pass

    def __bool__(self):
        return not self.is_zero()