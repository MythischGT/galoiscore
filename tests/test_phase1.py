import pytest

from src.crypto.ecc.curves import P_256, SEC_P256K1, get_curve
from src.core.prime import PrimeField
from src.crypto.ecc.point import Point
from src.utils.arithmetic import xgcd, mod_inverse, ct_equal, ct_select
from src.utils.primes import is_prime, next_prime, generate_large_prime

# Fixtures
@pytest.fixture
def F223():
    return PrimeField(223)

@pytest.fixture
def small_curve(F223):
    a = F223(0)
    b = F223(7)
    return a, b, F223

# PrimeField Tests

class TestPrimeField:
    def test_field_creation(self):
        F = PrimeField(223)
        assert F.prime == 223
    
    def test_field_element_creation(self, F223):
        x = F223(192)
        assert x.num == 192
        assert x.prime == 223
    
    def test_zero(self, F223):
        zero = F223(0)
        assert zero.num == 0
        assert zero.is_zero()

    def test_one(self, F223):
        one = F223(1)
        assert one.num == 1
        assert not one.is_zero()

    def test_out_of_range(self, F223):
        with pytest.raises(ValueError):
            F223(223)  # Should wrap to 0
        with pytest.raises(ValueError):
            F223(500)   # Too large

    def test_verify_prime(self):
        with pytest.raises(ValueError):
            PrimeField(15, verify_prime = True)  # Not prime
        with pytest.raises(ValueError):
            PrimeField(1, verify_prime = True)   # Not prime
        with pytest.raises(ValueError):
            PrimeField(0, verify_prime = True)   # Not prime
        with pytest.raises(ValueError):
            PrimeField(-7, verify_prime = True)  # Not prime
    
    def test_immutable_elements(self, F223):
        x = F223(192)
        with pytest.raises(AttributeError):
            x.num = 100  # Should not be able to modify num
        with pytest.raises(AttributeError):
            x.prime = 101  # Should not be able to modify prime
    
    def test_representation(self, F223):
        x = F223(192)
        assert "192" in repr(x)
        assert "223" in repr(x)


# PrimeFieldElement Tests

class TestPrimeFieldElement:
    def test_addition(self, F223):
        assert F223(192) + F223(105) == F223(74)  # 297 mod 223 = 74
        assert F223(0) + F223(0) == F223(0)
        assert F223(222) + F223(1) == F223(0)

    def test_subtraction(self, F223):
        assert F223(192) - F223(105) == F223(87)  # 87 mod 223 = 87
        assert F223(0) - F223(0) == F223(0)
        assert F223(0) - F223(1) == F223(222)

    def test_multiplication(self, F223):
        assert F223(192) * F223(105) == F223(90)  # 20160 mod 223 = 90
        assert F223(0) * F223(105) == F223(0)
        assert F223(222) * F223(1) == F223(222)

    def test_negation(self, F223):
        assert -F223(192) == F223(31)  # -192 mod 223 = 31
        assert -F223(0) == F223(0)
        assert -F223(222) == F223(1)

    def test_exponentiation(self, F223):
        assert F223(192) ** 2 == F223(69)  # 36864 mod 223 = 69
        assert F223(192) ** 3 == F223(91)   # 7077888 mod 223 = 91
        assert F223(0) ** 5 == F223(0)
        assert F223(1) ** 100 == F223(1)
        assert F223(222) ** 2 == F223(1)    # 49284 mod 223 = 1
    
    def test_negative_exponentiation(self, F223):
        assert F223(192) ** -1 == F223(187)  # 187 is the multiplicative inverse of 192 mod 223
        assert F223(105) ** -1 == F223(17)  # 17 is the multiplicative inverse of 105 mod 223
        with pytest.raises(ValueError):
            F223(0) ** -1  # Zero does not have a multiplicative inverse

    def test_division(self, F223):
        assert F223(192) / F223(105) == F223(142)  # 192 * 17 mod 223 = 47
        assert F223(105) / F223(192) == F223(11)  # 105 * 182 mod 223 = 11
        with pytest.raises(ValueError):
            F223(192) / F223(0)  # Division by zero should raise an error
        
    def test_inverse(self, F223):
        assert F223(192).inverse() == F223(187)
        assert F223(105).inverse() == F223(17)
        with pytest.raises(ValueError):
            F223(0).inverse()  # Zero does not have an inverse

    def test_cross_field_operations(self, F223):
        with pytest.raises(TypeError):
            F223(192) + 5  # Cannot add int to PrimeFieldElement
        with pytest.raises(TypeError):
            F223(192) - 5  # Cannot subtract int from PrimeFieldElement
        with pytest.raises(TypeError):
            F223(192) * 5  # Cannot multiply PrimeFieldElement by int
        with pytest.raises(TypeError):
            F223(192) / 5  # Cannot divide PrimeFieldElement by int
    
    def test_equality(self, F223):
        assert F223(192) == F223(192)
        assert F223(192) != F223(193)
        assert F223(0) == F223(0)
        assert F223(222) == F223(-1)  # -1 mod 223 = 222

    def test_boolean_context(self, F223):
        assert bool(F223(0)) == False
        assert bool(F223(1)) == True
        assert bool(F223(222)) == True

    def test_field_order(self, F223):
        assert F223(192).field_order == 223
        assert F223(0).field_order == 223
        assert F223(222).field_order == 223

