import json
import numpy as np
import matplotlib.pyplot as plt
import os
import random

def calculate_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return max(abs(x1 - x2), abs(y1 - y2))

def index_to_coordinates(index, cols=4):
    x = int(index) // cols
    y = int(index) % cols
    return (x, y)

def calculate_distances(actions):
    center1 = index_to_coordinates(17)
    center2 = index_to_coordinates(18)
    min_distances = []
    for action in actions:
        action_coords = index_to_coordinates(action)
        distance_to_17 = calculate_distance(action_coords, center1)
        distance_to_18 = calculate_distance(action_coords, center2)
        min_distance = min(distance_to_17, distance_to_18)
        min_distances.append(min_distance)
    return min_distances

def load_action_sequences_from_all_files(folder_path, player_name, start=1, end=50):
    actions_list = []
    for i in range(start, end + 1):
        file_path = os.path.join(folder_path, f'league_results{i}.json')
        if not os.path.exists(file_path):
            print(f"경로 없는 파일: {file_path}")
            continue
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
                for record in data:
                    if record.get('player1') == player_name:
                        actions = [int(a) for a in record.get('actions', [])]
                        actions_list.append(actions)
            except Exception as e:
                print(f"{file_path} 처리 중 오류 발생: {e}")
    return actions_list

def moving_average_with_nan(values, window_size=2):
    result = [np.nan]  # 첫 값은 NaN
    for i in range(1, len(values)):
        window = values[i - 1:i + 1]
        avg = np.mean(window)
        result.append(avg)
    return result

def generate_random_actions(num_sequences=50, max_length=36):
    random_actions_list = []
    for _ in range(num_sequences):
        actions = random.sample(range(36), k=max_length)  # 중복 없이 0~35에서 36개 선택
        random_actions_list.append(actions)
    return random_actions_list

# 설정
players = ['EQRQAC_nmcts400', 'EQRQAC_nmcts100', 'EQRQAC_nmcts50', 'EQRQAC_nmcts10', 'EQRQAC_nmcts2', 'random']
folder_path = 'gamefile'

# 마커 설정
marker_styles = {
    'EQRQAC_nmcts400': ('o', 'b'),  # 파란 원
    'EQRQAC_nmcts100': ('s', 'b'),  # 파란 네모
    'EQRQAC_nmcts50': ('^', 'b'),   # 파란 삼각형
    'EQRQAC_nmcts10': ('v', 'b'),   # 파란 역삼각형
    'EQRQAC_nmcts2': ('D', 'b'),    # 파란 다이아몬드
    'random': ('o', 'g')            # 초록 원
}

plt.figure(figsize=(4, 4))

for player_name in players:
    try:
        if player_name == 'random':
            actions_list = generate_random_actions()
        else:
            actions_list = load_action_sequences_from_all_files(folder_path, player_name)

        min_distance_lists = [calculate_distances(actions) for actions in actions_list]

        if not min_distance_lists:
            print(f"{player_name}: 데이터 없음")
            continue

        max_length = max(len(dist) for dist in min_distance_lists)
        avg_distances = []
        for i in range(max_length):
            values = [dist[i] for dist in min_distance_lists if i < len(dist)]
            avg = np.mean(values)
            avg_distances.append(avg)

        smoothed_avg_distances = moving_average_with_nan(avg_distances)
        x_range = range(len(smoothed_avg_distances))

        marker, color = marker_styles.get(player_name, ('o', 'b'))
                # alpha 설정: nmcts 숫자가 작을수록 더 연하게
        alpha_map = {
            'EQRQAC_nmcts400': 1.0,
            'EQRQAC_nmcts100': 0.8,
            'EQRQAC_nmcts50': 0.65,
            'EQRQAC_nmcts10': 0.5,
            'EQRQAC_nmcts2': 0.35,
            'random': 1.0
        }
        alpha = alpha_map.get(player_name, 1.0)
        plt.plot(x_range, smoothed_avg_distances, marker=marker, linestyle='-', color=color, markersize=4, alpha=alpha, label=player_name)

    except Exception as e:
        print(f'{player_name} 처리 중 오류:', str(e))

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.xticks([0, 10, 20, 30])
plt.yticks([0, 1, 2, 3, 4, 5])
plt.xlabel('Move number')
plt.ylabel('Distance to board center')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()
