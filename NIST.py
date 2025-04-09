import secrets
from bbs import BlumBlumShubPRNG
from chacha20 import ChaChaPRNG

# Ask the user for input.
num_bits_input = input("Enter the number of bits to generate for both PRNGs: ")
try:
    num_bits = int(num_bits_input)
except ValueError:
    print("Invalid input. Please enter an integer value for the number of bits.")
    exit(1)

# --- Generate ChaCha20 Output ---
# Use secrets for key and nonce generation.
key = secrets.token_bytes(32)
nonce = secrets.token_bytes(12)
cha_prng = ChaChaPRNG(key, nonce)
cha_bits = cha_prng.generate_bits(num_bits)

with open("chacha20_output.txt", "w") as f:
    f.write(cha_bits)
print("ChaCha20 output saved to chacha20_output.txt")

# --- Generate BBS Output ---
# Using small primes for demonstration purposes.
p = 499    # p must be prime and ≡ 3 mod 4.
q = 547    # q must be prime and ≡ 3 mod 4.
seed = 1597  # A seed that is coprime with p*q.
bbs_prng = BlumBlumShubPRNG(p, q, seed)
bbs_bits = bbs_prng.generate_bits(num_bits)

with open("bbs_output.txt", "w") as f:
    f.write(bbs_bits)
print("BBS output saved to bbs_output.txt")

