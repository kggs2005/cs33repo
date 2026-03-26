def euclid(a: int, b: int) -> int:
    """
    Euclid's algorithm returns the greatest common divisor (GCD) of two integers
    using the following lemma:
    
    `GCD(a, b) = GCD(a - b, b)`

    Parameters:
        a (int): The first integer.
        b (int): The second integer.
    
    Returns:
        int: The GCD of `a` and `b`.
    """
    return a if b == 0 else euclid(b, a % b)


def extended_euclid(a: int, b: int) -> tuple[int, int, int]:
    """
    The extended Euclid algorithm returns the GCD as a linear combination of `a` and `b`.
    This is possible due to Bezout's lemma:

    If `g` is the GCD of `a` and `b`, then there exists integers `x`, `y`such that:

    `g = ax + by`

    Parameters:
        a (int): The first integer.
        b (int): The second integer.
    
    Returns:
        tuple[int,int,int]: The GCD, `x`, and `y`.
    """
    def _extended_euclid(a2: int, x: int, y: int, b2: int, x2: int, y2: int) -> tuple[int, int, int]:
        if b2 == 0:
            return (a2, x, y)
        else:
            quotient = a2 // b2
            return _extended_euclid(b2, x2, y2, a2 - quotient * b2, x - quotient * x2, y - quotient * y2)
    
    return _extended_euclid(a, 1, 0, b, 0, 1)


def linear_diophantine(a: int, b: int, c: int) -> tuple[int, int] | None:
    """
    This algorithm solves linear Diophantine equations of 2 variables:

    `ax + by = c`

    using Bezout's lemma.

    Parameters:
        a (int): The first integer.
        b (int): The second integer.
    
    Returns:
        tuple[int,int]: `x` and `y`.
    """
    gcd, x, y = extended_euclid(a, b)
    if gcd % c != 0:
        return None
    e = gcd // c
    return (x * e, y * e)