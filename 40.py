from helpers import *
import numpy as np
import scipy as sp
import math
import itertools

def p31():
    """
    In England he currency is made of the pound P and pence p. There are 8 coins in
    circulation: 1p, 2p, 5p, 10p, 20p, 50p, 1P(100p), and 2P(200p)

    How many ways can 2P be made using any number of coins.
    """
    count = 1
    coins = [200,100,50,20,10,5,2] # Treat pence seperately
    pence = 0
    allocation = [1,0,0,0,0,0,0]   # first arangement
    while pence != 200:            # last arangement
        count += 0
        tot = sum(a*b for a,b in zip(coins,allocation))
        pence = 200 - tot
        for i in reversed(range(len(allocation))):   # Change to next arangement
            if allocation[i] != 0:                   # Less smallest non pence
                allocation[i] -= 1
                tot -= coins[i]
                for j in range(i+1,len(allocation)): # Add smaller coins
                    if 200 - tot - coins[j] >= 0:
                        more = (200 - tot)/coins[j]
                        allocation[j] += more
                        tot += more * coins[j]
                break
    return count

def p32():
    """
    The Identity, 39 * 186 = 7254, containing multiplicand, multiplier, and
    product is 1 through 9 pandigital. Find the sum of all products whose multiplic
    and/multiplier/product identity can be written as a 1 through 9 pandigital.
    """
    # 9   * 999  = 8991  (8  digits)
    # 1   * 1111 = 1111  (9  digits) *  hence 1 with 5
    # 11  * 111  = 1221  (9  digits) *  hence 2 with 5
    # 11  * 1111 = 12221 (10 digits)
    pans = set()
    for y in (1,2):
        for subs in itertools.permutations('123456789',5):
            l  = int(reduce(lambda x,y: x+y, (str(x) for x in subs[:y]))) # tuple -> int
            r  = int(reduce(lambda x,y: x+y, (str(x) for x in subs[y:])))
            lr = l*r
            if sorted(str(lr)) == sorted(set('123456789')-set(subs)):
                print("{} * {} = {}".format(l,r,lr))
                pans.add(lr)
    return reduce(lambda x,y: x+y, pans)

def p33():
    """
    We call a fraction curious if the digits have the property xy/xz = y/z
    or yx/zx = y/z (and x != 0 in the latter case as that would be trivial).
    There are 4 nontrivial curious fractions of two digits, less than 1 in value
    Find the value of the denominator of the product in lowest common terms
    """
    fracs = set()
    for den in range(2,10):
        for num in range(1,den):
            for x in range(10):
                for a,b,c,d in ((num, x ,den, x ),
                                ( x ,num,den, x ),
                                (num, x , x ,den),
                                ( x ,num, x ,den)):
                    if (b == d == 0) or (c == d == 0) or (a == c == 0):
                        continue
                    Num,Den = ("%d%d %d%d"%(a,b,c,d)).split(' ')
                    if float(num)/den == float(Num)/float(Den):
                        print('{}/{} = {}/{}'.format(num,den,Num,Den))
                        fracs.add((num,den))
    product_num = reduce(lambda x,y: x*y,(x[0] for x in fracs) )
    product_den = reduce(lambda x,y: x*y,(x[1] for x in fracs) )
    return product_den / gcd(product_den,product_num)

def p34():
    """
    Find the sum of all numbers which are equal to the sum of the factorial of
    their digits. Note: as 1! = 1 and 2! = 2 are not sums they are not included.
    """
    for i in itertools.count(1):
        if math.factorial(9) * i < int('9'*i):
            break
    upperbound = math.factorial(9) * i
    s = 0
    for num in range(3,upperbound):
        if num == sum(math.factorial(int(i)) for i in str(num)):
            s += num
    return s

