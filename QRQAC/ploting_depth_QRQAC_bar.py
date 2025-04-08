import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# 파일 로드
file_path = "csv_files/QRQAC_planning_depths.xlsx"
df = pd.read_excel(file_path)
mean_values = df.mean()

nmcts_labels = ["nmcts2", "nmcts10", "nmcts50", "nmcts100", "nmcts400"]
nmcts_values = [2, 10, 50, 100, 400]

eqrqac_means = mean_values[[f"EQRQAC_{label}" for label in nmcts_labels]].values
qrqac_columns = [col for col in df.columns if "QRQAC" in col and "EQRQAC" not in col]


def extract_quantile(col_name):
    match = re.search(r'quantiles(\d+)', col_name)
    return int(match.group(1)) if match else float('inf')

qrqac_columns_sorted = sorted(qrqac_columns, key=extract_quantile)
qrqac_means_sorted = mean_values[qrqac_columns_sorted].values.reshape(len(qrqac_columns_sorted) // 5, 5)
num_qrqac = qrqac_means_sorted.shape[0]

width = 0.12
font_size = 18
group_width = (num_qrqac + 1) * width
x = np.arange(len(nmcts_labels))

fig, ax = plt.subplots(figsize=(4, 5))  # 가로 너비 축소

for i in range(num_qrqac):
    ax.bar(x - group_width / 2 + i * width,
           qrqac_means_sorted[i], width, color="red",
           alpha=(i + 1) / num_qrqac)

# EQRQAC 막대 그래프 추가
ax.bar(x - group_width / 2 + num_qrqac * width, eqrqac_means, width, label="EQRQAC", color="blue")

# X, Y축 레이블 설정
plt.xlabel(r"$N_{\text{mcts}}$", fontsize=font_size, labelpad=10)
ax.set_ylabel("Planning Depth", fontsize=18, labelpad=10)

# X축 눈금 설정
ax.set_xticks(x)
ax.set_xticklabels(nmcts_values, fontsize=18)
ax.yaxis.get_major_locator().set_params(integer=True)
ax.tick_params(axis='y', labelsize=18)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Y축 0부터 시작하도록 설정
max_value = max(np.max(qrqac_means_sorted), np.max(eqrqac_means))
ax.set_ylim(0, max_value * 1.05)  # 5% 여유만 추가, 0에서 시작

plt.tight_layout()

unique_quantiles = sorted(set(extract_quantile(q) for q in qrqac_columns_sorted))
qrqac_handles = [plt.Rectangle((0, 0), 1, 1, color="red", alpha=(i + 1) / num_qrqac) for i in range(len(unique_quantiles))]
quantile_labels = [f"$\\text{{QR-QAC}} ~ N_{{\\tau}}={q}$" for q in unique_quantiles]
eqrqac_handle = plt.Rectangle((0, 0), 1, 1, color="blue", label="EQRQAC")

ax.legend(handles=qrqac_handles + [eqrqac_handle],
          labels=quantile_labels + ["EQR-QAC"],
          loc="upper left",
          bbox_to_anchor=(0, 1.05),
          fontsize=16,
          fancybox=True,
          edgecolor='black',
          framealpha=0.8,
          columnspacing=0.4,  # 열 간 간격 줄이기
          handlelength=0.6,  # 색상 박스 길이 줄이기
          handletextpad=0.2  # 색상과 모델명 간 간격 줄이기
          )

plt.show()