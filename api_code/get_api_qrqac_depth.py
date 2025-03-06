import wandb
import pandas as pd

api = wandb.Api()

runs_info = [
    # ("hails/gym_4iar_sh2/kcc396eh", "QRQAC_nmcts2_quantiles3.csv"),
    # ("hails/gym_4iar_sh2/98wuregn", "QRQAC_nmcts2_quantiles9.csv"),
    # ("hails/gym_4iar_sh2/9ev08f72", "QRQAC_nmcts2_quantiles27.csv"),
    # ("hails/gym_4iar_sh2/plw69861", "QRQAC_nmcts2_quantiles81.csv"),
    # ("hails/gym_4iar_sh2/nxrr7r2b", "QRQAC_nmcts10_quantiles3.csv"),
    # ("hails/gym_4iar_sh2/og1a3a1n", "QRQAC_nmcts10_quantiles9.csv"),
    # ("hails/gym_4iar_sh2/r16pg6cl", "QRQAC_nmcts10_quantiles27.csv"),
    # ("hails/gym_4iar_sh2/ngw2lja5", "QRQAC_nmcts10_quantiles81.csv"),
    # ("hails/gym_4iar_sh2/v3uslmvf", "QRQAC_nmcts50_quantiles3.csv"),
    # ("hails/gym_4iar_sh2/22qmu3s9", "QRQAC_nmcts50_quantiles9.csv"),
    # ("hails/gym_4iar_sh2/tn49czn5", "QRQAC_nmcts50_quantiles27.csv"),
    # ("hails/gym_4iar_sh2/q6z1qy6j", "QRQAC_nmcts50_quantiles81.csv"),
    # ("hails/gym_4iar_sh2/0icc3vkp", "QRQAC_nmcts100_quantiles3.csv"),
    # ("hails/gym_4iar_sh2/7izyyz4o", "QRQAC_nmcts100_quantiles9.csv"),
    # ("hails/gym_4iar_sh2/earclbay", "QRQAC_nmcts100_quantiles27.csv"),
    # ("hails/gym_4iar_sh2/36vpk2uc", "QRQAC_nmcts100_quantiles81.csv"),
    # ("hails/gym_4iar_sh2/2tq9qh02", "QRQAC_nmcts400_quantiles3.csv"),
    # ("hails/gym_4iar_sh2/vaf24xlt", "QRQAC_nmcts400_quantiles9.csv"),
    # ("hails/gym_4iar_sh2/yo1kxju0", "QRQAC_nmcts400_quantiles27.csv"),
    # ("hails/gym_4iar_sh2/dp63mjgg", "QRQAC_nmcts400_quantiles81.csv"),
    ("hails/gym_4iar_sh2/kkbmgahl", "EQRQAC_nmcts2.csv"),
    ("hails/gym_4iar_sh2/znmzti9n", "EQRQAC_nmcts10.csv"),
    ("hails/gym_4iar_sh2/42y28jtw", "EQRQAC_nmcts50.csv"),
    ("hails/gym_4iar_sh2/m3cks2d9", "EQRQAC_nmcts100.csv"),
    ("hails/gym_4iar_sh2/e5xk5z8p", "EQRQAC_nmcts400.csv"),
]

for run_path, csv_name in runs_info:
    run = api.run(run_path)
    history = run.history(samples=10000000)

    # Filter to keep only the specified column
    column_name = "depth_fre_game_iter_100"
    if column_name in history.columns:
        filtered_history = history[[column_name]].dropna()  # Keep only the column and drop NaN rows
        filtered_history.to_csv(csv_name, index=False)