def p35(n = 1000000):
    """
    The number, 197, is called a circular prime because all rotations of the
    digits: 197, 971, and 719, are themselves prime. There are thirteen such
    primes below 100: 2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.
    How many circular primes are there below one million?
    """
    primes = set(primeSieve(n))

    circularprimes = []
    while len(primes) > 0:
        for p in primes:
            break # get a prime without pop
        circs = set()
        circular = True
        for i in range(len(str(p))):                  # check rotations
            rotation = int(str(p)[i:] + str(p)[:i])
            circs.add(rotation)
            if rotation not in primes:
                circular = False
        if circular:
            circularprimes += list(circs)
        primes -= circs
    print(' '.join((str(x) for x in circularprimes)))
    return len(sorted(circularprimes))


def p36(n=1000000):
    """
    Find the sum of all numbers, less than one million,
    which are palindromic in base 10 and base 2.
    """
    pal = palindromes()
    p = next(pal)
    res = 0
    while p < n:
        if bin(p)[2:] == bin(p)[2:].lstrip('0')[::-1]: # if its binary palindromic
            res += p
        p = next(pal)
    return res

def isTruncatablePrime(n):
    '''
    checks if it is a truncatable prime
    '''
    for i in range(len(str(n))):
        d = divisors(int(str(n)[i:]))
        if d != {1}:
            return False
    return True


def Rtrunkgen():
    trunks = [3,7]
    index = 0
    while index < len(trunks):
        n = trunks[index]
        mag = len(str(n))
        trunks += [x for x in (n + nextdigit * 10 ** mag
                        for nextdigit in range(1,10)) if isPrime(x)]
        yield n
        index += 1

def p37():
    """
    The number 3797 has an interesting property. Being prime itself, it is
    possible to continuously remove digits from left to right, and remain prime
    at each stage: 3797, 797, 97, and 7. Similarly we can work from right to left:
    3797, 379, 37, and 3. Find the sum of the only eleven primes that are both
    truncatable from left to right and right to left.
    NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.
    """
    found = []
    rg = Rtrunkgen()
    assert rg.next() == 3
    assert rg.next() == 7
    while len(found) < 11:
        x = rg.next()
        Ltrunk = True
        for i in range(1,len(str(x))):
            if not isPrime(int(str(x)[:-i])):
                Ltrunk = False
        if Ltrunk:
            print x
            found.append(x)
    return sum(found)


def p38():
    """
    What is the largest 1 to 9 pandigital 9-digit number that can be formed as
    the concatenated product of an integer with (1,2, ... , n) where n > 1?
    """
    pandigitals = []
    for num in range(9999,0,-1):
        n = 2
        cat = str(num) + str(num * n)
        while len(cat) < 9:
            n += 1
            cat += str(num * n)
        if sorted(cat) == [str(x) for x in range(1,10)]:
            pandigitals.append(int(cat))
    return max(pandigitals)

def p39():
    """
    If p is the perimeter of a right angle triangle with integral length sides,
    {a,b,c}, there are exactly three solutions for p = 120.
    {20,48,52}, {24,45,51}, {30,40,50}
    For which value of p <= 1000, is the number of solutions maximised?
    """
    ppt = primativePythagoreanTriples()
    triples = []
    for i in range(100):
        triples.append(next(ppt))

    maxP, maxSol = 0,0
    for p in range(1,1001):
        sol = 0
        for t in triples:
            if p % sum(t) == 0:
                sol += 1
        if sol > maxSol:
            maxP, maxSol = p, sol

    return maxP

def champerownePlace(d):
    """
    returns that place

    123456789 10 11 12 13
    --1 mag-- -- -- -- --
                steps  then places
    """
    d-=1 # counting from 0 vs 1
    mag, interval = 0, 9
    while d >= interval:
        d -= interval
        mag += 1
        interval = (10**(mag+1) - 10**mag) * (mag+1) # places to next magnitude
    steps  = d / (mag+1)
    places = d % (mag+1)    # digit in integer
    s = 10**mag + steps     # integer in question
    res = int(str(s)[places])
    return res

def p40():
    """
    An irrational decimal fraction is created by concatenating the positive
    integers: 0.123456789101112131415161718192021...
    If dn represents the nth digit of the fractional part, find the value of the
    following expression: d1 * d10 * d100 * d1000 * d10000 * d100000 * d1000000
    """
    return reduce(lambda x,y: x*y,(champerownePlace(10**d) for d in range(7)))