# Point Tests

class TestPoint:
    def _make_curve(self, prime = 223):
        F = PrimeField(prime)
        a = F(0)
        b = F(7)
        return F, a, b
    
    def test_valid_point(self):
        F, a, b = self._make_curve()
        p = Point(F(192), F(105), a, b)
        assert p.x == F(192)
        assert p.y == F(105)
        assert p.a == a
        assert p.b == b

    def test_invalid_point(self):
        F, a, b = self._make_curve()
        with pytest.raises(ValueError):
            Point(F(200), F(119), a, b)  # Not on the curve y^2 = x^3 + 7
        with pytest.raises(ValueError):
            Point(F(1), F(1), a, b)  # Not on the curve y^2 = x^3 + 7
    
    def test_point_at_infinity(self):
        F, a, b = self._make_curve()
        p_inf = Point(None, None, a, b)
        assert p_inf.is_infinity()
        assert p_inf.x is None
        assert p_inf.y is None

    def test_mixed_coordinates(self):
        F, a, b = self._make_curve()
        with pytest.raises(ValueError):
            Point(F(192), None, a, b)  # x is valid but y is None
        with pytest.raises(ValueError):
            Point(None, F(105), a, b)  # y is valid but x is None

    def test_identity_addition(self):
        F, a, b = self._make_curve()
        p_inf = Point(None, None, a, b)
        p = Point(F(192), F(105), a, b)
        assert p + p_inf == p
        assert p_inf + p == p

    def test_additive_inverse(self):
        F, a, b = self._make_curve()
        p = Point(F(192), F(105), a, b)
        p_neg = -p
        assert p + p_neg == Point(None, None, a, b)  # Should equal point at infinity

    def test_point_doubling(self):
        F, a, b = self._make_curve()
        p = Point(F(192), F(105), a, b)
        p_double = p + p
        expected_x = F(49)
        expected_y = F(71)
        assert p_double.x == expected_x
        assert p_double.y == expected_y

    def test_scalar_multiplication(self):
        F, a, b = self._make_curve()
        p = Point(F(192), F(105), a, b)
        p_double = 2 * p
        expected_x = F(49)
        expected_y = F(71)
        assert p_double.x == expected_x
        assert p_double.y == expected_y

    def test_scalar_multiplication_matches_addition(self):
        F, a, b = self._make_curve()
        p = Point(F(192), F(105), a, b)
        p_double_add = p + p
        p_double_scalar = 2 * p
        assert p_double_add == p_double_scalar

    def test_scalar_multiplication_zero(self):
        F, a, b = self._make_curve()
        p = Point(F(192), F(105), a, b)
        p_zero = 0 * p
        assert p_zero.is_infinity()

    def test_scalar_multiplication_one(self):
        F, a, b = self._make_curve()
        p = Point(F(192), F(105), a, b)
        p_one = 1 * p
        assert p_one == p

    def test_p_times_p_multiplication(self):
        """P * k and k * P should both work."""
        F, a, b = self._make_curve()
        P = Point(F(192), F(105), a, b)
        assert P * 3 == 3 * P

    def test_commutativity(self):
        F, a, b = self._make_curve()
        P = Point(F(192), F(105), a, b)
        Q = Point(F(17), F(56), a, b)  # Another point on the curve
        assert P + Q == Q + P

    def test_associativity(self):
        F, a, b = self._make_curve()
        P = Point(F(192), F(105), a, b)
        Q = Point(F(17), F(56), a, b)  # Another point on the curve
        R = Point(F(1), F(193), a, b)   # Another point on the curve
        assert (P + Q) + R == P + (Q + R)

    def test_different_curves(self):
        F1, a1, b1 = self._make_curve()
        F2, a2, b2 = self._make_curve(prime=227)  # Different prime field
        p1 = Point(F1(192), F1(105), a1, b1)
        p2 = Point(F2(0), F2(37), a2, b2)
        with pytest.raises(TypeError):
            p1 + p2  # Cannot add points from different curves
    
    def test_scalar_non_integer(self):
        F, a, b = self._make_curve()
        p = Point(F(192), F(105), a, b)
        with pytest.raises(TypeError):
            p * 2.5  # Scalar must be an integer
        with pytest.raises(TypeError):
            p * "3"  # Scalar must be an integer

    def test_repr_infinity(self):
        F, a, b = self._make_curve()
        p_inf = Point(None, None, a, b)
        assert "Infinity" in repr(p_inf)

