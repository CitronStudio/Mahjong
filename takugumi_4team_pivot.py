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
game_count = 5

# 1チーム当たりのメンバー　=　全参加者 ÷4
team_mem = member // 4

# 動作確認の為の試行回数カウント
retry_count = 0

# m人の参加者を作成
players = list(range(1, member + 1))

# 各チームの参加者の番号を定義する
team_a = players[:team_mem]
team_b = players[team_mem:team_mem*2]
team_c = players[team_mem*2:team_mem*3]
team_d = players[team_mem*3:]

def int_to_letter(n):
    if 1 <= n <= 26:
        return chr(ord('A') + n - 1)
    else:
        return chr(ord('A') + round((n - 1) // 26) - 1) + chr(ord('A') + (n - 1) % 26)

def generate_match(team1, team2, team3, team4, match_history): 
    # team1から一人選ぶ
    player1 = random.choice(team1)
    
    # team2から一人選ぶ。但しteam1と対戦済みの選手は除く
    available_team2 = [p for p in team2 if (player1, p) not in match_history]
    if not available_team2:
        return None
    player2 = random.choice(available_team2)
    
    # team3から一人選ぶ。但しteam1、2と対戦済みの選手は除く
    available_team3 = [p for p in team3 if (player1, p) not in match_history and (player2, p) not in match_history]
    if not available_team3:
        return None
    player3 = random.choice(available_team3)
    
    # team4から一人選ぶ。但しteam1、2、3と対戦済みの選手は除く
    available_team4 = [p for p in team4 if (player1, p) not in match_history and (player2, p) not in match_history and (player3, p) not in match_history]
    if not available_team4:
        return None
    player4 = random.choice(available_team4)

    team1.remove(player1)
    team2.remove(player2)
    team3.remove(player3)
    team4.remove(player4)

    return player1, player2, player3, player4

while True:
    # 対戦履歴を記録するリスト
    match_history = []
    game_records = []

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{member}人・1チーム{team_mem}人(Retry Count : {retry_count})")
    print()

    loop_count = 0
    i = 0
    
    while i < game_count:   
        # チームをリセット
        team_a_copy = team_a.copy()
        team_b_copy = team_b.copy()
        team_c_copy = team_c.copy()
        team_d_copy = team_d.copy()
        
        round_output = []
        current_round_matches = []
        for j in range(team_mem):
            table_name = int_to_letter(j + 1)
            table_output = f"第{i + 1}試合\t{table_name}卓"
            match = generate_match(team_a_copy, team_b_copy, team_c_copy, team_d_copy, match_history)
            
            # 対戦カードを作成出来なかった場合
            if match is None:
                loop_count += 1
                break
            player1, player2, player3, player4 = match
            table_output += f"\t\t{player1}\t{player2}\t{player3}\t{player4}"
            round_output.append(table_output)
            game_records.append((i + 1, table_name, player1))
            game_records.append((i + 1, table_name, player2))
            game_records.append((i + 1, table_name, player3))
            game_records.append((i + 1, table_name, player4))
            current_round_matches.extend([(player1, player2), (player1, player3), (player1, player4), (player2, player3), (player2, player4), (player3, player4)])
        else:
            for output in round_output:
                print(output)
            print()
            match_history.extend(current_round_matches)
            loop_count = 0
            i += 1
            
        # リトライが一定数を超えたら、もう一度全て最初からやり直す。リトライ数は挙動を見ながら変えてもよい
        if loop_count > 100:
            break   
    
    # 5戦目まで作成が成功した場合、プログラムを終了する
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
print()
