import unittest
from galois_core.field import FieldElement

class TestFieldElement(unittest.TestCase):

    def setUp(self):
        # We use a small prime for easy manual verification if needed
        self.prime = 31

    def test_init_validation(self):
        """Ensure we cannot create invalid field elements."""
        with self.assertRaises(ValueError):
            FieldElement(31, self.prime) # Equal to prime
        with self.assertRaises(ValueError):
            FieldElement(-1, self.prime) # Negative
        with self.assertRaises(ValueError):
            FieldElement(32, self.prime) # Larger than prime

    def test_addition(self):
        a = FieldElement(2, self.prime)
        b = FieldElement(15, self.prime)
        # 2 + 15 = 17
        self.assertEqual(a + b, FieldElement(17, self.prime))
        
        # Wrap around: 17 + 21 = 38 % 31 = 7
        c = FieldElement(17, self.prime)
        d = FieldElement(21, self.prime)
        self.assertEqual(c + d, FieldElement(7, self.prime))

    def test_subtraction(self):
        a = FieldElement(29, self.prime)
        b = FieldElement(4, self.prime)
        # 29 - 4 = 25
        self.assertEqual(a - b, FieldElement(25, self.prime))
        
        # Negative result wrapping: 15 - 30 = -15 % 31 = 16
        c = FieldElement(15, self.prime)
        d = FieldElement(30, self.prime)
        self.assertEqual(c - d, FieldElement(16, self.prime))

    def test_multiplication(self):
        a = FieldElement(24, self.prime)
        b = FieldElement(19, self.prime)
        # 24 * 19 = 456 % 31 = 22
        self.assertEqual(a * b, FieldElement(22, self.prime))

    def test_pow(self):
        a = FieldElement(17, self.prime)
        # 17^3 = 4913 % 31 = 15
        self.assertEqual(a**3, FieldElement(15, self.prime))
        
        # Fermat's Little Theorem: a^(p-1) == 1
        self.assertEqual(a**(self.prime - 1), FieldElement(1, self.prime))

    def test_division(self):
        a = FieldElement(3, self.prime)
        b = FieldElement(24, self.prime)
        
        # 3 / 24 = 3 * 24^-1
        # 24 * 4 = 96 = 3 mod 31 -> Inverse of 24 is 4? No.
        # 24 * 22 = 528 % 31 = 1. Inverse of 24 is 22.
        # 3 * 22 = 66 % 31 = 4.
        self.assertEqual(a / b, FieldElement(4, self.prime))

        # Self-consistency check: (a / b) * b == a
        self.assertEqual((a / b) * b, a)

    def test_type_safety(self):
        """Ensure we can't operate on different fields."""
        a = FieldElement(3, 31)
        b = FieldElement(3, 13) # Different prime
        
        with self.assertRaises(TypeError):
            _ = a + b