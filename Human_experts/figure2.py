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

def calculate_pairwise_distances(action_vector):
    """Calculate distances between pairs of actions (0-2, 1-3, 2-4, ...)."""
    distances = [0, 0]  # The first two indices have no previous pair, so distance is 0

    for i in range(2, len(action_vector)):
        pos1 = index_to_coordinates(action_vector[i - 2])
        pos2 = index_to_coordinates(action_vector[i])
        distance = calculate_distance(pos1, pos2)
        distances.append(distance)

    return distances

def smooth(data, window_size):
    """Smooth the data using a simple moving average with NaN padding to maintain the initial value."""
    smoothed = np.convolve(data, np.ones(window_size)/window_size, mode='valid')
    # Add NaN padding at the beginning to maintain the original length
    padding = [data[0]] * (window_size - 1)
    smoothed = np.concatenate((padding, smoothed))
    return smoothed

if __name__ == '__main__':
    # Generate a random action sequence of length 34
    action_sequence = random.sample(range(36), 34)

    # Calculate pairwise distances (0-2, 1-3, 2-4, ...)
    distances = calculate_pairwise_distances(action_sequence)

    # Smoothing the distances with a window size of 2
    window_size = 2
    smoothed_distances = smooth(distances, window_size)

    # Plot the original and smoothed distances
    plt.figure(figsize=(8, 4))
    plt.plot(range(len(distances)), distances, marker='o', linestyle='-', color='b', label='Original Distance')
    plt.plot(range(len(smoothed_distances)), smoothed_distances, marker='x', linestyle='-', color='r', label=f'Smoothed Distance (window={window_size})')

    # Adjusting the plot to have a "¤¤" shape border
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # x-axis settings: show only 0, 10, 20, 30
    plt.xticks([0, 10, 20, 30])

    # y-axis settings: show only integers (0, 1, 2, 3, ...)
    plt.yticks(range(0, int(max(distances)) + 2))

    # plt.title('Pairwise Distances between Stones (0-2, 1-3, 2-4, ...)')
    plt.xlabel('Move number')
    plt.ylabel('Distance to own pieces')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    plt.show()
