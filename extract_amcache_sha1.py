#!/usr/bin/env python3
"""Extract unique SHA1 hashes from every CSV in an Amcache folder and save them to one CSV.

Usage:
    python3 extract_amcache_sha1.py <amcache_folder> [output.csv]

Example:
    python3 extract_amcache_sha1.py BCHUKIR-NB/00_Execution/Amcache amcache_sha1.csv
"""
import csv
import re
import sys
from pathlib import Path

SHA1_RE = re.compile(r"^[0-9a-fA-F]{40}$")


def find_sha1_columns(header):
    """Return indexes of columns that hold SHA1 values (name contains 'sha1')."""
    return [i for i, h in enumerate(header) if "sha1" in h.strip().lower()]


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    folder = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("amcache_sha1.csv")

    hashes = set()
    for f in sorted(folder.rglob("*.csv")):
        with open(f, newline="", encoding="utf-8-sig", errors="ignore") as fh:
            reader = csv.reader(line.replace("\x00", "") for line in fh)
            header = next(reader, None)
            if not header:
                continue
            cols = find_sha1_columns(header)
            if not cols:
                continue
            before = len(hashes)
            for row in reader:
                for i in cols:
                    if i < len(row):
                        v = row[i].strip()
                        # Amcache sometimes prefixes SHA1 with 4 zeros (44 chars)
                        if len(v) == 44 and v.startswith("0000"):
                            v = v[4:]
                        if SHA1_RE.match(v):
                            hashes.add(v.lower())
            print(f"{f.name}: +{len(hashes) - before} new")

    with open(out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["sha1"])
        for h in sorted(hashes):
            w.writerow([h])
    print(f"\n{len(hashes)} unique SHA1 hashes written to {out}")


if __name__ == "__main__":
    main()