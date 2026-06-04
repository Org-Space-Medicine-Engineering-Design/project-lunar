#!/usr/bin/env python3
"""
Build nhanes_biopro_all_cycles_combined.csv from NHANES BIOPRO public-use files.

Purpose
-------
Combines BIOPRO laboratory files across NHANES cycles into a single row-stacked
chemistry dataset for LUNAR. SEQN is retained as the participant identifier.
The script adds source metadata columns so provenance is preserved.

Expected input layout
---------------------
Place NHANES XPT files in a directory such as data/raw/nhanes/biopro/.
The default file map expects the files listed in CYCLE_FILE_MAP below.

Output
------
processed_csv/nhanes_biopro_all_cycles_combined.csv

Important notes
---------------
- This script concatenates BIOPRO files by rows across cycles; it does not merge
  separate laboratory domains.
- SEQN is a subject identifier, not a measured laboratory variable.
- Some cycles contain different variable sets; pandas aligns columns by name and
  leaves absent variables missing.
- The file includes main-exam records, 2017-March 2020 pre-pandemic records, and
  the available 2001-2002 second-exam BIOPRO file when present.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


CYCLE_FILE_MAP = [
    # cycle, source filename, exam_type
    ("1999-2000", "LAB18.xpt", "main"),
    ("2001-2002", "L40_B.xpt", "main"),
    ("2001-2002", "L40_2_B.xpt", "second_exam"),
    ("2003-2004", "L40_C.xpt", "main"),
    ("2005-2006", "BIOPRO_D.xpt", "main"),
    ("2009-2010", "BIOPRO_F.xpt", "main"),
    ("2011-2012", "BIOPRO_G.xpt", "main"),
    ("2013-2014", "BIOPRO_H.xpt", "main"),
    ("2015-2016", "BIOPRO_I.xpt", "main"),
    ("2017-2018", "BIOPRO_J.xpt", "main"),
    ("2017-March 2020", "P_BIOPRO.xpt", "main_pre_pandemic"),
]


def read_xpt(path: Path) -> pd.DataFrame:
    """Read a SAS XPORT file with pandas and normalize column names."""
    df = pd.read_sas(path, format="xport")
    df.columns = [str(c).strip() for c in df.columns]
    return df


def build(raw_dir: Path, output_csv: Path, allow_missing: bool = True) -> None:
    frames: list[pd.DataFrame] = []
    missing_files: list[str] = []

    for cycle, filename, exam_type in CYCLE_FILE_MAP:
        path = raw_dir / filename
        if not path.exists():
            missing_files.append(filename)
            if allow_missing:
                continue
            raise FileNotFoundError(f"Missing expected NHANES BIOPRO file: {path}")

        df = read_xpt(path)
        if "SEQN" not in df.columns:
            raise ValueError(f"{filename} does not contain SEQN.")
        df["nhanes_cycle"] = cycle
        df["source_file"] = filename
        df["exam_type"] = exam_type
        frames.append(df)

    if not frames:
        raise RuntimeError(f"No BIOPRO files were found in {raw_dir}")

    combined = pd.concat(frames, ignore_index=True, sort=False)

    # Put provenance columns near the front after SEQN.
    front = [c for c in ["SEQN", "nhanes_cycle", "source_file", "exam_type"] if c in combined.columns]
    remaining = [c for c in combined.columns if c not in front]
    combined = combined[front + remaining]

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(output_csv, index=False)

    print(f"Wrote: {output_csv}")
    print(f"Rows: {len(combined):,}")
    print(f"Unique SEQN: {combined['SEQN'].nunique():,}")
    print(f"Columns: {len(combined.columns):,}")
    if missing_files:
        print("Skipped missing files:", ", ".join(missing_files))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build all-cycles NHANES BIOPRO combined CSV.")
    parser.add_argument("--raw-dir", default="data/raw/nhanes/biopro", type=Path)
    parser.add_argument("--output", default="processed_csv/nhanes_biopro_all_cycles_combined.csv", type=Path)
    parser.add_argument("--strict", action="store_true", help="Fail if any expected BIOPRO source file is missing.")
    args = parser.parse_args()
    build(args.raw_dir, args.output, allow_missing=not args.strict)
