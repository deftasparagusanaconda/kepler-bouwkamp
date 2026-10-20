# kepler-bouwkamp

calculate [Kepler-Bouwkamp constant](https://en.wikipedia.org/wiki/Kepler%E2%80%93Bouwkamp_constant) ([0.1149420448...](https://oeis.org/A085365
)) to **100,000** digits for [daamath](https://deftasparagusanaconda.github.io/daamath/), using [FLINT](https://flintlib.org/)'s [Hurwitz zeta](https://en.wikipedia.org/wiki/Hurwitz_zeta_function) function

![formula.png](https://github.com/deftasparagusanaconda/kepler-bouwkamp/blob/main/formula.png)

[kepler_bouwkamp_1k.txt](https://github.com/deftasparagusanaconda/kepler-bouwkamp/blob/main/kepler_bouwkamp_1k.txt)  
[kepler_bouwkamp_10k.txt](https://github.com/deftasparagusanaconda/kepler-bouwkamp/blob/main/kepler_bouwkamp_10k.txt)  
[kepler_bouwkamp_100k.txt](https://github.com/deftasparagusanaconda/kepler-bouwkamp/blob/main/kepler_bouwkamp_100k.txt)  

# code

simplified version of [kepler_boukamp.py](https://github.com/deftasparagusanaconda/kepler-bouwkamp/blob/main/kepler_bouwkamp.py):

```python
from math import log10, ceil
from flint import arb, ctx

def kepler_bouwkamp(dps):
	ctx.dps = dps
	iter_count = ceil(dps / log10(9 / 4))

	sum = arb(0)
	for k in range(2, 2 * iter_count, 2):
		p = arb(2) ** k
		z = arb(k).zeta(3)
		sum += ((z/k) * (p-1)) * ((z+1) + (1/p))
	return (sum * -2).exp()

print(kepler_bouwkamp(100_100).str(more=True))
```
