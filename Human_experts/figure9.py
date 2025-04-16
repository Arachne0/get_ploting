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

        # If 3 consecutive stones are found in one direction and at least one empty end
        if consecutive == 3 and empty_ends > 0:
            threat_count += 1

    return threat_count

def count_blocked_threats(actions, is_black=True):
    """Count the number of blocked threat moves."""
    board = [[0 for _ in range(4)] for _ in range(9)]
    blocked_counts = []

    for i, action in enumerate(actions):
        x, y = index_to_coordinates(action)

        # Skip if the current move does not belong to the current color
        if (is_black and i % 2 == 0) or (not is_black and i % 2 == 1):
            blocked_counts.append(0)
            continue

        # Place the stone on the board
        color = 1 if is_black else 2
        opponent_color = 2 if is_black else 1

        # Count opponent's threats before placing the stone
        initial_threat_count = 0
        for row in range(9):
            for col in range(4):
                if board[row][col] == opponent_color:
                    initial_threat_count += check_threat(board, row, col, opponent_color)

        # Place the stone
        board[x][y] = color

        # Count opponent's threats after placing the stone
        final_threat_count = 0
        for row in range(9):
            for col in range(4):
                if board[row][col] == opponent_color:
                    final_threat_count += check_threat(board, row, col, opponent_color)

        # Calculate the number of blocked threats
        blocked_count = max(0, initial_threat_count - final_threat_count)
        blocked_counts.append(blocked_count)

    return blocked_counts

def smooth(data, window_size):
    """Smooth the data using a simple moving average with NaN padding."""
    smoothed = np.convolve(data, np.ones(window_size) / window_size, mode='valid')
    # Add NaN padding at the beginning to maintain the original length
    padding = [data[0]] * (window_size - 1)
    smoothed = np.concatenate((padding, smoothed))
    return smoothed

# Generate a random action sequence (length 34) with values between 0 and 35 (9x4 board)
action_sequence = random.sample(range(36), 34)

# Count blocked threats made by the black player
blocked_counts_black = count_blocked_threats(action_sequence, is_black=True)

# Smoothing the blocked threat counts with a window size of 2
window_size = 2
smoothed_counts = smooth(blocked_counts_black, window_size)

# Plotting the blocked threat count over time for black stones
plt.figure(figsize=(8, 5))
plt.plot(range(len(blocked_counts_black)), blocked_counts_black, marker='o', linestyle='-', color='green', label='Original Blocked Threat Count (Black)')
plt.plot(range(len(smoothed_counts)), smoothed_counts, marker='x', linestyle='-', color='red', label=f'Smoothed Blocked Threat Count (window={window_size})')

# Adjusting the plot to have a "¤¤" shape border
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# x-axis settings: show only 0, 10, 20, 30
plt.xticks([0, 10, 20, 30])

# y-axis settings: show only integers (0, 1, 2, 3, ...)
plt.yticks(range(0, int(max(blocked_counts_black)) + 2))

# plt.title("Number of Blocked Threats Over Time (Black)")
plt.xlabel('Move number')
plt.ylabel("Number of threats defended")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend()
plt.show()
