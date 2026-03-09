from __future__ import annotations
from typing import Union
from src.core.prime import PrimeField, PrimeFieldElement

class Point:
    __slots__ = ("x", "y", "a", "b")

    def __init__(
            self, 
            x: Union[PrimeFieldElement, None], 
            y: Union[PrimeFieldElement, None], 
            a: PrimeFieldElement, 
            b: PrimeFieldElement
        ) -> None:

        self.a = a
        self.b = b
        self.x = x
        self.y = y

        # Case 0: Point at Infinity (Identity Element)
        if self.x is None and self.y is None:
            return

        # Case 1: Validate the point is actually on the curve
        # Equation: y^2 = x^3 + ax + b
        if self.y is None or self.x is None:
             raise ValueError("Coordinates must be both None (Infinity) or both PrimeFieldElements")

        # Check curve equation
        lhs = self.y ** 2
        rhs = self.x ** 3 + self.a * self.x + self.b
        
        if lhs != rhs:
            raise ValueError(f"Point ({x}, {y}) is not on the curve y^2 = x^3 + {a.num}x + {b.num}")
        
    # Representation
    def __repr__(self) -> str:
        if self.x is None:
            return f"Point(Infinity) on curve y^2 = x^3 + {self.a.num}x + {self.b.num}"
        return f"Point({self.x.num}, {self.y.num})_a{self.a.num}_b{self.b.num} on curve y^2 = x^3 + {self.a.num}x + {self.b.num} over GF({self.x.prime})"
    
    def is_infinity(self) -> bool:
        return self.x is None and self.y is None
    
    # Equality
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return False
        return (
            self.x == other.x 
            and self.y == other.y 
            and self.a == other.a 
            and self.b == other.b
        )
    
    def __hash__(self) -> int:
        x_hash = hash(self.x) if self.x is not None else None
        y_hash = hash(self.y) if self.y is not None else None
        return hash((x_hash, y_hash, self.a, self.b))
    
    # Additive inverse
    def __neg__(self) -> Point:
        if self.is_infinity():
            return self
        return self.__class__(self.x, -self.y, self.a, self.b)
    
    # Point addition
    def __add__(self, other: Point) -> Point:

        if self.a != other.a or self.b != other.b:
            raise TypeError("Cannot add points from different curves.")

        if self.x is None:
            return other
        if other.x is None:
            return self

        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)

        # Use the field factory to create constants in the same field
        F = PrimeField(self.x.prime)

        if self == other:
            if self.y.num == 0:
                return self.__class__(None, None, self.a, self.b)
            # slope = (3x^2 + a) / (2y)
            three = F(3)
            two   = F(2)
            slope = (three * self.x ** 2 + self.a) / (two * self.y)
        else:
            slope = (other.y - self.y) / (other.x - self.x)

        x3 = slope ** 2 - self.x - other.x
        y3 = slope * (self.x - x3) - self.y

        return self.__class__(x3, y3, self.a, self.b)
    
    # Scalar multiplication using double-and-add algorithm
    def __rmul__(self, coefficient: int) -> Point:
        if not isinstance(coefficient, int):
            raise TypeError("Scalar multiplication requires an integer coefficient")
        
        if coefficient < 0:
            raise ValueError("Scalar multiplication does not support negative coefficients")
        
        if coefficient == 0:
            return self.__class__(None, None, self.a, self.b)  # Return the point at infinity
        
        identity = self.__class__(None, None, self.a, self.b)  # Point at infinity
        R0 = identity
        R1 = self
        
        for bit_index in range(coefficient.bit_length() - 1, -1, -1):
            bit = (coefficient >> bit_index) & 1
            if bit == 0:
                R1 = R0 + R1  # R1 = R0 + R1
                R0 = R0 + R0  # R0 = 2R0
            else:
                R0 = R0 + R1  # R0 = R0 + R1
                R1 = R1 + R1  # R1 = 2R1
        
        return R0
    
    def __mul__(self, coefficient: int) -> Point:
        return self.__rmul__(coefficient)