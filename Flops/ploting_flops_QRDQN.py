import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# file_path = "csv_files/QRDQN_flops_results.csv"
file_path = "QRDQN_flops_results.csv"
df = pd.read_csv(file_path)
columns_to_plot = ["quantile81_flops", "our_model_flops"]

nmcts_alpha = {
    2: 0.1,
    10: 0.3,
    50: 0.5,
    100: 0.7,
    400: 1.0
}

qrdqn_colors = {
    "quantile81_flops": (1, 0, 1),  # 마젠타 (QRDQN)
    "our_model_flops": (0, 1, 1)    # 시안 (EQRDQN)
}

window_size = 20  # Moving average window size
fig, ax = plt.subplots(figsize=(5, 5))

for nmcts, group in df.groupby("nmcts"):
    for col in columns_to_plot:
        color_with_alpha = (*qrdqn_colors[col], nmcts_alpha[nmcts])
        flops_per_step = group[col].diff() / 1e6
        smoothed_flops = flops_per_step.rolling(window=window_size, min_periods=1).mean()
        ax.plot(group["step"], smoothed_flops, linestyle='-', linewidth=2,
                color=color_with_alpha, alpha=nmcts_alpha[nmcts], zorder=nmcts)

ax.set_xlabel("Training Step", fontsize=16)
ax.set_ylabel("FLOPs per Step (MFLOPs)", fontsize=16)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.tick_params(axis='x', labelsize=16)
ax.tick_params(axis='y', labelsize=16)

ax.yaxis.grid(True, linestyle='--', alpha=0.7)
ax.xaxis.grid(False)

# x축 범위 및 눈금 설정
ax.set_xlim(df["step"].min(), df["step"].max())
ax.set_xticks(np.arange(0, df["step"].max() + 1, 100))

ax.legend([plt.Line2D([0], [0], color=qrdqn_colors["quantile81_flops"], linewidth=3),
           plt.Line2D([0], [0], color=qrdqn_colors["our_model_flops"], linewidth=3)],
          ["QR-DQN", "EQR-DQN"],
          fontsize=14,
          loc='upper left',
          bbox_to_anchor=(0.97, 1),
          frameon=False,
          handlelength = 0.7,
          handletextpad = 0.3,
          borderpad = 0.3
)

plt.subplots_adjust(top=0.95, right=0.75, left=0.2
                    )
plt.show()
