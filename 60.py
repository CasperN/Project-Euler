import numpy as np
import scipy as cp
import math
import itertools
from helpers import *
import pyprimesieve as pyPrime
from collections import Counter

def p51():
    """
    By replacing the 1st digit of the 2-digit number *3, it turns out that six
    of the nine possible values: 13, 23, 43, 53, 73, and 83, are all prime.
    By replacing the 3rd and 4th digits of 56**3 with the same digit, this
    5-digit number is the first example having seven primes among the ten
    generated numbers, yielding the family: 56003, 56113, 56333, 56443, 56663,
    56773, and 56993. Consequently 56003, being the first member of this family,
    is the smallest prime with this property. Find the smallest prime which, by
    replacing part of the number (not necessarily adjacent digits) with the same
    digit, is part of an eight prime value family.
    """ # sorry for all the loops
    primegen = (p for p in pyPrime.primes(1000000) if p > 56993)
    for p in primegen:
        for replaceNo in range(1,4):
            for places in itertools.combinations(range(len(str(p))),replaceNo):
                family = set()
                for replaceWith in range(10):
                    s = list(str(p)) # str doesn't allow replacement
                    r = str(replaceWith)
                    for i in places:
                        s[i] = r
                    s = ''.join(s)
                    if s[0]!='0' and isPrime(int(s)):
                        family.add(s)
                if len(family) == 8:
                    return family

def p52():
    """
    Find the smallest positive integer, x, such that 2x, 3x, 4x, 5x, and 6x,
    contain the same digits.
    """
    for magnitude in itertools.count(1): # not possible with single digits
        for i in range(10 ** magnitude, 10 ** (magnitude+1)/6 + 1):
            # max multiple is 6x, +1 to be inclusive
            x = Counter(str(i))
            if all( x == Counter(str(i * n)) for n in range(2,7)):
                return i

def p53():
    """
    It is not until n = 23, that a value exceeds 1000000: 23 choose 10 = 1144066.
    how many values of n choose r for n  <= 100 are greater than 1000000?
    """
    count = 0
    for n in range(23,101):
        for r in range(n/2,0,-1): # observe that to max n choose r, r = n/2
            n_choose_r = math.factorial(n)/math.factorial(r)/math.factorial(n-r)
            if n_choose_r > 1000000:
                if r == float(n)/2:
                    count += 1
                else:
                    count += 2 # n choose r = n choose (n-r)
            else:
                break
    return count

def pokerhand(hand):
    """
    1:  High Card:          Highest value card.
    2:  One Pair:           Two cards of the same value.
    3:  Two Pairs:          Two different pairs.
    4:  Three of a Kind:    Three cards of the same value.
    5:  Straight:           All cards are consecutive values.
    6:  Flush:              All cards of the same suit.
    7:  Full House:         Three of a kind and a pair.
    8:  Four of a Kind:     Four cards of the same value.
    9:  Straight Flush:     All cards are consecutive values of same suit.
    10: Royal Flush:        Ten, Jack, Queen, King, Ace, in same suit.
    Return (comborank, highcard)
    """ # if you think of it... a royal flush is the biggest straight flush
    assert len(hand) == 5
    if set('TJKQA') == set(h[0] for h in hand): # Royal flush
        return 10, 0
    value = [(str(v),v) for v in range(2,10)]
    value = dict( value + [('T',10),('J',11), ('Q',12),('K',13),('A',14)])
    flush = Counter(h[1] for h in hand).most_common()[0][1] == 5
    numbers = Counter(value[h[0]] for h in hand).items()
    numbers.sort(key = lambda card: (card[1], card[0]),reverse=True)
    # sort descending by frequency then by value
    high = numbers[0][0]
    second = numbers[1][0]
    if len(numbers) == 5:                    # straight or nothing
        low = numbers[4][0]
        straight = (high - low == 4)
        if straight and flush:
            return 9, high, second
        elif flush:
            return 6, high, second
        elif straight:
            return 5, high, second
        else:
            return 1, high, second
    elif len(numbers) == 4:                   # one pair
            return 2, high, second
    elif len(numbers) == 3:                   # two pair or triple
        if numbers[0][1] == 3:
            return 4, high, second
        else:
            return 3, high, second
    elif len(numbers) == 2:                   # full house or 4 of a kind
        if numbers[0][1] == 4:
            return 8, high, second
        else:
            return 7, high, second

def p54():
    """
    Given the file... how many hands of poker does player 1 win
    """
    FILE = "p054_poker.txt"
    f = open(FILE,'r')

    count = 0
    for line in f:
        cards = line.strip().split(' ')
        s1, s2 = pokerhand(cards[:5]), pokerhand(cards[5:])
        p1wins = []
        assert any(a!=b for a,b in zip(s1,s2))
        res = 'lose'
        for p1,p2 in zip(s1,s2):
            if p1 > p2:
                count +=1
                break
            elif p2 > p1:
                break
    f.close()
    return count

def p55(strt = 0, N=10000):
    """
    A number that never forms a palindrome through the reverse and add process
    is called a Lychrel number. Due to the theoretical nature of these numbers,
    and for the purpose of this problem, we shall assume that a number is
    Lychrel until proven otherwise. In addition you are given that for every
    number below ten-thousand, it will either (i) become a palindrome in less
    than fifty iterations, or, (ii) no one, with all the computing power that
    exists, has managed so far to map it to a palindrome.
    How many Lychrel numbers are there below ten-thousand?
    """
    untested = set(range(strt,N))
    lychrel = set()
    while len(untested) > 0:
        t = untested.pop()
        tested = [t]
        lyc = True
        for _ in range(50):
            t += int(str(t)[::-1])
            tested.append(t)
            if str(t) == str(t)[::-1]: # is palindrome
                lyc = False
                for x in tested[:-1]:
                    untested.discard(x) # discard non lychrel
                break
        if lyc:
            lycs = {t for t in tested if t < N}
            untested -= lycs
            lychrel |= lycs
    return len(lychrel)

def p56():
    """
    consider natural numbers of the form a**b, a,b<100.
    what is the maximal digit sum?
    """
    m = 0
    for a in range(100):
        for b in range(a,100):
            m = max(m, sum(int(s) for s in str(a**b)))
    return m
