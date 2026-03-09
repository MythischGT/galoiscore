"""
utils.py

Helper functions for number theoretic operations required by Finite Fields
and Elliptic Curves.
"""

def xgcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Extended Euclidean Algorithm.
    
    Computes g, x, y such that:
    a*x + b*y = g = gcd(a, b)
    
    Args:
        a: First integer
        b: Second integer (modulus)
        
    Returns:
        tuple(g, x, y)
    """
    x0, x1, y0, y1 = 1, 0, 0, 1
    
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
        
    return a, x0, y0

def modular_inverse(a: int, n: int) -> int:
    """
    Computes the modular multiplicative inverse of a modulo n.
    
    Solves for x in: (a * x) % n == 1
    
    Args:
        a: The integer to invert
        n: The modulus (must be prime for a field)
        
    Returns:
        int: The inverse x
        
    Raises:
        ValueError: If a is not invertible modulo n (i.e., gcd(a, n) != 1)
    """
    g, x, _ = xgcd(a, n)
    
    if g != 1:
        raise ValueError(f"{a} has no inverse modulo {n} (GCD is {g})")
    
    # x might be negative from xgcd, so we wrap it modulo n
    return x % n