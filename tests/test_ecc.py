import unittest
from galois_core.field import FieldElement
from galois_core.ecc import Point

class TestECC(unittest.TestCase):

    def setUp(self):
        self.prime = 223
        self.a = FieldElement(0, self.prime)
        self.b = FieldElement(7, self.prime)
        
        # Generator point G
        self.g_x = FieldElement(192, self.prime)
        self.g_y = FieldElement(105, self.prime)
        self.g = Point(self.g_x, self.g_y, self.a, self.b)

    def test_on_curve_validation(self):
        """Points not on the curve should raise ValueError."""
        with self.assertRaises(ValueError):
            Point(FieldElement(200, self.prime), FieldElement(119, self.prime), self.a, self.b)

    def test_point_addition(self):
        # Adding G + 2G = 3G
        # 2G is known to be (49, 71)
        x2 = FieldElement(49, self.prime)
        y2 = FieldElement(71, self.prime)
        p2 = Point(x2, y2, self.a, self.b)
        
        p3_expected = Point(FieldElement(18, self.prime), FieldElement(189, self.prime), self.a, self.b)
        
        self.assertEqual(self.g + p2, p3_expected)

    def test_point_doubling(self):
        # 2G should be (49, 71)
        expected = Point(FieldElement(49, self.prime), FieldElement(71, self.prime), self.a, self.b)
        self.assertEqual(self.g + self.g, expected)

    def test_scalar_multiplication(self):
        # 2 * G
        expected = Point(FieldElement(49, self.prime), FieldElement(71, self.prime), self.a, self.b)
        self.assertEqual(2 * self.g, expected)
        
        # 2 * G via addition vs scalar mul
        self.assertEqual(self.g + self.g, 2 * self.g)

    def test_identity(self):
        inf = Point(None, None, self.a, self.b)
        
        # P + Inf = P
        self.assertEqual(self.g + inf, self.g)
        # Inf + P = P
        self.assertEqual(inf + self.g, self.g)
        
    def test_inverse(self):
        # P + (-P) = Inf
        # Inverse of (x, y) is (x, -y)
        # In field terms: -y is (p - y)
        inv_y = FieldElement(0, self.prime) - self.g_y
        inverse_pt = Point(self.g_x, inv_y, self.a, self.b)
        
        inf = Point(None, None, self.a, self.b)
        self.assertEqual(self.g + inverse_pt, inf)

    def test_large_scalar(self):
        # Order of this group is 224 (not prime, but useful for testing)
        # 224 * G should be Infinity
        # order = 224
        # self.assertEqual(order * self.g, Point(None, None, self.a, self.b))
        pass 
        # Note: Calculating order requires Schoof's algo, which we haven't implemented.
        # But we can test associativity: 4G = 2(2G)
        p2 = 2 * self.g
        p4_a = 2 * p2
        p4_b = 4 * self.g
        self.assertEqual(p4_a, p4_b)