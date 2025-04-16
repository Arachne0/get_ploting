# json 파일의 인덱스 수정

import json
import os

for i in range(2, 51):  # 2부터 50까지 반복
    input_path = f"gamefile/league_results{i}.json"
    output_path = f"gamefile/league_results{i}.json"

    # 파일이 실제로 존재하는지 확인 (오류 방지)
    if not os.path.exists(input_path):
        print(f"파일이 존재하지 않음: {input_path}")
        continue

    with open(input_path, "r") as f:
        data = json.load(f)

    count_10 = 0
    count_18 = 0

    for game in data:
        if game["player1"] == "EQRQAC_nmcts400":
            actions = game["actions"]

            count_10 += actions.count("10")
            count_18 += actions.count("18")

            if "18" in actions:
                if "10" in actions:
                    idx_10 = actions.index("10")
                    idx_18 = actions.index("18")
                    actions[idx_10], actions[idx_18] = actions[idx_18], actions[idx_10]
                    game["actions"] = actions
            else:
                actions = ["18" if a == "10" else a for a in actions]
                game["actions"] = actions

    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[{input_path}] 처리 완료 - '10': {count_10}회, '18': {count_18}회 → 저장: {output_path}")
