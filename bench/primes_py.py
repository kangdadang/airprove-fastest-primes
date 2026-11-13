# Standalone bytearray sieve in Python (benchmark comparison only, NOT the entry).
# Run: echo 5000000 | python3 bench/primes_py.py
import sys

def pi(n):
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
    return sum(sieve) + 1  # +1 for prime 2 (sieve covers odds only)

data = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
print(pi(int(data)))
