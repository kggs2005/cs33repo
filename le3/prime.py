def find_prime_factor(n: int) -> int | None:
    """
    Naive algorithm that finds the smallest prime number of a given number
    `n` by trying to divide the number from all numbers from `2` to `sqrt(n)`.

    Parameters:
        n (int): The number whose prime factor will be found.
    
    Returns:
        int: The smallest prime factor of `number`, or `None` if not found.
    """
    def _find_prime_factor(num: int) -> int:
        assert num >= 2
        for prime in range(2, num + 1):
            if prime**2 > num:
                return num
            if num % prime == 0:
                return prime
        assert False

    if n < 0:
        return find_prime_factor(-n)
    elif n in [0, 1]:
        return None
    else:
        return _find_prime_factor(n)


def eratosthenes_sieve(m: int) -> list[bool]:
    """
    The Eratosthenes sieve is an algorithm that checks all numbers up to the
    integer `m` on whether they are prime.

    Parameters:
        m (int): The upper limit of the sieve.
    
    Returns:
        list[bool]: If this list is `is_prime`, then `is_prime[n]` is `True` if
            `n` is prime, and `False` otherwise.
    """
    is_prime = [True] * (m + 1)
    is_prime[0] = is_prime[1] = False

    for d in range(2, m + 1):
        if is_prime[d]:
            for n in range(2 * d, m + 1, d):
                is_prime[n] = False
    
    return is_prime