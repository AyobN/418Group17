#!/usr/bin/env python3
import os
import time
import secrets
from bitstring import BitArray
from chacha20 import ChaChaPRNG

def main():
    # --- Get Number of Bits ---
    num_bits_input = input("Enter the number of bits to generate for ChaCha20: ")
    try:
        num_bits = int(num_bits_input)
    except ValueError:
        print("Invalid input. Please enter an integer value for the number of bits.")
        exit(1)

    # --- Generate ChaCha20 Key and Nonce ---
    key = secrets.token_bytes(32)
    nonce = secrets.token_bytes(12)
    
    # Initialize ChaCha20 PRNG
    cha_prng = ChaChaPRNG(key, nonce)

    start_time = time.perf_counter()
    cha_bits = cha_prng.generate_bits(num_bits)
    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"ChaCha20: Generated {num_bits} bits in {duration:.4f} seconds.")

    prng_name = input("Name your ChaCha: ").strip()

    # Create output directory if it doesn't exist
    output_dir = "chacha_output"
    os.makedirs(output_dir, exist_ok=True)

    # Save binary output using user-defined base name
    cha_bin_filename = f"{prng_name}_output.bin"
    cha_bin_path = os.path.join(output_dir, cha_bin_filename)
    with open(cha_bin_path, "wb") as f:
        f.write(cha_bits.tobytes())
    print(f"ChaCha20 binary output saved to {cha_bin_filename}")

    # Save bit string output using user-defined base name
    cha_txt_filename = f"{prng_name}_output.txt"
    cha_txt_path = os.path.join(output_dir, cha_txt_filename)
    with open(cha_txt_path, "w") as f:
        f.write(cha_bits.bin)
    print(f"ChaCha20 bit string output saved to {cha_txt_filename}")


    constant = cha_prng.get_c()
    c_int = 0
    for const in constant:
        c_int = (c_int << 32) | const
    c_string = hex(c_int)

    key_int = int.from_bytes(key, byteorder='big')
    nonce_int = int.from_bytes(nonce, byteorder='big')

    # --- Save PRNG information to an info file ---
    info_filename = f"{prng_name}_info.txt"
    info_path = os.path.join(output_dir, info_filename)
    with open(info_path, "w") as f:
        f.write(f"PRNG integer value: {cha_bits.uint}\n")
        f.write(f"PRNG hex value: {cha_bits.hex}\n")
        f.write(f"Key integer value: {key_int}\n")
        f.write(f"Key hex value: {key.hex()}\n")
        f.write(f"Constant int value: {c_int}\n")
        f.write(f"Constant hex value: {c_string}\n")
        f.write(f"Nonce integer value: {nonce_int}\n")
        f.write(f"Nonce hex value: {nonce.hex()}\n")
        f.write(f"\n Generated in {duration:.4f} seconds\n")

    print(f"ChaCha20 PRNG info saved to {info_filename}")


if __name__ == '__main__':
    main()
