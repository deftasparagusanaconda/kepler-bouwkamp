import pickle, pathlib
from concurrent.futures import ThreadPoolExecutor
from flint import arb, ctx
from math import ceil, log10

ctx.dps = 100100
ctx.threads = 1

thread_count = 16

input_dir = pathlib.Path(f'zeta_k_3 pkls at {ctx.dps} dps')
output_pkl = f'kepler_bouwkamp_{ctx.dps}.pkl'

term_count = ceil(ctx.dps / log10(9 / 4))

def partial_sum(start_k, stop_k):
    acc = arb(0)

    for k in range(start_k, stop_k, 2):
        filepath = input_dir / f'zeta_{k}_3.pkl'

        try:
            with filepath.open('rb') as file:
                z = pickle.load(file)
        except:
            print(f'WARNING: skipping zeta_{k}_3.pkl. your digits *will* be incorrect')
            continue

        p = arb(2) ** k

        acc += ((z / k) * (p - 1)) * ((z + 1) + (1 / p))

        if k % 1000 == 0:
            print(f'{(k - start_k) / (stop_k - start_k):%}')

    return acc


def kepler_bouwkamp():
    chunk_size = ceil((term_count - 1) / thread_count)

    chunks = [
        (
            2 + 2 * i * chunk_size,
            min(2 + 2 * (i + 1) * chunk_size, 2 * term_count),
        )
        for i in range(thread_count)
        if i * chunk_size < term_count - 1
    ]

    with ThreadPoolExecutor(max_workers=thread_count) as pool:
        acc = sum(pool.map(lambda bounds: partial_sum(*bounds), chunks))

    result = (-2 * acc).exp()

    with open(output_pkl, 'wb') as file:
        pickle.dump(result, file)

    # cause most people dont know how to unpickle or interpret an arb
    with open('kepler_bouwkamp_100k.txt', 'w') as file:
        file.write(result.str(radius=False)[:100_000 + 2])


if __name__ == '__main__':
    kepler_bouwkamp()
