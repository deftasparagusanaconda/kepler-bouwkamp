# FIX: if a thread finishes its strip, the other threads dont help out
# ... is that a big deal though?

from concurrent.futures import ThreadPoolExecutor
import pathlib

dps = 100100
output_dir = pathlib.Path(f'zeta_k_3 pkls at {dps} dps')

thread_count = 1
ctx_threads = 16

# starting from 20000 takes about 8GiB of memory, decreasing as k increases.
# starting from 10000 is not okay for 16 processes. ballooned to 500MB per process, roughly
start_k = 700
stop_k = 90000
#stop_k  = 568456 # ceil(log10(9 / 4)) * 2

def kepler_bouwkamp_partial(thread_index, thread_count, dps):
    from flint import arb, ctx
    import pickle
    
    ctx.dps = dps
    ctx.threads = ctx_threads

    step_size = 2 * thread_count

    for k in range(start_k + 2 * thread_index, stop_k, step_size):
        filepath = output_dir / f'zeta_{k}_3.pkl'
        
        if filepath.is_file():
            if filepath.stat().st_size > 0:
                print('skipping', filepath.name)
                continue
            else:
                #raise Exception(filepath.name, 'should NOT be empty. pkl saving is unreliable')
                print('overwriting', filepath.name)

        print('calculating', filepath.name, 'on thread', thread_index)

        temppath = filepath.with_suffix('.tmp')
        with temppath.open('wb') as file:
            pickle.dump(arb(k).zeta(3), file)
        temppath.replace(filepath)

def kepler_bouwkamp(dps, thread_count=thread_count):
    from functools import partial
    from more_itertools import consume
    
    with ThreadPoolExecutor(max_workers=thread_count) as pool:
        worker = partial(
            kepler_bouwkamp_partial,
            thread_count=thread_count,
            dps=dps,
        )
        consume(pool.map(worker, range(thread_count)))

if __name__ == '__main__':
    pathlib.Path(output_dir).mkdir(exist_ok=True)
    print('stop by spamming ctrl + c lmao')
    kepler_bouwkamp(dps)
