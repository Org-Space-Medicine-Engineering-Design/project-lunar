import pandas as pd
from pathlib import Path

DATA_DIR = Path(
    r"C:\Users\cosmi\Inspiration4_Project\project-lunar-main\data\raw\Inspiration4"
)

OUT_DIR = Path(
    r"C:\Users\cosmi\Inspiration4_Project\outputs"
)
OUT_DIR.mkdir(exist_ok=True)

cmp = pd.read_csv(DATA_DIR / "LSDS-8_Comprehensive_Metabolic_Panel_CMP.upload_SUBMITTED.csv")
cardio = pd.read_csv(DATA_DIR / "LSDS-8_Multiplex_serum.cardiovascular.EvePanel_SUBMITTED.csv")
immune_eve = pd.read_csv(DATA_DIR / "LSDS-8_Multiplex_serum.immune.EvePanel_SUBMITTED.csv")
immune_alamar = pd.read_excel(DATA_DIR / "LSDS-8_Multiplex_serum.immune.AlamarPanel_SUBMITTED.xlsx")
demo = pd.read_excel(DATA_DIR / "Demographics_inspiration4.xlsx")

cmp_clean = cmp.rename(columns={
    "SUBJECT_ID": "Subject_ID",
    "timepoint": "Timepoint",
    "ANALYTE": "Variable",
    "VALUE": "Value",
    "UNITS": "Unit",
    "SEX": "Sex"
})

cmp_clean["Panel"] = "CMP"
cmp_clean = cmp_clean[[
    "Subject_ID", "Sex", "Timepoint", "Variable", "Value", "Unit", "Panel"
]]

def clean_multiplex(df, panel_name):
    df = df.rename(columns={
        "ID": "Subject_ID",
        "Analyte": "Variable",
        "Concentration": "Value"
    })

    df["Panel"] = panel_name

    return df[[
        "Subject_ID", "Timepoint", "Variable", "Value", "Unit", "Panel"
    ]]

cardio_clean = clean_multiplex(cardio, "Cardiovascular_Eve")
immune_eve_clean = clean_multiplex(immune_eve, "Immune_Eve")
immune_alamar_clean = clean_multiplex(immune_alamar, "Immune_Alamar")

master_long = pd.concat(
    [
        cmp_clean,
        cardio_clean,
        immune_eve_clean,
        immune_alamar_clean
    ],
    ignore_index=True
)

demo_clean = demo.rename(columns={
    "Subject ID": "Subject_ID"
})

master_long = master_long.merge(
    demo_clean,
    on="Subject_ID",
    how="left",
    suffixes=("", "_demo")
)

master_long.to_csv(
    OUT_DIR / "Inspiration4_Master_Long.csv",
    index=False
)

master_wide = master_long.pivot_table(
    index=["Subject_ID", "Timepoint"],
    columns=["Panel", "Variable"],
    values="Value",
    aggfunc="first"
)

master_wide.columns = [
    f"{panel}__{variable}" for panel, variable in master_wide.columns
]

master_wide = master_wide.reset_index()

master_wide.to_csv(
    OUT_DIR / "Inspiration4_Master_Wide.csv",
    index=False
)

print("Done!")
print("Long file rows/columns:", master_long.shape)
print("Wide file rows/columns:", master_wide.shape)
print()
print("Saved files:")
print(OUT_DIR / "Inspiration4_Master_Long.csv")
print(OUT_DIR / "Inspiration4_Master_Wide.csv")