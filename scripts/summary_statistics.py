import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = Path(
    r"C:\Users\cosmi\Inspiration4_Project\project-lunar-main\data\raw\Inspiration4"
)

OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

LONG_FILE = OUTPUT_DIR / "Inspiration4_Master_Long.csv"
WIDE_FILE = OUTPUT_DIR / "Inspiration4_Master_Wide.csv"
OUT_XLSX = OUTPUT_DIR / "Inspiration4_Data_Quality_Summary.xlsx"


def read_data_file(file_path):
    suffix = file_path.suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(file_path)

    elif suffix in [".xlsx", ".xls"]:
        return pd.read_excel(file_path)

    else:
        raise ValueError(f"Unsupported file type: {file_path}")


def clean_colnames(df):
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.replace(r"\s+", "_", regex=True)
    )
    return df


def find_col(df, possible):
    cols_lower = {c.lower(): c for c in df.columns}

    for p in possible:
        if p.lower() in cols_lower:
            return cols_lower[p.lower()]

    for c in df.columns:
        for p in possible:
            if p.lower() in c.lower():
                return c

    return None


def summarize_dataset(file_path):
    df = clean_colnames(read_data_file(file_path))

    participant_col = find_col(df, [
        "participant", "subject", "subject_id",
        "participant_id", "crew", "crew_id",
        "sample_id"
    ])

    timepoint_col = find_col(df, [
        "timepoint", "collection_timepoint",
        "mission_day", "sampling_timepoint",
        "event", "visit"
    ])

    age_col = find_col(df, ["age"])
    sex_col = find_col(df, ["sex", "gender"])
    bmi_col = find_col(df, ["bmi"])

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    inventory = {
        "Dataset": file_path.name,
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Participants": df[participant_col].nunique() if participant_col else np.nan,
        "Timepoints": df[timepoint_col].nunique() if timepoint_col else np.nan,
        "Numeric_Measures": len(numeric_cols),
        "Missing_Total": df.isna().sum().sum(),
        "Missing_Percent": round(df.isna().mean().mean() * 100, 2),
        "Participant_Column": participant_col,
        "Timepoint_Column": timepoint_col,
        "Age_Column": age_col,
        "Sex_Column": sex_col,
        "BMI_Column": bmi_col,
    }

    variable_stats = []

    for col in numeric_cols:
        s = df[col].dropna()

        variable_stats.append({
            "Dataset": file_path.name,
            "Variable": col,
            "N": s.shape[0],
            "Missing_N": df[col].isna().sum(),
            "Missing_Percent": round(df[col].isna().mean() * 100, 2),
            "Mean": s.mean() if len(s) else np.nan,
            "Median": s.median() if len(s) else np.nan,
            "SD": s.std() if len(s) > 1 else np.nan,
            "IQR": s.quantile(0.75) - s.quantile(0.25) if len(s) else np.nan,
            "Min": s.min() if len(s) else np.nan,
            "Max": s.max() if len(s) else np.nan,
        })

    missing_by_variable = pd.DataFrame({
        "Dataset": file_path.name,
        "Variable": df.columns,
        "Missing_N": df.isna().sum().values,
        "Missing_Percent": (df.isna().mean().values * 100).round(2),
        "Nonmissing_N": df.notna().sum().values,
    })

    participant_missing = pd.DataFrame()
    if participant_col:
        participant_missing = (
            df.groupby(participant_col)
            .apply(lambda x: pd.Series({
                "Dataset": file_path.name,
                "Participant": x.name,
                "Rows": x.shape[0],
                "Missing_N": x.isna().sum().sum(),
                "Missing_Percent": round(x.isna().mean().mean() * 100, 2)
            }))
            .reset_index(drop=True)
        )

    timepoint_missing = pd.DataFrame()
    if timepoint_col:
        timepoint_missing = (
            df.groupby(timepoint_col)
            .apply(lambda x: pd.Series({
                "Dataset": file_path.name,
                "Timepoint": x.name,
                "Rows": x.shape[0],
                "Missing_N": x.isna().sum().sum(),
                "Missing_Percent": round(x.isna().mean().mean() * 100, 2)
            }))
            .reset_index(drop=True)
        )

    participant_timepoint_missing = pd.DataFrame()
    if participant_col and timepoint_col:
        participant_timepoint_missing = (
            df.groupby([participant_col, timepoint_col])
            .apply(lambda x: pd.Series({
                "Dataset": file_path.name,
                "Participant": x.name[0],
                "Timepoint": x.name[1],
                "Rows": x.shape[0],
                "Missing_N": x.isna().sum().sum(),
                "Missing_Percent": round(x.isna().mean().mean() * 100, 2)
            }))
            .reset_index(drop=True)
        )

    demographics = []
    demo_cols = [c for c in [participant_col, age_col, sex_col, bmi_col] if c]

    if demo_cols:
        demo_df = df[demo_cols].drop_duplicates()

        for col in demo_df.columns:
            if pd.api.types.is_numeric_dtype(demo_df[col]):
                demographics.append({
                    "Dataset": file_path.name,
                    "Variable": col,
                    "N": demo_df[col].notna().sum(),
                    "Mean": demo_df[col].mean(),
                    "Median": demo_df[col].median(),
                    "SD": demo_df[col].std(),
                    "IQR": demo_df[col].quantile(0.75) - demo_df[col].quantile(0.25),
                    "Min": demo_df[col].min(),
                    "Max": demo_df[col].max(),
                    "Unique_Values": ""
                })
            else:
                demographics.append({
                    "Dataset": file_path.name,
                    "Variable": col,
                    "N": demo_df[col].notna().sum(),
                    "Mean": "",
                    "Median": "",
                    "SD": "",
                    "IQR": "",
                    "Min": "",
                    "Max": "",
                    "Unique_Values": "; ".join(map(str, demo_df[col].dropna().unique()))
                })

    unit_cols = [c for c in df.columns if "unit" in c.lower()]
    units = []

    for col in unit_cols:
        units.append({
            "Dataset": file_path.name,
            "Unit_Column": col,
            "Unique_Units": "; ".join(map(str, df[col].dropna().unique()))
        })

    naming = pd.DataFrame({
        "Dataset": file_path.name,
        "Original_Variable": df.columns,
        "Lowercase": [c.lower() for c in df.columns],
        "Contains_Space": [" " in c for c in df.columns],
        "Contains_Dash": ["-" in c for c in df.columns],
        "Contains_Slash": ["/" in c for c in df.columns],
        "Contains_Parentheses": [("(" in c) or (")" in c) for c in df.columns],
    })

    return {
        "inventory": inventory,
        "variable_stats": pd.DataFrame(variable_stats),
        "missing_by_variable": missing_by_variable,
        "missing_by_participant": participant_missing,
        "missing_by_timepoint": timepoint_missing,
        "missing_by_participant_timepoint": participant_timepoint_missing,
        "demographics": pd.DataFrame(demographics),
        "units": pd.DataFrame(units),
        "naming": naming,
    }


