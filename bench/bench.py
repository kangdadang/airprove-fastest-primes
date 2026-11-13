#!/usr/bin/env python3
"""Benchmark the fastest-primes variants. Run: python3 bench/bench.py
Measures wall-clock latency (min / median of 5 runs) per N, verifies output
against the known pi(x) values from the challenge cases.json."""
import json
import statistics
import subprocess
import sys
import time

HERE = __file__.rsplit('/', 1)[0] + '/..'
CASES = {10: 4, 100: 25, 1000: 168, 100000: 9592, 1000000: 78498, 5000000: 348513}

VARIANTS = {
    'sh run.sh (ENTRY, py-first, node fallback)': ['sh', HERE + '/run.sh'],
    'python primes.py (table+bisect)': ['python3', HERE + '/primes.py'],
    'node index.js (table+bisect)': ['node', HERE + '/index.js'],
    'node sieve.js (odd-only sieve)': ['node', HERE + '/bench/sieve.js'],
    'python bytearray sieve': ['python3', HERE + '/bench/primes_py.py'],
    'C binary -O3 (precompiled, run only)': ['/tmp/primes_c'],
}


def run(cmd, n):
    t0 = time.perf_counter()
    p = subprocess.run(cmd, input=str(n).encode(), stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, timeout=120)
    dt = time.perf_counter() - t0
    return dt, p.stdout.decode().strip(), p.returncode


def main():
    print(f"{'N':>9} {'variant':<38} {'min ms':>8} {'med ms':>8}  out")
    for n, want in CASES.items():
        for name, cmd in VARIANTS.items():
            times, outs, rcs = [], set(), set()
            for _ in range(5):
                dt, out, rc = run(cmd, n)
                times.append(dt * 1000)
                outs.add(out)
                rcs.add(rc)
            ok = outs == {str(want)} and rcs == {0}
            print(f"{n:>9} {name:<38} {min(times):8.1f} {statistics.median(times):8.1f}  "
                  f"{sorted(outs)[0]}{' OK' if ok else '  <-- WRONG, want ' + str(want)}")
    print('done')


if __name__ == '__main__':
    main()
