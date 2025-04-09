import gmpy2
from gmpy2 import next_prime

def generate_blum_prime(min_value):
    """
    Generate a prime number greater than or equal to min_value that is congruent to 3 mod 4.
    
    Parameters:
        min_value (int): The minimum value (lower bound) for the generated prime.
    
    Returns:
        An integer prime p such that p >= min_value and p % 4 == 3.
    """
    candidate = gmpy2.mpz(next_prime(min_value))
    # Ensure that the candidate satisfies the condition p % 4 == 3.
    while candidate % 4 != 3:
        candidate = gmpy2.mpz(next_prime(candidate))
    return int(candidate)