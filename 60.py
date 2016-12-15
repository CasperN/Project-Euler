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
        for b in range(100):
            m = max(m, sum(int(s) for s in str(a**b)))
    return m

def p57():
    """
    square root of two is the limit of this fractional series
    of the first 1000 points, how many has more digits in the numerator
    """
    #1 calculate recurisve part
    a,b = 1,2 # first fraction
    count = 0
    for i in range(1,1000):
        a,b = nextab(a,b)
        print(a+b,b)
        digits_num = len(str(a+b)) #unsimplified
        digits_den = len(str(b))
        count += (digits_num > digits_den)
    return count

def nextab(a,b):
    return b, 2*b+a

def p58():
    """
    Arrange the natural numbers in a counterclockwise spiral and observe
    squares centered at 1. At what square side length does the percentage of
    primes along the main diagonals fall below 10%
    """
    n = 1           # square of length 2n-1
    numprimes = 3.0   # 3,5,7
    while numprimes/(4*n+1) >= .1: # 4n+1 is number of entries on main diagonals
        n += 1
        corners = [(2*n + 1)**2 - x*n for x in (2,4,6)] # last corner is square numbers
        numprimes += sum(isPrime(c) for c in corners)
    return 2*n + 1


def p59():
    """"""

    with open('p059_cipher.txt','r') as f:
        raw = [tobin(x) for x in f.read().strip().split(',')]

    cyphers = []
    for key in itertools.permutations('abcdefghijklmnopqrstuvwxyz',3):
        junk = 0
        keybin = [tobin(ord(k)) for k in key]
        text = ''
        for i, x in enumerate(raw):
            c = chr(int(xor(keybin[i%3],x),2))
            text += c
            junk += (c in '{\}|&!`~/=?<>$%-^*(+);@#')
            if junk >= 20:
                break

        if junk < 20:
            cyphers.append((key,junk,text))
    cyphers.sort(key = lambda x:x[1])
    return cyphers

def tobin(x):
    return bin(256+int(x))[3:]

def xor(a,b):
    """
    a xor b, where they are both 8 bit binary strings
    """
    return ''.join(str(x) for x in (int   (bool(int(i)) != bool(int(j)))
                                for i,j in zip(a,b)))


def p60(n=10000,k=5):
    """
    Find the lowest sum of a set of 5 primes for which the concatination of
    and two primes will result in a prime
    """
    ps = primeSieve(n)
    ps = ps[1:] #2 is obviously not gonna work out
    pairGraph = {}
    for a,b in itertools.combinations(ps,2):
        ab = int("%d%d"%(a,b))
        ba = int("%d%d"%(b,a))
        if (isPrime(ab) and isPrime(ba)):
                pairGraph[a] = pairGraph.get(a,set()) | {b}
                pairGraph[b] = pairGraph.get(b,set()) | {a}
    # We now have a graph and need to find a 5 clique (k5)

    changes = True
    while changes:
        changes = False
        for v in pairGraph.keys():
            pairGraph[v] = {n for n in pairGraph[v] if
                            len(pairGraph.get(n,set()) & pairGraph[v]) >= k-2 }
            # if intersection < k-2 then n,v don't share a k clique
            if len(pairGraph[v]) < k-1:
                pairGraph.pop(v)
                changes = True

    return sum(pairGraph.keys())

"""
    pairs = set()
    for k in pairGraph.keys():
        for v in pairGraph[k]:
            if k<v:
                pairs.add((k,v))
            else:
                pairs.add((v,k))
    pairs = [set(a) for a in pairs]

    print "finding quads on {} pairs".format(len(pairs))

    quads = []
    for a,b in itertools.combinations(pairs,2):
        if len(a.intersection(b))>0:
            continue
        if any(a.union(b) <= q for q in quads):
            continue
        a1,a2 = a
        b1,b2 = b
        concat_permutations = [(a1,b1),(b1,a1), (a1,b2),(b2,a1),
                               (a2,b1),(b1,a2), (a2,b2),(b2,a2)]
        if all(isPrime(int("%d%d"%(x,y))) for x,y in concat_permutations):
            quads.append(a.union(b))
    print '{} quads'.format(len(quads))
    print quads
    quintuples = []
    for a,b in itertools.combinations(quads,2):
        if not len(a.intersection(b))==3:
            continue
        x,y = a^b
        if isPrime(int("%d%d"%(x,y))) and isPrime(int("%d%d"%(y,x))):
            quintuples.append(a.union(b))

    return quintuples
"""
