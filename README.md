# SparkOrigin — independent, reproducible evidence

This repository lets you check, for yourself and without trusting me, that
**SparkOrigin recovers real governing laws from data — laws that keep holding outside
the range they were fit on.** That last property is the whole point: a curve
that merely overfits can reproduce the data it was given, but it falls apart
the moment you step outside that range. A real law does not.

`verify.py` is a plain ~90-line **numpy** script. It does **not** use the SparkOrigin
engine. For each dataset it fits a power law on a *training* region only, then
predicts a *held-out extrapolation* region the fit never saw, and reports the
recovered exponent and the held-out error. This is an *independent* re-check, so
the numbers below differ slightly from the preprint (which uses SparkOrigin's own
pipeline) — that is intentional. You don't have to take SparkOrigin's word for it.

## Run it

```bash
python verify.py        # needs only numpy
```

## What you get (real output of `verify.py` on the included data)

| domain | train → held-out | exponent recovered | textbook | held-out median err | held-out p90 |
|---|---:|---:|---:|---:|---:|
| **Kepler (planets)** | 5 inner → 4 outer | **1.500** | 1.50 | **0.07%** | 0.09% |
| Metabolic (mammals) | 124 → 53 | 0.711 | ~0.75 | 31.5% | 157.6% |
| Zipf (Moby Dick) | 1400 → 600 | −1.075 | −1.00 | 2.77% | 6.17% |
| City size (US) | 700 → 300 | −0.724 | ~−0.73 | 6.98% | 10.6% |

**Kepler** is the cleanest case: trained on the five innermost planets alone,
the recovered exponent is 1.500 (the law is `P ∝ a^(3/2)`), and it reconstructs
the outer planets — Saturn through Pluto, a range it never saw — to **0.07%**
median error. **Zipf** and **city size** recover their exponents with
single-digit median extrapolation error.

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
  **[preprint DOI — paste Zenodo link here]**.
- Nothing here is tuned to flatter the method: `verify.py` is a transparent
  independent fit, and the numbers are whatever it computes.

## Author

Jun Liu · `jun.liu@sparkorigin.net` · ORCID [0009-0009-9837-8565](https://orcid.org/0009-0009-9837-8565)

Code: MIT. Data: see sources above (all public).
