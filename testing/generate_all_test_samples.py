# File: testing/generate_all_test_samples.py

import os
import secrets
import sys
sys.path.append("..") 

from bitstring import BitArray
from chacha20 import ChaChaPRNG
from bbs import BlumBlumShubPRNG
from primes import generate_blum_prime

OUTPUT_DIR = "diehard_inputs"
NUM_BITS = 1_000_000  # 1 million bits

os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_bin(bits: BitArray, filename: str):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "wb") as f:
        f.write(bits.tobytes())
    print(f"[✔] Saved: {path}")

# --- ChaCha20 ---
def generate_chacha(label="chacha"):
    key = secrets.token_bytes(32)
    nonce = secrets.token_bytes(12)
    prng = ChaChaPRNG(key, nonce)
    bits = prng.generate_bits(NUM_BITS)
    save_bin(bits, f"{label}_{NUM_BITS}bits.bin")

# --- BBS with custom prime size ---
def generate_bbs(prime_size=512, label="bbs"):
    p = generate_blum_prime(prime_size)
    q = generate_blum_prime(prime_size)
    seed = secrets.randbelow(p * q - 1) + 1
    prng = BlumBlumShubPRNG(p, q, seed)
    bits = prng.generate_bits(NUM_BITS)
    save_bin(bits, f"{label}_{prime_size}bit_{NUM_BITS}bits.bin")

# --- Master run ---
if __name__ == "__main__":
    print("▶ Generating PRNG samples for Dieharder testing...\n")

    generate_chacha(label="chacha")
    generate_bbs(prime_size=256, label="bbs_small")
    generate_bbs(prime_size=1024, label="bbs_large")

    print("\n✅ All samples generated in 'diehard_inputs/'")
