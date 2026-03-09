from __future__ import annotations
import random
import os

_DETERMINISTIC_WITNESSES = [
    (3_215_031_751,                     [2, 3, 5, 7]),
    (3_317_044_064_679_887_385_961_981, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]),
]
_PROBABILISTIC_ROUNDS = 40


def _miller_rabin_test(n, witnesses):
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for a in witnesses:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def is_prime(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    small_primes = [5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return False
    for bound, witnesses in _DETERMINISTIC_WITNESSES:
        if n < bound:
            return _miller_rabin_test(n, witnesses)
    # Use getrandbits — avoids Windows OverflowError with large integers
    bit_len = n.bit_length()
    witnesses = []
    while len(witnesses) < _PROBABILISTIC_ROUNDS:
        w = random.getrandbits(bit_len)
        if 2 <= w <= n - 2:
            witnesses.append(w)
    return _miller_rabin_test(n, witnesses)


def generate_large_prime(bit_length):
    if bit_length < 2:
        raise ValueError(f"bit_length must be >= 2, got {bit_length}.")
    low = 1 << (bit_length - 1)
    while True:
        raw = int.from_bytes(os.urandom((bit_length + 7) // 8), "big")
        candidate = low | (raw >> (raw.bit_length() - bit_length + 1 if raw.bit_length() >= bit_length else 0)) | 1
        candidate = (low | (raw & ((1 << bit_length) - 1)) | 1)
        if candidate.bit_length() == bit_length and is_prime(candidate):
            return candidate



def next_prime(n):
    if n <= 2:
        return 2
    candidate = n if n % 2 != 0 else n + 1
    while not is_prime(candidate):
        candidate += 2
    return candidate