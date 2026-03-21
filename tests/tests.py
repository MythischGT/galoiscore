import os
import sys
import unittest

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR  = os.path.normpath(os.path.join(THIS_DIR, '..', 'src'))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from core.prime import PrimeField
from crypto.ecc.curves import P_256, SEC_P256K1, get_curve
from crypto.ecc.point import Point
from utils.arithmetic import xgcd, mod_inverse, ct_equal, ct_select
from utils.primes import is_prime, next_prime, generate_large_prime


# ===========================================================================
# PrimeField
# ===========================================================================

class TestPrimeField(unittest.TestCase):

    def test_field_creation(self):
        F = PrimeField(223)
        self.assertEqual(F.prime, 223)

    def test_field_element_creation(self):
        F = PrimeField(223)
        x = F(192)
        self.assertEqual(x.num, 192)
        self.assertEqual(x.prime, 223)

    def test_zero(self):
        F = PrimeField(223)
        zero = F(0)
        self.assertEqual(zero.num, 0)
        self.assertTrue(zero.is_zero())

    def test_one(self):
        F = PrimeField(223)
        one = F(1)
        self.assertEqual(one.num, 1)
        self.assertFalse(one.is_zero())

    def test_out_of_range(self):
        F = PrimeField(223)
        with self.assertRaises(ValueError):
            F(223)
        with self.assertRaises(ValueError):
            F(500)

    def test_verify_prime(self):
        for bad in (15, 1, 0, -7):
            with self.subTest(value=bad):
                with self.assertRaises(ValueError):
                    PrimeField(bad, verify_prime=True)

    def test_immutable_elements(self):
        F = PrimeField(223)
        x = F(192)
        with self.assertRaises(AttributeError):
            x.num = 100
        with self.assertRaises(AttributeError):
            x.prime = 101

    def test_representation(self):
        F = PrimeField(223)
        x = F(192)
        self.assertIn("192", repr(x))
        self.assertIn("223", repr(x))


# ===========================================================================
# PrimeFieldElement
# ===========================================================================

class TestPrimeFieldElement(unittest.TestCase):

    def setUp(self):
        self.F = PrimeField(223)

    def test_addition(self):
        F = self.F
        self.assertEqual(F(192) + F(105), F(74))   # 297 mod 223 = 74
        self.assertEqual(F(0)   + F(0),   F(0))
        self.assertEqual(F(222) + F(1),   F(0))

    def test_subtraction(self):
        F = self.F
        self.assertEqual(F(192) - F(105), F(87))
        self.assertEqual(F(0)   - F(0),   F(0))
        self.assertEqual(F(0)   - F(1),   F(222))

    def test_multiplication(self):
        F = self.F
        self.assertEqual(F(192) * F(105), F(90))   # 20160 mod 223 = 90
        self.assertEqual(F(0)   * F(105), F(0))
        self.assertEqual(F(222) * F(1),   F(222))

    def test_negation(self):
        F = self.F
        self.assertEqual(-F(192), F(31))
        self.assertEqual(-F(0),   F(0))
        self.assertEqual(-F(222), F(1))

    def test_exponentiation(self):
        F = self.F
        self.assertEqual(F(192) ** 2,   F(69))
        self.assertEqual(F(192) ** 3,   F(91))
        self.assertEqual(F(0)   ** 5,   F(0))
        self.assertEqual(F(1)   ** 100, F(1))
        self.assertEqual(F(222) ** 2,   F(1))

    def test_negative_exponentiation(self):
        F = self.F
        self.assertEqual(F(192) ** -1, F(187))
        self.assertEqual(F(105) ** -1, F(17))
        with self.assertRaises(ValueError):
            F(0) ** -1

    def test_division(self):
        F = self.F
        self.assertEqual(F(192) / F(105), F(142))
        self.assertEqual(F(105) / F(192), F(11))
        with self.assertRaises(ValueError):
            F(192) / F(0)

    def test_inverse(self):
        F = self.F
        self.assertEqual(F(192).inverse(), F(187))
        self.assertEqual(F(105).inverse(), F(17))
        with self.assertRaises(ValueError):
            F(0).inverse()

    def test_cross_field_operations(self):
        F = self.F
        with self.assertRaises(TypeError):
            F(192) + 5
        with self.assertRaises(TypeError):
            F(192) - 5
        with self.assertRaises(TypeError):
            F(192) * 5
        with self.assertRaises(TypeError):
            F(192) / 5

    def test_equality(self):
        F = self.F
        self.assertEqual(F(192), F(192))
        self.assertNotEqual(F(192), F(193))
        self.assertEqual(F(0),   F(0))
        self.assertEqual(F(222), F(-1))

    def test_boolean_context(self):
        F = self.F
        self.assertFalse(bool(F(0)))
        self.assertTrue(bool(F(1)))
        self.assertTrue(bool(F(222)))

    def test_field_order(self):
        F = self.F
        self.assertEqual(F(192).field_order, 223)
        self.assertEqual(F(0).field_order,   223)
        self.assertEqual(F(222).field_order, 223)


