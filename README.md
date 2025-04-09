# Blum Blum Shub vs Cha Cha 20

Python implementations for two cryptographically secure pseudorandom number generators (PRNGs):

ChaCha20 PRNG (implemented in chacha20.py)

Blum Blum Shub (BBS) PRNG (implemented in bbs.py)

The goal of the project is to compare these two PRNGs by generating long bit strings (which you can later test with the NIST Statistical Test Suite) and analyzing their randomness properties.

## Overview
ChaCha20 PRNG:
A stream cipher–based PRNG that produces random bits using a 32-byte key and a 12-byte nonce. This implementation focuses on clarity and ease of comparison.

Blum Blum Shub (BBS) PRNG:
A PRNG based on the hardness of factoring large numbers. BBS produces random bits by repeatedly squaring modulo n = p × q. For demonstration, small primes are currently used, but you are encouraged to use larger primes for more robust experiments.

Output Generation:
NIST.py prompts the user for the desired number of bits, generates random bit strings using both PRNGs, and saves the outputs to text files.
