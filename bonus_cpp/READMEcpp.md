# ChaCha20 Encryption Tool

This is a command-line program that performs **ChaCha20 encryption and decryption** using a 256-bit key and a 96-bit nonce.  
ChaCha20 is a symmetric stream cipher — the same function is used for both encryption and decryption.

---

## Requirements

You must provide:

- `key.txt` — a **32-byte** binary file (your ChaCha20 key)
- `nonce.txt` — a **12-byte** binary file (your nonce)
- `input.txt` — (optional) the file to encrypt or decrypt

---

## How to Use

### Encrypt or Decrypt a File

```bash
./program key.txt nonce.txt input.txt