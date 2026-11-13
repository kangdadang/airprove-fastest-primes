# Python table variant (benchmark comparison only): load primes.bin, bisect.
# Run: echo 5000000 | python3 bench/primes_py_table.py
import array
import bisect
import os
import sys

MAX_TABLE = 5000000


def pi_sieve(n):
    if n < 2:
        return 0
    size = (n + 1) // 2
    sieve = bytearray(b'\x01') * size
    sieve[0] = 0
    import math
    for i in range(3, int(math.isqrt(n)) + 1, 2):
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
    here = os.path.dirname(os.path.abspath(__file__))
    table_path = os.path.join(here, '..', 'primes.bin')
    primes = None
    if n <= MAX_TABLE:
        try:
            a = array.array('I')
            with open(table_path, 'rb') as f:
                a.frombytes(f.read())
            if len(a) == 348513:
                primes = a
        except OSError:
            pass
    if primes is not None:
        print(bisect.bisect_right(primes, n))
    else:
        print(pi_sieve(n))


if __name__ == '__main__':
    main()
