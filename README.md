# Blum Blum Shub vs Cha Cha 20

Python implementations for two cryptographically secure pseudorandom number generators (PRNGs):

ChaCha20 PRNG (implemented in chacha20.py)

Blum Blum Shub (BBS) PRNG (implemented in bbs.py)

The goal of the project is to compare these two PRNGs by generating long bit strings (which you can later test with test suite of your choice) and analyzing their randomness properties.

## Overview
ChaCha20 PRNG:
A stream cipher–based PRNG that produces random bits using a 32-byte key and a 12-byte nonce. This implementation focuses on clarity and ease of comparison.

Blum Blum Shub (BBS) PRNG:
A PRNG based on the hardness of factoring large numbers. BBS produces random bits by repeatedly squaring modulo n = p × q.

Output Generation:
generator.py prompts the user for the desired number of bits, generates random bit strings using both PRNGs, and saves the outputs to text files.

## Usage

## Usage

### Generate output for both PRNGs (ChaCha20 and BBS)

    python generator.py

You will be prompted for:
- Number of bits to generate
- (Optional) Custom primes `p` and `q` for BBS
- (Optional) Custom seed for BBS

Outputs:
- Bit string and binary files for both PRNGs in `output/`
- Info files with internal parameters and timing stats

---

### Generate ChaCha20 PRNG output only

    python cha_gen.py

Prompts for:
- Number of bits
- Custom name for output

Outputs saved in `chacha_output/`:
- `<name>_output.bin`: binary bitstream
- `<name>_output.txt`: bitstring
- `<name>_info.txt`: key, nonce, constant, and generation time

---

### Generate BBS PRNG output only

    python bbs_gen.py

Prompts for:
- Number of bits
- (Optional) custom `p`, `q`, and seed
- Custom name for output

Outputs saved in `bbs_output/`:
- `<name>_output.bin`: binary bitstream
- `<name>_output.txt`: bitstring
- `<name>_info.txt`: p, q, seed, and generation time

---

### Use ChaCha20 in your own code

    from chacha20 import ChaChaPRNG
    import secrets

    key = secrets.token_bytes(32)
    nonce = secrets.token_bytes(12)
    prng = ChaChaPRNG(key, nonce)

    bits = prng.generate_bits(256)
    bytes_ = prng.generate_bytes(32)
    string = prng.generate_string(128)

---

### Use Blum Blum Shub in your own code

    from bbs import BlumBlumShubPRNG

    p, q = 499, 547
    seed = 1597
    bbs = BlumBlumShubPRNG(p, q, seed)

    bits = bbs.generate_bits(256)
    bytes_ = bbs.generate_bytes(32)
    string = bbs.generate_string(128)


## Dependencies

This project relies on the following external Python libraries:

- **[sympy](https://www.sympy.org/)**  
  A powerful library for symbolic mathematics. In this project, sympy is used for efficient prime generation and verification, which is essential for cryptographic applications such as Blum Blum Shub (BBS).

- **[bitstring](https://github.com/scottprahl/bitstring)**  
  A versatile library for bit-level manipulation. It is used in our implementation for creating and handling bit-level data, converting between different representations, and working with binary sequences.

### Installation

You can install both libraries using pip by running:

```bash
pip install sympy bitstring