# testing/generate_test_samples.py
import os
import time
import secrets
import argparse
import sys
sys.path.append("..")  

from bitstring import BitArray
from chacha20 import ChaChaPRNG
from bbs import BlumBlumShubPRNG
from primes import generate_blum_prime

def generate_bbs(bits, prime_size, label):
    p = generate_blum_prime(prime_size)
    q = generate_blum_prime(prime_size)
    seed = secrets.randbelow(p * q - 1) + 1
    bbs = BlumBlumShubPRNG(p, q, seed)
    out = bbs.generate_bits(bits)

    filename = f"bbs_{label}_{prime_size}bit_{bits}bits.bin"
    with open(os.path.join("diehard_inputs", filename), "wb") as f:
        f.write(out.tobytes())
    print(f"[✔] BBS output saved as {filename}")

def generate_chacha(bits, label):
    key = secrets.token_bytes(32)
    nonce = secrets.token_bytes(12)
    prng = ChaChaPRNG(key, nonce)
    out = prng.generate_bits(bits)

    filename = f"chacha_{label}_{bits}bits.bin"
    with open(os.path.join("diehard_inputs", filename), "wb") as f:
        f.write(out.tobytes())
    print(f"[✔] ChaCha20 output saved as {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", required=True, choices=["bbs", "chacha"])
    parser.add_argument("--bits", type=int, default=1000000)
    parser.add_argument("--label", type=str, default="test")
    parser.add_argument("--prime_size", type=int, default=512)
    args = parser.parse_args()

    os.makedirs("diehard_inputs", exist_ok=True)

    if args.type == "bbs":
        generate_bbs(args.bits, args.prime_size, args.label)
    elif args.type == "chacha":
        generate_chacha(args.bits, args.label)