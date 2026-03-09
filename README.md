# GaloisCore

**GaloisCore** is a pure Python implementation of the mathematical primitives required for Elliptic Curve Cryptography (ECC).
It is designed as an educational "clean-room" implementation, avoiding black-box libraries like `openssl` or `cryptography` in favor of transparent, algebraic logic. This library serves as the foundation for higher-level protocols (DHKE, MQV, STS).

## Features

- **Finite Fields GF(p):** Full support for modular arithmetic (addition, subtraction, multiplication, division via Extended Euclidean Algorithm).
- **Elliptic Curves:** Weierstrass form implementation (y² = x³ + ax + b).
- **Group Laws:** Point addition, doubling, and scalar multiplication using the Montgomery ladder algorithm.
- **Named Curves:** Built-in support for secp256k1 and P-256.
- **Pure Python:** Zero external dependencies.

## Installation

Since this is a local development library, install it in editable mode:

```bash
git clone https://github.com/yourusername/GaloisCore.git
cd GaloisCore
pip install -e .[dev]
```

## Usage

```python
from core.prime import PrimeField
from crypto.ecc.curves import SEC_P256K1

# Finite field arithmetic
F = PrimeField(223)
x = F(192)
y = F(105)
print(x + y)   # FieldElement_GFp(74, p=223)

# Elliptic curve scalar multiplication
G = SEC_P256K1.G
n = SEC_P256K1.n
print((n * G).is_infinity())  # True
```

## Running Tests

```bash
python -m pytest tests/test_phase1.py -v
```

## Project Structure

```
src/
├── core/
│   ├── base.py       # Abstract base class for field elements
│   └── prime.py      # GF(p) prime field implementation
├── crypto/
│   └── ecc/
│       ├── point.py  # Elliptic curve point arithmetic
│       └── curves.py # Named curve parameters (secp256k1, P-256)
└── utils/
    ├── arithmetic.py # Extended GCD, modular inverse, constant-time helpers
    └── primes.py     # Miller-Rabin primality testing, prime generation
```

## Roadmap

- GF(2^m) binary fields
- GF(p^n) extension fields
- Higher-level protocols: DHKE, ECDH, ECDSA