import decimal
import numpy as np

def primeSieve(n):
    """
    yields primes up to n
    can be fed primes
    """
    n+=1
    sieve = [True]*n
    sieve[1] = 0
    primes = [2]
    morePrimes = True
    while morePrimes:
        for i in range(primes[-1]*2 ,n ,primes[-1]):
            sieve[i] = False
        morePrimes = False
        for s in range(primes[-1] + 1, n):
            if sieve[s] != 0:
                morePrimes = True
                primes.append(s)
                break
    return primes



def primegenerator():
    """
    generates prime number (in order)
    Its horribly inefficient and should be updated
    use pyprimes
    """
    yield 2
    primes = [2]
    current = 3
    while True:
        isprime = True
        for p in primes:
            if current % p == 0:
                isprime  = False
                break
        if isprime:
            primes.append(current)
            yield current
        current +=1

def fibbonacci(n):
    """
    formula for nth digit
    """
    decimal.getcontext().prec = 20
    phi = decimal.Decimal((1+5.0**.5)/2)
    psi = decimal.Decimal((1-5.0**.5)/2)
    return int((phi ** n - psi ** n)/decimal.Decimal(5.0**.5))

def divisors(n, proper = True):
    """
    returns a list of (proper) divisors
    """
    curr, small_divs, big_divs = 2,[1],[n]
    while curr < big_divs[-1]:
        if n % curr == 0:
            small_divs.append(curr)
            big_divs.append(n/curr)
        curr +=1
    if proper:
        return set(small_divs + big_divs[1:])
    else:
        return set(small_divs+big_divs)


def primedivisors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

def sequenceDifference(gen,both = True):
    """
    yields the sequence and difference between points in the sequence
    """
    a = next(gen)
    while True:
        b = a
        a = next(gen)
        yield b, a-b

def palindromes():
    """
    yields base 10 palindromes (leading zeros do not count)
    """
    mag = 1
    while True:
        firsthalf = mag/2 + mag%2
        for i in range(10 ** (firsthalf-1), 10 ** firsthalf):
            s = str(i)
            yield int( s + s[-1-(mag%2)::-1] )
        mag+=1

def isPrime(n):
    """
    returns if n is prime (surprise!!!)
    """
    if n == 2 or n == 3:     return True
    if n < 2  or n % 2 == 0: return False
    if n < 9:                return True
    if n%3 == 0:             return False
    r = int(n**0.5)
    f = 5
    while f <= r:
        if n % f == 0:          return False
        if n % (f + 2) == 0:    return False
        f +=6
    return True

def primativePythagoreanTriples(limit=None):
    """
    generates prime Pythagorean triples
    Stolen from stackexchange... wolfram has the proof
    http://mathworld.wolfram.com/PythagoreanTriple.html
    """
    u = np.mat(' 1  2  2; -2 -1 -2; 2 2 3')
    a = np.mat(' 1  2  2;  2  1  2; 2 2 3')
    d = np.mat('-1 -2 -2;  2  1  2; 2 2 3')
    uad = np.array([u, a, d])
    m = np.array([3, 4, 5])
    while m.size:
        m = m.reshape(-1, 3)
        if limit:
            m = m[m[:, 2] <= limit]
        for triple in m:
            yield triple
        m = np.dot(m, uad)


def gcd(x,y):
    """
    Euclid's Algorithm for finding greatest common divisor
    """
    assert x >= y
    #print "{}\t=\t{}\t*\t{}\t+\t{}".format(x,x/y,y,x%y)
    n = x%y # note n < y
    if x%y == 0:
        return y
    else:
        return gcd(y,n)
