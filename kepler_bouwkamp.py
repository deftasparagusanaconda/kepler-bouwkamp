from concurrent.futures import ProcessPoolExecutor
from math import log10, ceil
from decimal import Decimal

# flint's threading doesnt help much so we let threads calculate strides of the terms
thread_count = 16

def kepler_bouwkamp_partial(thread_index, thread_count, dps):
    from flint import arb, ctx

    ctx.dps = dps
    sum = arb(0)
    iter_count = ceil(dps / log10(9 / 4)) + 1

    for k in range(2 * (1 + thread_index), 2 * iter_count, 2 * thread_count):
        p = arb(2) ** k

        # z = arb(k).zeta(0.5)
        # sum += ((z / k) / (p - 1)) * ((z - p) + (1 / p))
        
        #z = arb(k).zeta()
        #sum += (((p - 1) / k) * z) * ((z - 1) - (1 / p))
        #sum += ((z / k) * (p - 1)) * ((z - 1) - (1 / p))
    
        # z = arb(k).zeta(2)
        # sum += (((z / k) * (p - 1)) * ((z + 1) + (1 / p))) * (z + 1)
        
        z = arb(k).zeta(3)
        sum += ((z / k) * (p - 1)) * ((z + 1) + (1 / p))

        #sum += ((z / arb(k).zeta()) * (p - 1)) * arb(k).zeta(3)
        
    return str(sum)

def kepler_bouwkamp(dps, thread_count=thread_count):
    from flint import arb, ctx
    from functools import partial
    
    with ProcessPoolExecutor(max_workers=thread_count) as pool:
        worker = partial(
            kepler_bouwkamp_partial,
            thread_count=thread_count,
            dps=ctx.dps,
        )
        partials = list(pool.map(worker, range(thread_count)))
    
    ctx.dps = dps
    partials = map(arb, partials)
    result = sum(partials)
    return (-2 * result).exp()

def count_match(A: str, B: str):
    A = Decimal(A).as_tuple().digits
    B = Decimal(B).as_tuple().digits

    n = 0
    for a, b in zip(A, B):
        if a != b:
            break
        n += 1
    
    return n

# benchmark various dps
if __name__ == "__main__":
    from flint import ctx
    from time import perf_counter

    reference_str = open('kepler_bouwkamp_100k.txt').read()
    
    print('dps,time,mismatches,result')
    # for dps in [100_100]:
    for dps in [40, 50, 63, 80, 
        100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 
        1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 
        10000, 12500, 16000, 20000, 25000, 31500, 40000, 50000, 63000, 80000, 100000]:
        
        ctx.dps = dps
        
        start = perf_counter()
        result = kepler_bouwkamp(ctx.dps)
        stop = perf_counter()
        
        mismatches = ctx.dps - count_match(result.str(radius=False, more=True), reference_str)
        print(ctx.dps, stop - start, mismatches, result.str(more=True), sep=',')