# ===========================================================================
# Point
# ===========================================================================

class TestPoint(unittest.TestCase):

    def _curve(self, prime=223):
        F = PrimeField(prime)
        return F, F(0), F(7)

    def test_valid_point(self):
        F, a, b = self._curve()
        p = Point(F(192), F(105), a, b)
        self.assertEqual(p.x, F(192))
        self.assertEqual(p.y, F(105))
        self.assertEqual(p.a, a)
        self.assertEqual(p.b, b)

    def test_invalid_point(self):
        F, a, b = self._curve()
        with self.assertRaises(ValueError):
            Point(F(200), F(119), a, b)
        with self.assertRaises(ValueError):
            Point(F(1), F(1), a, b)

    def test_point_at_infinity(self):
        F, a, b = self._curve()
        inf = Point(None, None, a, b)
        self.assertTrue(inf.is_infinity())
        self.assertIsNone(inf.x)
        self.assertIsNone(inf.y)

    def test_mixed_coordinates(self):
        F, a, b = self._curve()
        with self.assertRaises(ValueError):
            Point(F(192), None, a, b)
        with self.assertRaises(ValueError):
            Point(None, F(105), a, b)

    def test_identity_addition(self):
        F, a, b = self._curve()
        inf = Point(None, None, a, b)
        p   = Point(F(192), F(105), a, b)
        self.assertEqual(p + inf, p)
        self.assertEqual(inf + p, p)

    def test_additive_inverse(self):
        F, a, b = self._curve()
        p = Point(F(192), F(105), a, b)
        self.assertTrue((p + (-p)).is_infinity())

    def test_point_doubling(self):
        F, a, b = self._curve()
        p = Point(F(192), F(105), a, b)
        d = p + p
        self.assertEqual(d.x, F(49))
        self.assertEqual(d.y, F(71))

    def test_scalar_multiplication(self):
        F, a, b = self._curve()
        p = Point(F(192), F(105), a, b)
        d = 2 * p
        self.assertEqual(d.x, F(49))
        self.assertEqual(d.y, F(71))

    def test_scalar_multiplication_matches_addition(self):
        F, a, b = self._curve()
        p = Point(F(192), F(105), a, b)
        self.assertEqual(p + p, 2 * p)

    def test_scalar_multiplication_zero(self):
        F, a, b = self._curve()
        p = Point(F(192), F(105), a, b)
        self.assertTrue((0 * p).is_infinity())

    def test_scalar_multiplication_one(self):
        F, a, b = self._curve()
        p = Point(F(192), F(105), a, b)
        self.assertEqual(1 * p, p)

    def test_p_times_k_equals_k_times_p(self):
        F, a, b = self._curve()
        p = Point(F(192), F(105), a, b)
        self.assertEqual(p * 3, 3 * p)

    def test_commutativity(self):
        F, a, b = self._curve()
        P = Point(F(192), F(105), a, b)
        Q = Point(F(17),  F(56),  a, b)
        self.assertEqual(P + Q, Q + P)

    def test_associativity(self):
        F, a, b = self._curve()
        P = Point(F(192), F(105), a, b)
        Q = Point(F(17),  F(56),  a, b)
        R = Point(F(1),   F(193), a, b)
        self.assertEqual((P + Q) + R, P + (Q + R))

    def test_different_curves(self):
        F1, a1, b1 = self._curve(prime=223)
        F2, a2, b2 = self._curve(prime=227)
        p1 = Point(F1(192), F1(105), a1, b1)
        p2 = Point(F2(0),   F2(37),  a2, b2)
        with self.assertRaises(TypeError):
            p1 + p2

    def test_scalar_non_integer(self):
        F, a, b = self._curve()
        p = Point(F(192), F(105), a, b)
        with self.assertRaises(TypeError):
            p * 2.5
        with self.assertRaises(TypeError):
            p * "3"

    def test_repr_infinity(self):
        F, a, b = self._curve()
        inf = Point(None, None, a, b)
        self.assertIn("Infinity", repr(inf))


# ===========================================================================
# Named curves
# ===========================================================================

