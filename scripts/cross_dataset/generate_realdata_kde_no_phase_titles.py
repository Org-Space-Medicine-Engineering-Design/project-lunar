
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator
from scipy.stats import gaussian_kde

# -----------------------------
# Inputs
# -----------------------------
SUMMARY_WORKBOOK = Path("mahalanobis_distance_summary.xlsx")
SHEET_NAME = "Long_Results_First_50000"

# -----------------------------
# Load real bootstrap results
# -----------------------------
df = pd.read_excel(SUMMARY_WORKBOOK, sheet_name=SHEET_NAME)

phase_order = ["Preflight", "Postflight", "Pre-BR", "In-BR", "Post-BR"]

phase_labels = {
    "Preflight": "Inspiration4 Preflight",
    "Postflight": "Inspiration4 Postflight",
    "Pre-BR": "Bed Rest Pre-BR",
    "In-BR": "Bed Rest In-BR",
    "Post-BR": "Bed Rest Post-BR",
}

phase_colors = {
    "Preflight": "#4C78A8",
    "Postflight": "#F58518",
    "Pre-BR": "#54A24B",
    "In-BR": "#E45756",
    "Post-BR": "#B279A2",
}

# Subject colors
i4_subjects = sorted(df.loc[df["Dataset"] == "Inspiration4", "Subject_ID"].unique())
br_subjects = sorted(df.loc[df["Dataset"] == "Bed Rest", "Subject_ID"].unique())

i4_colors = {
    i4_subjects[0]: "#D62728",
    i4_subjects[1]: "#1F77B4",
    i4_subjects[2]: "#2CA02C",
    i4_subjects[3]: "#9467BD",
}

br_colors = {
    br_subjects[0]: "#FF7F0E",
    br_subjects[1]: "#17BECF",
    br_subjects[2]: "#E377C2",
}

subject_colors = {**i4_colors, **br_colors}

# -----------------------------
# Figure setup
# -----------------------------
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.titlesize": 19,
    "axes.labelsize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 9,
})

fig, ax = plt.subplots(figsize=(14, 8))

x = np.linspace(0, 24, 1600)
ymax = 0

# -----------------------------
# Real KDE curves
# -----------------------------
for phase in phase_order:
    vals = df.loc[df["Phase"] == phase, "Mahalanobis_Distance"].dropna().to_numpy(float)
    kde = gaussian_kde(vals)  # real bootstrap data; default Scott bandwidth
    y = kde(x)
    ymax = max(ymax, y.max())

    ax.plot(x, y, color=phase_colors[phase], lw=2.4, zorder=3)
    ax.fill_between(x, y, color=phase_colors[phase], alpha=0.22, zorder=2)

# -----------------------------
# Subject median lines
# -----------------------------
subject_medians = (
    df.groupby(["Dataset", "Subject_ID", "Phase"], as_index=False)["Mahalanobis_Distance"]
      .median()
)

for _, row in subject_medians.iterrows():
    ax.axvline(
        row["Mahalanobis_Distance"],
        color=subject_colors[row["Subject_ID"]],
        linestyle=(0, (5, 3)),
        lw=1.45,
        alpha=0.95,
        zorder=5
    )

# -----------------------------
# Axes, ticks, labels
# -----------------------------
ax.set_xlim(0, 24)
ax.set_ylim(0, ymax * 1.15)

ax.xaxis.set_major_locator(MultipleLocator(2))
ax.xaxis.set_minor_locator(MultipleLocator(0.25))
ax.tick_params(axis="x", which="major", length=6)
ax.tick_params(axis="x", which="minor", length=3)

ax.set_title("Multivariate Deviation from NHANES Reference: Kernel Density Plot", pad=22)
ax.text(
    0.5, 1.01,
    "Mahalanobis distance (17 biomarkers)",
    transform=ax.transAxes,
    ha="center",
    va="bottom",
    fontsize=13,
    style="italic"
)

ax.set_xlabel("Mahalanobis distance from NHANES reference")
ax.set_ylabel("Density")

ax.grid(axis="y", alpha=0.25, linestyle="--")
ax.grid(axis="x", alpha=0.12, linestyle="-")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# -----------------------------
# Legend
# -----------------------------
section_i4 = Line2D([], [], color="none", label="Inspiration4 subject lines")
i4_handles = [
    Line2D(
        [0], [0],
        color=i4_colors[s],
        linestyle=(0, (5, 3)),
        lw=1.8,
        label=f"Crew member {i+1} ({s})"
    )
    for i, s in enumerate(i4_subjects)
]

section_br = Line2D([], [], color="none", label="Bed Rest subject lines")
br_handles = [
    Line2D(
        [0], [0],
        color=br_colors[s],
        linestyle=(0, (5, 3)),
        lw=1.8,
        label=f"Bed rest subject {i+1} ({s})"
    )
    for i, s in enumerate(br_subjects)
]

section_kde = Line2D([], [], color="none", label="KDE distributions")
kde_handles = [
    Patch(
        facecolor=phase_colors[p],
        edgecolor=phase_colors[p],
        alpha=0.25,
        label=phase_labels[p]
    )
    for p in phase_order
]

handles = [section_i4] + i4_handles + [section_br] + br_handles + [section_kde] + kde_handles

leg = ax.legend(
    handles=handles,
    title="Legend",
    loc="center left",
    bbox_to_anchor=(1.01, 0.5),
    frameon=True,
    borderpad=1.1,
    labelspacing=0.75,
    handlelength=2.8
)

for txt in leg.get_texts():
    if txt.get_text() in ["Inspiration4 subject lines", "Bed Rest subject lines", "KDE distributions"]:
        txt.set_weight("bold")

# -----------------------------
# Footnote
# -----------------------------
fig.text(
    0.5,
    0.055,
    "Curves show KDEs of the real 1,000-iteration bootstrap Mahalanobis distances. "
    "Dashed vertical lines show each subject's median distance within each phase.",
    ha="center",
    va="center",
    fontsize=10,
    style="italic",
    bbox=dict(boxstyle="round,pad=0.55", facecolor="white", edgecolor="0.75")
)

fig.text(
    0.25,
    0.018,
    "Smaller distance = more similar to NHANES reference",
    ha="center",
    va="center",
    fontsize=10,
    color="#1F4E99"
)

fig.text(
    0.70,
    0.018,
    "Larger distance = more deviation from NHANES reference",
    ha="center",
    va="center",
    fontsize=10,
    color="#B00000"
)

plt.tight_layout(rect=[0, 0.08, 0.83, 0.96])

# -----------------------------
# Save
# -----------------------------
fig.savefig("realdata_kde_no_phase_medians_no_phase_titles.png", dpi=300, bbox_inches="tight")
fig.savefig("realdata_kde_no_phase_medians_no_phase_titles.pdf", bbox_inches="tight")
plt.close(fig)

print("Saved:")
print("realdata_kde_no_phase_medians_no_phase_titles.png")
print("realdata_kde_no_phase_medians_no_phase_titles.pdf")
