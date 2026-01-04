# GaloisCore

**GaloisCore** is a pure Python implementation of the mathematical primitives required for Elliptic Curve Cryptography (ECC). 

It is designed as an educational "clean-room" implementation, avoiding black-box libraries like `openssl` or `cryptography` in favor of transparent, algebraic logic. This library serves as the foundation for higher-level protocols (DHKE, MQV, STS).

## Features

* **Finite Fields (GF(p)):** Full support for modular arithmetic (addition, subtraction, multiplication, division via Extended Euclidean Algorithm).
* **Elliptic Curves:** Weierstrass form implementation ($y^2 = x^3 + ax + b$).
* **Group Laws:** Point addition, doubling, and scalar multiplication using the Double-and-Add algorithm.
* **Pure Python:** Zero external dependencies.

## Installation

Since this is a local development library, install it in editable mode:

```bash
git clone [https://github.com/yourusername/GaloisCore.git](https://github.com/yourusername/GaloisCore.git)
cd GaloisCore
pip install -e .[dev]