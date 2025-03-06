import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the provided Excel file
file_path = "ploting/csv_files/QRDQN/QRDQN_num_of_quantile.xlsx"
df = pd.read_excel(file_path)

# Define MCTS labels
nmcts_labels = ["nmcts2", "nmcts10", "nmcts50", "nmcts100", "nmcts400"]

# Extract time series data for EQRDQN
time_series_length = len(df)  # Number of time steps
time_steps = np.arange(time_series_length)  # Create time indices
eqrqac_series = {label: df[f"EQRDQN_{label}"].values for label in nmcts_labels}

# Apply moving average for smoothing
window_size = 100
smoothed_eqrqac_series = {label: np.convolve(values, np.ones(window_size) / window_size, mode='valid')
                          for label, values in eqrqac_series.items()}

# Adjust time steps to match the smoothed data
smoothed_time_steps = np.arange(len(smoothed_eqrqac_series["nmcts2"]))

# Plot the smoothed time series data
fig, ax = plt.subplots(figsize=(7, 6))

# Define alpha values (lower alpha for better overlapping effect)
alpha_values = np.linspace(0.3, 0.9, len(nmcts_labels))  # Keep slightly different opacity

for label, alpha in zip(nmcts_labels, alpha_values):
    ax.plot(smoothed_time_steps, smoothed_eqrqac_series[label], label=f"EQR-DQN ({label})",
            linestyle='-', color='blue', alpha=0.7, linewidth=1.2)  # Reduce linewidth for tighter spacing

ax.set_xlabel("Time Step", fontsize=16)
ax.set_ylabel("Number of Quantiles", fontsize=16)
ax.tick_params(axis='both', labelsize=16)

# Set y-axis ticks to 3, 9, 27, 81
ax.set_yticks([3, 9, 27, 81])

# Remove vertical grid lines but keep horizontal ones
ax.yaxis.grid(True, linestyle='--', alpha=0.5)  # Reduce grid opacity
ax.xaxis.grid(False)

# Remove top and right spines
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Move legend inside the graph, lower right position
ax.legend(loc="lower right", fontsize=14, fancybox=True, edgecolor='black')

# Reduce spacing between subplots (if needed)
plt.tight_layout()

plt.show()