# Named curves

class TestCurves:

    def test_secp256k1_generator_on_curve(self):
        """G must satisfy the curve equation."""
        G = SEC_P256K1.G
        assert not G.is_infinity()

    def test_secp256k1_order(self):
        """n * G == O (point at infinity)."""
        G = SEC_P256K1.G
        n = SEC_P256K1.n
        result = n * G
        assert result.is_infinity(), f"Expected infinity, got {result}"

    def test_p256_generator_on_curve(self):
        G = P_256.G
        assert not G.is_infinity()

    def test_p256_order(self):
        G = P_256.G
        n = P_256.n
        assert (n * G).is_infinity()

    def test_get_curve_valid(self):
        curve = get_curve("secp256k1")
        assert curve.name == "secp256k1"

    def test_get_curve_invalid(self):
        with pytest.raises(KeyError):
            get_curve("nonexistent_curve")

    def test_secp256k1_known_scalar(self):
        """2 * G should match a known precomputed value."""
        G = SEC_P256K1.G
        two_G = 2 * G
        # Known value from SEC 2 / test vectors
        expected_x = 0xC6047F9441ED7D6D3045406E95C07CD85C778E4B8CEF3CA7ABAC09B95C709EE5
        assert two_G.x.num == expected_x


# ===========================================================================
# Utils: arithmetic
# ===========================================================================

class TestXGCD:

    def test_basic(self):
        g, x, y = xgcd(35, 15)
        assert g == 5
        assert 35 * x + 15 * y == g

    def test_coprime(self):
        g, x, y = xgcd(3, 11)
        assert g == 1
        assert 3 * x + 11 * y == 1

    def test_one(self):
        g, x, y = xgcd(1, 5)
        assert g == 1

    def test_commutative_gcd(self):
        g1, _, _ = xgcd(12, 8)
        g2, _, _ = xgcd(8, 12)
        assert g1 == g2 == 4


class TestModularInverse:

    def test_basic(self):
        assert mod_inverse(3, 11) == 4    # 3 * 4 = 12 ≡ 1 mod 11

    def test_inverse_of_inverse(self):
        inv = mod_inverse(7, 11)
        assert mod_inverse(inv, 11) == 7

    def test_non_invertible_raises(self):
        with pytest.raises(ZeroDivisionError):
            mod_inverse(4, 8)  # gcd(4, 8) = 4 != 1


class TestConstantTime:

    def test_ct_equal_true(self):
        assert ct_equal(42, 42)
        assert ct_equal(0, 0)

    def test_ct_equal_false(self):
        assert not ct_equal(42, 43)
        assert not ct_equal(0, 1)

    def test_ct_select_true(self):
        assert ct_select(True, 10, 20) == 10

    def test_ct_select_false(self):
        assert ct_select(False, 10, 20) == 20


# Test Primes

class TestIsPrime:
    def test_small_primes(self):
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 223]
        for p in primes:
            assert is_prime(p), f"{p} should be prime"

    def test_composites(self):
        composites = [0, 1, 4, 6, 8, 9, 10, 15, 221, 224]
        for n in composites:
            assert not is_prime(n), f"{n} should not be prime"

    def test_large_prime(self):
        # secp256k1 field prime — must be prime
        p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        assert is_prime(p)

    def test_secp256k1_order_is_prime(self):
        n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        assert is_prime(n)


class TestNextPrime:

    def test_already_prime(self):
        assert next_prime(11) == 11
        assert next_prime(223) == 223

    def test_composite_input(self):
        assert next_prime(10) == 11
        assert next_prime(14) == 17

    def test_edge_cases(self):
        assert next_prime(2) == 2
        assert next_prime(1) == 2


class TestGeneratePrime:

    def test_correct_bit_length(self):
        p = generate_large_prime(64)
        assert p.bit_length() == 64
        assert is_prime(p)

    def test_different_each_call(self):
        # Astronomically unlikely to match, but not impossible
        p1 = generate_large_prime(128)
        p2 = generate_large_prime(128)
        # Just verify both are prime and correct length
        assert is_prime(p1) and p1.bit_length() == 128
        assert is_prime(p2) and p2.bit_length() == 128

    def test_invalid_bit_length(self):
        with pytest.raises(ValueError):
            generate_large_prime(1)
