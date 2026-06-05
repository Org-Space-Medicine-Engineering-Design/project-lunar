from pathlib import Path
import numpy as np
import pandas as pd
import xlsxwriter

BASE = Path('/mnt/data')
NHANES_FILE = BASE / 'nhanes_biopro_cmp_focused_main_exam.csv'
I4_VAR_FILE = BASE / 'Inspiration4_Master_Long.csv'
OUT_XLSX = BASE / 'LUNAR_NHANES_Data_Quality_Summary_v1.xlsx'
OUT_CSV = BASE / 'LUNAR_NHANES_CMP_Overlap_Data_v1.csv'
SUBJECT_STATS_CSV = BASE / 'LUNAR_NHANES_Subject_Stats_v1.csv'
SUBJECT_MISSINGNESS_CSV = BASE / 'LUNAR_NHANES_Subject_Missingness_v1.csv'

VAR_META = {
    'LBXSAL':   ('Albumin','ALBUMIN','g/dL','CMP','Direct'),
    'LBXSAPSI': ('Alkaline Phosphatase','ALKALINE PHOSPHATASE','U/L','CMP','Direct'),
    'LBXSASSI': ('AST','AST','U/L','CMP','Direct'),
    'LBXSATSI': ('ALT','ALT','U/L','CMP','Direct'),
    'LBXSBU':   ('Urea Nitrogen (BUN)','UREA NITROGEN (BUN)','mg/dL','CMP','Direct'),
    'LBXSC3SI': ('Carbon Dioxide','CARBON DIOXIDE','mmol/L','CMP','Direct'),
    'LBXSCA':   ('Calcium','CALCIUM','mg/dL','CMP','Direct'),
    'LBXSCLSI': ('Chloride','CHLORIDE','mmol/L','CMP','Direct'),
    'LBXSCR':   ('Creatinine','CREATININE','mg/dL','CMP','Direct'),
    'LBXSGB':   ('Globulin','GLOBULIN','g/dL','CMP','Direct'),
    'LBXSGL':   ('Glucose','GLUCOSE','mg/dL','CMP','Direct'),
    'LBXSIR':   ('Iron','','ug/dL','Chemistry','NHANES only'),
    'LBXSKSI':  ('Potassium','POTASSIUM','mmol/L','CMP','Direct'),
    'LBXSNASI': ('Sodium','SODIUM','mmol/L','CMP','Direct'),
    'LBXSTB':   ('Total Bilirubin','BILIRUBIN; TOTAL','mg/dL','CMP','Direct'),
    'LBXSTP':   ('Total Protein','PROTEIN; TOTAL','g/dL','CMP','Direct'),
    'LBXSUA':   ('Uric Acid','','mg/dL','Chemistry','NHANES only'),
}
CORE_VARS = list(VAR_META.keys())
DERIVED = {
    'Albumin/Globulin Ratio': ('ALBUMIN/GLOBULIN RATIO','ratio','LBXSAL / LBXSGB'),
    'BUN/Creatinine Ratio': ('BUN/CREATININE RATIO','ratio','LBXSBU / LBXSCR')
}

def clean_value(x):
    if x is None: return None
    if isinstance(x, float) and np.isnan(x): return None
    if isinstance(x, (np.floating,)): return float(x)
    if isinstance(x, (np.integer,)): return int(x)
    return x

def write_df(wb, sheet_name, data, header_fmt, num_fmt, pct_fmt, int_fmt):
    ws = wb.add_worksheet(sheet_name[:31])
    ws.freeze_panes(1, 0)
    ws.hide_gridlines(2)
    headers = list(data.columns)
    for j, h in enumerate(headers):
        ws.write(0, j, h, header_fmt)
        # width from header and a small sample
        try:
            sample_len = int(data[h].head(100).astype(str).str.len().max()) if len(data) else 0
        except Exception:
            sample_len = 0
        width = min(max(len(str(h)) + 2, sample_len + 2, 12), 42)
        fmt = None
        if any(k in str(h) for k in ['Percent','CV']): fmt = pct_fmt
        elif pd.api.types.is_integer_dtype(data[h]): fmt = int_fmt
        elif pd.api.types.is_float_dtype(data[h]): fmt = num_fmt
        ws.set_column(j, j, width, fmt)
    if len(data) > 0:
        ws.autofilter(0, 0, len(data), len(headers)-1)
    for r, row in enumerate(data.itertuples(index=False, name=None), start=1):
        ws.write_row(r, 0, [clean_value(x) for x in row])
    return ws

