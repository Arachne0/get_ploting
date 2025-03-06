import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 파일 로드
file_path = 'ploting/csv_files/QRQAC/QRQAC_num_of_quantiles2.xlsx'
df = pd.read_excel(file_path)

mean_values = df.mean()

nmcts_labels = ["nmcts2", "nmcts10", "nmcts50", "nmcts100", "nmcts400"]
nmcts_values = [2, 10, 50, 100, 400]
eqrqac_means = mean_values[[f"EQRQAC_{label}" for label in nmcts_labels]].values

width = 0.14  # 막대 너비 유지
x = np.arange(len(nmcts_labels)) * 0.4  # x 간격 더 좁게 조정

fig, ax = plt.subplots(figsize=(4, 6))  # 그래프 가로 크기 줄이기
ax.bar(x, eqrqac_means, width, label="EQR-QAC", color="blue")

ax.set_xlabel("Number of MCTS simulations", fontsize=18)
ax.set_ylabel("Number of Quantiles", fontsize=18, labelpad=5)

ax.set_xticks(x)
ax.set_xticklabels(nmcts_values, fontsize=18)
ax.set_yticks([0, 3, 9, 27, 81])
ax.tick_params(axis='y', labelsize=18)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.set_xlim(min(x) - width / 2, max(x) + width / 2)
plt.subplots_adjust(left=0.2, top=0.96, right=0.95)

# ax.legend(loc="upper right", fontsize=18, bbox_to_anchor=(1, 1.05), fancybox=True, edgecolor='black')

plt.show()
