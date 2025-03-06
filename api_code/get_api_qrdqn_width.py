import wandb
import pandas as pd

api = wandb.Api()

runs_info = [
    # ("hails/gym_4iar_sh2/u0xp5toe", "QRDQN_nmcts2_quantiles3.csv"),
    # ("hails/gym_4iar_sh2/i1eed1ki", "QRDQN_nmcts2_quantiles9.csv"),
    # ("hails/gym_4iar_sh2/tq3tt1hp", "QRDQN_nmcts2_quantiles27.csv"),
    # ("hails/gym_4iar_sh2/6yko9uro", "QRDQN_nmcts2_quantiles81.csv"),
    # ("hails/gym_4iar_sh2/tum6os8p", "QRDQN_nmcts10_quantiles3.csv"),
    # ("hails/gym_4iar_sh2/gkgyvhj5", "QRDQN_nmcts10_quantiles9.csv"),
    # ("hails/gym_4iar_sh2/shwq4mx4", "QRDQN_nmcts10_quantiles27.csv"),
    # ("hails/gym_4iar_sh2/l97oiy2h", "QRDQN_nmcts10_quantiles81.csv"),
    # ("hails/gym_4iar_sh2/4gpa4y3e", "QRDQN_nmcts50_quantiles3.csv"),
    # ("hails/gym_4iar_sh2/hmkjwase", "QRDQN_nmcts50_quantiles9.csv"),
    # ("hails/gym_4iar_sh2/o9fiz8de", "QRDQN_nmcts50_quantiles27.csv"),
    # ("hails/gym_4iar_sh2/ec05rpsi", "QRDQN_nmcts50_quantiles81.csv"),
    # ("hails/gym_4iar_sh2/hznekwam", "QRDQN_nmcts100_quantiles3.csv"),
    # ("hails/gym_4iar_sh2/zkaa66mq", "QRDQN_nmcts100_quantiles9.csv"),
    # ("hails/gym_4iar_sh2/nn2j4qu0", "QRDQN_nmcts100_quantiles27.csv"),
    # ("hails/gym_4iar_sh2/zkp2matb", "QRDQN_nmcts100_quantiles81.csv"),
    # ("hails/gym_4iar_sh2/8tza4yau", "QRDQN_nmcts400_quantiles3.csv"),
    # ("hails/gym_4iar_sh2/oiggnafx", "QRDQN_nmcts400_quantiles9.csv"),
    # ("hails/gym_4iar_sh2/obpapfle", "QRDQN_nmcts400_quantiles27.csv"),
    # ("hails/gym_4iar_sh2/gp2twehd", "QRDQN_nmcts400_quantiles81.csv"),
    ("hails/gym_4iar_sh2/olagzb8p", "EQRDQN_nmcts2.csv"),
    ("hails/gym_4iar_sh2/v0o9xl2v", "EQRDQN_nmcts10.csv"),
    ("hails/gym_4iar_sh2/l6b3z7mf", "EQRDQN_nmcts50.csv"),
    ("hails/gym_4iar_sh2/1ddrjlwg", "EQRDQN_nmcts100.csv"),
    ("hails/gym_4iar_sh2/ezyw0q6a", "EQRDQN_nmcts400.csv"),
]

for run_path, csv_name in runs_info:
    run = api.run(run_path)
    history = run.history(samples=10000000)

    # Filter to keep only the specified column
    column_name = "resource/depth"
    if column_name in history.columns:
        filtered_history = history[[column_name]].dropna()  # Keep only the column and drop NaN rows
        filtered_history.to_csv(csv_name, index=False)

