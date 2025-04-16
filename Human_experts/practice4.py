import json
import os

# 폴더 경로
folder = "gamefile"

# 반복 처리 (1번부터 50번까지)
for i in range(1, 51):
    input_filename = f"league_results{i}.json"
    output_filename = f"league_results{i}.json"

    input_filepath = os.path.join(folder, input_filename)
    output_filepath = os.path.join(folder, output_filename)

    try:
        # 파일 열기
        with open(input_filepath, 'r') as f:
            data_list = json.load(f)

        # 각 게임 데이터 처리
        for data in data_list:
            # 1. player1 변경
            data["player1"] = "EQRQAC_nmcts400"

            # 2. actions에서 18, 17, 15 순서로 정렬
            actions = data.get("actions", [])

            # 관심 있는 액션들
            priority_actions = ["18", "17", "15"]
            # 우선순위 액션들을 따로 모으고 나머지는 기존 순서 유지
            priority_part = [a for a in priority_actions if a in actions]
            remaining_part = [a for a in actions if a not in priority_part]

            # 새롭게 정렬된 actions
            data["actions"] = priority_part + remaining_part

        # 수정된 결과 저장
        with open(output_filepath, 'w') as f:
            json.dump(data_list, f, indent=4)

        print(f"[완료] {input_filename} → {output_filename}")

    except Exception as e:
        print(f"[오류] {input_filename}: {e}")
