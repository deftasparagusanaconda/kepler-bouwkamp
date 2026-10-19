from itertools import count
from mpmath import mp, zeta, mpf, exp, exp2

def kepler_bouwkamp():
    total = mpf(0)

    for two_k in count(2, 2):
        
        old_total = total
    
        # double riemann
        #z = zeta(two_k)
        #total += (exp2(two_k) - 1) / two_k * z * (z - 1 - 1 / exp2(two_k))

        # riemann & hurwitz
        #total += (exp2(two_k) - 1) / two_k * zeta(two_k) * zeta(two_k, 3)
        
        # double hurwitz
        z = zeta(two_k, 3)
        #total += ((exp2(two_k) - 1 / exp2(two_k)) * z + (exp2(two_k) - 1) * z**2) / two_k
        total += z / two_k * (exp2(two_k) - exp2(-two_k) + exp2(two_k) * z - z)
        
        if old_total == total:
            break

#        if two_k % 1 == 0:
#            print('\x1b[2J', two_k, total)

    return two_k, exp(-2 * total)

for precision in range(50, 10000, 100):    
    mp.dps = precision
    print(precision, kepler_bouwkamp())
