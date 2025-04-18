import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_path = "csv_files/player_elo_result.csv"
elo_data = pd.read_csv(file_path)

elo_data["Model"] = elo_data["Player Name"].apply(lambda x: re.match(r"([A-Za-z]+)", x).group(0))
elo_data["n_mcts"] = elo_data["Player Name"].apply(
    lambda x: "efficient" if "efficient" in x else int(re.search(r"\d+", x).group(0))
)

elo_data = elo_data[elo_data["n_mcts"] != "efficient"]
elo_data["n_mcts"] = pd.to_numeric(elo_data["n_mcts"])
elo_data["Elo Rating"] = pd.to_numeric(elo_data["Elo Rating"], errors="coerce")

filtered_data = elo_data[elo_data["Model"].isin(["AC", "QRAC"])]

max_elo_per_group = filtered_data.loc[filtered_data.groupby(["Model", "n_mcts"])['Elo Rating'].idxmax()]

player_name_list = max_elo_per_group["Player Name"].tolist()

plt.figure(figsize=(4, 5))
font_size = 18
bar_width = 0.12  # 막대 너비 조정

custom_order_groups = [
    ["AC", "QRAC"]
]

model_colors = {
    "AC": "orange", "QRAC": "yellow"
}

x_mapping = {2: 0, 10: 0.4, 50: 0.8, 100: 1.2, 400: 1.6}   # x축 위치 조정\
# x_mapping = {2: 0, 10: 0.4, 50: 0.8, 100: 1.5, 400: 2.0}
num_groups = len(custom_order_groups)

group_offsets = [-0.05, 0.05]

group_idx_map = {model: i for i, group in enumerate(custom_order_groups) for model in group}

for group_idx, group in enumerate(custom_order_groups):
    for model_idx, model in enumerate(group):
        model_data = filtered_data[filtered_data["Model"] == model]
        for n_mcts in x_mapping.keys():
            # subset = model_data[(model_data["Player Name"].isin(player_name_list)) & (model_data["n_mcts"] == n_mcts)]
            subset = model_data[model_data["n_mcts"] == n_mcts]

            if not subset.empty:
                offset = group_offsets[model_idx]  # 각 모델 막대 위치 조정
                plt.bar(
                    x_mapping[n_mcts] + offset,
                    subset["Elo Rating"].values[0],
                    width=bar_width,
                    color=model_colors[model],
                    label=model if n_mcts == 2 else ""
                )

plt.xticks(list(x_mapping.values()), labels=list(x_mapping.keys()), fontsize=font_size)
plt.xlabel(r"$N_{\text{mcts}}$", fontsize=font_size)

plt.ylabel("Elo Rating", fontsize=font_size)
plt.ylim(1100, 2100)
plt.yticks([1200, 1400, 1600, 1800, 2000], fontsize=font_size)

plt.subplots_adjust(left=0.1)

plt.legend(
    loc="upper center",
    fontsize=16,
    frameon=True,
    edgecolor="none",
    bbox_to_anchor=(0.5, 1.1),  # 범례 위치 조정
    ncol=3,  # 3개 나란히 배치
    columnspacing=0.4,  # 열 간 간격 줄이기
    handlelength=0.6,  # 색상 박스 길이 줄이기
    handletextpad=0.2,  # 색상과 모델명 간 간격 줄이기
    borderpad=0.2  # 범례 내부 패딩 줄이기
)

plt.grid(axis="y", alpha=0.3)
plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)
plt.tight_layout()
plt.show()
