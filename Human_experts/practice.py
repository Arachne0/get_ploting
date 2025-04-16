# 게임 파일 50개중에서 한 플레이어가 몇번 나오는지 & 그 플레이어의 action은 몇개인지

import json

player_name = 'EQRQAC_nmcts400'
game_count = 0
action_count = 0

try:
    for i in range(1, 51):
        file_path = f'gamefile/league_results{i}.json'
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for record in data:
                    if record.get('player1') == player_name:
                        actions = record.get('actions', [])
                        action_count += len(actions)
                        game_count += 1
        except FileNotFoundError:
            print(f'File not found: {file_path}')
            continue
    print(f'Total games for player {player_name}:', game_count)
    print(f'Total actions for player {player_name}:', action_count)
except Exception as e:
    print('Error:', str(e))