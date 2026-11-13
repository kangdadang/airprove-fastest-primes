#!/bin/sh
# AIProve fastest-primes run command: sh run.sh
# Prefers Python (fast startup + table lookup); falls back to Node (same table).
# Reads N on stdin or as $1; prints the number of primes <= N. See README.md.
DIR=$(dirname "$0")
if command -v python3 >/dev/null 2>&1; then
  exec python3 "$DIR/primes.py" "$@"
else
  exec node "$DIR/index.js" "$@"
fi
