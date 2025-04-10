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

```bash
    python generator.py

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