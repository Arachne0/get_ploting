import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# file_path = "csv_files/QRDQN_flops_results.csv"
file_path = "QRDQN_flops_results.csv"
df = pd.read_csv(file_path)
columns_to_plot = ["quantile81_flops", "our_model_flops"]

nmcts_alpha = {
    2: 0.45,
    10: 0.55,
    50: 0.65,
    100: 0.75,
    400: 1.0
}

qrdqn_colors = {
    "quantile81_flops": (1, 0, 1),  # 마젠타 (QRDQN)
    "our_model_flops": (0, 1, 1)  # 시안 (EQRDQN)
}

window_size = 20  # Moving average window size
fig, ax = plt.subplots(figsize=(5.5, 5))

for nmcts, group in df.groupby("nmcts"):
    for col in columns_to_plot:
        color_with_alpha = (*qrdqn_colors[col], nmcts_alpha[nmcts])
        flops_per_step = group[col].diff() / 1e6
        smoothed_flops = flops_per_step.rolling(window=window_size, min_periods=window_size).mean()
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

# 기존 모델별 범례 (왼쪽 정렬)
model_legend = [
    plt.Line2D([0], [0], color=qrdqn_colors["quantile81_flops"], linewidth=3, markersize=8, label="QR-DQN"),
    plt.Line2D([0], [0], color=qrdqn_colors["our_model_flops"], linewidth=3, markersize=8, label="EQR-DQN")
]

# nmcts 값에 따른 검은색 선 범례 추가 (오른쪽 정렬)
nmcts_legend = [
    plt.Line2D([0], [0], color="black", linewidth=2, markersize=8, alpha=nmcts_alpha[nmcts], label=f"$N_{{mcts}}={nmcts}$")
    for nmcts in sorted(nmcts_alpha.keys())
]

# combined_legend = model_legend + nmcts_legend
#
# # 하나의 열로 세로 정렬된 범례로 표시
# ax.legend(handles=combined_legend, fontsize=14, loc='upper left',
#           bbox_to_anchor=(1.02, 1.0), frameon=False, handlelength=1,
#           handletextpad=0.2, borderpad=0.2, ncol=1)

# legend1 = ax.legend(handles=model_legend, fontsize=14, loc='upper left', bbox_to_anchor=(1.0, 1.0),
#                     frameon=False, handlelength=1, handletextpad=0.2, borderpad=0.2)
# legend2 = ax.legend(handles=nmcts_legend, fontsize=14, loc='upper left', bbox_to_anchor=(1.5, 1.0),
#                     frameon=False, handlelength=1, handletextpad=0.2, borderpad=0.2)

# ax.add_artist(legend1)  # 첫 번째 범례를 유지

plt.subplots_adjust(top=0.98, right=0.65, left=0.2,)
plt.show()