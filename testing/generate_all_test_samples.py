# File: testing/generate_all_test_samples.py

import os
import secrets
import sys
import argparse
sys.path.append("..")  # So it can find chacha20.py, bbs.py, etc.

from bitstring import BitArray
from chacha20 import ChaChaPRNG
from bbs import BlumBlumShubPRNG
from primes import generate_blum_prime

DEFAULT_BITS = 1_000_000  # Default to 1 million bits
OUTPUT_DIR = "diehard_inputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_bin(bits: BitArray, filename: str):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "wb") as f:
        f.write(bits.tobytes())
    print(f"[✔] Saved: {path}")

def generate_chacha(bits: int, label="chacha"):
    key = secrets.token_bytes(32)
    nonce = secrets.token_bytes(12)
    prng = ChaChaPRNG(key, nonce)
    output = prng.generate_bits(bits)
    save_bin(output, f"{label}_{bits}bits.bin")

def generate_bbs(prime_size: int, bits: int, label="bbs"):
    p = generate_blum_prime(prime_size)
    q = generate_blum_prime(prime_size)
    seed = secrets.randbelow(p * q - 1) + 1
    prng = BlumBlumShubPRNG(p, q, seed)
    output = prng.generate_bits(bits)
    save_bin(output, f"{label}_{prime_size}bit_{bits}bits.bin")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate PRNG bitstreams for Dieharder testing")
    parser.add_argument("--bits", type=int, default=DEFAULT_BITS, help="Number of bits to generate (default: 1,000,000)")
    args = parser.parse_args()

    print(f"▶ Generating PRNG samples ({args.bits} bits each)...\n")

    generate_chacha(bits=args.bits, label="chacha")
    generate_bbs(prime_size=256, bits=args.bits, label="bbs_small")
    generate_bbs(prime_size=1024, bits=args.bits, label="bbs_large")

    print("\n✅ All samples generated in 'diehard_inputs/'")
