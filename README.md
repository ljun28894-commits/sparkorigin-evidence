# SparkOrigin — independent, reproducible evidence

This repository lets you check, for yourself and without trusting me, that
**SparkOrigin recovers real governing laws from data — laws that keep holding outside
the range they were fit on.** That last property is the whole point: a curve
that merely overfits can reproduce the data it was given, but it falls apart
the moment you step outside that range. A real law does not.

`verify.py` is a plain ~90-line **numpy** script. It does **not** use the SparkOrigin
engine. For each dataset it fits a power law on a *training* region only, then
predicts a *held-out extrapolation* region the fit never saw, and reports the
recovered exponent and the held-out error. It uses the same train/extrapolation
split the preprint reports, so these numbers reproduce the preprint's — to within the
small difference between a plain numpy fit and SparkOrigin's own pipeline. You don't
have to take SparkOrigin's word for it.

## Run it

```bash
python verify.py        # needs only numpy
```

## What you get (real output of `verify.py` on the included data)

| domain | train → held-out | exponent recovered | textbook | held-out median err | held-out p90 |
|---|---:|---:|---:|---:|---:|
| **Kepler (planets)** | 5 inner → 4 outer | **1.500** | 1.50 | **0.07%** | 0.09% |
| Metabolic (mammals) | 124 → 53 | 0.711 | ~0.75 | 31.5% | 157.6% |
| Zipf (Moby Dick) | top 400 → 1600 | −1.024 | −1.00 | 14.0% | 17.5% |
| City size (US) | top 120 → 880 | −0.726 | ~−0.73 | 1.3% | 8.3% |

**Kepler** is the cleanest case: trained on the five innermost planets alone,
the recovered exponent is 1.500 (the law is `P ∝ a^(3/2)`), and it reconstructs
the outer planets — Saturn through Pluto, a range it never saw — to **0.07%**
median error. **City size** recovers its exponent (−0.73) and extrapolates from the
120 largest cities down to the rest at **1.3%** median; **Zipf** recovers its exponent
(−1.02) and, extrapolating from the top 400 words across a far longer tail (ranks
401–2000), holds to **14%** median.

**Metabolic scaling is reported honestly, including where it is rough.** The
exponent comes out at 0.71 — squarely in the empirical 2/3–3/4 band — but real
biological scatter makes *point* extrapolation poor (31% median, 157% at the
90th percentile). The law is there; individual predictions across the gap are
not tight. We show this rather than hide it, because honest reporting of where a
method is weak is the point of the project, not an embarrassment to it.

## The laws SparkOrigin reported (for reference)

- Kepler: `log P = 1.49981 · log a`  (i.e. `P ∝ a^1.4998`)
- Metabolic: `log(rate) = 0.69271 · log(mass) + 1.1438`
- Zipf (Moby Dick): `freq ∝ rank^(−1.024)`
- City size (US): `population ∝ rank^(−0.726)`

These are the SparkOrigin engine's own outputs; the table above is the independent
numpy refit. They agree, with only small numpy-vs-engine differences (e.g. metabolic
0.711 vs 0.693, both inside the 2/3–3/4 band).

Per-domain log–log fit-and-extrapolation plots are in [`figures/`](figures/).

## Data (real and publicly citable)

- **Kepler** — NASA Planetary Fact Sheet / IAU (solar-system orbital elements).
- **Metabolic** — AnimalTraits (2022); Kleiber (1932); West–Brown–Enquist (1997).
- **Zipf / Moby Dick** — Project Gutenberg #2701 (Melville, public domain); Zipf (1949).
- **City size** — `plotly/datasets` us-cities-top-1k (derived from US Census); Gabaix (1999).

## Scope and honesty

- This is a **results-and-verification** repository. The SparkOrigin engine itself is
  not included here.
- The four cases above are a subset chosen because they are clean to re-check
  independently. The full study — more domains, the trust/extrapolation gate,
  the dynamical-systems and causal-direction results, and a domain where SparkOrigin
  *fails* (log-linear seismic scaling, reported plainly) — is in the preprint:
  **[preprint — DOI 10.5281/zenodo.20577739](https://doi.org/10.5281/zenodo.20577739)**.
- Nothing here is tuned to flatter the method: `verify.py` is a transparent
  independent fit, and the numbers are whatever it computes.

## Author

Jun Liu · `jun.liu@sparkorigin.net` · ORCID [0009-0009-9837-8565](https://orcid.org/0009-0009-9837-8565)

Code: MIT. Data: see sources above (all public).
