import numpy as np
import pandas as pd
import csv

ncmtss = [2, 10, 50, 100, 400]

file_path1 = '../QRQAC/csv_files/QRQAC_planning_depths.xlsx'
data1 = pd.ExcelFile(file_path1)
sheet_data1 = data1.parse('Sheet1')
columns1 = sheet_data1.columns

groups = ['nmcts2', 'nmcts10', 'nmcts50', 'nmcts100', 'nmcts400']

# Reorganize the columns based on group and specified quantile order
ordered_columns = []
for group in groups:
    ordered_columns.extend([
        f'QRQAC_{group}_quantiles3',
        f'QRQAC_{group}_quantiles9',
        f'QRQAC_{group}_quantiles27',
        f'QRQAC_{group}_quantiles81',
        f'EQRQAC_{group}'
    ])

grouped_data = sheet_data1[ordered_columns].to_numpy()
nmcts_groups = [
    grouped_data[:, i:i + 5] for i in range(0, 25, 5)
]

file_path2 = '../QRQAC/csv_files/QRQAC_num_of_quantiles2.xlsx'
data2 = pd.ExcelFile(file_path2)
sheet_data2 = data2.parse('Sheet1')

eqrqac_columns = [col for col in sheet_data2.columns if col.startswith('EQRQAC')]
eqrqac = sheet_data2[eqrqac_columns].to_numpy()

# Models flops for different quantile numbers
models_flops = [20736, 34560, 76032, 200448]

output_file_path = 'QRQAC_flops_results.csv'
header = ['step', 'nmcts', 'quantile3_flops', 'quantile9_flops', 'quantile27_flops', 'quantile81_flops',
          'our_model_flops']
results = []

for nmcts, nmcts_group, width in zip(ncmtss, nmcts_groups, eqrqac.T):
    model1, model2, model3, model4 = 0, 0, 0, 0
    flops_our = 0

    for i in range(len(nmcts_group)):  # 1~400
        # Cumulative flops for QRQAC models
        model1 += nmcts_group[i, 0] * models_flops[0]
        model2 += nmcts_group[i, 0] * models_flops[1]
        model3 += nmcts_group[i, 0] * models_flops[2]
        model4 += nmcts_group[i, 0] * models_flops[3]

        # Cumulative flops for
        # our model
        if width[i] == 3:
            flops_our += nmcts_group[i, -1] * models_flops[0]
        elif width[i] == 9:
            flops_our += nmcts_group[i, -1] * models_flops[1]
        elif width[i] == 27:
            flops_our += nmcts_group[i, -1] * models_flops[2]
        elif width[i] == 81:
            flops_our += nmcts_group[i, -1] * models_flops[3]
        else:
            print(f'Unexpected width value: {width[i]}')

        results.append([i + 1, nmcts, model1, model2, model3, model4, flops_our])

# Save results to a single CSV file
with open(output_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(results)

print(f'Saved cumulative flops data to {output_file_path}')
