import os
import math
import secrets
import time
from bitstring import BitArray
from bbs import BlumBlumShubPRNG
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

def main():
    # --- Get Number of Bits ---
    num_bits_input = input("Enter the number of bits to generate for BBS: ")
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
    custom_bool = False

    if custom_pq in ["y", "yes"]:
        try:
            p_input = int(input("Enter prime p (should be prime and ≡ 3 mod 4): "))
            q_input = int(input("Enter prime q (should be prime and ≡ 3 mod 4): "))
            if (p_input % 4 != 3) or (q_input % 4 != 3):
                print("Provided primes do not satisfy p, q ≡ 3 mod 4. Using default primes.")
                p, q = default_p, default_q
            else:
                p, q = p_input, q_input
                custom_bool = True
        except ValueError:
            print("Invalid numerical input. Using default primes.")
            p, q = default_p, default_q
    else:
        # Auto-generate p, q: ask the user for size (in bits)
        try:
            threshold_input = int(input("How many bits do you want your primes to be? "))
        except ValueError:
            print("Invalid input. Using small primes")
            threshold_input = 16
        p = generate_blum_prime(threshold_input)
        q = generate_blum_prime(threshold_input)

    print(f"Using primes for BBS: p = {p}, q = {q}")

    # --- Handle Seed Selection ---
    if custom_bool:
        seed_choice = input("Your p,q are custom. Do you want to customize your seed? (Y/N): ").strip().lower()
        if seed_choice in ['y', 'yes']:
            try:
                seed_input = int(input("Enter the seed (should be an integer and coprime with p*q): "))
                # Note: valid seed must be in range [1, p*q)
                if math.gcd(seed_input, p * q) != 1 or (seed_input <= 0 or seed_input >= (p * q)):
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

    # --- Generate BBS Output ---
    bbs_prng = BlumBlumShubPRNG(p, q, seed)
    start_time = time.perf_counter()
    bbs_bits = bbs_prng.generate_bits(num_bits)
    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"BBS: Generated {num_bits} bits in {duration:.4f} seconds.")

    # Create output directory if it doesn't exist
    output_dir = "bbs_output"
    os.makedirs(output_dir, exist_ok=True)

    prng_name = input("Name your BBS: ").strip()

    # Save binary output
    bbs_bin_filename = f"{prng_name}_output.bin"
    bbs_bin_path = os.path.join(output_dir, bbs_bin_filename)
    with open(bbs_bin_path, "wb") as f:
        f.write(bbs_bits.tobytes())
    print(f"BBS binary output saved to {bbs_bin_filename}")

    # Save bit string output
    bbs_txt_filename = f"{prng_name}_output.txt"
    bbs_txt_path = os.path.join(output_dir, bbs_txt_filename)
    with open(bbs_txt_path, "w") as f:
        f.write(bbs_bits.bin)
    print(f"BBS bit string output saved to {bbs_txt_filename}")

    # --- Save PRNG information to an info file ---
    info_filename = f"{prng_name}_info.txt"
    info_path = os.path.join(output_dir, info_filename)
    with open(info_path, "w") as f:
        f.write(f"PRNG integer value: {bbs_bits.uint}\n")
        f.write(f"PRNG hex value: {bbs_bits.hex}\n")
        # Secrets
        f.write(f"p: {p}\n")
        f.write(f"q: {q}\n")
        f.write(f"seed: {seed}\n")
        f.write(f"\n Generated in {duration:.4f} seconds\n")
    print(f"BBS PRNG info saved to {info_filename}")


if __name__ == '__main__':
    main()