class TestCurves(unittest.TestCase):

    def test_secp256k1_generator_on_curve(self):
        self.assertFalse(SEC_P256K1.G.is_infinity())

    def test_secp256k1_order(self):
        result = SEC_P256K1.n * SEC_P256K1.G
        self.assertTrue(result.is_infinity(), f"Expected infinity, got {result}")

    def test_p256_generator_on_curve(self):
        self.assertFalse(P_256.G.is_infinity())

    def test_p256_order(self):
        self.assertTrue((P_256.n * P_256.G).is_infinity())

    def test_get_curve_valid(self):
        curve = get_curve("secp256k1")
        self.assertEqual(curve.name, "secp256k1")

    def test_get_curve_invalid(self):
        with self.assertRaises(KeyError):
            get_curve("nonexistent_curve")

    def test_secp256k1_known_scalar(self):
        """2 * G must match a known precomputed value (SEC 2 test vector)."""
        two_G = 2 * SEC_P256K1.G
        expected_x = 0xC6047F9441ED7D6D3045406E95C07CD85C778E4B8CEF3CA7ABAC09B95C709EE5
        self.assertEqual(two_G.x.num, expected_x)


# ===========================================================================
# Utils: arithmetic
# ===========================================================================

class TestXGCD(unittest.TestCase):

    def test_basic(self):
        g, x, y = xgcd(35, 15)
        self.assertEqual(g, 5)
        self.assertEqual(35 * x + 15 * y, g)

    def test_coprime(self):
        g, x, y = xgcd(3, 11)
        self.assertEqual(g, 1)
        self.assertEqual(3 * x + 11 * y, 1)

    def test_one(self):
        g, x, y = xgcd(1, 5)
        self.assertEqual(g, 1)

    def test_commutative_gcd(self):
        g1, _, _ = xgcd(12, 8)
        g2, _, _ = xgcd(8, 12)
        self.assertEqual(g1, 4)
        self.assertEqual(g2, 4)


class TestModularInverse(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(mod_inverse(3, 11), 4)

    def test_inverse_of_inverse(self):
        inv = mod_inverse(7, 11)
        self.assertEqual(mod_inverse(inv, 11), 7)

    def test_non_invertible_raises(self):
        with self.assertRaises(ZeroDivisionError):
            mod_inverse(4, 8)


class TestConstantTime(unittest.TestCase):

    def test_ct_equal_true(self):
        self.assertTrue(ct_equal(42, 42))
        self.assertTrue(ct_equal(0, 0))

    def test_ct_equal_false(self):
        self.assertFalse(ct_equal(42, 43))
        self.assertFalse(ct_equal(0, 1))

    def test_ct_select_true(self):
        self.assertEqual(ct_select(True, 10, 20), 10)

    def test_ct_select_false(self):
        self.assertEqual(ct_select(False, 10, 20), 20)


# ===========================================================================
# Utils: primes
# ===========================================================================

class TestIsPrime(unittest.TestCase):

    def test_small_primes(self):
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 223]:
            with self.subTest(p=p):
                self.assertTrue(is_prime(p))

    def test_composites(self):
        for n in [0, 1, 4, 6, 8, 9, 10, 15, 221, 224]:
            with self.subTest(n=n):
                self.assertFalse(is_prime(n))

    def test_large_prime(self):
        p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        self.assertTrue(is_prime(p))

    def test_secp256k1_order_is_prime(self):
        n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        self.assertTrue(is_prime(n))


class TestNextPrime(unittest.TestCase):

    def test_already_prime(self):
        self.assertEqual(next_prime(11),  11)
        self.assertEqual(next_prime(223), 223)

    def test_composite_input(self):
        self.assertEqual(next_prime(10), 11)
        self.assertEqual(next_prime(14), 17)

    def test_edge_cases(self):
        self.assertEqual(next_prime(2), 2)
        self.assertEqual(next_prime(1), 2)


class TestGeneratePrime(unittest.TestCase):

    def test_correct_bit_length(self):
        p = generate_large_prime(64)
        self.assertEqual(p.bit_length(), 64)
        self.assertTrue(is_prime(p))

    def test_different_each_call(self):
        p1 = generate_large_prime(128)
        p2 = generate_large_prime(128)
        self.assertTrue(is_prime(p1) and p1.bit_length() == 128)
        self.assertTrue(is_prime(p2) and p2.bit_length() == 128)

    def test_invalid_bit_length(self):
        with self.assertRaises(ValueError):
            generate_large_prime(1)


if __name__ == "__main__":
    unittest.main(verbosity=2)