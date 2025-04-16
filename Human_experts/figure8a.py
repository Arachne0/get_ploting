import random
import matplotlib.pyplot as plt
import numpy as np
import os
import json

def get_directions():
    """Return all 4 possible direction vectors for checking."""
    return [(0, 1), (1, 0), (1, 1), (1, -1)]  # Right, Down, Diagonal \, Diagonal /

def index_to_coordinates(index, cols=4):
    """Convert 1D index to 2D coordinates."""
    x = index // cols
    y = index % cols
    return (x, y)

def coordinates_to_index(x, y, cols=4):
    """Convert 2D coordinates to 1D index."""
    return x * cols + y

def is_within_board(x, y, rows=9, cols=4):
    """Check if the position is within the board."""
    return 0 <= x < rows and 0 <= y < cols

def check_threat(board, x, y, color):
    """Check if placing a stone at (x, y) creates a threat."""
    directions = get_directions()
    threat_count = 0

    for dx, dy in directions:
        count = 0
        empty_ends = 0

        # Check in both directions (forward and backward)
        for d in [-1, 1]:
            consecutive = 0
            for step in range(1, 5):  # Check up to 4 in a row
                nx, ny = x + d * step * dx, y + d * step * dy
                if is_within_board(nx, ny):
                    if board[nx][ny] == color:
                        consecutive += 1
                    elif board[nx][ny] == 0:
                        empty_ends += 1
                        break
                    else:
                        break
                else:
                    break

        # Threat conditions
        if consecutive == 3 and empty_ends > 0:
            threat_count += 1

        # Winning move
        if consecutive == 4:
            return -1

    return threat_count

def count_threats(actions, is_black=True):
    """Count the number of threat moves made by the player."""
    board = [[0 for _ in range(4)] for _ in range(9)]
    threat_counts = []

    for i, action in enumerate(actions):
        x, y = index_to_coordinates(action)

        # Skip if the current move does not belong to the current color
        if (is_black and i % 2 == 0) or (not is_black and i % 2 == 1):
            threat_counts.append(0)
            continue

        # Place the stone on the board
        color = 1 if is_black else 2
        board[x][y] = color

        # Check for threats
        threat_count = check_threat(board, x, y, color)
        if threat_count == -1:
            print(f"Game over at step {i + 1}, winning move by {'Black' if is_black else 'White'}")
            break

        # Sum all threats for current state
        current_threat_count = 0
        for row in range(9):
            for col in range(4):
                if board[row][col] == color:
                    current_threat_count += check_threat(board, row, col, color)

        # Append the current threat count
        threat_counts.append(current_threat_count)

    return threat_counts

def smooth(data, window_size):
    """Smooth the data using a simple moving average with NaN padding."""
    smoothed = np.convolve(data, np.ones(window_size) / window_size, mode='valid')
    # Add NaN padding at the beginning to maintain the original length
    padding = [data[0]] * (window_size - 1)
    smoothed = np.concatenate((padding, smoothed))
    return smoothed


def apply_moving_average(data, window):
    return smooth(data, window)


try:
    smoothed_distances = [0.0, 0.0, 0.0, 0.0, 0.4655, 0.447, 0.3919,
                          0.3897, 0.4456, 0.3973, 0.4939, 0.4303, 0.3431,
                          0.3369, 0.2104, 0.2038, 0.2097, 0.1601, 0.1559,
                          0.1282, 0.1247, 0.1177, 0.0849, 0.0995, 0.0974,
                          0.0815, 0.0644, 0.0648, 0.0528, 0.0198, 0.0000,
                          0.0000, 0.0000, 0.0000, 0.0000, 0.0000]
    smoothed_distances = apply_moving_average(smoothed_distances, window=2)


    random_distances = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0919, 0.0897,
                        0.1456, 0.1473, 0.0939, 0.0803, 0.1431, 0.1369,
                        0.1104, 0.1038, 0.2097, 0.0601, 0.0559, 0.0282,
                        0.0247, 0.0177, 0.0000, 0.0000, 0.0000, 0.0000,
                        0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
                        0.0000, 0.0000, 0.0000, 0.0000]

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
    plt.yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
    plt.xlabel('Move number')
    plt.ylabel("Number of threats made")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    # plt.legend()
    plt.show()

except Exception as e:
    print('전체 오류 발생:', str(e))