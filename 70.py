from helpers import *
import itertools

def p61():
    """
    Find the sum of the only ordered set of six cyclic four digit numbers
    for which each polynomial type 3,4,5,6,7,8 is represented by a different
    number in each set.
    """
    kgons = {}
    for k in [3,4,5,6,7,8]:
        for n in itertools.count(1):
            # pkn, nth k-gon, is added to k-gons if pkn has 4 digits
            pkn = ( (n**2)*(k-2) - n*(k-4) )/(2)
            if pkn >= 10000:
                break
            elif pkn >= 1000:
                kgons[k] = kgons.get(k,[]) + [pkn]
    nextdict = kgons.copy()
    nextdict.pop(3)
    for p3n in kgons[3]:
        start,end = str(p3n)[:2], str(p3n)[2:]
        res = p61_helper(start,end,nextdict)
        if res != None:
            return sum([p3n]+res)
    assert False

def p61_helper(start,end,kgons):
    """
    recursively find the solution to p61
    stopping conditions: 1) no more cycles => return None
                         2) no more kgons  => return solution (list)
    """
    if len(kgons) == 0:
        if start == end:    return []
        else:               return None
    no_cycles = True
    for k in kgons:
        nextdict = kgons.copy()
        nextdict.pop(k)
        for num in kgons[k]:
            if str(num)[:2] == end:
                no_cycles = False
                res = p61_helper(start, str(num)[2:], nextdict)
                if res != None:
                    return [ num ] + res
    return None

def p62(k = 5):
    """
    Find the smallest cube for which exactly 5 permutations are cubes
    """
    digits = {}
    for i in itertools.count():
        x = ''.join(sorted(str(i**3)))
        digits[x] = digits.get(x,[]) + [i**3]
        if len(digits[x]) == k:
            return digits[x]

def p63():
    """
    how many n digit positive numbers exist that are also an nth power
    """
    count = 0
    for n in range(1000):
        for i in itertools.count(1):
            digits = len(str(i**n))
            if digits == n:
                count += 1
                print "%d: %d"%(n,i**n)
            elif digits > n:
                break
    return count
