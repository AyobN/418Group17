import secrets
from sympy import nextprime

def generate_blum_prime(bits):
    """
    Generate BBS prime

    Parameters:
        bits (int): The bit length of the desired prime
    
    Returns:
        int: A prime number of 'bits' bits such that prime % 4 == 3
    """
    assert bits >= 2, "Bit size must be at least 2."
    
    while True:
        # Generate a candidate with the desired bit length.
        # Ensure the high bit is set so that the candidate has exactly 'bits' bits,
        # and force it to be odd.
        candidate = secrets.randbits(bits)
        candidate |= (1 << (bits - 1)) | 1

        candidate = nextprime(candidate)

        # Ensure the candidate is still of the correct bit length.
        if candidate.bit_length() > bits:
            continue

        if candidate % 4 == 3:
            return candidate
        else:
            # If the candidate is prime but not congruent to 3 mod 4,
            # iterate through successive primes until we find one that meets the condition.
            while candidate.bit_length() == bits:
                candidate = nextprime(candidate)
                if candidate % 4 == 3:
                    return candidate
            # If we exceeded the bit length, start over.
            continue