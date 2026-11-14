#!/bin/sh
DIR=${0%/*}
[ "$DIR" = "$0" ] && DIR=.
if command -v python3 >/dev/null 2>&1; then
  exec python3 -S "$DIR/primes.py" "$@"
else
  exec node "$DIR/index.js" "$@"
fi
