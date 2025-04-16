import random
import matplotlib.pyplot as plt
import numpy as np
import os
import json

def get_neighbors(x, y):
    """Return the coordinates of 8 possible neighbors."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),  # Horizontal and vertical
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonal
    neighbors = [(x + dx, y + dy) for dx, dy in directions]
    # Filter neighbors that are within the board (9x4)
    return [(nx, ny) for nx, ny in neighbors if 0 <= nx < 9 and 0 <= ny < 4]

def coordinates_to_index(x, y, cols=4):
    """Convert 2D coordinates to 1D index."""
    return x * cols + y

def index_to_coordinates(index, cols=4):
    """Convert 1D index to 2D coordinates."""
    x = index // cols
    y = index % cols
    return (x, y)

def count_adjacent_stones_over_time(actions, is_black=True):
    """Count adjacent own stones for each step in the action sequence."""
    adjacent_counts = []

    for current_index in range(len(actions)):
        # Determine odd or even indices based on stone color
        if is_black:
            own_actions = [actions[i] for i in range(current_index + 1) if i % 2 == 1]
        else:
            own_actions = [actions[i] for i in range(current_index + 1) if i % 2 == 0]

        # Current action to evaluate
        current_action = actions[current_index]

        # Current stone coordinates
        current_pos = index_to_coordinates(current_action)

        # Get neighbors
        neighbors = get_neighbors(*current_pos)

        # Count own stones among neighbors
        count = 0
        for neighbor in neighbors:
            neighbor_index = coordinates_to_index(*neighbor)
            if neighbor_index in own_actions:
                count += 1

        # Append the current adjacent count
        adjacent_counts.append(count)

    return adjacent_counts

def smooth(data, window_size):
    """Smooth the data using a simple moving average with NaN padding to maintain the initial value."""
    smoothed = np.convolve(data, np.ones(window_size) / window_size, mode='valid')
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
    # actions_list = load_action_sequences_from_files(folder_path, player_name)
    # distance_lists = [count_adjacent_stones_over_time(actions) for actions in actions_list]

    # if actions_list:
    #     avg_distances = compute_average_distance(distance_lists)
    #     smoothed_distances = apply_moving_average(avg_distances, window=2)
    # else:
    #     smoothed_distances = []


    smoothed_distances = [0.0, 0.1156, 0.188, 0.2655, 0.347,
 0.4319, 0.5197, 0.61, 0.7026, 0.7973, 0.8939, 0.9303, 0.9688, 1.0431, 1.1169, 1.1904,
 1.2638, 1.337, 1.4101, 1.4831, 1.5559, 1.6282, 1.7, 1.771,
 1.8409, 1.9095, 1.9764, 2.0415, 2.1044, 2.1648, 2.2226, 2.2774,
 2.3287, 2.3761, 2.4183, 2.45]
    smoothed_distances = apply_moving_average(smoothed_distances, window=2)

    random_distances = [0.0, 0.012, 0.0293, 0.0505, 0.0748, 0.1015, 0.1303, 0.161, 0.1935,
 0.228, 0.2647, 0.3042, 0.3468, 0.3931, 0.4436, 0.4988, 0.559,
 0.6245, 0.6953, 0.7716, 0.853, 0.9393, 1.03, 1.1245, 1.2223,
 1.3227, 1.4253, 1.5294, 1.6346, 1.7408, 1.8477, 1.9555, 2.0642,
 2.1742, 2.286, 2.4]
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
    plt.yticks([0,0.5,1.0,1.5,2.0,2.5])
    plt.xlabel('Move number')
    plt.ylabel("Number of own neighbors")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    # plt.legend()
    plt.show()

except Exception as e:
    print('전체 오류 발생:', str(e))
