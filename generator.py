import time
import math
import secrets
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

def bitstring_to_bytes(bitstring):
    """
    Convert a bit string (e.g., '01001100...') into a bytes object.
    Assumes the bit string's length is a multiple of 8.
    """
    num_bytes = len(bitstring) // 8
    return int(bitstring, 2).to_bytes(num_bytes, byteorder='big')

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

if custom_pq in ["y", "yes"]:
    try:
        p_input = int(input("Enter prime p (should be prime and ≡ 3 mod 4): "))
        q_input = int(input("Enter prime q (should be prime and ≡ 3 mod 4): "))
        if (p_input % 4 != 3) or (q_input % 4 != 3):
            print("Provided primes do not satisfy p, q ≡ 3 mod 4. Using default primes.")
            p, q = default_p, default_q
        else:
            p, q = p_input, q_input
    except ValueError:
        print("Invalid numerical input. Using default primes.")
        p, q = default_p, default_q
else:
    # Auto-generate p, q: ask the user for the threshold before generating.
    try:
        threshold_input = int(input("Enter the threshold (minimum value) for prime generation: "))
    except ValueError:
        print("Invalid threshold input. Using default threshold of 1000.")
        threshold_input = 1000
    p = generate_blum_prime(threshold_input)
    q = generate_blum_prime(p + 1)

print(f"Using primes for BBS: p = {p}, q = {q}")

# --- Handle Seed Selection ---
if (p != default_p) or (q != default_q):
    seed_choice = input("Your p,q are custom. Do you want to generate a new valid seed automatically (G) or choose your own (C)? ").strip().lower()
    if seed_choice == 'c':
        try:
            seed_input = int(input("Enter the seed (should be an integer and coprime with p*q): "))
            if math.gcd(seed_input, p * q) != 1:
                print("The provided seed is not coprime with p*q. Generating a valid seed instead.")
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
cha_bitstring = cha_prng.generate_bits(num_bits)
end_time = time.perf_counter()
cha_duration = end_time - start_time
print(f"ChaCha20: Generated {num_bits} bits in {cha_duration:.4f} seconds.")

cha_binary = bitstring_to_bytes(cha_bitstring)
cha_bin_filename = f"chacha20_output_{num_bits}.bin"
with open(cha_bin_filename, "wb") as f:
    f.write(cha_binary)
print(f"ChaCha20 binary output saved to {cha_bin_filename}")

cha_txt_filename = f"chacha20_output_{num_bits}.txt"
with open(cha_txt_filename, "w") as f:
    f.write(cha_bitstring)
print(f"ChaCha20 bit string output saved to {cha_txt_filename}")

# --- Generate BBS Output ---
bbs_prng = BlumBlumShubPRNG(p, q, seed)
start_time = time.perf_counter()
bbs_bitstring = bbs_prng.generate_bits(num_bits)
end_time = time.perf_counter()
bbs_duration = end_time - start_time
print(f"BBS: Generated {num_bits} bits in {bbs_duration:.4f} seconds.")

bbs_binary = bitstring_to_bytes(bbs_bitstring)
bbs_bin_filename = f"bbs_output_{num_bits}.bin"
with open(bbs_bin_filename, "wb") as f:
    f.write(bbs_binary)
print(f"BBS binary output saved to {bbs_bin_filename}")

bbs_txt_filename = f"bbs_output_{num_bits}.txt"
with open(bbs_txt_filename, "w") as f:
    f.write(bbs_bitstring)
print(f"BBS bit string output saved to {bbs_txt_filename}")