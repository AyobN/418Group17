# File: testing/generate_bbs_samples.py

import os
import time
import secrets
import sys
sys.path.append("..")

from bitstring import BitArray
from bbs import BlumBlumShubPRNG
from primes import generate_blum_prime

# Prime sizes to test
PRIME_SIZES = [32, 64, 128, 256, 512, 768, 1024]
BIT_COUNT = 100_000_000  # 100 million bits
BIN_DIR = "bbs_analysis_data/binaries"
TXT_PATH = "bbs_analysis_data/timing_results.txt"

os.makedirs(BIN_DIR, exist_ok=True)

def generate_bbs(bits, prime_size, label):
    p = generate_blum_prime(prime_size)
    q = generate_blum_prime(prime_size)
    seed = secrets.randbelow(p * q - 1) + 1
    prng = BlumBlumShubPRNG(p, q, seed)

    start = time.perf_counter()
    bitstream = prng.generate_bits(bits)
    end = time.perf_counter()
    duration = end - start

    # Save binary
    bin_path = os.path.join(BIN_DIR, f"bbs_{label}_{prime_size}bit_{bits}bits.bin")
    with open(bin_path, "wb") as f:
        f.write(bitstream.tobytes())

    return duration

if __name__ == "__main__":
    print("Running BBS analysis sweep...\n")

    results = []
    for size in PRIME_SIZES:
        label = f"{size}bit"
        print(f"Generating {BIT_COUNT:,} bits with {size}-bit primes...")
        time_taken = generate_bbs(BIT_COUNT, size, label)
        results.append((size, time_taken))
        print(f"Finished in {time_taken:.2f} seconds.\n")

    # Save timing results
    os.makedirs(os.path.dirname(TXT_PATH), exist_ok=True)
    with open(TXT_PATH, "w") as f:
        f.write("PrimeSizeBits,TimeSeconds\n")
        for size, time_taken in results:
            f.write(f"{size},{time_taken:.6f}\n")

    print("All generations complete.")
    print(f"Timing data saved to: {TXT_PATH}")
    print(f"Binary outputs saved to: {BIN_DIR}")