# Load and prepare.
df = pd.read_csv(NHANES_FILE)
for col in ['SEQN'] + CORE_VARS:
    df[col] = pd.to_numeric(df[col], errors='coerce')
df['Albumin/Globulin Ratio'] = np.where(df['LBXSGB'].notna() & (df['LBXSGB'] != 0), df['LBXSAL'] / df['LBXSGB'], np.nan)
df['BUN/Creatinine Ratio'] = np.where(df['LBXSCR'].notna() & (df['LBXSCR'] != 0), df['LBXSBU'] / df['LBXSCR'], np.nan)
try:
    i4_vars = set(pd.read_csv(I4_VAR_FILE, encoding='latin1')['Unique Variables'].astype(str))
except Exception:
    i4_vars = set()

n_rows = len(df)
n_participants = df['SEQN'].nunique(dropna=True)
missing_total = int(df[CORE_VARS].isna().sum().sum())
missing_pct = missing_total / (n_rows * len(CORE_VARS)) * 100
all_measure_cols = CORE_VARS + list(DERIVED.keys())

notes = pd.DataFrame([
    ['Source NHANES file', NHANES_FILE.name],
    ['Source Inspiration4 variable inventory', I4_VAR_FILE.name],
    ['Workbook purpose', 'NHANES CMP-focused data quality summary modeled after the Inspiration4 data quality workbook.'],
    ['Important structural difference', 'NHANES is cross-sectional; timepoint-specific Inspiration4 sheets were omitted.'],
    ['Participant identifier', 'SEQN'],
    ['Primary data scope', 'Main-exam NHANES biochemistry/CMP-focused variables across available cycles.'],
    ['Derived variables included', 'Albumin/Globulin Ratio; BUN/Creatinine Ratio'],
    ['Derived variables not included', 'eGFR was not calculated because age/sex/race demographics are not present in the CMP-focused file.'],
    ['Full participant-level overlap data', OUT_CSV.name],
    ['Full subject-level stats', SUBJECT_STATS_CSV.name],
    ['Full subject-level missingness', SUBJECT_MISSINGNESS_CSV.name],
    ['Excel participant sheets', 'Previewed first 1000 rows in workbook; full participant-level tables are exported as CSVs to keep workbook responsive.'],
], columns=['Item','Value'])

dataset_inventory = pd.DataFrame([{
    'Dataset': NHANES_FILE.name, 'Rows': n_rows, 'Columns': df.shape[1], 'Participants': n_participants,
    'Cycles': df['nhanes_cycle'].nunique(dropna=True), 'Numeric_Measures': len(CORE_VARS), 'Derived_Measures': len(DERIVED),
    'Missing_Total_Raw_Measures': missing_total, 'Missing_Percent_Raw_Measures': missing_pct, 'Participant_Column': 'SEQN',
    'Cycle_Column': 'nhanes_cycle', 'Source_File_Column': 'source_file', 'Exam_Type_Column': 'exam_type'
}])

stats_rows = []
for col in all_measure_cols:
    s = pd.to_numeric(df[col], errors='coerce')
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    if col in VAR_META:
        var, i4, unit, group, match = VAR_META[col]
        nh = col
    else:
        var = col
        i4, unit, _ = DERIVED[col]
        nh = 'Derived'; group = 'Derived CMP'; match = 'Derived direct analog'
    stats_rows.append({
        'Variable': var, 'NHANES_Variable': nh, 'Inspiration4_Variable': i4, 'Group': group, 'Unit': unit, 'Match_Type': match,
        'N': int(s.notna().sum()), 'Missing_N': int(s.isna().sum()), 'Missing_Percent': float(s.isna().mean()*100),
        'Mean': s.mean(), 'Median': s.median(), 'SD': s.std(ddof=1), 'IQR': q3-q1, 'Min': s.min(), 'Max': s.max()
    })
variable_stats = pd.DataFrame(stats_rows)
missing_by_variable = variable_stats[['Variable','NHANES_Variable','Inspiration4_Variable','Missing_N','Missing_Percent','N']].rename(columns={'N':'Nonmissing_N'})
variable_coverage = variable_stats[['Variable','NHANES_Variable','Inspiration4_Variable','N','Missing_N','Missing_Percent','Unit','Group','Match_Type']].copy()
variable_coverage['Expected_Participant_Rows'] = n_rows
variable_coverage['Percent_Complete'] = 100 - variable_coverage['Missing_Percent']
variable_coverage = variable_coverage[['Variable','NHANES_Variable','Inspiration4_Variable','N','Expected_Participant_Rows','Percent_Complete','Missing_N','Missing_Percent','Unit','Group','Match_Type']]

