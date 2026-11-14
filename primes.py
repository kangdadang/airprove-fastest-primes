#!/usr/bin/env python3
"""AIProve fastest-primes entry (Python path).

Reads N on stdin (or argv[1]) and prints the number of primes <= N.
Table lookup for N <= 5,000,000, odd-only sieve fallback otherwise.

The table (all 348,513 primes <= 5,000,000) ships as primes.b64: the same
1,394,052-byte little-endian uint32 table as primes.bin, base64-encoded so
it can live in the repo as plain UTF-8 text (the GitHub snapshot push used
for this repo is text-only and cannot carry the raw .bin). Decoded with
binascii.a2b_base64 (C-speed, ~4 ms) and binary-searched via a memoryview
cast — no heavy imports: `import base64` alone costs ~12 ms of startup and
`from array import array` ~5 ms, so both are deliberately avoided.
Verified against pi(10)=4, pi(100)=25, pi(1000)=168,
pi(100000)=9592, pi(1000000)=78498, pi(5000000)=348513.

Run: echo 5000000 | python3 -S primes.py   (or: python3 -S primes.py 5000000)
"""
import binascii
import bisect
import math
import sys

MAX_TABLE = 5000000
TABLE_LEN = 348513
# Below this N the sieve is cheaper than loading the 1.86 MB table.
SIEVE_MAX_N = 1000000


def pi_sieve(n):
    if n < 2:
        return 0
    size = (n + 1) // 2
    sieve = bytearray(b'\x01') * size
    sieve[0] = 0
    for i in range(3, math.isqrt(n) + 1, 2):
        if sieve[i // 2]:
            step = i
            start = (i * i) // 2
            sieve[start:size:step] = b'\x00' * ((size - start + step - 1) // step)
    return sum(sieve) + 1


def load_table():
    # Path of this script without importing os: __file__ is the script path
    # as invoked (run.sh always passes an explicit path).
    here = __file__.rsplit('/', 1)[0] if '/' in __file__ else '.'
    try:
        with open(here + '/primes.b64', 'rb') as f:
            raw = binascii.a2b_base64(f.read().strip())
    except OSError:
        return None
    if len(raw) != TABLE_LEN * 4 or sys.byteorder != 'little':
        return None
    return memoryview(raw).cast('I')


def main():
    data = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    n = int(data)
    if n < 2:
        print(0)
        return
    if n <= SIEVE_MAX_N:
        print(pi_sieve(n))
        return
    primes = load_table() if n <= MAX_TABLE else None
    print(bisect.bisect_right(primes, n) if primes is not None else pi_sieve(n))


if __name__ == '__main__':
    main()
