from __future__ import annotations
from typing import Union
from .field import FieldElement

class Point:
    """
    Represents a point P(x, y) on the elliptic curve y^2 = x^3 + ax + b.
    """

    def __init__(self, x: Union[FieldElement, None], y: Union[FieldElement, None], 
                 a: FieldElement, b: FieldElement):
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
             raise ValueError("Coordinates must be both None (Infinity) or both FieldElements")

        # Check curve equation
        # We use the overloaded operators from FieldElement here!
        lhs = self.y ** 2
        rhs = self.x ** 3 + self.a * self.x + self.b
        
        if lhs != rhs:
            raise ValueError(f"Point ({x}, {y}) is not on the curve y^2 = x^3 + {a.num}x + {b.num}")

    def __repr__(self):
        if self.x is None:
            return "Point(Infinity)"
        return f"Point({self.x.num}, {self.y.num})_a{self.a.num}_b{self.b.num}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return False
        return (self.x == other.x and self.y == other.y and 
                self.a == other.a and self.b == other.b)

    def __add__(self, other: Point) -> Point:
        if self.a != other.a or self.b != other.b:
            raise TypeError("Points are not on the same curve")

        # Case 1: Identity Element (I + P = P)
        if self.x is None:
            return other
        if other.x is None:
            return self

        # Case 2: Vertical Line / Additive Inverse (P + (-P) = 0)
        # x1 == x2 and y1 != y2 (or y1 == -y2)
        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)

        # Case 3: Tangent Line / Point Doubling (P == Q)
        # x1 == x2 and y1 == y2
        if self == other:
            # Special sub-case: if y == 0, the tangent is vertical -> Infinity
            if self.y.num == 0:
                return self.__class__(None, None, self.a, self.b)
            
            # Slope s = (3x^2 + a) / (2y)
            three = FieldElement(3, self.x.prime)
            two = FieldElement(2, self.x.prime)
            
            slope = (three * self.x**2 + self.a) / (two * self.y)

            # Case 4: General Addition (P != Q)
        # Case 4: General Addition (P != Q)
        else:
            # Slope s = (y2 - y1) / (x2 - x1)
            slope = (other.y - self.y) / (other.x - self.x)

        # Calculate new intersection point (x3, y3)
        # x3 = s^2 - x1 - x2
        x3 = slope**2 - self.x - other.x
        
        # y3 = s(x1 - x3) - y1
        y3 = slope * (self.x - x3) - self.y
        
        return self.__class__(x3, y3, self.a, self.b)

    def __rmul__(self, coefficient: int) -> Point:
        """
        Scalar Multiplication (k * P) using Double-and-Add algorithm.
        O(log k) complexity.
        """
        if not isinstance(coefficient, int):
             raise TypeError("Scalar multiplication requires an integer coefficient")
             
        # Initialize result as Point at Infinity
        current = self
        result = self.__class__(None, None, self.a, self.b)
        
        # Iterate bits of the scalar from LSB to MSB? 
        # Actually, iterating LSB to MSB is easier for 'current = current + current' logic
        while coefficient:
            if coefficient & 1: # If LSB is 1
                result = result + current
            current = current + current # Double the point
            coefficient >>= 1 # Shift right
            
        return result