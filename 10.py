from helpers import primegenerator
from functools import reduce


def problem1():
    """
    How many numbers < 1000 are multiples of 3 or 5
    """
    return sum(i for i in range(1000) if i % 5 == 0 or i % 3 == 0)


def problem2():
    s, f_old, f_new = 0, 0, 1
    while f_new < 4000000:
        if f_new % 2 == 0:
            s += f_new
        temp = f_new
        f_new += f_old
        f_old = temp
    return s


def problem3(number=600851475143):
    """
    The prime factors of 13195 are 5, 7, 13 and 29.
    What is the largest prime factor of the number 600851475143 ?
    """

    p = 2
    factors = []
    while p < number:
        if number % p == 0:
            number /= p
            factors.append(p)
            print("{} and {}".format(p, number))
        else:
            p += 1
    factors.append(number)
    return max(factors)


def problem4():
    """
    A palindromic number reads the same both ways. The largest palindrome made
    from the product of two 2-digit numbers is 9009 = 91 x 99.
    Find the largest palindrome made from the product of two 3-digit numbers.
    """
    for n in range(1000):
        for i in range(n / 2 + n % 2):  # first half round up
            a = 999 + i - n
            b = 999 - i
            if str(a * b) == "".join(reversed(str(a * b))):
                return a, b
    assert False


def problem6():
    """
    Find the difference between the sum of the squares of the first one hundred
    natural numbers and the square of the sum.
    """
    s, ss = 0, 0
    for i in range(1, 101):
        s += i
        ss += i ** 2
    return s ** 2 - ss


def problem7(n=10001):
    """
    What is the 10 001st prime number?
    """
    gen = primegenerator()
    for i in range(10000):
        next(gen)
    yield next(gen)


def problem8():
    number = """73167176531330624919225119674426574742355349194934
    96983520312774506326239578318016984801869478851843
    85861560789112949495459501737958331952853208805511
    12540698747158523863050715693290963295227443043557
    66896648950445244523161731856403098711121722383113
    62229893423380308135336276614282806444486645238749
    30358907296290491560440772390713810515859307960866
    70172427121883998797908792274921901699720888093776
    65727333001053367881220235421809751254540594752243
    52584907711670556013604839586446706324415722155397
    53697817977846174064955149290862569321978468622482
    83972241375657056057490261407972968652414535100474
    82166370484403199890008895243450658541227588666881
    16427171479924442928230863465674813919123162824586
    17866458359124566529476545682848912883142607690042
    24219022671055626321111109370544217506941658960408
    07198403850962455444362981230987879927244284909188
    84580156166097919133875499200524063689912560717606
    05886116467109405077541002256983155200055935729725
    71636269561882670428252483600823257530420752963450
    """
    number = number.replace(" ", "").replace("\n", "")
    sup = 0
    for i in range(len(number) - 13):
        subsequence = number[i : i + 13]
        prod = reduce(lambda x, y: int(x) * int(y), subsequence)
        if prod > sup:
            sup = prod
    return sup


def problem9():
    """
    There exists exactly one Pythagorean triplet for which a + b + c = 1000.
    Find the product abc.
    """
    a, b, c = 0, 0, 0
    for i in range(2, 1000):  # avoid 0
        breaker = False
        for j in range(1, i / 2 + i % 2):
            a = i - j
            b = j
            c = 1000 - i
            if a ** 2 + b ** 2 == c ** 2:
                breaker = True
                break
        if breaker:
            break
    return a * b * c


def problem10(n=2000000):
    """
    Find the sum of all the primes below 2 million
    """
    tot, prime, pg = 0, 0, primegenerator()
    while prime < n:
        tot += prime
        prime = next(pg)
    return tot
