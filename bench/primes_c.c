// Standalone C sieve (benchmark comparison only, NOT the entry — the entry
// is Node so no compile step is ever timed). Compile: gcc -O3 -o /tmp/primes_c bench/primes_c.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
int main(int argc, char **argv) {
    long n;
    if (argc > 1) n = atol(argv[1]);
    else { if (scanf("%ld", &n) != 1) return 1; }
    if (n < 2) { printf("0\n"); return 0; }
    long size = (n + 1) / 2;
    unsigned char *c = calloc(size, 1);
    long sq = (long)sqrt((double)n);
    for (long i = 3; i <= sq; i += 2) {
        if (!c[i / 2]) {
            for (long j = (i * i) / 2; j < size; j += i) c[j] = 1;
        }
    }
    long cnt = 1;
    for (long i = 1; i < size; i++) if (!c[i]) cnt++;
    printf("%ld\n", cnt);
    return 0;
}
