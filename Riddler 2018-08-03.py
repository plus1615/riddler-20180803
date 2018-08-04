import math
from functools import reduce

def tri(x):
    """xth triangular number."""
    return x * (x+1) // 2

def trf(x):
    """Floor of the triangular root of x."""
    return math.floor((math.sqrt(8*x + 1) - 1)/2)

def coeff(x):
    """The coefficient of 2**-x for the Riddler answer."""
    return sum(pow(-1, i+1) * (tri(i) % i == x % i) for i in range(1, trf(x)+1))

def factors(n):    
    return set(reduce(list.__add__, 
        ([i, n//i] for i in range(1, int(pow(n, 0.5) + 1)) if n % i == 0)))

def hoeft(x):
    """The coefficient using magic."""
    co = 0
    for h in factors(x):
        # We're only looking at odd factors of x.
        if h % 2 == 0:
            continue
        if h + 1 <= 2 * x // h:
            co += 1
        else:
            co -= 1
    return co

def solve(x, algo=hoeft):
    """The answer for all exponents up to x."""
    return sum(pow(2, -x) * algo(x) for x in range(1, x+1))

def middiv(x):
    """Found this on OEIS by searching for the coefficient results.
    No idea why it works."""
    co = 0
    for i in factors(x):
        if pow(x/2, 0.5) <= i < pow(x*2, 0.5):
            co += 1
    return co
