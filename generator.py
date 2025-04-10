import time
import os
import math
import secrets
from bitstring import BitArray
from bbs import BlumBlumShubPRNG
from chacha20 import ChaChaPRNG
from primes import generate_blum_prime

def generate_valid_seed(p, q):
    """
    Generate a valid seed for Blum Blum Shub given primes p and q.
    A valid seed is an integer in the range [1, p*q) that is coprime with p*q.
    """
    n = p * q
    while True:
        seed = secrets.randbelow(n - 1) + 1  # Random integer in [1, n-1]
        if math.gcd(seed, n) == 1:
            return seed

# --- Get Number of Bits ---
num_bits_input = input("Enter the number of bits to generate for both PRNGs: ")
try:
    num_bits = int(num_bits_input)
except ValueError:
    print("Invalid input. Please enter an integer value for the number of bits.")
    exit(1)

# --- Default values for BBS ---
default_p = 499       # Must be ≡ 3 mod 4.
default_q = 547       # Must be ≡ 3 mod 4.
default_seed = 1597   # Must be coprime with p*q.

# --- Handle Custom p, q Selection ---
custom_pq = input("Do you want a custom p, q selection? (Y/N): ").strip().lower()
custom_bool = 0

if custom_pq in ["y", "yes"]:
    try:
        p_input = int(input("Enter prime p (should be prime and ≡ 3 mod 4): "))
        q_input = int(input("Enter prime q (should be prime and ≡ 3 mod 4): "))
        if (p_input % 4 != 3) or (q_input % 4 != 3):
            print("Provided primes do not satisfy p, q ≡ 3 mod 4. Using default primes.")
            p, q = default_p, default_q
        else:
            p, q = p_input, q_input
            custom_bool = 1
    except ValueError:
        print("Invalid numerical input. Using default primes.")
        p, q = default_p, default_q
else:
    # Auto-generate p, q: ask the user for size
    try:
        threshold_input = int(input("How many bits do you want your primes to be? "))
    except ValueError:
        print("Invalid input. Using small primes")
        threshold_input = 16
    p = generate_blum_prime(threshold_input)
    q = generate_blum_prime(threshold_input)

print(f"Using primes for BBS: p = {p}, q = {q}")

# --- Handle Seed Selection ---
if (custom_bool == 1):
    seed_choice = input("Your p,q are custom. Do you want to customize your seed? (Y/N)").strip().lower()
    if seed_choice == 'y' or seed_choice == 'yes':
        try:
            seed_input = int(input("Enter the seed (should be an integer and coprime with p*q): "))
            if math.gcd(seed_input, p * q) != 1 or (seed_input <=0 or seed_input > (p * q)):
                print("The provided seed is invalid. Generating a valid seed instead.")
                seed = generate_valid_seed(p, q)
            else:
                seed = seed_input
        except ValueError:
            print("Invalid seed input. Generating a valid seed instead.")
            seed = generate_valid_seed(p, q)
    else:
        print("Generating a new valid seed automatically...")
        seed = generate_valid_seed(p, q)
else:
    seed = default_seed

print(f"Using seed for BBS: {seed}")

# --- Generate ChaCha20 Output ---
key = secrets.token_bytes(32)
nonce = secrets.token_bytes(12)    
cha_prng = ChaChaPRNG(key, nonce)

start_time = time.perf_counter()
cha_bits = cha_prng.generate_bits(num_bits)
end_time = time.perf_counter()
cha_duration = end_time - start_time
print(f"ChaCha20: Generated {num_bits} bits in {cha_duration:.4f} seconds.")

dir = "output"
os.makedirs(dir, exist_ok=True)

#TODO save PRNG secrets to txt in dirs

cha_bin_filename = f"chacha20_{num_bits}_output"
cha_bin_path = os.path.join(dir, cha_bin_filename)
with open(cha_bin_path, "wb") as f:
    f.write(cha_bits.tobytes())
print(f"ChaCha20 binary output saved to {cha_bin_filename}")

cha_txt_filename = f"chacha20_output_{num_bits}.txt"
cha_txt_path = os.path.join(dir, cha_txt_filename)
cha_string = cha_bits.bin
with open(cha_txt_path, "w") as f:
    f.write(cha_string)
print(f"ChaCha20 bit string output saved to {cha_txt_filename}")

# === Save ChaCha20 info file ===
cha_info_filename = f"chacha20_output_{num_bits}_info.txt"
cha_info_path = os.path.join(dir, cha_info_filename)


constants = cha_prng.get_c()
c_int = 0
for const in constants:
    c_int = (c_int << 32) | const
c_hex = hex(c_int)

key_int = int.from_bytes(key, byteorder='big')
nonce_int = int.from_bytes(nonce, byteorder='big')

with open(cha_info_path, "w") as f:
    f.write(f"PRNG integer value: {cha_bits.uint}\n")
    f.write(f"PRNG hex value: {cha_bits.hex}\n")
    f.write(f"Key integer value: {key_int}\n")
    f.write(f"Key hex value: {key.hex()}\n")
    f.write(f"Constant int value: {c_int}\n")
    f.write(f"Constant hex value: {c_hex}\n")
    f.write(f"Nonce integer value: {nonce_int}\n")
    f.write(f"Nonce hex value: {nonce.hex()}\n")
    f.write(f"\nGenerated in {cha_duration:.4f} seconds\n")
print(f"ChaCha20 info saved to {cha_info_filename}")

# --- Generate BBS Output ---
bbs_prng = BlumBlumShubPRNG(p, q, seed)
start_time = time.perf_counter()
bbs_bits = bbs_prng.generate_bits(num_bits)
end_time = time.perf_counter()
bbs_duration = end_time - start_time
print(f"BBS: Generated {num_bits} bits in {bbs_duration:.4f} seconds.")

bbs_bin_filename = f"bbs_output_{num_bits}"
bbs_bin_path = os.path.join(dir, bbs_bin_filename)
with open(bbs_bin_path, "wb") as f:
    f.write(bbs_bits.tobytes())
print(f"BBS binary output saved to {bbs_bin_filename}")

bbs_string = bbs_bits.bin
bbs_txt_filename = f"bbs_output_{num_bits}.txt"
bbs_txt_path = os.path.join(dir, bbs_txt_filename)
with open(bbs_txt_path, "w") as f:
    f.write(bbs_string)
print(f"BBS bit string output saved to {bbs_txt_filename}")

bbs_info_filename = f"bbs_{num_bits}_info.txt"
bbs_info_path = os.path.join(dir, bbs_info_filename)

with open(bbs_info_path, "w") as f:
    f.write(f"PRNG integer value: {bbs_bits.uint}\n")
    f.write(f"PRNG hex value: {bbs_bits.hex}\n")
    f.write(f"p: {p}\n")
    f.write(f"q: {q}\n")
    f.write(f"seed: {seed}\n")
    f.write(f"\nGenerated in {bbs_duration:.4f} seconds\n")
print(f"BBS info saved to {bbs_info_filename}")