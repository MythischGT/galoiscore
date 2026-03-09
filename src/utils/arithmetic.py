from __future__ import annotations

# Extended Euclidean Algorithm for computing gcd and modular inverse
def xgcd(a: int, b: int) -> tuple[int, int, int]:
    """Return gcd(a, b) and coefficients x, y such that ax + by = gcd(a, b)"""
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    return a, x0, y0

# Modular inverse using Extended Euclidean Algorithm
def mod_inverse(a: int, m: int) -> int:
    """Return the modular inverse of a modulo m using Extended Euclidean Algorithm"""
    try:
        return pow(a, -1, m)
    except ValueError:
        from math import gcd
        g = gcd(a, m)
        raise ZeroDivisionError(
            f"No modular inverse for {a} mod {m} since gcd is {g}"
        ) from None
    
# Constant-time utilities
def ct_equal(a: int, b: int) -> bool:
    """Constant-time equality check to prevent timing attacks"""
    diff = a ^ b
    result = 0

    while diff:
        result |= diff & 1
        diff >>= 1
    return result == 0

def ct_select(condition: bool, a: int, b: int) -> int:
    """Constant-time selection between a and b based on condition"""
    mask = -int(condition)  # All bits set to 1 if condition is True, else 0
    return (a & mask) | (b & ~mask)