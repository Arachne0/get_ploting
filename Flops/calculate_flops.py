import numpy as np
import csv

import pandas as pd
ncmtss = [2, 10, 50, 100, 400]
# 3 9 27 81
for nmcts in ncmtss:
    # QR-QAC
    models_flops = [32256, 59904, 142848, 391680]  # critic 의 flops for different quantile number
    models_depth = np.random.randint(0,12,size=(400,5))  # QRQAC with 4 qunaitles + EQRQAC = 5 models

    # file_path = "Planning_depth.xlsx"
    # sheet_name = "Sheet1"  # 엑셀 시트 이름
    # data = pd.read_excel(file_path, sheet_name=sheet_name)
    # models_depth = data.values

    # models_depth = "/Planning_depth.xlsx"
    models_width = np.random.choice([3,9,27,81], size=(400,)) # EQRQAC's width
    model1, model2, model3, model4, model5 = 0, 0, 0, 0, 0

    eqrqac_depth = models_depth[:, :5]
    qrqac_depth = models_depth[:, 5:]

    models_flops_qrqac = [32256, 142848, 142848, 391680, 391680]
    models_flops_eqrqac = [32256, 142848, 142848, 391680, 391680]
    #
    qrqac_results = [0] * 5  # QRQAC 결과 저장
    eqrqac_results = [0] * 5  # EQRQAC 결과 저장

    for i in range(len(qrqac_depth)):
        for j in range(5):
            qrqac_results[j] += qrqac_depth[i, j] * models_flops_qrqac[j]
            if qrqac_depth.shape[0] < 5:
                break

        print(qrqac_results)

    for i in range(len(eqrqac_depth)):
        for j in range(5):
            eqrqac_results[j] += eqrqac_depth[i, j] * models_flops_eqrqac[j]
            if eqrqac_depth.shape[0] < 5:
                break
        print(eqrqac_results)

    # our model
    flops_our = 0
    for i in range(len(models_width)):
        if models_width[i] == 3:
            flops_our += models_depth[i,-1] * models_flops[0]
        elif models_width[i] == 9:
            flops_our += models_depth[i, -1] * models_flops[1]
        elif models_width[i] == 27:
            flops_our += models_depth[i, -1] * models_flops[2]
        elif models_width[i] == 81:
            flops_our += models_depth[i, -1] * models_flops[3]
        else:
            print('wtf')
    print(flops_our)



    # for i in range(0, len(models_depth), 5):  # 5개씩 묶기
    #     chunk = models_depth[i:i + 5, :]  # 5개의 행 추출
    #     if chunk.shape[0] < 5:  # 마지막 묶음이 5개보다 작으면 무시
    #         break
    #
    #     for row in chunk:
    #         # 각 모델의 FLOPs 계산
    #         model1 += row[0] * models_flops[0]  # 첫 번째 모델
    #         model2 += row[1] * models_flops[1]  # 두 번째 모델
    #         model3 += row[2] * models_flops[2]  # 세 번째 모델
    #         model4 += row[3] * models_flops[3]  # 네 번째 모델
    #         model5 += row[4] * models_flops[3]  # 다섯 번째 모델
    #
    #
    # print (model1,model2,model3,model4,model5)
    # for i in range(len(models_depth)): # 1~400
    #     ## other models flops
    #     model1 += models_depth[i, 0] * models_flops[0]  # (400,)
    #     model2 += models_depth[i, 0] * models_flops[2]
    #     model3 += models_depth[i, 0] * models_flops[2]
    #     model4 += models_depth[i, 0] * models_flops[3]
    #     model5 += models_depth[i, 0] * models_flops[3]
    #
    # print(model1, model2, model3, model4, model5)
    #
    # ## our model
    # flops_our = 0
    # for i in range(len(models_width)):
    #     if models_width[i] == 3:
    #         flops_our += models_depth[i,-1] * models_flops[0]
    #     elif models_width[i] == 9:
    #         flops_our += models_depth[i, -1] * models_flops[1]
    #     elif models_width[i] == 27:
    #         flops_our += models_depth[i, -1] * models_flops[2]
    #     elif models_width[i] == 81:
    #         flops_our += models_depth[i, -1] * models_flops[3]
    #     else:
    #         print('wtf')
    #
    # output_file = "model_flops_results.csv"
    #
    # with open(output_file, mode='w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(["Model1", "Model2", "Model3", "Model4", "Model5", "Flops_Our"])
    #     writer.writerow([model1, model2, model3, model4, model5, flops_our])
    #
    #