sub = df[['SEQN','nhanes_cycle','source_file','exam_type'] + CORE_VARS].copy()
sub['Records'] = 1
sub['Numeric_Variables'] = len(CORE_VARS)
sub['Variables_Present'] = sub[CORE_VARS].notna().sum(axis=1)
sub['Variables_Missing'] = sub[CORE_VARS].isna().sum(axis=1)
sub['Percent_Missing'] = sub['Variables_Missing'] / len(CORE_VARS) * 100
sub['Percent_Complete'] = 100 - sub['Percent_Missing']
sub['Mean_Across_Raw_Measures_QC_Only'] = sub[CORE_VARS].mean(axis=1)
sub['Median_Across_Raw_Measures_QC_Only'] = sub[CORE_VARS].median(axis=1)
sub['SD_Across_Raw_Measures_QC_Only'] = sub[CORE_VARS].std(axis=1)
sub['Min_Across_Raw_Measures_QC_Only'] = sub[CORE_VARS].min(axis=1)
sub['Max_Across_Raw_Measures_QC_Only'] = sub[CORE_VARS].max(axis=1)
subject_stats = sub[['SEQN','nhanes_cycle','source_file','exam_type','Records','Numeric_Variables','Variables_Present','Variables_Missing','Percent_Complete','Mean_Across_Raw_Measures_QC_Only','Median_Across_Raw_Measures_QC_Only','SD_Across_Raw_Measures_QC_Only','Min_Across_Raw_Measures_QC_Only','Max_Across_Raw_Measures_QC_Only']]
subject_missingness = sub[['SEQN','nhanes_cycle','source_file','exam_type','Numeric_Variables','Variables_Present','Variables_Missing','Percent_Missing']]
missing_by_participant = subject_missingness.rename(columns={'SEQN':'Participant','Numeric_Variables':'Expected_Variables','Variables_Present':'Present','Variables_Missing':'Missing'})
participant_audit = subject_stats[['SEQN','nhanes_cycle','source_file','exam_type','Records','Numeric_Variables','Variables_Present','Variables_Missing','Percent_Complete']].rename(columns={'SEQN':'Subject'})

isv = variable_stats[['Variable','NHANES_Variable','Inspiration4_Variable','N','Mean','SD','Median','Min','Max','Unit']].copy()
isv['CV_Percent'] = np.where(isv['Mean'].abs() > 0, isv['SD'] / isv['Mean'].abs() * 100, np.nan)
isv = isv.rename(columns={'N':'N_Subjects','Mean':'Population_Mean','SD':'Population_SD','Median':'Population_Median','Min':'Population_Min','Max':'Population_Max'})
isv = isv[['Variable','NHANES_Variable','Inspiration4_Variable','N_Subjects','Population_Mean','Population_SD','CV_Percent','Population_Median','Population_Min','Population_Max','Unit']]

units_audit = pd.DataFrame([{'Dataset': NHANES_FILE.name, 'Variable': m[0], 'NHANES_Variable': c, 'Unit': m[2], 'Unit_Source': 'NHANES variable label / biochemistry convention'} for c, m in VAR_META.items()] + [{'Dataset': NHANES_FILE.name, 'Variable': n, 'NHANES_Variable': 'Derived', 'Unit': m[1], 'Unit_Source': 'Calculated from ' + m[2]} for n, m in DERIVED.items()])
naming_audit = pd.DataFrame([{'Original_Variable': c, 'Display_Name': VAR_META[c][0] if c in VAR_META else c, 'Lowercase': c.lower(), 'Contains_Space': ' ' in c, 'Contains_Dash': '-' in c, 'Contains_Slash': '/' in c, 'Contains_Parentheses': '(' in c or ')' in c, 'Starts_With_LB': c.startswith('LB')} for c in CORE_VARS + ['SEQN','nhanes_cycle','source_file','exam_type']])

