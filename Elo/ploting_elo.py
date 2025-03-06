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

models_with_eps = ["DQN", "QRDQN", "EQRDQN"]
filtered_data = elo_data[
    (~elo_data["Model"].isin(models_with_eps)) | (elo_data["Player Name"].str.contains("eps0.4", na=False))
]

max_elo_per_group = filtered_data.loc[filtered_data.groupby(["Model", "n_mcts"])['Elo Rating'].idxmax()]

player_name_list = max_elo_per_group["Player Name"].tolist()

plt.figure(figsize=(8, 5))
font_size = 16
bar_width = 0.1

custom_order_groups = [
    ["AC", "QRAC"],
    ["QAC", "QR-QAC", "EQR-QAC"],
    ["DQN", "QR-DQN", "EQR-DQN"]
]
filtered_data["Model"] = filtered_data["Model"].replace({
    "QRQAC": "QR-QAC",
    "QRDQN": "QR-DQN",
    "EQRDQN": "EQR-DQN",
    "EQRQAC": "EQR-QAC"
})

model_colors = {
    "AC": "orange", "QRAC": "yellow",
    "QAC": "purple", "QR-QAC": "red", "EQR-QAC": "blue",
    "DQN": "green", "QR-DQN": "magenta", "EQR-DQN": "cyan"
}

x_mapping = {2: 0, 10: 1, 50: 2, 100: 3, 400: 4}
num_groups = len(custom_order_groups)

group_offsets = [-0.25, 0, 0.3]  # 그룹 간 간격을 조정
inner_spacing = 0.08  # 같은 그룹 내 모델 간 간격을 좁게 조정하여 그룹별로 묶음 유지

group_idx_map = {model: i for i, group in enumerate(custom_order_groups) for model in group}

for group_idx, group in enumerate(custom_order_groups):
    base_offset = group_offsets[group_idx]
    for model_idx, model in enumerate(group):
        model_data = filtered_data[filtered_data["Model"] == model]
        for n_mcts in x_mapping.keys():
            subset = model_data[(model_data["Player Name"].isin(player_name_list)) & (model_data["n_mcts"] == n_mcts)]
            if not subset.empty:
                offset = base_offset + (model_idx * inner_spacing)
                plt.bar(
                    x_mapping[n_mcts] + offset,
                    subset["Elo Rating"].values[0],
                    width=bar_width,
                    color=model_colors[model],
                    label=model if n_mcts == 2 else ""
                )

plt.xticks(list(x_mapping.values()), labels=list(x_mapping.keys()), fontsize=font_size)
plt.yticks(fontsize=font_size)
plt.xlabel("Number of MCTS simulations", fontsize=font_size)
plt.ylabel("Elo Rating", fontsize=font_size)
plt.ylim(1000, plt.ylim()[1])
plt.legend(
    title="Model",
    loc="lower left",
    fontsize=font_size,
    title_fontsize=font_size,
    frameon=True,
    edgecolor="black",
    bbox_to_anchor=(1, 0)
)
plt.grid(axis="y", alpha=0.3)
plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)
plt.tight_layout()
plt.show()
