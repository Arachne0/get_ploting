import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 파일 로드
file_path = 'csv_files/QRDQN_num_of_quantile.xlsx'
df = pd.read_excel(file_path)

mean_values = df.mean()

nmcts_labels = ["nmcts2", "nmcts10", "nmcts50", "nmcts100", "nmcts400"]
nmcts_values = [2, 10, 50, 100, 400]
eqrdqn_means = mean_values[[f"EQRDQN_{label}" for label in nmcts_labels]].values

width = 0.14  # 막대 너비 유지
x = np.arange(len(nmcts_labels)) * 0.4  # x 간격 더 좁게 조정
font_size = 18

fig, ax = plt.subplots(figsize=(4, 5))  # 그래프 가로 크기 줄이기
ax.bar(x, eqrdqn_means, width, label="EQR-DQN", color="cyan")

plt.xlabel(r"$N_{\text{mcts}}$", fontsize=font_size, labelpad=10)  # labelpad 추가
ax.set_ylabel(r"$N_{\tau}$", fontsize=font_size, labelpad=10)  # labelpad 추가

ax.set_xticks(x)
ax.set_xticklabels(nmcts_values, fontsize=18)
ax.set_yticks([0, 3, 9, 27, 81])
ax.tick_params(axis='y', labelsize=18)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.set_xlim(min(x) - width / 2, max(x) + width / 2)
plt.subplots_adjust(left=0.25, bottom=0.2, top=0.96, right=0.95)  # left와 bottom 조정

plt.tight_layout()

# ax.legend(loc="upper right", fontsize=18, bbox_to_anchor=(1, 1.05), fancybox=True, edgecolor='black')

plt.show()