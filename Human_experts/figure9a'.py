import matplotlib.pyplot as plt
import numpy as np

def smooth(data, window_size):
    smoothed = np.convolve(data, np.ones(window_size) / window_size, mode='valid')
    padding = [data[0]] * (window_size - 1)
    return np.concatenate((padding, smoothed))

# 데이터 시퀀스
random_distances = [
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0099, 0.0087,
    0.0156, 0.0143, 0.0099, 0.0083, 0.0041, 0.0039,
    0.0014, 0.0038, 0.0020, 0.0001, 0.0000, 0.0000,
    0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
    0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
    0.0000, 0.0000, 0.0000, 0.0000
]

eqrqac_dict = {
    'EQRQAC_nmcts2': [
        0.0, 0.0, 0.0, 0.0, 0.0305, 0.0597, 0.0469,
        0.0497, 0.0546, 0.0597, 0.0639, 0.0523, 0.0381,
        0.0369, 0.0304, 0.0189, 0.0287, 0.0243, 0.0189,
        0.0102, 0.0074, 0.0057, 0.0020, 0.0000, 0.0000,
        0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
        0.0000, 0.0000, 0.0000, 0.0000, 0.0000
    ],
    'EQRQAC_nmcts10': [
        0.0, 0.0, 0.0, 0.0, 0.0535, 0.0967, 0.0759,
        0.0797, 0.0986, 0.1033, 0.0979, 0.0843, 0.0571,
        0.0549, 0.0444, 0.0258, 0.0367, 0.0297, 0.0209,
        0.0102, 0.0092, 0.0071, 0.0024, 0.0000, 0.0000,
        0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
        0.0000, 0.0000, 0.0000, 0.0000, 0.0000
    ],
    'EQRQAC_nmcts50': [
        0.0, 0.0, 0.0, 0.0, 0.0865, 0.1567, 0.1339,
        0.1297, 0.1606, 0.1683, 0.1599, 0.1053, 0.0931,
        0.0899, 0.0724, 0.0428, 0.0617, 0.0497, 0.0349,
        0.0172, 0.0157, 0.0117, 0.0034, 0.0000, 0.0000,
        0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
        0.0000, 0.0000, 0.0000, 0.0000, 0.0000
    ],
    'EQRQAC_nmcts100': [
        0.0, 0.0, 0.0, 0.0, 0.1105, 0.1997, 0.1859,
        0.1737, 0.2026, 0.2123, 0.2019, 0.1553, 0.1201,
        0.1149, 0.0924, 0.0548, 0.0787, 0.0637, 0.0449,
        0.0222, 0.0207, 0.0157, 0.0054, 0.0000, 0.0000,
        0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
        0.0000, 0.0000, 0.0000, 0.0000, 0.0000
    ],
    'EQRQAC_nmcts400': [
        0.0, 0.0, 0.0, 0.0, 0.1355, 0.2447, 0.2719,
        0.2897, 0.2456, 0.2573, 0.2439, 0.1603, 0.1431,
        0.1369, 0.1104, 0.0638, 0.0997, 0.0797, 0.0559,
        0.0282, 0.0247, 0.0177, 0.0060, 0.0000, 0.0000,
        0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
        0.0000, 0.0000, 0.0000, 0.0000, 0.0000
    ]
}

# 순서, 마커, 투명도
n_keys = ['EQRQAC_nmcts400', 'EQRQAC_nmcts100', 'EQRQAC_nmcts50', 'EQRQAC_nmcts10', 'EQRQAC_nmcts2']
markers = ['p', 'D', 'v', 's', 'o']
alpha_values = [1.0, 0.65, 0.55, 0.45, 0.35]

# 그래프 그리기
plt.figure(figsize=(4, 4))

# EQRQAC 그래프
for i, key in enumerate(n_keys):
    smoothed = smooth(eqrqac_dict[key], window_size=2)
    plt.plot(range(35), smoothed[:35], linestyle='-', marker=markers[i], color='blue',
             alpha=alpha_values[i], markersize=5, label=key)

# random 그래프
random_smoothed = smooth(random_distances, window_size=2)
plt.plot(range(35), random_smoothed[:35], linestyle='--', color='green', label='random')

# 스타일 설정
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.xticks([0, 10, 20, 30])
plt.yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
plt.xlabel('Move number')
plt.ylabel("Number of threats defended")
plt.grid(axis='y', linestyle='--', alpha=0.7)
# plt.legend()
plt.tight_layout()
plt.show()
