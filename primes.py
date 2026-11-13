#!/usr/bin/env python3
"""AIProve fastest-primes entry (Python path).
Reads N on stdin (or argv[1]) and prints the number of primes <= N.
Table lookup (primes.bin) for N <= 5,000,000, odd-only sieve fallback otherwise.
Run: echo 5000000 | python3 primes.py   (or: python3 primes.py 5000000)
"""
import array
import bisect
import math
import os
import sys

MAX_TABLE = 5000000
TABLE_LEN = 348513


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


def main():
    data = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    n = int(data)
    if n < 2:
        print(0)
        return
    primes = None
    if n <= MAX_TABLE:
        try:
            here = os.path.dirname(os.path.abspath(__file__))
            a = array.array('I')
            with open(os.path.join(here, 'primes.bin'), 'rb') as f:
                a.frombytes(f.read())
            if len(a) == TABLE_LEN:
                primes = a
        except OSError:
            pass
    print(bisect.bisect_right(primes, n) if primes is not None else pi_sieve(n))


if __name__ == '__main__':
    main()
