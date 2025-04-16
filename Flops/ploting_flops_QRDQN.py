import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# file_path = "csv_files/QRDQN_flops_results.csv"
file_path = "QRDQN_flops_results.csv"
df = pd.read_csv(file_path)
columns_to_plot = ["quantile81_flops", "our_model_flops"]

nmcts_alpha = {
    2: 0.35,
    10: 0.45,
    50: 0.55,
    100: 0.65,
    400: 1.0
}

marker_list = ['o', 's', 'v', 'D', 'p', '*', 'x', '+', '<', '>']
nmcts_markers = {key: marker_list[i % len(marker_list)] for i, key in enumerate(sorted(nmcts_alpha.keys()))}

qrdqn_colors = {
    "quantile81_flops": (1, 0, 1),  # Magenta (QRDQN)
    "our_model_flops": (0, 1, 1)    # Cyan (EQRDQN)
}

window_size = 20  # Moving average window size
fig, ax = plt.subplots(figsize=(8, 5))

for nmcts, group in df.groupby("nmcts"):
    group = group.sort_values("step")
    for col in columns_to_plot:
        color_with_alpha = (*qrdqn_colors[col], nmcts_alpha[nmcts])
        marker = nmcts_markers[nmcts]

        flops_per_step = group[col].diff() / 1e6
        smoothed_flops = flops_per_step.rolling(window=window_size, min_periods=window_size).mean()
        smoothed_flops = smoothed_flops.interpolate(method='linear')

        ax.plot(group["step"], smoothed_flops, linestyle='-', linewidth=2,
                color=color_with_alpha, alpha=nmcts_alpha[nmcts], zorder=nmcts,
                marker=marker, markersize=3.5)

ax.set_xlabel("Training Step", fontsize=16)
ax.set_ylabel("FLOPs per Step (MFLOPs)", fontsize=16)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.tick_params(axis='x', labelsize=16)
ax.tick_params(axis='y', labelsize=16)

ax.yaxis.grid(False)
ax.xaxis.grid(False)

ax.set_xlim(df["step"].min(), df["step"].max())
ax.set_xticks(np.arange(0, df["step"].max() + 1, 100))

# Set y-axis ticks to 0.25, 0.5, 0.75
ax.set_yticks([0.25, 0.5, 0.75, 1.0, 1.25, 1.5])
x_min = df["step"].min()
x_max = df["step"].max()
ax.set_xticks(np.arange(100, x_max + 1, 100))

model_legend = [
    plt.Line2D([0], [0], color=qrdqn_colors["quantile81_flops"], linewidth=3, markersize=8, label="QR-DQN"),
    plt.Line2D([0], [0], color=qrdqn_colors["our_model_flops"], linewidth=3, markersize=8, label="EQR-DQN")
]

nmcts_legend = [
    plt.Line2D([0], [0], color="black", linewidth=2, markersize=5, alpha=nmcts_alpha[nmcts], label=f"$N_{{mcts}}={nmcts}$")
    for nmcts in sorted(nmcts_alpha.keys())
]

legend1 = ax.legend(handles=model_legend, fontsize=14, loc='upper left', bbox_to_anchor=(1.0, 1.0),
                    frameon=False, handlelength=1, handletextpad=0.2, borderpad=0.2)

ax.add_artist(legend1)

plt.subplots_adjust(top=0.97, right=0.8, left=0.12)
plt.show()
