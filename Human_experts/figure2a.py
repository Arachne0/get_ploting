import json
import os
import numpy as np
import matplotlib.pyplot as plt

# 거리 계산 관련 함수
def calculate_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return max(abs(x1 - x2), abs(y1 - y2))

def index_to_coordinates(index, cols=4):
    x = int(index) // cols
    y = int(index) % cols
    return (x, y)

def calculate_pairwise_distances(action_vector):
    distances = [0, 0]
    for i in range(2, len(action_vector)):
        pos1 = index_to_coordinates(action_vector[i - 2])
        pos2 = index_to_coordinates(action_vector[i])
        distance = calculate_distance(pos1, pos2)
        distances.append(distance)
    return distances

def smooth(data, window_size):
    smoothed = np.convolve(data, np.ones(window_size)/window_size, mode='valid')
    padding = [data[0]] * (window_size - 1)
    smoothed = np.concatenate((padding, smoothed))
    return smoothed

# 파일에서 action sequence를 불러오는 함수
def load_action_sequences_from_files(folder_path, player_name, file_count=50):
    all_actions_list = []
    for i in range(1, file_count + 1):
        file_path = os.path.join(folder_path, f'league_results{i}.json')
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for record in data:
                    if record.get('player1') == player_name:
                        actions = [int(a) for a in record.get('actions', [])]
                        all_actions_list.append(actions)
        except FileNotFoundError:
            continue
        except Exception as e:
            continue
    return all_actions_list

# 실제 사용 부분
folder_path = 'gamefile'
player_name = 'EQRQAC_nmcts400'

# actions_list = load_action_sequences_from_files(folder_path, player_name)
# distance_lists = [calculate_pairwise_distances(actions) for actions in actions_list]
# max_len = max(len(d) for d in distance_lists) if distance_lists else 0
# padded = [d + [np.nan]*(max_len - len(d)) for d in distance_lists]
# avg_distances = np.nanmean(padded, axis=0) if padded else []
# smoothed_distances = smooth(avg_distances, window_size=2) if len(avg_distances) > 0 else []

smoothed_distances = [0.        , 0.        , 2.26795108, 2.48150822, 2.991447, 3.097595, 3.202231, 3.30399, 3.401789, 3.494934,
 3.583184, 3.666779, 3.746415, 3.823174, 3.89842, 3.973667,
 4.050425, 4.130061, 4.213656, 4.301907, 4.395051, 4.49285,
 4.594609, 4.699245, 4.805393, 4.911541, 5.016177, 5.117936,
 5.215735, 5.30888, 5.39713, 5.480725, 5.560361, 5.63712,
 5.712366]

smoothed_distances = smooth(smoothed_distances, window_size=2)
# 랜덤 시퀀스 하나 생성
random_sequence = np.random.choice(range(36), size=34, replace=False)
# random_distances = calculate_pairwise_distances(random_sequence)
random_distances = [0,0,2.5,3.1,3.66, 3.991, 4.079, 4.163, 4.24 , 4.309, 4.37 , 4.424, 4.473,
       4.519, 4.563, 4.609, 4.66 , 4.716, 4.78 , 4.852, 4.931, 5.016, 5.01,
       5.106, 5.197, 5.288, 5.374, 5.456, 5.53 , 5.597, 5.656, 5.708, 5.73,
       5.755, 5.8  ]
random_smoothed = smooth(random_distances, window_size=2)

# 그래프 출력
plt.figure(figsize=(4, 4))
if len(smoothed_distances) > 0:
    plt.plot(range(35), smoothed_distances[:35], marker='o', linestyle='-', color='b', markersize=4, label='EQRQAC_nmcts400')

# plt.plot(range(35), random_smoothed[:35], marker='o', linestyle='-', color='g', markersize=4, label='random')
plt.plot(range(35), random_smoothed[:35], linestyle='--', color='g', label='random')

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.xticks([0, 10, 20, 30])
plt.yticks(range(0, int(max(max(smoothed_distances[:33], default=0), max(random_smoothed[:30]))) + 2))
plt.xlabel('Move number')
plt.ylabel('Distance to own pieces')
plt.grid(axis='y', linestyle='--', alpha=0.7)
# plt.legend()
plt.show()
