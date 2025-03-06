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

filtered_data = elo_data[elo_data["Model"].isin(["AC", "QRAC"])]

max_elo_per_group = filtered_data.loc[filtered_data.groupby(["Model", "n_mcts"])['Elo Rating'].idxmax()]

player_name_list = max_elo_per_group["Player Name"].tolist()

plt.figure(figsize=(4, 5))
font_size = 18
bar_width = 0.18  # 막대 너비를 살짝 키움

custom_order_groups = [
    ["AC", "QRAC"]
]

model_colors = {
    "AC": "orange", "QRAC": "yellow"
}

x_mapping = {2: 0, 10: 0.7, 50: 1.4, 100: 2.0, 400: 2.6}  # 간격을 조정하여 막대 간격을 좁힘
num_groups = len(custom_order_groups)

group_offsets = [-0.09, 0.09]  # 두 모델이 겹치지 않도록 약간씩 좌우로 이동

group_idx_map = {model: i for i, group in enumerate(custom_order_groups) for model in group}

for group_idx, group in enumerate(custom_order_groups):
    for model_idx, model in enumerate(group):
        model_data = filtered_data[filtered_data["Model"] == model]
        for n_mcts in x_mapping.keys():
            subset = model_data[(model_data["Player Name"].isin(player_name_list)) & (model_data["n_mcts"] == n_mcts)]
            if not subset.empty:
                offset = group_offsets[model_idx]  # 각 모델의 막대를 조금씩 이동
                plt.bar(
                    x_mapping[n_mcts] + offset,
                    subset["Elo Rating"].values[0],
                    width=bar_width,
                    color=model_colors[model],
                    label=model if n_mcts == 2 else ""
                )

plt.xticks(list(x_mapping.values()), labels=list(x_mapping.keys()), fontsize=font_size)
# plt.xlabel("Number of MCTS simulations", fontsize=font_size)
plt.xlabel(r"$N_{{mcts}}$ simulation", fontsize=font_size)
plt.ylabel("Elo Rating", fontsize=font_size)

plt.ylim(1100, 2100)
plt.yticks([1000, 1200, 1400, 1600, 1800, 2000], fontsize=font_size)

plt.legend(
    title="Model",
    loc="upper left",
    fontsize=font_size,
    title_fontsize=font_size,
    frameon=True,
    edgecolor="black",
    bbox_to_anchor=(0, 1),  # 좌상단 위치
    handlelength=0.9,  # 색상 박스 길이 줄이기 (기본값: 2.0)
    handletextpad=0.3,  # 색상과 모델명 간 간격 줄이기 (기본값: 1.0)
    borderpad=0.3  # 범례 내부 패딩 줄이기 (기본값: 0.4~0.5)
)

plt.grid(axis="y", alpha=0.3)
plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)
plt.tight_layout()
plt.show()