files = []

if RAW_DIR.exists():
    files.extend(sorted(RAW_DIR.glob("*.csv")))
    files.extend(sorted(RAW_DIR.glob("*.xlsx")))
    files.extend(sorted(RAW_DIR.glob("*.xls")))

if LONG_FILE.exists():
    files.append(LONG_FILE)

if WIDE_FILE.exists():
    files.append(WIDE_FILE)

print("\nFiles to summarize:")
for f in files:
    print(f" - {f.name}")

all_inventory = []
all_variable_stats = []
all_missing_var = []
all_missing_participant = []
all_missing_timepoint = []
all_missing_pt_tp = []
all_demographics = []
all_units = []
all_naming = []

for f in files:
    print(f"\nSummarizing: {f.name}")
    result = summarize_dataset(f)

    all_inventory.append(result["inventory"])
    all_variable_stats.append(result["variable_stats"])
    all_missing_var.append(result["missing_by_variable"])
    all_missing_participant.append(result["missing_by_participant"])
    all_missing_timepoint.append(result["missing_by_timepoint"])
    all_missing_pt_tp.append(result["missing_by_participant_timepoint"])
    all_demographics.append(result["demographics"])
    all_units.append(result["units"])
    all_naming.append(result["naming"])

inventory_df = pd.DataFrame(all_inventory)
variable_stats_df = pd.concat(all_variable_stats, ignore_index=True)
missing_var_df = pd.concat(all_missing_var, ignore_index=True)
missing_participant_df = pd.concat(all_missing_participant, ignore_index=True)
missing_timepoint_df = pd.concat(all_missing_timepoint, ignore_index=True)
missing_pt_tp_df = pd.concat(all_missing_pt_tp, ignore_index=True)
demographics_df = pd.concat(all_demographics, ignore_index=True)
units_df = pd.concat(all_units, ignore_index=True)
naming_df = pd.concat(all_naming, ignore_index=True)

with pd.ExcelWriter(OUT_XLSX, engine="openpyxl") as writer:
    inventory_df.to_excel(writer, sheet_name="Dataset_Inventory", index=False)
    demographics_df.to_excel(writer, sheet_name="Demographics", index=False)
    variable_stats_df.to_excel(writer, sheet_name="Variable_Stats", index=False)
    missing_var_df.to_excel(writer, sheet_name="Missing_By_Variable", index=False)
    missing_participant_df.to_excel(writer, sheet_name="Missing_By_Participant", index=False)
    missing_timepoint_df.to_excel(writer, sheet_name="Missing_By_Timepoint", index=False)
    missing_pt_tp_df.to_excel(writer, sheet_name="Missing_By_Part_Time", index=False)
    units_df.to_excel(writer, sheet_name="Units_Audit", index=False)
    naming_df.to_excel(writer, sheet_name="Naming_Audit", index=False)

print(f"\nSaved summary workbook to:")
print(OUT_XLSX)