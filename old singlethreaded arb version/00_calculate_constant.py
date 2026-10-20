from flint import arb, ctx
from math import log10

def kepler_bouwkamp(dps):
    ctx.dps = dps
    sum = arb(0)
    iter_count = int(ctx.dps * log10(9/4))
    
    for k in range(2, 2 * iter_count, 2):
        z = arb(k).zeta(3)
        p = arb(2) ** k
        sum += ((z / k) * (1 - p)) * ((z + 1) + (1 / p))
    
    result = (2 * sum).exp()
    
    return sum, result, iter_count 

#print(kepler_bouwkamp(3_000))

# for dps in range(1000):
#     print(kepler_bouwkamp(dps))

from time import perf_counter
print('dps,iter_count,time')
for dps in range(100, 999999999999, 100):
    start = perf_counter()
    sum, result, iter_count = kepler_bouwkamp(dps)
    stop = perf_counter()
    print(dps, iter_count, stop - start, sep=',')
