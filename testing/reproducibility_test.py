import os
import hashlib
import sys
sys.path.append("..")

from bitstring import BitArray
from chacha20 import ChaChaPRNG
from bbs import BlumBlumShubPRNG

output_dir = os.path.join(os.path.dirname(__file__), "diehard_inputs")
os.makedirs(output_dir, exist_ok=True)

def sha256sum(file_path):
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

# --- BBS Test ---
p, q, seed = 499, 547, 1597
bbs1 = BlumBlumShubPRNG(p, q, seed)
bbs2 = BlumBlumShubPRNG(p, q, seed)

bbs_bits_1 = bbs1.generate_bits(1_000_000)
bbs_bits_2 = bbs2.generate_bits(1_000_000)

bbs_file_1 = os.path.join(output_dir, "bbs_repro_1.bin")
bbs_file_2 = os.path.join(output_dir, "bbs_repro_2.bin")

with open(bbs_file_1, "wb") as f:
    f.write(bbs_bits_1.tobytes())
with open(bbs_file_2, "wb") as f:
    f.write(bbs_bits_2.tobytes())

bbs_match = bbs_bits_1 == bbs_bits_2
bbs_hash_1 = sha256sum(bbs_file_1)
bbs_hash_2 = sha256sum(bbs_file_2)

# --- ChaCha20 Test ---
key = bytes.fromhex("00" * 32)
nonce = bytes.fromhex("11" * 12)
cha1 = ChaChaPRNG(key, nonce)
cha2 = ChaChaPRNG(key, nonce)

cha_bits_1 = cha1.generate_bits(1_000_000)
cha_bits_2 = cha2.generate_bits(1_000_000)

cha_file_1 = os.path.join(output_dir, "chacha_repro_1.bin")
cha_file_2 = os.path.join(output_dir, "chacha_repro_2.bin")

with open(cha_file_1, "wb") as f:
    f.write(cha_bits_1.tobytes())
with open(cha_file_2, "wb") as f:
    f.write(cha_bits_2.tobytes())

cha_match = cha_bits_1 == cha_bits_2
cha_hash_1 = sha256sum(cha_file_1)
cha_hash_2 = sha256sum(cha_file_2)

print("\n=== PRNG Reproducibility Test ===")
print(f"BBS match: {'✓' if bbs_match else '✗'}")
print(f"BBS hash 1: {bbs_hash_1}")
print(f"BBS hash 2: {bbs_hash_2}\n")

print(f"ChaCha20 match: {'✓' if cha_match else '✗'}")
print(f"ChaCha hash 1: {cha_hash_1}")
print(f"ChaCha hash 2: {cha_hash_2}")