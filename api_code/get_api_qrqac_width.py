import wandb
import pandas as pd

# Initialize the wandb API
api = wandb.Api()

# Define the run paths and corresponding model names
runs_info = [
    ("hails/gym_4iar_sh2/kkbmgahl", "EQRQAC_nmcts2"),
    ("hails/gym_4iar_sh2/znmzti9n", "EQRQAC_nmcts10"),
    ("hails/gym_4iar_sh2/42y28jtw", "EQRQAC_nmcts50"),
    ("hails/gym_4iar_sh2/m3cks2d9", "EQRQAC_nmcts100"),
    ("hails/gym_4iar_sh2/e5xk5z8p", "EQRQAC_nmcts400"),
]

# Initialize an empty DataFrame to store all data
combined_data = pd.DataFrame()

# Column name to extract
column_name = "resource/depth"

for run_path, model_name in runs_info:
    run = api.run(run_path)
    history = run.history(samples=10000000)

    # Check if the column exists and has data
    if column_name in history.columns and not history[column_name].dropna().empty:
        # Extract the specified column and drop NaN values
        filtered_history = history[[column_name]].dropna()
        filtered_history.columns = [model_name]  # Rename column to model name

        # Combine the data with the main DataFrame
        if combined_data.empty:
            combined_data = filtered_history
        else:
            combined_data = pd.concat([combined_data, filtered_history], axis=1)

# Fill missing values with the last valid value in each column, then fill remaining with 0
combined_data = combined_data.ffill().fillna(0)

# Save the combined data to a single CSV file
combined_data.to_csv("combined_resource_depth.csv", index=False)
