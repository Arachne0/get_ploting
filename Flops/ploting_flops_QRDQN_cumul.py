# 다시 파일 로드
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


file_path = "QRDQN_flops_results.csv"
df = pd.read_csv(file_path)
columns_to_plot = ["quantile81_flops", "our_model_flops"]

nmcts_alpha = {
    2: 0.1,
    10: 0.1,
    50: 0.3,
    100: 0.5,
    400: 1.0
}

qrdqn_colors = {
    "quantile81_flops": (1, 0, 1),  # 마젠타 (QRQAC)
    "our_model_flops": (0, 1, 1)    # 시안 (EQRQAC)
}

legend_labels = {
    "quantile81_flops": "QR-DQN (Nmcts{nmcts}, Quantiles81, eps0.4)",
    "our_model_flops": "EQR-DQN (Nmcts{nmcts}, eps0.4)"
}

fig, ax = plt.subplots(figsize=(7.6, 5))

for nmcts, group in df.groupby("nmcts"):
    for col in columns_to_plot:
        color_with_alpha = (*qrdqn_colors[col], nmcts_alpha[nmcts])  # RGB + Alpha 포함
        ax.plot(group["step"], group[col] / 1e6, marker='.', linestyle='-', linewidth=1, markersize=4,
                color=color_with_alpha, alpha=nmcts_alpha[nmcts], zorder=nmcts,  # alpha 적용, zorder로 큰 nmcts가 위로 가도록 설정
                label=legend_labels[col].format(nmcts=nmcts))

ax.set_xlabel("Training Step", fontsize=18, labelpad=1)
ax.set_ylabel("Cumulative FLOPs (MFLOPs)", fontsize=16)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.tick_params(axis='x', labelsize=18)
ax.tick_params(axis='y', labelsize=18)

ax.yaxis.grid(True, linestyle='--', alpha=0.7)
ax.xaxis.grid(False)

# x축 범위 및 눈금 설정
ax.set_xlim(df["step"].min(), df["step"].max())
ax.set_xticks(np.arange(0, df["step"].max() + 1, 100))

handles, labels = ax.get_legend_handles_labels()
unique_labels = dict(zip(labels, handles))

legend_handles = [plt.Line2D([0], [0], color=(*qrdqn_colors[col], nmcts_alpha[nmcts]), linewidth=3)
                  for nmcts in nmcts_alpha for col in columns_to_plot]

ax.legend(legend_handles, unique_labels.keys(), fontsize=12, loc='upper left', bbox_to_anchor=(0.99, 1), frameon=False)

plt.subplots_adjust(top=0.95,right=0.45)
plt.show()
