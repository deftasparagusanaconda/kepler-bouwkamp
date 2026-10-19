from itertools import count
from flint import arb, ctx

def kepler_bouwkamp(precision):
    'calculate kepler_bouwkamp constant using python-flint/arb in a given decimal precision'
    ctx.dps = precision
    
    sum = arb(0)
    target = arb(10) ** (-precision)

    for two_k in count(2, 2):
        z = arb(two_k).zeta(3)
        p = arb(2) ** two_k

        term = z / two_k * (p - 1 / p + p * z - z)
        sum += term

        # For n >= two_k + 2, the terms are bounded by
        # 2 * (4/9)**n / n, with n = two_k/2.
        n = two_k // 2 + 1
        ratio = arb(4) / 9
        tail_bound = 2 * ratio**n / n / (1 - ratio)
        
        if tail_bound < target:
            break
        # if two_k % 10 == 0:
        #     print(two_k, sum)

    iterations = two_k // 2
    result = (-2 * sum).exp()

    return iterations, result

print(kepler_bouwkamp(2000))
for precision in range(1000):
    iterations, value = kepler_bouwkamp(precision)
    print(precision, iterations, value)

# from time import perf_counter
# print('precision, iterations, seconds')
# for precision in range(100, 1000000001, 100):
#     start = perf_counter()
#     iterations, result = kepler_bouwkamp(precision)
#     elapsed = perf_counter() - start
#
#     print(f"{precision:>6},{iterations:>7},{elapsed:>8.2f}")

