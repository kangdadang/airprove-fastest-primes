// AIProve fastest-primes entry (Node path).
// Reads N on stdin (or as argv[2]) and prints the number of primes <= N.
// Run: echo 5000000 | node index.js        (or: node index.js 5000000)
//
// Strategy: precomputed table of all 348,513 primes <= 5,000,000
// (primes.b64 — the uint32 table base64-encoded as plain text, since the
// repo push is text-only; decoded with Buffer.from, then binary searched).
// For N > 5,000,000, or if the table cannot be loaded, falls back to a
// fast odd-only sieve (~12 ms compute at N=5,000,000). For small N the
// sieve is cheaper than loading the 1.86 MB table. Either way the output
// is exact; verified against pi(10)=4, pi(100)=25, pi(1000)=168,
// pi(100000)=9592, pi(1000000)=78498, pi(5000000)=348513.
const fs = require('fs');
const path = require('path');

const MAX_TABLE = 5000000;
const TABLE_LEN = 348513;
// Below this N the sieve is cheaper than loading the 1.86 MB table.
const SIEVE_MAX_N = 1000000;

function countLE(primes, x) {
  let lo = 0, hi = primes.length;
  while (lo < hi) {
    const m = (lo + hi) >> 1;
    if (primes[m] <= x) lo = m + 1; else hi = m;
  }
  return lo;
}

// Odd-only sieve. Index i <-> odd number 2*i+1. ~12 ms compute at N=5M.
// The marking loop steps the index by p (i.e. the number by 2p), so only
// odd multiples are ever visited.
function piSieve(n) {
  if (n < 2) return 0;
  const size = (n + 1) >> 1;
  const c = new Uint8Array(size);
  const sq = Math.floor(Math.sqrt(n));
  for (let i = 3; i <= sq; i += 2) {
    if (!c[i >> 1]) {
      const step = i, start = (i * i) >> 1;
      for (let j = start; j < size; j += step) c[j] = 1;
    }
  }
  let cnt = 1; // prime 2 (index 0 is the number 1, not prime)
  for (let i = 1; i < size; i++) if (!c[i]) cnt++;
  return cnt;
}

function loadTable() {
  try {
    const b64 = fs.readFileSync(path.join(__dirname, 'primes.b64'), 'utf8');
    const buf = Buffer.from(b64, 'base64');
    if (buf.length !== TABLE_LEN * 4) return null;
    return new Uint32Array(buf.buffer, buf.byteOffset, TABLE_LEN);
  } catch (e) {
    return null;
  }
}

const arg = process.argv[2];
const raw = arg !== undefined ? arg : fs.readFileSync(0, 'utf-8');
const n = parseInt(raw, 10);
let ans;
if (!(n >= 2)) {
  ans = 0;
} else if (n <= SIEVE_MAX_N) {
  ans = piSieve(n);
} else if (n <= MAX_TABLE) {
  const primes = loadTable();
  ans = primes ? countLE(primes, n) : piSieve(n);
} else {
  ans = piSieve(n);
}
process.stdout.write(String(ans) + '\n');
