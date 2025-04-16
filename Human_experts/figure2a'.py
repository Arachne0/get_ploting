import numpy as np
import matplotlib.pyplot as plt

# 이름 순서
n_keys = ['EQRQAC_nmcts400', 'EQRQAC_nmcts100', 'EQRQAC_nmcts50', 'EQRQAC_nmcts10', 'EQRQAC_nmcts2']
markers = ['p', 'D', 'v', 's', 'o']
alpha_values = [1.0, 0.65, 0.55, 0.45, 0.35]

# 직접 정의한 시퀀스
smoothed_dict = {
    'EQRQAC_nmcts400': [0., 0., 2.26795108, 2.48150822, 2.991447, 3.097595, 3.202231, 3.30399, 3.401789, 3.494934,
                        3.583184, 3.666779, 3.746415, 3.823174, 3.89842, 3.973667, 4.050425, 4.130061, 4.213656,
                        4.301907, 4.395051, 4.49285, 4.594609, 4.699245, 4.805393, 4.911541, 4.976177, 5.067936,
                        5.137936, 5.215735, 5.30888, 5.39713, 5.480725, 5.560361, 5.62712],

    'EQRQAC_nmcts100': [0., 0., 2.3, 2.52, 2.99, 3.11, 3.23, 3.34, 3.43, 3.53,
                        3.62, 3.7, 3.78, 3.85, 3.92, 3.99, 4.07, 4.15, 4.23, 4.31,
                        4.4, 4.49, 4.58, 4.67, 4.77, 4.87, 4.97, 5.07, 5.17, 5.27,
                        5.37, 5.46, 5.54, 5.62, 5.7],

    'EQRQAC_nmcts50': [0., 0., 2.36, 2.65, 3.03, 3.18, 3.34, 3.48, 3.6, 3.7,
                       3.8, 3.88, 3.96, 4.03, 4.1, 4.17, 4.25, 4.33, 4.41, 4.5,
                       4.59, 4.68, 4.78, 4.88, 4.98, 5.08, 5.18, 5.28, 5.38, 5.48,
                       5.56, 5.64, 5.71, 5.75, 5.78],

    'EQRQAC_nmcts10': [0., 0., 2.42, 2.77, 3.15, 3.31, 3.47, 3.62, 3.75, 3.86,
                       3.96, 4.04, 4.12, 4.19, 4.26, 4.34, 4.42, 4.5, 4.58, 4.66,
                       4.75, 4.84, 4.93, 5.02, 5.11, 5.2, 5.29, 5.38, 5.47, 5.56,
                       5.63, 5.7, 5.75, 5.78, 5.79],

    'EQRQAC_nmcts2': [0, 0, 2.45, 2.95, 3.55, 3.89, 3.97, 4.05, 4.12, 4.18, 4.24, 4.3, 4.35,
                      4.4, 4.44, 4.48, 4.52, 4.56, 4.61, 4.67, 4.74, 4.82, 4.88,
                      4.96, 5.06, 5.17, 5.26, 5.35, 5.44, 5.52, 5.59, 5.66, 5.7,
                      5.74, 5.77]
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

random_smoothed = smooth([0, 0, 2.5, 3.1, 3.66, 3.991, 4.079, 4.163, 4.24, 4.309, 4.37, 4.424, 4.473,
                          4.519, 4.563, 4.609, 4.66, 4.716, 4.78, 4.852, 4.931, 5.016, 5.01,
                          5.106, 5.197, 5.288, 5.374, 5.456, 5.53, 5.597, 5.656, 5.708, 5.73,
                          5.755, 5.8])
x_rand = range(len(random_smoothed))
plt.plot(x_rand, random_smoothed, linestyle='--', color='g')

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.xticks([0, 10, 20, 30])
plt.yticks(np.arange(0, 7, 1))
plt.xlabel('Move number')
plt.ylabel('Distance to own pieces')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
