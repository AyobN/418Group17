import math
import struct
import secrets
from bitstring import BitArray

# "expand 32-byte k"
constants = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]

"""
Rotation function for rotating bits
v: 32 bit block (chacha inner block size)
c: num bits to rotate
"""
def rotate(v, c):
    # mod 32 as to not shift bigger than block size
    c = c % 32
    # shift left and mask bits
    left_shift = (v << c) & 0xffffffff
    counter = 32 - c
    # Get wrapped bits
    right_shift = v >> counter
    return (left_shift | right_shift)

"""
Function to simulate ChaCha20 quarter round
a,b,c,d : indicate which indices to operate on
"""
def quarter_round(state, a, b, c, d):
    state[a] = (state[a] + state[b]) & 0xffffffff
    state[d] = state[d] ^ state[a]
    state[d] = rotate(state[d], 16)

    state[c] = (state[c] + state[d]) & 0xffffffff
    state[b] = state[b] ^ state[c]
    state[b] = rotate(state[b], 12)

    state[a] = (state[a] + state[b]) & 0xffffffff
    state[d] = state[d] ^ state[a]
    state[d] = rotate(state[d], 8)

    state[c] = (state[c] + state[d]) & 0xffffffff
    state[b] = state[b] ^ state[c]
    state[b] = rotate(state[b], 7)

"""
Function to generate 512 bit pseudorandom block
k: 256 bit key (as bytes)
c: counter
n: 96 bit nonce (as bytes)

return: 512 pseudorandom bits
"""
def chacha20_block(k, c, n):
    k_bits = list(struct.unpack('<8L', k))
    n_bits = list(struct.unpack('<3L', n))

    initial_state = constants + k_bits + [c] + n_bits
    current_state = initial_state.copy()

    # Do 20 quarter rounds [10 column, 10 diagonal]
    for i in range(10):
        # Columns
        quarter_round(current_state, 0, 4, 8, 12)
        quarter_round(current_state, 1, 5, 9, 13)
        quarter_round(current_state, 2, 6, 10, 14)
        quarter_round(current_state, 3, 7, 11, 15)
        # Diags
        quarter_round(current_state, 0, 5, 10, 15)
        quarter_round(current_state, 1, 6, 11, 12)
        quarter_round(current_state, 2, 7, 8, 13)
        quarter_round(current_state, 3, 4, 9, 14)

    # Mix state
    for i in range(16):
        current_state[i] = (current_state[i] + initial_state[i]) & 0xffffffff

    # return bytes
    bytes = struct.pack('<16L', *current_state)
    
    return bytes

"""
Our ChaCha20 PRNG
Key length: 256 bits
Nonce: 96 bits
Generates 512 bit keystreams. Use functions generate_bits/generate_bytes
    to return output desired amount of bits/bytes
"""
class ChaChaPRNG:
    def __init__(self, key, nonce, counter=1):
        if len(key) != 32:
            raise ValueError("Key must be 32 bytes long.")
        if len(nonce) != 12:
            raise ValueError("Nonce must be 12 bytes long.")
        self.key = key
        self.nonce = nonce
        self.counter = counter

        # Internal buffer for block bytes and pointer to the next unread byte.
        self.buffer = b""
        self.buffer_offset = 0

    """
    Generate a new 64-byte block of pseudorandom data.
    """
    def _refill(self):
        self.buffer = chacha20_block(self.key, self.counter, self.nonce)
        self.counter += 1
        self.buffer_offset = 0

    
    def generate_bytes(self, n):
        """
        Return n pseudorandom bytes.
        """
        result = bytearray()
        while n > 0:
            if self.buffer_offset >= len(self.buffer):
                self._refill()
            available = len(self.buffer) - self.buffer_offset
            take = min(n, available)
            result.extend(self.buffer[self.buffer_offset:self.buffer_offset+take])
            self.buffer_offset += take
            n -= take
        return bytes(result)
    
    def generate_string(self, n):
        """
        Return string of n random bits
        n: number of bits to generate
        """
        # Calculate the number of bytes required to produce at least n bits.
        num_bytes = (n + 7) // 8
        rand_bytes = self.generate_bytes(num_bytes)
        # Convert each byte to its 8-bit binary representation.
        bit_str = ''.join(f'{b:08b}' for b in rand_bytes)
        # Return only the first n bits.
        return bit_str[:n]
    
    
    def generate_bits(self, n):
        """
        Return n random bits of BitArray
        n: number of bits to generate
        """
        # Calculate the number of bytes required to produce at least n bits.
        num_bytes = (n + 7) // 8
        rand_bytes = self.generate_bytes(num_bytes)
        # Convert each byte to its 8-bit binary representation.
        bits = BitArray(bytes=rand_bytes)
        # Return only the first n bits.
        return bits[:n]
    
    def get_key():
        return key
    
    def get_nonce():
        return nonce
    
    def get_c():
        return constants

# Example usage:
if __name__ == "__main__":
    # Define a secure 32-byte key and a 12-byte nonce.
    key = secrets.token_bytes(32)
    nonce = secrets.token_bytes(12) 
    
    # Create the PRNG object.
    prng = ChaChaPRNG(key, nonce)
    
    # Generate 128 pseudorandom bytes.
    random_bytes_output = prng.generate_bytes(128)
    print("Random Bytes (hex):", random_bytes_output.hex())

    
    # Generate 1000 pseudorandom bits (String).
    random_string = prng.generate_string(1000)
    print("Length of Random Bits Output:", len(random_string))
    # Show first 100 bits
    print("First 100 bits:", random_string[:100])

    # Generate 1000 pseudorandom bits
    random_bits = prng.generate_bits(1000)
    print("Length of Random Bits Output:", len(random_bits))
    # Show first 100 bits
    print("First 100 bits:", random_bits[:100].bin)