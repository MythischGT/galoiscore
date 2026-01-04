from src.galois_core.field import FieldElement
from src.galois_core.ecc import Point

prime = 223
a = FieldElement(0, prime)
b = FieldElement(7, prime)

x = FieldElement(192, prime)
y = FieldElement(105, prime)

p1 = Point(x, y, a, b)

print(f"Base Point: {p1}")

# Test 1: Point Doubling
p2 = p1 + p1
print(f"2 * P (Add): {p2}")

# Test 2: Scalar Multiplication
p2_scalar = 2 * p1
print(f"2 * P (Scalar): {p2_scalar}")

# Expected values for verification
expected_x = FieldElement(49, prime)
expected_y = FieldElement(71, prime)

assert p2.x == expected_x
assert p2.y == expected_y
assert p2 == p2_scalar

print("SUCCESS: ECC Arithmetic verified.")