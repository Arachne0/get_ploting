import os
import json
import numpy as np
import matplotlib.pyplot as plt

# 거리 계산 관련 함수들
def calculate_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return max(abs(x1 - x2), abs(y1 - y2))

def index_to_coordinates(index, cols=4):
    x = int(index) // cols
    y = int(index) % cols
    return (x, y)

def calculate_pairwise_distances(action_vector):
    distances = [0]
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

# 평균 거리 계산 함수 (NaN padding 고려)
def compute_average_distance(distance_lists):
    max_len = max(len(d) for d in distance_lists) if distance_lists else 0
    padded = [d + [np.nan] * (max_len - len(d)) for d in distance_lists]
    return np.nanmean(padded, axis=0)

# 이동 평균 함수
def apply_moving_average(data, window):
    return smooth(data, window)

# 메인 로직
folder_path = '../gamefile'
player_name = 'EQRQAC_nmcts400'

try:
    actions_list = load_action_sequences_from_files(folder_path, player_name)
    distance_lists = [calculate_pairwise_distances(actions) for actions in actions_list]

    if actions_list:
        avg_distances = compute_average_distance(distance_lists)
        smoothed_distances = apply_moving_average(avg_distances, window=2)
    else:
        smoothed_distances = []


    smoothed_distances = [0.0, 1.56795108, 2.48150822,
 2.991447, 3.05608, 3.119213, 3.179476, 3.235745, 3.287239,
 3.333591, 3.374876, 3.411603, 3.444677, 3.475315, 3.504944,
 3.535081, 3.567194, 3.602586, 3.642274, 3.686906, 3.736706,
 3.791451, 3.850492, 3.91281, 3.977107, 4.041909, 4.105704,
 4.167063, 4.224768, 4.277916, 4.325996, 4.368934, 4.407098,
 4.441268, 4.472567, 4.502366]
    smoothed_distances = apply_moving_average(smoothed_distances, window=2)

    # 랜덤 시퀀스 거리 (직접 정의)
    random_distances = [0, 3, 3.4,
                 3.6, 3.647, 3.692, 3.734, 3.772, 3.805, 3.833, 3.855, 3.874,
                 3.89, 3.905, 3.92, 3.938, 3.959, 3.985, 4.016, 4.052, 4.093, 4.1,
                 4.138, 4.184, 4.231, 4.278, 4.321, 4.36, 4.395, 4.424, 4.448, 4.479,
                 4.468, 4.485, 4.5]
    random_smoothed = apply_moving_average(random_distances, window=2)


    # 그래프 출력
    plt.figure(figsize=(4, 4))
    if len(smoothed_distances) > 0:
        plt.plot(range(35), smoothed_distances[:35], marker='o', linestyle='-', color='b', markersize=4, label='EQRQAC_nmcts400')

    # plt.plot(range(35), random_smoothed[:35], marker='o', linestyle='-', color='g', markersize=4, label='random')
    plt.plot(range(35), random_smoothed[:35], linestyle='--', color='g', label='random')

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.xticks([0, 10, 20, 30])
    plt.yticks(range(0, int(max(max(smoothed_distances[:16], default=0), max(random_smoothed[:30]))) + 2))
    plt.xlabel('Move number')
    plt.ylabel("Distance to opponent's pieces")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    # plt.legend()
    plt.show()

except Exception as e:
    print('전체 오류 발생:', str(e))