cross = []
for c, m in VAR_META.items():
    var, i4, unit, group, match = m
    cross.append({'Inspiration4_Variable': i4, 'Inspiration4_Present': bool(i4 in i4_vars) if i4 else False, 'NHANES_Variable': c, 'NHANES_Display_Name': var, 'NHANES_Unit': unit, 'Match_Type': match, 'Use_In_Overlap_Data': 'Yes' if match == 'Direct' else 'Optional', 'Notes': 'Direct chemistry analog.' if match == 'Direct' else 'Present in NHANES CMP-focused file but not observed in uploaded Inspiration4 inventory.'})
for n, m in DERIVED.items():
    i4, unit, inputs = m
    cross.append({'Inspiration4_Variable': i4, 'Inspiration4_Present': bool(i4 in i4_vars), 'NHANES_Variable': 'Derived', 'NHANES_Display_Name': n, 'NHANES_Unit': unit, 'Match_Type': 'Derived direct analog', 'Use_In_Overlap_Data': 'Yes', 'Notes': 'Calculated as ' + inputs + '.'})
for i4 in ['eGFR AFRICAN AMERICAN','eGFR NON-AFR. AMERICAN']:
    if i4 in i4_vars:
        cross.append({'Inspiration4_Variable': i4, 'Inspiration4_Present': True, 'NHANES_Variable': '', 'NHANES_Display_Name': '', 'NHANES_Unit': 'mL/min/1.73m2', 'Match_Type': 'Not calculated in this workbook', 'Use_In_Overlap_Data': 'No', 'Notes': 'Requires creatinine plus demographic equation inputs; CMP-focused file does not include age/sex/race variables.'})
overlap_crosswalk = pd.DataFrame(cross)

derived_audit = pd.DataFrame([
    {'Derived_Variable':'Albumin/Globulin Ratio','Formula':'Albumin / Globulin','NHANES_Inputs':'LBXSAL; LBXSGB','Inspiration4_Variable':'ALBUMIN/GLOBULIN RATIO','Included':'Yes'},
    {'Derived_Variable':'BUN/Creatinine Ratio','Formula':'Urea Nitrogen (BUN) / Creatinine','NHANES_Inputs':'LBXSBU; LBXSCR','Inspiration4_Variable':'BUN/CREATININE RATIO','Included':'Yes'},
    {'Derived_Variable':'eGFR','Formula':'Not calculated','NHANES_Inputs':'Creatinine + demographics required','Inspiration4_Variable':'eGFR AFRICAN AMERICAN; eGFR NON-AFR. AMERICAN','Included':'No'},
])

overlap_data = df[['SEQN','nhanes_cycle','source_file','exam_type'] + CORE_VARS + list(DERIVED.keys())].rename(columns={c: VAR_META[c][0] for c in CORE_VARS})
overlap_data.to_csv(OUT_CSV, index=False)
subject_stats.to_csv(SUBJECT_STATS_CSV, index=False)
subject_missingness.to_csv(SUBJECT_MISSINGNESS_CSV, index=False)

sheets = [
    ('v1_Notes', notes), ('Dataset_Inventory', dataset_inventory), ('Variable_Stats', variable_stats),
    ('Missing_By_Variable', missing_by_variable), ('Variable_Coverage', variable_coverage),
    ('Units_Audit', units_audit), ('Naming_Audit', naming_audit),
    ('Subject_Stats_Preview', subject_stats.head(1000)), ('Subject_Missingness_Preview', subject_missingness.head(1000)),
    ('Participant_Audit_Preview', participant_audit.head(1000)),
    ('Inter_Subject_Variability', isv), ('Overlap_Crosswalk', overlap_crosswalk), ('Derived_Variables_Audit', derived_audit),
    ('Overlap_Data_Preview', overlap_data.head(1000))
]

if OUT_XLSX.exists(): OUT_XLSX.unlink()
wb = xlsxwriter.Workbook(str(OUT_XLSX), {'constant_memory': True, 'strings_to_urls': False, 'nan_inf_to_errors': True})
header_fmt = wb.add_format({'bold': True, 'font_color': 'white', 'bg_color': '#1F4E78', 'border': 1, 'text_wrap': True, 'align': 'center', 'valign': 'vcenter'})
num_fmt = wb.add_format({'num_format': '0.00'})
pct_fmt = wb.add_format({'num_format': '0.0'})
int_fmt = wb.add_format({'num_format': '#,##0'})
for sheet_name, data in sheets:
    write_df(wb, sheet_name, data, header_fmt, num_fmt, pct_fmt, int_fmt)
wb.close()
print(OUT_XLSX)
print(OUT_CSV)
print(SUBJECT_STATS_CSV)
print(SUBJECT_MISSINGNESS_CSV)
