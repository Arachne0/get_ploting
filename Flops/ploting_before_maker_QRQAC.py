import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# File path for the CSV data
file_path = "QRQAC_flops_results.csv"
df = pd.read_csv(file_path)
columns_to_plot = ["quantile81_flops", "our_model_flops"]

# Alpha values based on Nmcts
nmcts_alpha = {
    2: 0.45,
    10: 0.55,
    50: 0.65,
    100: 0.75,
    400: 1.0
}

# Colors for each model
qrqac_colors = {
    "quantile81_flops": (1, 0, 0),  # Red (QRQAC)
    "our_model_flops": (0, 0, 1)    # Blue (EQRQAC)
}

# Moving average window size
window_size = 20
fig, ax = plt.subplots(figsize=(5.5, 5))

# Plot the data grouped by Nmcts
for nmcts, group in df.groupby("nmcts"):
    for col in columns_to_plot:
        color_with_alpha = (*qrqac_colors[col], nmcts_alpha[nmcts])
        flops_per_step = group[col].diff() / 1e6
        smoothed_flops = flops_per_step.rolling(window=window_size, min_periods=window_size).mean()
        ax.plot(group["step"], smoothed_flops, linestyle='-', linewidth=2,
                color=color_with_alpha, alpha=nmcts_alpha[nmcts], zorder=nmcts)

# Set axis labels
ax.set_xlabel("Training Step", fontsize=16)
ax.set_ylabel("FLOPs per Step (MFLOPs)", fontsize=16)

# Remove the top and right spines
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Set tick label sizes
ax.tick_params(axis='x', labelsize=16)
ax.tick_params(axis='y', labelsize=16)

# Add grid lines on the y-axis
ax.yaxis.grid(True, linestyle='--', alpha=0.7)
ax.xaxis.grid(False)

# Set x-axis range and tick intervals
ax.set_xlim(df["step"].min(), df["step"].max())
ax.set_xticks(np.arange(0, df["step"].max() + 1, 100))

# Model-specific legend (aligned to the left)
model_legend = [
    plt.Line2D([0], [0], color=qrqac_colors["quantile81_flops"], linewidth=3, markersize=8, label="QR-QAC"),
    plt.Line2D([0], [0], color=qrqac_colors["our_model_flops"], linewidth=3, markersize=8, label="EQR-QAC")
]

# Nmcts levels in descending order
nmcts_levels = [1.0, 0.8, 0.6, 0.5, 0.4]

# Nmcts-specific legend (descending order)
nmcts_legend = [
    plt.Line2D([0], [0], color=plt.cm.Greys(level), linewidth=2, markersize=8, label=f"$N_{{mcts}}={nmcts}$")
    for nmcts, level in zip(sorted(nmcts_alpha.keys(), reverse=True), nmcts_levels)
]

# Combine both legends into a single column
combined_legend = model_legend + nmcts_legend

# Display the combined legend in a single column, vertically aligned
ax.legend(handles=combined_legend, fontsize=14, loc='upper left',
          bbox_to_anchor=(1.02, 1.0), frameon=False, handlelength=1,
          handletextpad=0.2, borderpad=0.2, ncol=1)

# Adjust the plot layout
plt.subplots_adjust(top=0.98, right=0.65, left=0.2)
plt.show()
