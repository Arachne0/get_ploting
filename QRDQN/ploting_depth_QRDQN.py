import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# 파일 로드
file_path = "ploting/csv_files/QRDQN/QRDQN_planning_depth.xlsx"
df = pd.read_excel(file_path)
mean_values = df.mean()

nmcts_labels = ["nmcts2", "nmcts10", "nmcts50", "nmcts100", "nmcts400"]
nmcts_values = [2, 10, 50, 100, 400]

eqrdqn_means = mean_values[[f"EQRDQN_{label}" for label in nmcts_labels]].values
qrdqn_columns = [col for col in df.columns if "QRDQN" in col and "EQRDQN" not in col]

def extract_quantile(col_name):
    match = re.search(r'quantiles(\d+)', col_name)
    return int(match.group(1)) if match else float('inf')

qrdqn_columns_sorted = sorted(qrdqn_columns, key=extract_quantile)
qrdqn_means_sorted = mean_values[qrdqn_columns_sorted].values.reshape(len(qrdqn_columns_sorted) // 5, 5)
num_qrdqn = qrdqn_means_sorted.shape[0]

# 그래프 크기 조정
width = 0.12  # 막대 너비 조정
group_width = (num_qrdqn + 1) * width
x = np.arange(len(nmcts_labels))

fig, ax = plt.subplots(figsize=(4.5, 6))  # 가로 크기 축소

# QRDQN 막대 그래프 그리기
for i in range(num_qrdqn):
    ax.bar(x - group_width / 2 + i * width,
           qrdqn_means_sorted[i], width, color="magenta",
           alpha=(i + 1) / num_qrdqn)

# EQRDQN 막대 그래프 추가
ax.bar(x - group_width / 2 + num_qrdqn * width, eqrdqn_means, width, label="EQRDQN", color="cyan")

# X, Y축 레이블 설정
ax.set_xlabel("Number of MCTS simulations", fontsize=18)
ax.set_ylabel("Planning Depth", fontsize=18)

# X축 눈금 설정
ax.set_xticks(x)
ax.set_xticklabels(nmcts_values, fontsize=18)
ax.yaxis.get_major_locator().set_params(integer=True)
ax.tick_params(axis='y', labelsize=18)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Y축 0부터 시작하도록 설정
max_value = max(np.max(qrdqn_means_sorted), np.max(eqrdqn_means))
ax.set_ylim(0, max_value * 1.05)

plt.subplots_adjust(top=0.95,)

# 범례 설정 (LaTeX 스타일 적용)
unique_quantiles = sorted(set(extract_quantile(q) for q in qrdqn_columns_sorted))

# QR-DQN quantile labels with proper LaTeX formatting
quantile_labels = [r"$\text{QR-DQN}~N_{\text{tau}}" + str(q) + r",~N_{\mathrm{eps}}0.4$" for q in unique_quantiles]
eqrdqn_label = r"$\text{EQR-DQN}~(N_{\text{eps}}0.4)$"

# 범례 등록
qrdqn_handles = [plt.Rectangle((0, 0), 1, 1, color="magenta", alpha=(i + 1) / num_qrdqn) for i in range(len(unique_quantiles))]
eqrdqn_handle = plt.Rectangle((0, 0), 1, 1, color="cyan")

ax.legend(handles=qrdqn_handles + [eqrdqn_handle],
          labels=quantile_labels + [eqrdqn_label],
          loc="upper left", bbox_to_anchor=(-0.02, 1.05),
          fontsize=14, fancybox=True, edgecolor='black', framealpha=0.8)

plt.show()
