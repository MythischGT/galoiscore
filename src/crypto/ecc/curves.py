from __future__ import annotations
from core.prime import PrimeField, PrimeFieldElement
from crypto.ecc.point import Point


class CurveParameters:
    def __init__(self, name, prime, a, b, g_x, g_y, n, h, bits):
        self.name = name
        self.prime    = prime
        self.a    = a
        self.b    = b
        self.g_x   = g_x
        self.g_y   = g_y
        self.n    = n
        self.h    = h
        self.bits = bits
        # Cached objects — built on first access
        self._field  = None
        self._G      = None
        self._a_elem = None
        self._b_elem = None

    @property
    def field(self) -> PrimeField:
        if object.__getattribute__(self, "_field") is None:
            object.__setattr__(self, "_field", PrimeField(self.prime))
        return object.__getattribute__(self, "_field")
    
    @property
    def a_elem(self) -> PrimeFieldElement:
        if object.__getattribute__(self, "_a_elem") is None:
            object.__setattr__(self, "_a_elem", self.field(self.a))
        return object.__getattribute__(self, "_a_elem")

    @property
    def b_elem(self) -> PrimeFieldElement:
        if object.__getattribute__(self, "_b_elem") is None:
            object.__setattr__(self, "_b_elem", self.field(self.b))
        return object.__getattribute__(self, "_b_elem")

    @property
    def G(self) -> Point:
        if object.__getattribute__(self, "_G") is None:
            F = self.field
            object.__setattr__(self, "_G", Point(F(self.g_x), F(self.g_y), self.a_elem, self.b_elem))
        return object.__getattribute__(self, "_G")
    
    @property
    def infinity(self) -> Point:
        return Point(None, None, self.a_elem, self.b_elem) 
    
    def validate_point(self, x: int, y: int) -> bool:
        """Check if the point (x, y) is on the curve."""
        F = self.field
        return Point(F(x), F(y), self.a_elem, self.b_elem)
    
    def __repr__(self) -> str:
        return f"CurveParameters(name={self.name}, prime={self.prime}, a={self.a}, b={self.b}, g_x={self.g_x}, g_y={self.g_y}, n={self.n}, bits={self.bits}, h={self.h})"
    

# secp256k1 - parameters from https://www.secg.org/sec2-v2.pdf
# bitcoin's curve, used in ECDSA and Schnorr signatures

SEC_P256K1 = CurveParameters(
    name="secp256k1",
    bits=256,
    prime=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
    a=0,
    b=7,
    g_x=55066263022277343669578718895168534326250603453777594175500187360389116729240,
    g_y=32670510020758816978083085130507043184471273380659243275938904335757337482424,
    n=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
    h=1
)

# NIST P-256 - parameters from https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf
# widely used general-purpose curve, used in ECDSA and ECDH

P_256 = CurveParameters(
    name="P-256",
    bits=256,
    prime=0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF,
    a=0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC,
    b=0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B,
    g_x=0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
    g_y=0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5,
    n=0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551,
    h=1
)

# NIST P-384 - parameters from https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf
# stronger security level than P-256, used in ECDSA and ECDH

P_384 = CurveParameters(
    name="P-384",
    bits=384,
    prime=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFF0000000000000000FFFFFFFF,
    a=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFF0000000000000000FFFFFFFC,
    b=0xB3312FA7E23EE7E4988E056BE3F82D19181D9C6EFE8141120314088F5013875AC656398D8A2ED19D2A85C8EDD3EC2AEF,
    g_x=0xAA87CA22BE8B05378EB1C71EF320AD746E1D3B628BA79B9859F741E082542A385502F25DBF55296C3A545E3872760AB7,
    g_y=0x3617DE4A96262C6F5D9E98BF9292DC29F8F41DBD289A147CE9DA3113B5F0B8C00A60B1CE1D7E819D7A431D7C90EA0E5F,
    n=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC7634D81F4372DDF581A0DB248B0A77AECEC196ACCC52973,
    h=1
)

# Curve registry for easy lookup
CURVE_REGISTRY = {
    "secp256k1": SEC_P256K1,
    "P-256": P_256,
    "P-384": P_384,
}  

def get_curve(name: str) -> CurveParameters:
    try:
        return CURVE_REGISTRY[name]
    except KeyError:
        available = ", ".join(CURVE_REGISTRY.keys())
        raise KeyError(f"Curve '{name}' not found. Available curves: {available}") from None