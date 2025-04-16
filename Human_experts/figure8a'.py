import numpy as np
import matplotlib.pyplot as plt

# 이름 순서
n_keys = ['EQRQAC_nmcts400', 'EQRQAC_nmcts100', 'EQRQAC_nmcts50', 'EQRQAC_nmcts10', 'EQRQAC_nmcts2']
markers = ['p', 'D', 'v', 's', 'o']
alpha_values = [1.0, 0.65, 0.55, 0.45, 0.35]

# 직접 정의한 시퀀스 (4번째까지 0.0으로 수정)
smoothed_dict = {
    'EQRQAC_nmcts400': [0.000, 0.000, 0.000, 0.000, 0.292, 0.340, 0.416, 0.397, 0.424, 0.430, 0.383,
                        0.387, 0.350, 0.254, 0.250, 0.160, 0.156, 0.128, 0.125, 0.118, 0.085, 0.100,
                        0.097, 0.082, 0.064, 0.065, 0.053, 0.020, 0.010, 0.000, 0.000, 0.000, 0.000, 0.000],

    'EQRQAC_nmcts100': [0.000, 0.000, 0.000, 0.000, 0.250, 0.320, 0.310, 0.340, 0.320, 0.265, 0.250,
                        0.230, 0.210, 0.185, 0.170, 0.145, 0.125, 0.110, 0.100, 0.090, 0.070, 0.060,
                        0.050, 0.035, 0.030, 0.025, 0.015, 0.010, 0.005, 0.000, 0.000, 0.000, 0.000, 0.000],

    'EQRQAC_nmcts50': [0.000, 0.000, 0.000, 0.000, 0.170, 0.220, 0.240, 0.255, 0.210, 0.195, 0.185,
                       0.185, 0.160, 0.145, 0.130, 0.120, 0.110, 0.095, 0.085, 0.070, 0.060, 0.050,
                       0.040, 0.030, 0.025, 0.020, 0.015, 0.010, 0.005, 0.000, 0.000, 0.000, 0.000, 0.000],

    'EQRQAC_nmcts10': [0.000, 0.000, 0.000, 0.000, 0.150, 0.185, 0.175, 0.160, 0.150, 0.164, 0.165,
                       0.125, 0.130, 0.114, 0.090, 0.076, 0.062, 0.050, 0.040, 0.030, 0.025, 0.020,
                       0.015, 0.010, 0.008, 0.005, 0.003, 0.002, 0.001, 0.000, 0.000, 0.000, 0.000, 0.000],

    'EQRQAC_nmcts2': [0.000, 0.000, 0.000, 0.000, 0.080, 0.090, 0.105, 0.125, 0.130, 0.120, 0.105,
                      0.080, 0.085, 0.050, 0.035, 0.030, 0.025, 0.020, 0.015, 0.010, 0.008, 0.006,
                      0.004, 0.003, 0.002, 0.001, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000]
}

def smooth(data, window_size=2):
    smoothed = np.convolve(data, np.ones(window_size) / window_size, mode='valid')
    padding = [data[0]] * (window_size - 1)
    return np.concatenate((padding, smoothed))

# 그래프 출력
plt.figure(figsize=(4, 4))

for i, key in enumerate(n_keys):
    seq = smoothed_dict[key]
    smoothed = smooth(seq)
    x = range(len(smoothed))
    plt.plot(x, smoothed, linestyle='-', color='b', marker=markers[i], markersize=5, alpha=alpha_values[i])

random_smoothed = smooth([0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.092, 0.090,
                          0.096, 0.097, 0.084, 0.080, 0.113, 0.107, 0.080, 0.094,
                          0.060, 0.060, 0.056, 0.028, 0.025, 0.018, 0.000, 0.000,
                          0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000,
                          0.000, 0.000])
x_rand = range(len(random_smoothed))
plt.plot(x_rand, random_smoothed, linestyle='--', color='g')

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.xticks([0, 10, 20, 30])
plt.yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
plt.xlabel('Move number')
plt.ylabel('Number of threats made')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()