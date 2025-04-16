# 게임 파일에서 actions 리스트 중 조건에 만족하는 action 찾기

import json

# JSON 파일 열기
with open("gamefile/league_results1.json", "r") as f:
    data = json.load(f)

# 조건을 만족하는 actions 리스트 중 10과 18의 등장 횟수 세기
count_10 = 0
count_18 = 0

for game in data:
    if game["player1"] == "EQRQAC_nmcts400":
        count_10 += game["actions"].count("10")
        count_18 += game["actions"].count("18")

print(f'"10"의 등장 횟수: {count_10}')
print(f'"18"의 등장 횟수: {count_18}')
