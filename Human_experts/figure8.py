import random
import matplotlib.pyplot as plt
import numpy as np

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

# Generate a random action sequence (length 34) with values between 0 and 35 (9x4 board)
action_sequence = random.sample(range(36), 34)

# Count threats made by the black player
threat_counts_black = count_threats(action_sequence, is_black=True)

# Smoothing the threat counts with a window size of 2
window_size = 2
smoothed_counts = smooth(threat_counts_black, window_size)

# Plotting the threat count over time for black stones
plt.figure(figsize=(8, 5))
plt.plot(range(len(threat_counts_black)), threat_counts_black, marker='o', linestyle='-', color='blue', label='Original Threat Count (Black)')
plt.plot(range(len(smoothed_counts)), smoothed_counts, marker='x', linestyle='-', color='red', label=f'Smoothed Threat Count (window={window_size})')

# Adjusting the plot to have a "¤¤" shape border
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# x-axis settings: show only 0, 10, 20, 30
plt.xticks([0, 10, 20, 30])

# y-axis settings: show only integers (0, 1, 2, 3, ...)
plt.yticks(range(0, int(max(threat_counts_black)) + 2))

# plt.title("Number of Threats Over Time (Black)")
plt.xlabel('Move number')
plt.ylabel("Number of threats made")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend()
plt.show()
