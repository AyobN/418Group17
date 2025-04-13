# File: testing/test_performance.py

# Code to test timing performance of:
#   - Chacha
#   - BBS-weak(128 bit primes)
#   - BBS-strong(1024 bit primes)

import time
import secrets
import sys
sys.path.append("..")

from chacha20 import ChaChaPRNG
from bbs import BlumBlumShubPRNG
from primes import generate_blum_prime

BIT_SIZES = [1_000_000, 10_000_000, 100_000_000]
PRNGS = [
    {"label": "chacha", "type": "chacha"},
    {"label": "bbs_weak", "type": "bbs", "prime_size": 128},
    {"label": "bbs_strong", "type": "bbs", "prime_size": 1024},
]

results = []

def time_chacha(bits):
    key = secrets.token_bytes(32)
    nonce = secrets.token_bytes(12)
    prng = ChaChaPRNG(key, nonce)
    start = time.perf_counter()
    prng.generate_bits(bits)
    end = time.perf_counter()
    return end - start

def time_bbs(bits, prime_size):
    p = generate_blum_prime(prime_size)
    q = generate_blum_prime(prime_size)
    seed = secrets.randbelow(p * q - 1) + 1
    prng = BlumBlumShubPRNG(p, q, seed)
    start = time.perf_counter()
    prng.generate_bits(bits)
    end = time.perf_counter()
    return end - start

if __name__ == "__main__":
    print("Benchmarking PRNG generation times (in seconds):\n")

    for prng in PRNGS:
        for bits in BIT_SIZES:
            label = f"{prng['label']} - {bits // 1_000_000} million bits"
            print(f"Generating with {label}...")
            if prng["type"] == "chacha":
                duration = time_chacha(bits)
            else:
                duration = time_bbs(bits, prng["prime_size"])
            print(f"Completed in {duration:.3f} seconds.\n")
            results.append((prng["label"], bits, duration))

    # Save results to txt file
    txt_path = "testing/performance_results.txt"
    with open(txt_path, "w") as f:
        for row in results:
            label = f"{row[0]} ({row[1] // 1_000_000}M bits)"
            f.write(f"{label}: {row[2]:.3f} sec\n")

    print("Benchmark complete.")
    print(f"Results saved to: {txt_path}")
