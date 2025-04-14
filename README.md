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


---



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

## Testing

We have provided the scripts we used for our testing. You can use our code as described in the Usage section to generate your own 

### Generate specific PRNG samples to custom sizes and labels

    python testing/generate_test_samples.py --type [chacha|bbs] --label <name> --bits <count> --prime_size <size_for_bbs>

Creates a single sample for testing. Output is saved in `diehard_inputs/`.

---

### Generate full test set (ChaCha, BBS-weak, BBS-strong) at once

    python testing/generate_all_test_samples.py --bits <count>

Generates all 3 PRNGs with specified bit length (default: 1 million).

---

### Run Dieharder tests on generated `.bin` files

    bash testing/run_dieharder.sh

Runs 5 core randomness tests on all files in `diehard_inputs/`. Results go to `diehard_results/`.

---

### Check reproducibility of PRNGs

    python testing/reproducibility_test.py

Verifies that both BBS and ChaCha20 produce identical output when using same inputs.

---

### Benchmark PRNG speed at multiple sizes

    python testing/test_performance.py

Tests generation time at 1M, 10M, and 100M bits for ChaCha, BBS-weak (128-bit), and BBS-strong (1024-bit). Saves results to `testing/performance_results.txt`.

---

### Generate and benchmark BBS variants across prime sizes

    python testing/generate_bbs_samples.py

Generates 100M-bit samples for BBS with primes from 32 to 1024 bits. Saves binaries and timing logs to `bbs_analysis_data/`.



## Dependencies

- Python **3.6+**

This project relies on the following external Python libraries:

- **[sympy](https://www.sympy.org/)**  
  A powerful library for symbolic mathematics. In this project, sympy is used for efficient prime generation and verification, which is essential for cryptographic applications such as Blum Blum Shub (BBS).

- **[bitstring](https://github.com/scottprahl/bitstring)**  
  A versatile library for bit-level manipulation. It is used in our implementation for creating and handling bit-level data, converting between different representations, and working with binary sequences.

### Installation

You can install both libraries using pip by running:

```bash
pip install sympy bitstring
```


# 🔐 ChaCha20 Encryption Tool

This is a command-line program that performs **ChaCha20 encryption and decryption** using a 256-bit key and a 96-bit nonce, from files provided as command line arguments.  
ChaCha20 is a symmetric stream cipher — the same function is used for both encryption and decryption. An output file, output.txt is generated from the resultant XOR. To decrypt, one must rename the file 'output.txt' to another filename, inputting a file with the name 'output.txt' will present problems as the output file is of the same name. 

---

## ⚙️ Requirements

You must provide:

- `key.txt` — a **32-byte** binary file (your ChaCha20 key)
- `nonce.txt` — a **12-byte** binary file (your nonce)
- `input.txt` — (optional) the file to encrypt or decrypt

---

## 🚀 How to Use

### 🔁 Encrypt a File

```bash
$ ./program <key.txt> <nonce.txt> <input.txt>
```

For a 32-byte key file called `key.txt` and a 12-byte nonce file called `nonce.txt` and an an input file called lorem.txt (could be plain/ciphertext)
```bash
$ ./program key.txt nonce.txt lorem.txt
Operation complete. Output saved to 'output.txt'.
```
### 🔁 Decrypt a file
if your your ciphertext is named `output.txt` rename it to something else 
```bash
$ mv output.txt ciphertext
$ ./program key.txt nonce.txt ciphertext 
Operation complete. Output saved to 'output.txt'.
```
`output.txt` should be the same as `lorem.txt` or whatever your 'plaintext' was, as this program works with both binary and plaintext files (images, audio, text files, pdf's). 





Run the program with your ciphertext as input
```bsah
$ ./program key.txt nonce.txt ciphertext
```

