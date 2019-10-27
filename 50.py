import numpy as np
import scipy as cp
import math
import itertools
from helpers import *
import pyprimesieve as pyPrime


def p41():
    """
    what is the largest n-digit pandigital prime that exists
    """
    best = 0
    s = "123456789"
    for i in range(len(s), 0, -1):
        for p in itertools.permutations(s[:i]):  # not in ascending order :(
            p = int("".join(p))
            if p > best and isPrime(p):
                best = p
        if best != 0:
            return best


def p42():
    """
    By converting each letter in a word to a number corresponding to its
    alphabetical position and adding these values we form a word value.
    words.txt is a 16K text file containing nearly two-thousand common English
    words, how many words have word values that are triangle numbers.
    """
    FILENAME = "p042_words.txt"
    with open(FILENAME, "r") as f:
        words = (w for w in f.readline().replace('"', "").split(","))

    letno = {
        let: no for let, no in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", list(range(1, 27)))
    }

    count = 0
    for w in words:
        wordscore = sum(letno[l] for l in w)
        a, b, c = 1, 1, -2 * wordscore
        positiveroot = (-b + math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
        if positiveroot.is_integer():  # wordscore is triangle number
            count += 1
    return count


def p43():
    """
    The number, 1406357289, is a 0 to 9 pandigital number because it is made up
    of each of the digits 0 to 9 in some order, but it also has a rather
    interesting sub-string divisibility property. Let d1 be the 1st digit, d2 be
    the 2nd digit, and so on. In this way, we note the following:
    .    d2 d3 d4  = 406  is divisible by 2
    .    d3 d4 d5  = 063  is divisible by 3
    .    d4 d5 d6  = 635  is divisible by 5
    .    d5 d6 d7  = 357  is divisible by 7
    .    d6 d7 d8  = 572  is divisible by 11
    .    d7 d8 d9  = 728  is divisible by 13
    .    d8 d9 d10 = 289  is divisible by 17
    Find the sum of all 0 to 9 pandigital numbers with this property.
    """
    tot = 0
    for i in itertools.permutations("0123456789"):
        i = "".join(i)
        hasProperty = all(
            int(i[a : a + 3]) % b == 0
            for a, b in zip(list(range(1, 8)), [2, 3, 5, 7, 11, 13, 17])
        )
        if hasProperty:
            tot += int(i)
    return tot


def p44():
    """
    Pentagonal numbers are generated by the formula, Pn=n(3n-1)/2. The first ten
    pentagonal numbers are: 1, 5, 12, 22, 35, 51, 70, 92, 117, 145, ...
    It can be seen that P4 + P7 = 22 + 70 = 92 = P8. However, their difference,
    70 - 22 = 48, is not pentagonal. Find the pair of pentagonal numbers, Pj and
    Pk, for which their sum and difference are pentagonal and D = |Pk - Pj| is
    minimised; what is the value of D?
    """
    j = 1
    for j in itertools.count(1):
        pj = pent(j)
        for i in range(1, j + 1):
            pi = pent(i)
            pk = pi + pj
            if is_pent(
                pk
            ):  # Note difference pk with pi or pj are pentagonal - need only sum
                if is_pent(pi + pk):
                    return pj
                if is_pent(pj + pk):
                    return pi


def pent(i):
    return (3 * i - 1) * i / 2


def is_pent(x):
    """
    returns if x is a pentagonal number
    I found this online lol
    """
    return ((1 + (24 * x + 1) ** .5) / 6).is_integer()


def p45(start=144):
    """
    triangle    Tn = n( n + 1)/2  <->   0 = n**2  + n - 2Tn
    pentagonal  Pn = n(3n - 1)/2  <->   0 = 3n**2 - n - 2Pn
    hexagonal   Hn = n(2n - 1)    <->   0 = 2n**2 - n -  Hn
    T285 = P165 = H143
    Find the next triangle number that is also pentagonal and hexagonal.
    """
    for n_hexagon in itertools.count(start):  # we want next after 143
        num = 2 * n_hexagon ** 2 - n_hexagon

        a, b, c = 1, 1, -2 * num
        n_triangle = (-b + math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
        triangle = n_triangle.is_integer()

        a, b, c = 3, -1, -2 * num
        n_pentagon = (-b + math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
        pentagonal = n_pentagon.is_integer()

        if triangle and pentagonal:
            return num


def p46():
    """
    It was proposed by Christian Goldbach that every odd composite number can be
    written as the sum of a prime and twice a square. It turns out that the
    conjecture was false. What is the smallest odd composite that cannot be
    written as the sum of a prime and twice a square?
    """
    for n in itertools.count(9, 2):
        if isPrime(n):
            continue
        found = False
        for i in range(int(math.sqrt(n / 2 - 1) + 1)):
            if isPrime(n - 2 * i ** 2):
                found = True
                break
        if not found:
            return n


def p47(numfactors=4, consecutive=4):
    """
    Find the first four consecutive integers to have four distinct prime factors.
    What is the first of these numbers?
    """

    history = [False] * consecutive
    for n in itertools.count(2):
        history[n % consecutive] = len(set(primedivisors(n))) == numfactors
        if all(history):
            return n + 1 - consecutive


def p48():
    # Lol trivial in python
    return str(sum(n ** n for n in range(1, 1001)))[-10:]


def p49():
    """
    The arithmetic sequence, 1487, 4817, 8147, in which each of the terms
    increases by 3330, is unusual in two ways: (i) each of the three terms are
    prime, and, (ii) each of the 4-digit numbers are permutations of one
    another. There are no arithmetic sequences made up of three 1-, 2-, or
    3-digit primes, exhibiting this property, but there is one other 4-digit
    increasing sequence. What 12-digit number do you form by concatenating the
    three terms in this sequence?
    """
    for a in range(1000, 3341):
        b, c = a + 3330, a + 6660
        property1 = all(isPrime(x) for x in (a, b, c))
        property2 = set(str(a)) == set(str(b)) == set(str(c))
        if property1 and property2:
            print(str(a) + str(b) + str(c))


def p50(n=3950):  # solved a slightly different problem
    """
    The prime 41, can be written as the sum of six consecutive primes:
    41 = 2 + 3 + 5 + 7 + 11 + 13
    This is the longest sum of consecutive primes that adds to a prime below
    one-hundred. The longest sum of consecutive primes below one-thousand that
    adds to a prime, contains 21 terms, and is equal to 953. Which prime, below
    one-million, can be written as the sum of the most consecutive primes?
    """
    primes = pyPrime.primes(n)
    for consecutives in range(len(primes), 0, -1):
        for i in range(len(primes) - consecutives):
            p = sum(primes[i : i + consecutives])
            if isPrime(p):
                print(" ".join(str(c) for c in primes[i : i + consecutives]))
                return p
