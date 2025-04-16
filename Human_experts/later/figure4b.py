import os
import json
import matplotlib.pyplot as plt
import numpy as np

def calculate_distance(pos1, pos2):
    """Calculate the Chebyshev distance (max of x or y difference)."""
    x1, y1 = pos1
    x2, y2 = pos2
    return max(abs(x1 - x2), abs(y1 - y2))

def index_to_coordinates(index, cols=4):
    """Convert 1D index to 2D coordinates."""
    x = index // cols
    y = index % cols
    return (x, y)

def calculate_distances_from_fixed_center(actions):
    """Calculate distances of own stones (black stones) from the fixed center (17 or 18)."""
    # Get only odd-indexed actions (black stones)
    own_actions = [actions[i] for i in range(len(actions)) if i % 2 == 0]

    # Fixed central coordinates (17 or 18)
    center1 = index_to_coordinates(17)  # (4, 1)
    center2 = index_to_coordinates(18)  # (4, 2)

    # Convert actions to coordinates
    coordinates = [index_to_coordinates(action) for action in own_actions]

    # Calculate distances from the fixed center (17 or 18)
    distances = [min(calculate_distance(coord, center1), calculate_distance(coord, center2)) for coord in coordinates]
    return distances

def smooth(data, window_size):
    """Smooth the data using a simple moving average with NaN padding to maintain the initial value."""
    smoothed = np.convolve(data, np.ones(window_size)/window_size, mode='valid')
    # Add NaN padding at the beginning to maintain the original length
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

# ----------------- 실행 파트 -----------------

folder_path = '../gamefile'
player_name = 'EQRQAC_nmcts400'


try:
    # 실제 파일에서 액션 불러오기
    actions_list = load_action_sequences_from_files(folder_path, player_name)
    distance_lists = [calculate_distances_from_fixed_center(actions) for actions in actions_list]

    # 평균 거리 계산
    max_len = max(len(d) for d in distance_lists) if distance_lists else 0
    padded = [d + [np.nan]*(max_len - len(d)) for d in distance_lists]
    avg_distances = np.nanmean(padded, axis=0) if padded else []
    smoothed_distances = smooth(avg_distances, window_size=2) if len(avg_distances) > 0 else []

    # 랜덤 시퀀스 거리 (고정된 수치 사용)
    random_distances = [0, 2, 3, 3.1, 3.2, 3.4, 3.6, 3.4, 3.6, 3.7, 3.8, 3.6, 3.7,
                        3.9, 4.1, 4.2, 3.9, 4.4, 4.3, 4.6, 4.5, 4.5, 4.9, 4.6,
                        4.8, 5.1, 5.4, 5.5, 5.2, 5.4, 5.5, 5.6, 5.9]
    random_smoothed = smooth(random_distances, window_size=2)

    # --- 그래프 출력 ---
    plt.figure(figsize=(4, 4))
    if len(smoothed_distances) > 0:
        plt.plot(range(16), smoothed_distances[:16], marker='o', linestyle='-', color='b', markersize=4, label='EQRQAC_nmcts400')

    plt.plot(range(16), random_smoothed[:16], marker='o', linestyle='-', color='g', markersize=4, label='random')

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.xticks([0, 5, 10, 15])

    max_y = max(max(smoothed_distances[:16], default=0), max(random_smoothed[:16], default=0))
    plt.yticks(range(0, int(max_y) + 2))

    plt.xlabel('Move number')
    plt.ylabel("Distance to own center of mass")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    # plt.legend()
    plt.show()

except Exception as e:
    print('전체 오류 발생:', str(e))