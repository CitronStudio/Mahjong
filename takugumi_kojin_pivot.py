import random
import os
import time
import pandas as pd

# ピボットを全行出力する
pd.set_option('display.max_rows', None)

# 実行開始時刻を記録
start_time = time.time()

# 参加者及び試合数を設定。memberは4の倍数にすること
member = 36
game_count = 6

# 全参加者リストを作成
all_players = list(range(1, member + 1))

# 動作確認の為の試行回数カウント
retry_count = 0

def int_to_letter(n):
    if 1 <= n <= 26:
        return chr(ord('A') + n - 1)
    else:
         return chr(ord('A') + round((n - 1) // 26) - 1) + chr(ord('A') + (n - 1) % 26)

def generate_match(players, match_history, excluded_players):
    # 全参加者から、excluded_playersに含まれる者は除く
    players = [p for p in players if p not in excluded_players]
    
    player1 = random.choice(players)
    players.remove(player1)
    
    # 更にplayer1と対戦歴がある者を除く
    players = [p for p in players if p not in match_history[player1]]
    if not players:
        return None
    player2 = random.choice(players)
    players.remove(player2)
    
    # 更にplayer2と対戦歴がある者を除く
    players = [p for p in players if p not in match_history[player2]]
    if not players:
        return None
    player3 = random.choice(players)
    players.remove(player3)
    
    # 更にplayer3と対戦歴がある者を除く
    players = [p for p in players if p not in match_history[player3]]
    if not players:
        return None
    player4 = random.choice(players)
    
    return player1, player2, player3, player4

while True:
    # 各プレイヤーの対戦履歴を記録する辞書
    match_history = {player: set() for player in all_players}
    game_records = []
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{member}人・個人戦(Retry Count : {retry_count})")
    print()
    loop_count = 0
    i = 0
    players = all_players.copy()
    
    while i < game_count:     
        round_output = []
        current_round_matches = []
        excluded_players = set()
        
        for j in range(member // 4):
            table_name = int_to_letter(j + 1)
            table_output = f"第{i + 1}試合\t{table_name}卓"
            
            # 第1試合は、1番卓から番号の小さい順に選手を埋めてゆく
            if i == 0:
                match = tuple(players[0:4])
                players = players[4:]
                
            # 第2試合以降はランダムに埋めてゆく
            else:
                match = generate_match(players, match_history, excluded_players)
                
                # 対戦が成立しない場合、もう一度1番卓から作り直す
                if match is None:
                    loop_count += 1
                    break
            player1, player2, player3, player4 = match
            table_output += f"\t\t{player1}\t{player2}\t{player3}\t{player4}"
            round_output.append(table_output)
            
            # 記録
            game_records.append((i + 1, table_name, player1))
            game_records.append((i + 1, table_name, player2))
            game_records.append((i + 1, table_name, player3))
            game_records.append((i + 1, table_name, player4))
            
            current_round_matches.extend([(player1, player2), (player1, player3), (player1, player4), (player2, player3), (player2, player4), (player3, player4)])
            
            # プレイヤーを使用済みとして除外リストに追加
            excluded_players.update(match)

        else:
            for output in round_output:
                print(output)
            print()
            for match in current_round_matches:
                match_history[match[0]].add(match[1])
                match_history[match[1]].add(match[0])
            loop_count = 0
            i += 1
            players = all_players.copy()
            
        # loop_countが一定数を超えたら、もう一度全て最初からやり直す。loop数は挙動を見ながら変えてもよい
        if loop_count > 500:
            break
            
    # game_count戦目まで作成が成功した場合、プログラムを終了する
    if i == game_count:
        break
        
    retry_count += 1

# 実行終了時刻を記録
end_time = time.time()

# 各プレイヤーの各ゲームごとのテーブルを追跡
player_tables = {}
for game, table, player in game_records:
    if player not in player_tables:
        player_tables[player] = {}
    player_tables[player][f'Game{game}'] = table

# 再ピボット
df_pivot = pd.DataFrame.from_dict(player_tables, orient='index').fillna('')

# プレイヤーを昇順にソート
df_pivot = df_pivot.sort_index()

# ピボットを表示
print(df_pivot)
print()

# 実行時間を計算し、表示
elapsed_time = end_time - start_time
hours, rem = divmod(elapsed_time, 3600)
minutes, seconds = divmod(rem, 60)
print(f"実行時間: {int(hours)}時間{int(minutes):02d}分{seconds:02.0f}秒")
