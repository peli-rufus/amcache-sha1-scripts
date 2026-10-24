#!/usr/bin/env python3
"""Split a SHA1 CSV (one 'sha1' column) into files of 1000 hashes each.

Usage:
    python3 split_sha1_csv.py <input.csv> [output_dir] [chunk_size]

Example:
    python3 split_sha1_csv.py amcache_sha1.csv chunks
Produces chunks/amcache_sha1_part001.csv, _part002.csv, ...
"""
import csv
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    outdir = Path(sys.argv[2]) if len(sys.argv) > 2 else src.parent
    size = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    outdir.mkdir(parents=True, exist_ok=True)

    with open(src, newline="", encoding="utf-8-sig") as fh:
        reader = csv.reader(fh)
        header = next(reader, ["sha1"])
        hashes = [r[0].strip() for r in reader if r and r[0].strip()]

    parts = 0
    for i in range(0, len(hashes), size):
        parts += 1
        out = outdir / f"{src.stem}_part{parts:03d}.csv"
        with open(out, "w", newline="") as fo:
            w = csv.writer(fo)
            w.writerow(header)
            w.writerows([h] for h in hashes[i:i + size])
        print(f"{out.name}: {len(hashes[i:i + size])} hashes")
    print(f"\n{len(hashes)} hashes split into {parts} file(s) in {outdir}")


if __name__ == "__main__":
    main()