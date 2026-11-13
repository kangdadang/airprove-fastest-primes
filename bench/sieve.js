// Standalone odd-only sieve (benchmark comparison only, NOT the entry).
// Same algorithm as the fallback in index.js. Run: echo 5000000 | node bench/sieve.js
const fs = require('fs');
const raw = process.argv[2] !== undefined ? process.argv[2] : fs.readFileSync(0, 'utf-8');
const n = parseInt(raw, 10);
function piSieve(n) {
  if (n < 2) return 0;
  const size = (n + 1) >> 1;
  const c = new Uint8Array(size);
  const sq = Math.floor(Math.sqrt(n));
  for (let i = 3; i <= sq; i += 2) {
    if (!c[i >> 1]) {
      for (let j = (i * i) >> 1; j < size; j += i) c[j] = 1;
    }
  }
  let cnt = 1;
  for (let i = 1; i < size; i++) if (!c[i]) cnt++;
  return cnt;
}
process.stdout.write(String(piSieve(n)) + '\n');
