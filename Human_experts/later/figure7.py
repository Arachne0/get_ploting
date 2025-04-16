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

# Generate a random action sequence (length 34) with values between 0 and 35 (9x4 board)
action_sequence = random.sample(range(36), 34)

# Count adjacent own stones over the entire sequence (white stones)
adjacent_counts_white = count_adjacent_stones_over_time(action_sequence, is_black=False)

# Smoothing the adjacent counts with a window size of 2
window_size = 2
smoothed_counts = smooth(adjacent_counts_white, window_size)

# Plotting the adjacent count over time for white stones
plt.figure(figsize=(8, 5))
plt.plot(range(len(adjacent_counts_white)), adjacent_counts_white, marker='o', linestyle='-', color='red', label='Original Adjacent Count (White)')
plt.plot(range(len(smoothed_counts)), smoothed_counts, marker='x', linestyle='-', color='blue', label=f'Smoothed Adjacent Count (window={window_size})')

# Adjusting the plot to have a "¤¤" shape border
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# x-axis settings: show only 0, 10, 20, 30
plt.xticks([0, 10, 20, 30])

# y-axis settings: show only integers (0, 1, 2, 3, ...)
plt.yticks(range(0, int(max(adjacent_counts_white)) + 2))

# plt.title("Number of Adjacent Own Stones Over Time (White)")
plt.xlabel('Move number')
plt.ylabel("Number of opponent's neighbors")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend()
plt.show()
