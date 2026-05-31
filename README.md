# project-lunar
# Inspiration4 OSD-575 Data Integration

This repository combines Inspiration4 serum cytokine, multiplex, CMP, and demographic datasets into unified analysis-ready tables.

## Inputs

Place raw CSV files in:

data_raw/

Required files:

- LSDS 8 Multiplex SerumSpaceX_serum_non_bridged.csv
- LSDS 8 Multiplex Serum.csv
- Demographics Inspiration4.csv
- LSDS 8 Comprehensive Metabolic Panel CMP.csv
- ...

## Run

```bash
python scripts/combine_inspiration4_datasets.py
```

## Outputs

Generated files:

- outputs/Inspiration4_Master_Long.csv
- outputs/Inspiration4_Master_Wide.csv

## Output Dimensions

Long format:
8252 rows × 14 columns

Wide format:
28 rows × 304 columns
