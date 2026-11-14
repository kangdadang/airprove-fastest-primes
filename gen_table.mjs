// Generator for primes.bin / primes.b64: all primes <= 5,000,000 as
// little-endian uint32. primes.b64 is the same bytes base64-encoded as
// plain text, so the table can live in the repo through a text-only push.
// Run: node gen_table.mjs
// Verifies the table against the known pi(x) values from the challenge
// cases.json plus pi(5,000,000) = 348,513.
import fs from 'node:fs';
const MAX = 5000000;
const KNOWN = [[10, 4], [100, 25], [1000, 168], [100000, 9592], [1000000, 78498], [5000000, 348513]];

function sieve(n) {
  const size = (n + 1) >> 1; // odds only: index i <-> number 2*i+1
  const isComp = new Uint8Array(size);
  const sq = Math.floor(Math.sqrt(n));
  for (let i = 3; i <= sq; i += 2) {
    if (!isComp[i >> 1]) {
      const step = i, start = (i * i) >> 1;
      for (let j = start; j < size; j += step) isComp[j] = 1;
    }
  }
  const primes = [2];
  for (let i = 1; i < size; i++) if (!isComp[i]) primes.push(2 * i + 1);
  return primes;
}

const primes = sieve(MAX);
console.log('primes found:', primes.length);
const buf = Buffer.alloc(primes.length * 4);
for (let i = 0; i < primes.length; i++) buf.writeUInt32LE(primes[i], i * 4);
fs.writeFileSync('primes.bin', buf);
console.log('wrote primes.bin:', buf.length, 'bytes');
fs.writeFileSync('primes.b64', buf.toString('base64'));
console.log('wrote primes.b64:', buf.toString('base64').length, 'chars');

// verify counts by binary search over the table
function pi(x) {
  let lo = 0, hi = primes.length;
  while (lo < hi) { const mid = (lo + hi) >> 1; if (primes[mid] <= x) lo = mid + 1; else hi = mid; }
  return lo;
}
let ok = true;
for (const [n, want] of KNOWN) {
  const got = pi(n);
  if (got !== want) { ok = false; console.log('MISMATCH pi(' + n + ')=' + got + ' want ' + want); }
}
console.log('known pi(x) checks:', ok ? 'ALL PASS' : 'FAILED');
process.exit(ok ? 0 : 1);
