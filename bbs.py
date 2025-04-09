import math

"""
Our BBS PRNG
Algorithm:
    1. Choose two primes (p,q) that are both congruent to 3mod4
    2. n = p * q
    3. Choose an int relatively prime to n as seed
    4. x_0 = seed^2 mod n
    5. x_(i+1) = x_(i)^2 mod n
    6. output LSB of each state as random bit
Use functions generate_bits/generate_bytes
    to return output desired amount of bits/bytes
"""

class BlumBlumShubPRNG:

    def __init__(self, p, q, seed):
        # Ensure that p and q are congruent to 3 modulo 4.
        if p % 4 != 3 or q % 4 != 3:
            raise ValueError("Both p and q must be congruent to 3 modulo 4.")
        
        # Calculate n = p * q.
        self.n = p * q
        
        # Ensure that the seed is relatively prime to n.
        if math.gcd(seed, self.n) != 1:
            raise ValueError("Seed must be relatively prime to n (i.e., gcd(seed, n) must equal 1).")
        
        # Initialize the internal state: a common initialization is to set x0 = seed^2 mod n.
        self.state = (seed * seed) % self.n

    """
    Function to generate next bit
        
    Updates the internal state by squaring it mod n and returns
    LSB of new state
    """
    def _next_bit(self):
        # new state
        self.state = (self.state * self.state) % self.n
        
        # return LSB
        return self.state & 1

    """
    Return string of n random bits
    n: number of bits to generate
    """
    def generate_bits(self, n):
        bits = []
        for _ in range(n):
            bit = self._next_bit()
            bits.append(str(bit))
        return ''.join(bits)

    """
    Return n pseudorandom bytes.
    """
    def generate_bytes(self, n):
        total_bits = n * 8
        bit_str = self.generate_bits(total_bits)
        byte_array = bytearray()
        # Process the string 8 bits at a time to form each byte
        for i in range(0, total_bits, 8):
            byte_chunk = bit_str[i:i+8]
            byte_value = int(byte_chunk, 2)
            byte_array.append(byte_value)
        return bytes(byte_array)

# Example usage:
if __name__ == "__main__":
    # For demonstration, we'll use small primes
    # In practice, use much larger primes for security
    p = 499  # p must be a prime and congruent to 3 mod 4
    q = 547  # q must also be a prime and congruent to 3 mod 4
    seed = 1597  # Choose a seed that is relatively prime to n (p * q)

    # Create an instance of the Blum Blum Shub PRNG
    bbs = BlumBlumShubPRNG(p, q, seed)

    # Generate 100 random bits
    random_bits = bbs.generate_bits(100)
    print("100 random bits:")
    print(random_bits)

    # Generate 16 random bytes
    random_bytes = bbs.generate_bytes(16)
    print("16 random bytes (in hex):")
    print(random_bytes.hex())