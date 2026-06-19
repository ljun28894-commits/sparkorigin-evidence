"""
Independent verification of SparkOrigin's published cross-domain laws.

This script does NOT use the SparkOrigin engine. It is a plain, ~90-line numpy
re-check: for each dataset it fits a power law (log-log least squares) on a
TRAINING region only, then predicts a held-out EXTRAPOLATION region the fit
never saw, and reports the recovered exponent and the held-out error.

The point: you do not have to trust SparkOrigin. Run this and confirm for yourself
that the laws are real and that they hold *outside* the range they were fit on,
which is the property an overfit curve cannot have.

Data: real and publicly citable (see README.md). Dependencies: numpy only.
Run:  python verify.py
"""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"

# label, csv, x-column, y-column, textbook exponent, train fraction (low-x = top-ranked region), law
# Train fractions reproduce the preprint's training windows so this independent check
# matches the paper: Kepler 5 inner planets, Zipf top-400 words, cities top-120 cities.
CASES = [
    ("Kepler (planets)",    "kepler.csv",    "a",         "P",              1.50, 5 / 9, "P proportional to a^(3/2)"),
    ("Metabolic (mammals)", "metabolic.csv", "body_mass", "metabolic_rate", 0.75, 0.70,  "rate proportional to mass^(~0.7)"),
    ("Zipf (Moby Dick)",    "mobydick.csv",  "rank",      "freq",          -1.00, 0.20,  "freq proportional to rank^(-1)"),
    ("City size (US)",      "cities.csv",    "rank",      "population",    -0.75, 0.12,  "pop proportional to rank^(-alpha)"),
]


def load(path, xcol, ycol):
    xs, ys = [], []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                x, y = float(row[xcol]), float(row[ycol])
            except (ValueError, KeyError, TypeError):
                continue
            if x > 0 and y > 0:
                xs.append(x)
                ys.append(y)
    return np.array(xs), np.array(ys)


def fit_powerlaw(x, y):
    """log10(y) = b*log10(x) + c   <=>   y = 10^c * x^b. Returns (b, c)."""
    b, c = np.polyfit(np.log10(x), np.log10(y), 1)
    return float(b), float(c)


def run():
    print("=" * 80)
    print(" Independent verification: plain numpy log-log fit, no SparkOrigin engine")
    print(" Fit on the TRAINING region only, then predict a HELD-OUT region it never saw")
    print("=" * 80)
    print(f"{'domain':22s}{'n_tr':>5}{'n_te':>5}{'exp(fit)':>10}{'textbook':>9}"
          f"{'train R2':>10}{'OOS med%':>10}{'OOS p90%':>10}")
    print("-" * 80)
    for label, fname, xcol, ycol, known, trfrac, _law in CASES:
        path = DATA / fname
        if not path.exists():
            print(f"{label:22s}  (missing {fname}, copy it into ./data/)")
            continue
        x, y = load(path, xcol, ycol)
        order = np.argsort(x)
        x, y = x[order], y[order]
        n = len(x)
        ntr = max(2, round(trfrac * n))
        xtr, ytr, xte, yte = x[:ntr], y[:ntr], x[ntr:], y[ntr:]
        b, c = fit_powerlaw(xtr, ytr)
        pred_tr = b * np.log10(xtr) + c
        ss_res = float(np.sum((np.log10(ytr) - pred_tr) ** 2))
        ss_tot = float(np.sum((np.log10(ytr) - np.mean(np.log10(ytr))) ** 2))
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
        if len(xte):
            yhat = 10 ** (b * np.log10(xte) + c)
            rel = np.abs(yhat - yte) / np.abs(yte) * 100.0
            med, p90 = float(np.median(rel)), float(np.percentile(rel, 90))
        else:
            med = p90 = float("nan")
        print(f"{label:22s}{ntr:>5}{len(xte):>5}{b:>10.3f}{known:>9.2f}"
              f"{r2:>10.4f}{med:>10.2f}{p90:>10.2f}")
    print("-" * 80)
    print(" exp(fit): exponent recovered from the TRAINING region alone.")
    print(" OOS med%/p90%: median and 90th-percentile relative error on the")
    print(" held-out region the fit never saw. These are honest re-computations,")
    print(" not numbers reported by SparkOrigin. A curve that merely overfits cannot")
    print(" keep a low OOS error here. A real law can.")
    print("=" * 80)


if __name__ == "__main__":
    run()
