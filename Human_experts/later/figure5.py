
import random
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

def calculate_distances_from_fixed_center(actions, is_black=True):
    """Calculate distances of stones from the fixed center (17 or 18)."""
    # Determine odd or even indices based on the stone color (black or white)
    if is_black:
        # Get only odd-indexed actions (black stones)
        own_actions = [actions[i] for i in range(len(actions)) if i % 2 == 1]
    else:
        # Get only even-indexed actions (white stones)
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

# Generate a random action sequence (length 34) with values between 0 and 35 (9x4 board)
action_sequence = random.sample(range(36), 34)

# Calculate distances for white stones only
distances_white = calculate_distances_from_fixed_center(action_sequence, is_black=False)

# Smoothing the distances with a window size of 2
window_size = 2
smoothed_distances = smooth(distances_white, window_size)

# Plotting the distances for white stones
plt.figure(figsize=(8, 5))
plt.plot(range(len(distances_white)), distances_white, marker='o', linestyle='-', label='Original Distance (White)', color='red')
plt.plot(range(len(smoothed_distances)), smoothed_distances, marker='x', linestyle='-', color='blue', label=f'Smoothed Distance (window={window_size})')

# Adjusting the plot to have a "¤¤" shape border
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# x-axis settings: show only 0, 5, 10, 15
plt.xticks([0, 5, 10, 15])

# y-axis settings: show only integers (0, 1, 2, 3, ...)
plt.yticks(range(0, int(max(distances_white)) + 2))

# plt.title("Distances of White Stones from Fixed Center (17 or 18)")
plt.xlabel('Move number')
plt.ylabel("Distance to opponent's center of mass")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend()
plt.show()
