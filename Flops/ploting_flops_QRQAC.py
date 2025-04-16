import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# File path
file_path = "QRQAC_flops_results.csv"
df = pd.read_csv(file_path)
columns_to_plot = ["quantile81_flops", "our_model_flops"]

# Set alpha values based on Nmcts
nmcts_alpha = {
    2: 0.35,
    10: 0.45,
    50: 0.55,
    100: 0.65,
    400: 1.0
}

# Define markers for each Nmcts value
marker_list = ['o', 's', 'v', 'D', 'p', '*', 'x', '+', '<', '>']
nmcts_markers = {key: marker_list[i % len(marker_list)] for i, key in enumerate(sorted(nmcts_alpha.keys()))}

# Define colors for each model
qrqac_colors = {
    "quantile81_flops": (1, 0, 0),  # Red (QRQAC)
    "our_model_flops": (0, 0, 1)    # Blue (EQRQAC)
}

window_size = 20  # Moving average window size
fig, ax = plt.subplots(figsize=(8, 5))

# Group data by Nmcts and plot
for nmcts, group in df.groupby("nmcts"):
    group = group.sort_values("step")
    for col in columns_to_plot:
        color_with_alpha = (*qrqac_colors[col], nmcts_alpha[nmcts])
        marker = nmcts_markers[nmcts]

        flops_per_step = group[col].diff() / 1e6
        smoothed_flops = flops_per_step.rolling(window=window_size, min_periods=window_size).mean()
        smoothed_flops = smoothed_flops.interpolate(method='linear')

        ax.plot(group["step"], smoothed_flops, linestyle='-', linewidth=2,
                color=color_with_alpha, alpha=nmcts_alpha[nmcts], zorder=nmcts,
                marker=marker, markersize=3.5, label=f"{col} (Nmcts={nmcts})")

# Set axis labels
ax.set_xlabel("Training Step", fontsize=16)
ax.set_ylabel("FLOPs per Step (MFLOPs)", fontsize=16)

# Remove top and right spines
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Set tick label sizes
ax.tick_params(axis='x', labelsize=16)
ax.tick_params(axis='y', labelsize=16)

# Remove all grid lines
ax.yaxis.grid(False)
ax.xaxis.grid(False)

# Set x-axis range and ticks
x_min = df["step"].min()
x_max = df["step"].max()
# ax.set_xlim(x_min - 10, x_max)
ax.set_xticks(np.arange(100, x_max + 1, 100))

# Combine model and Nmcts legends into a single column
model_legend = [
    plt.Line2D([0], [0], color=qrqac_colors["quantile81_flops"], linewidth=3, markersize=8, label="QR-QAC"),
    plt.Line2D([0], [0], color=qrqac_colors["our_model_flops"], linewidth=3, markersize=8, label="EQR-QAC")
]

nmcts_legend = [
    plt.Line2D([0], [0], color="black", linewidth=2, markersize=5, marker=nmcts_markers[nmcts],
               label=f"$N_{{mcts}}={nmcts}$")
    for nmcts in sorted(nmcts_alpha.keys())
]

combined_legend = model_legend + nmcts_legend
ax.legend(handles=combined_legend[::-1], fontsize=14, loc='upper left', bbox_to_anchor=(1.0, 1.0),
          frameon=False, handlelength=1, handletextpad=0.2, borderpad=0.2, ncol=1)

plt.subplots_adjust(top=0.97, right=0.8, left=0.12)
plt.show()
