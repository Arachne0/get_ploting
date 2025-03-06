import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re


file_path = "csv_files/QRQAC_planning_depths.xlsx"
df = pd.read_excel(file_path)
mean_values = df.mean()
std_values = df.std()

nmcts_labels = ["nmcts2", "nmcts10", "nmcts50", "nmcts100", "nmcts400"]
nmcts_values = [2, 10, 50, 100, 400]

qrqac_columns = [col for col in df.columns if "QRQAC" in col and "EQRQAC" not in col]


def extract_quantile(col_name):
    match = re.search(r'quantiles(\d+)', col_name)
    return int(match.group(1)) if match else float('inf')


qrqac_columns_sorted = sorted(qrqac_columns, key=extract_quantile)
qrqac_means_sorted = mean_values[qrqac_columns_sorted].values.reshape(len(qrqac_columns_sorted) // 5, 5)
qrqac_stds_sorted = std_values[qrqac_columns_sorted].values.reshape(len(qrqac_columns_sorted) // 5, 5)
num_qrqac = qrqac_means_sorted.shape[0]


eqrqac_means = mean_values[[f"EQRQAC_{label}" for label in nmcts_labels]].values
eqrqac_stds = std_values[[f"EQRQAC_{label}" for label in nmcts_labels]].values

font_size = 18

x_positions = np.linspace(0, 1, len(nmcts_values))


offset = 0.03
x_shifts = np.linspace(-offset * (num_qrqac - 1) / 2, offset * (num_qrqac - 1) / 2, num_qrqac)
eqrqac_shift = offset * (num_qrqac // 2 + 1)

fig, ax = plt.subplots(figsize=(5, 6))


for i in range(num_qrqac):
    ax.errorbar(x=x_positions + x_shifts[i],
                y=qrqac_means_sorted[i],
                yerr=qrqac_stds_sorted[i],
                fmt='o', markersize=4, color="red",
                alpha=(i + 1) / num_qrqac,
                capsize=4, label=f"QR-QAC $N_{{\\tau}}={extract_quantile(qrqac_columns_sorted[i * 5])}$")


ax.errorbar(x=x_positions + eqrqac_shift,
            y=eqrqac_means,
            yerr=eqrqac_stds,
            fmt='s', markersize=4, color="blue",
            capsize=4, label="EQRQAC")

ax.set_xlabel("Number of MCTS simulations", fontsize=font_size)
ax.set_ylabel("Planning Depth", fontsize=font_size)
ax.set_xticks(x_positions)
ax.set_xticklabels(nmcts_values, fontsize=font_size)
ax.yaxis.get_major_locator().set_params(integer=True)
ax.tick_params(axis='y', labelsize=font_size)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

max_value = max(np.max(qrqac_means_sorted), np.max(eqrqac_means))
ax.set_ylim(0, max_value * 1.15)

plt.subplots_adjust(top=0.95, right=0.95)
ax.legend(loc="upper left",
          bbox_to_anchor=(0, 1.0),
          fontsize=font_size,
          fancybox=True,
          edgecolor='black',
          framealpha=0.8,
          handlelength=0.9,
          handletextpad=0.3,
          borderpad=0.3)

plt.show()
