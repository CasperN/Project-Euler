import itertools
import math
import decimal
import numpy as np
import re
from helpers import *

def p21(n = 10000):
    """
    Let d(n) be defined as the sum of proper divisors of n (numbers less than n
    which divide evenly into n). If d(a) = b and d(b) = a, where a != b, then a
    and b are an amicable pair and each of a and b are called amicable numbers.
    Evaluate the sum of all the amicable numbers under 10000.
    """

    pairs = [(a,sum(divisors(a))) for a in range(n)]
    res = 0
    for i in range(len(pairs)-1):
        lonely = True #no amicable pairs
        a = pairs[i]
        for b in pairs[i+1:]:
            if a[0]==b[1] and b[0]==a[1]:
                res += b[0]
                lonely = False
        if not lonely:
            res += a[0]
    return res

def p22():
    """
    Provided is a 46K text file containing over five-thousand first names, begin
    by sorting it into alphabetical order. Then working out the alphabetical
    value for each name, multiply this value by its alphabetical position in the
    list to obtain a name score.

    For example, when the list is sorted into  alphabetical order,
    COLIN, which is worth 3 + 15 + 12 + 9 + 14 = 53, is the  938th name in the
    list. So, COLIN would obtain a score of 938 * 53 = 49714.

    What is the total of all the name scores in the file?
    """
    FILENAME = 'p022_names.txt'
    letterno = {let:no for let,no in
                    zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ',range(1,27))}
    with open(FILENAME,'r') as f:
        names = f.readline().replace('"','').split(',')
    names = sorted(names)

    total,place = 0,1
    for name in names:
        score = reduce(lambda x,y: x+y, (letterno[let] for let in name))
        total += place * score
        place += 1
    return total

def p23():
    """
    a number n is called deficient if the sum of its proper divisors is less
    than n and abundant if this sum exceeds n. It can be shown that all integers
    greater than 28123 can be written as the sum of two abundant numbers.
    Find the sum of all positive integers that cannot be written as the sum of
    two abundant numbers.
    """
    abundants = [a for a in range(1,28123) if a < sum(divisors(a)) < 28123]
    not_sum_of_2_abundants = set(range(28123))
    for a,b in itertools.product(abundants,abundants):
        not_sum_of_2_abundants -= {a+b}
    return sum(not_sum_of_2_abundants)



def digitSwap_permuter( s, digit, permute):
    """
    helper to orderedPermutations, permutes the sequence
    [:] = [:a][a][a+1:b][b][b+1:] => [:a][b][a][a+1:b][b+1:]
    """
    a = len(s) - digit - 1
    b = a + permute
    return s[:a] + s[b] + s[a], s[a+1:b] + s[b+1:]

def orderedPermutations(n,start = '0123456789'):
    """"
    assuming start's digits are in ascending order
    returns the nth permutation in order
    """
    remainder = n-1 # I start counting from 0
    sequence = start
    while remainder > 0:
        i, ifac = 1,1
        while ifac <= remainder:
            i += 1
            ifac = math.factorial(i)
        i -= 1; ifac = math.factorial(i)
        assert i < len(sequence)
        permute   = remainder / ifac
        remainder = remainder % ifac
        sequence = digitSwap_permuter(sequence,i,permute)
    return sequence


def p24(s = '0123456789', n = 1000000):
    """
    A permutation is an ordered arrangement of objects.
    For example, 3124 is one possible permutation of the digits 1, 2, 3 and 4.
    If all of the permutations are listed numerically or alphabetically, we call
    it lexicographic order. The lexicographic permutations of 0, 1 and 2 are:
    012   021   102   120   201   210
    What is the millionth lexicographic permutation of the digits
    0, 1, 2, 3, 4, 5, 6, 7, 8 and 9?
    """
    return orderedPermutations(n,s)


def p25(n=1000):
    """
    what is the index of the first term in the Fibbonacci sequence to contain
    1000 digits?
    """
    mag = 1
    guess = 0
    while True:
        g = guess + 2**mag
        print g
        digits = len(str(fibbonacci(g)))
        if digits >= n:
            guess += 2 ** (mag-1)
            if mag == 1:
                break
            mag = 1
        else:
            mag +=1
    return guess

def p26(n=1000):
    """
    find the value d<1000 of which 1/d has the longest recurring cycle n its
    decimal fraction part
    """
    d = (0,0)
    for i in range(2,n):
        pd = [x for x in primedivisors(i) if x != 5 and x != 2]
        t = reduce(lambda x,y: x * y ,pd , 1)
        for rep in itertools.count(1):
            if int('9'*rep) % t == 0:
                if d[1] < rep:
                    d = (i, rep)
                break
    return d

def p27(lb=-1000,ub=1001):
    """
    Considering quadratics of the form:
    .   n**2 + a*n + b, where |a| < 1000 and |b| <= 1000
    Find the product of the coefficients, a and b, for the quadratic
    expression that produces the maximum number of primes for consecutive values
    of n, starting with n=0.
    """
    primes = primeSieve(3 * ub)

    streak = 0
    for a in range(lb,ub):
        for b in range(2-a,ub):
            seq = (n**2 + a*n + b for n in itertools.count())
            for i in itertools.count(1):
                seq_i = seq.next()
                if seq_i in primes:
                    if i > streak:
                        streak = i
                        ab = a,b
                else:
                    break
    return ab

def p28(side = 1001):
    """
    Starting with the number 1 and moving to the right in a clockwise direction a
    5 by 5 spiral is formed as follows:

    21 22 23 24 25
    20  7  8  9 10
    19  6  1  2 11
    18  5  4  3 12
    17 16 15 14 13

    It can be verified that the sum of the numbers on the diagonals is 101.
    What is the sum of the numbers on the diagonals in a 1001 by 1001 spiral
    formed in the same way?

    Note    3 +  5 +  7 +  9 = 4* 1 + 10* 2
    .      13 + 17 + 21 + 25 = 4* 9 + 10* 4
    """
    assert side % 2 == 1
    rotations = (side-1)/2
    total, base = 1,1
    for i in range(1,rotations+1):
        spacing = i*2
        total += 10*(i*2) + 4*base
        base += 4* spacing
    return total

def p29(low = 2, high = 100):
    """
    Consider all integer combinations of a**b for 2 <= a <= 5 and 2 <= b <= 5:
    If they are then placed in numerical order, with any repeats removed,
    we get the following sequence of 15 distinct terms:

    4, 8, 9, 16, 25, 27, 32, 64, 81, 125, 243, 256, 625, 1024, 3125

    How many distinct terms are in the sequence generated by a**b for
    2 <= a <= 100 and 2 <= b <= 100?
    """
    terms = set()
    for a in range(low, high + 1):
        for b in range(low, high +1):
            terms |= {a**b}
    return len(terms)

def p30(P = 5):
    """
    Find the sum of all the numbers that can be written as the sum of
    fifth powers of their digits.

    Note 5*9**6 = 354294 is the upper bound for all such numbers
    """
    for i in itertools.count(1):
        if 9 ** P * i < int('9' * i):
            break
    upperbound = (9 ** P) * i

    total = 0
    for number in range(2,upperbound+1): # start from 2 as 1 is not counted
        if number == sum(int(x)**P for x in str(number)):
            total  += number

    return total
