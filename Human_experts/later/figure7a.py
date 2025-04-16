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
        # Determine own actions based on stone color
        if is_black:
            own_actions = [actions[i] for i in range(current_index + 1) if i % 2 == 1]
        else:
            own_actions = [actions[i] for i in range(current_index + 1) if i % 2 == 0]

        # Current action to evaluate
        current_action = actions[current_index]

        # Check if the current action belongs to the correct color
        if (is_black and current_index % 2 == 0) or (not is_black and current_index % 2 == 1):
            # Skip if current action does not belong to the specified color
            adjacent_counts.append(0)
            continue

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

def apply_moving_average(data, window):
    return smooth(data, window)

try:
    smoothed_distances = [0.0,  0.188, 0.2655, 0.347,
                          0.4319, 0.5897, 0.6456, 0.7973, 0.8939, 0.9303, 1.0431, 1.1369, 1.2104,
                          1.3038, 1.397, 1.4601, 1.5559, 1.6282, 1.7, 1.771,
                          1.8409, 1.9095, 1.9764, 2.0415, 2.1044, 2.1648, 2.1825,2.1981,2.2126, 2.2774, 2.3131,
                          2.3587, 2.4161,2.4683,2.4983,  2.55]
    smoothed_distances = apply_moving_average(smoothed_distances, window=2)

    random_distances = [0.0, 0.0238, 0.0653, 0.1195, 0.1828, 0.2523, 0.326, 0.4024, 0.4805,
 0.5596, 0.6392, 0.7192, 0.7993, 0.8794, 0.9595, 1.0397, 1.1198, 1.2,
 1.2802, 1.3603, 1.4405, 1.5206, 1.6007, 1.6808, 1.7608, 1.8404, 1.8789,
 1.9195, 1.9976, 2.074, 2.1477, 2.2172, 2.2805, 2.3347, 2.3762,
 2.4, ]

    random_smoothed = apply_moving_average(random_distances, window=2)

    plt.figure(figsize=(4, 4))
    if len(smoothed_distances) > 0:
        plt.plot(range(35), smoothed_distances[:35], marker='o', linestyle='-', color='b', markersize=4,
                 label='EQRQAC_nmcts400')

    # plt.plot(range(35), random_smoothed[:35], marker='o', linestyle='-', color='g', markersize=4, label='random')
    plt.plot(range(35), random_smoothed[:35], linestyle='--', color='g', label='random')

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.xticks([0, 10, 20, 30])
    plt.yticks([0, 0.5, 1.0, 1.5, 2.0, 2.5])
    plt.xlabel('Move number')
    plt.ylabel("Number of opponent's neighbors")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    # plt.legend()
    plt.show()

except Exception as e:
    print('전체 오류 발생:', str(e))