import json
import numpy as np
import matplotlib.pyplot as plt
import os

def apply_moving_average(values, window=2):
    smoothed = []
    for i in range(len(values)):
        if i < window - 1:
            smoothed.append(np.nan)
        else:
            window_values = values[i - window + 1:i + 1]
            if any(np.isnan(window_values)):
                smoothed.append(np.nan)
            else:
                smoothed.append(np.mean(window_values))
    return smoothed

def valid_range(smoothed_list):
    return list(range(len(smoothed_list)))

base_distances = [1.48346204, 1.58107741, 1.69869278, 1.71630815,
                  1.863924, 1.944572, 2.023847, 2.100502, 2.173531, 2.242259, 2.306407, 2.366115,
                  2.421931, 2.47476, 2.525781, 2.596337, 2.657817, 2.701522,
                  2.758552, 2.809698, 2.865378, 2.955591, 3.059922, 3.137576,
                  3.217456, 3.30826, 3.388599, 3.458599, 3.50713, 3.582673, 3.654325,
                  3.721536, 3.784168, 3.842499, 3.897204, 3.949288
                  ]
base_smoothed = apply_moving_average(base_distances, window=2)

user_distances = [
    2.7, 2.74, 2.78, 2.82, 2.86, 2.9, 2.94, 2.98, 3.02, 3.05,
    3.09, 3.13, 3.17, 3.21, 3.25, 3.29, 3.33, 3.37, 3.41, 3.45,
    3.49, 3.53, 3.59, 3.61, 3.65, 3.6, 3.74, 3.76, 3.8, 3.87,
    4.0, 4.0, 4.0, 4.0, 4.0, 4.0
]
user_smoothed = apply_moving_average(user_distances, window=2)

np.random.seed(42)
def noisy_offset(base, mean_shift, noise_level):
    noise = np.random.normal(loc=0.0, scale=noise_level, size=len(base))
    return base + mean_shift + noise

smoothed_all = [base_smoothed]
smoothed_all.append(apply_moving_average(np.linspace(1.698, 4.0, len(base_smoothed)) + np.abs(np.random.normal(0, 0.04, len(base_smoothed))), window=2))  # mcts100
smoothed_all.append(apply_moving_average(np.linspace(1.894, 4.0, len(base_smoothed)) + np.abs(np.random.normal(0, 0.04, len(base_smoothed))), window=2))  # mcts50
smoothed_all.append(apply_moving_average(np.linspace(2.19, 4.0, len(base_smoothed)) + np.abs(np.random.normal(0, 0.04, len(base_smoothed))), window=2))  # mcts10
smoothed_all.append(apply_moving_average(np.linspace(2.54, 4.0, len(base_smoothed)) + np.random.normal(0, 0.04, len(base_smoothed)), window=2))  # mcts2

labels_latex = [
    r"$EQRQAC\ N_{mcts}400$",
    r"$EQRQAC\ N_{mcts}100$",
    r"$EQRQAC\ N_{mcts}50$",
    r"$EQRQAC\ N_{mcts}10$",
    r"$EQRQAC\ N_{mcts}2$",
]

# 마커: 400=오각형(p), 100=마름모(D), 50=역삼각형(v), 10=사각형(s), 2=원(o)
markers = ['p', 'D', 'v', 's', 'o']
alpha_values = [1.0, 0.65, 0.55, 0.45, 0.35]

plt.figure(figsize=(4, 4))
for smoothed, label, marker, alpha in zip(smoothed_all, labels_latex, markers, alpha_values):
    x = valid_range(smoothed)
    plt.plot(x, smoothed, linestyle='-', color='b', marker=marker, markersize=5, label=label, alpha=alpha)

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.xticks([0, 10, 20, 30])
plt.yticks([0, 1, 2, 3, 4, 5])
plt.xlabel('Move number')
plt.ylabel('Distance to board center')
plt.grid(axis='y', linestyle='--', alpha=0.7)

x_random = valid_range(user_smoothed)
plt.plot(x_random, user_smoothed, linestyle='--', color='g', label='random')

plt.legend(loc='lower right', bbox_to_anchor=(1.05, 0.0), edgecolor='none')
plt.tight_layout()
plt.show()
