import random
import console

# 参加者を設定。mは4の倍数にすること
m = 36

# 1チーム当たりのメンバー　=　全参加者 ÷4
team_mem = m // 4

#動作確認の為の試行回数カウント
Rcount = -1

# m人の参加者を作成
players = list(range(1, m + 1))

# 各チームの参加者の番号を定義する
team_a = players[:team_mem]
team_b = players[team_mem:team_mem*2]
team_c = players[team_mem*2:team_mem*3]
team_d = players[team_mem*3:]

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

    console.clear()
    Rcount += 1
    print(f"{m}人・1チーム{team_mem}人(Retry Count : {Rcount})")
    print()

    retry = 0
    i = 0
    while i < 5:
        round_output = []
        round_output.append(f"{i + 1}ゲーム目")

        # チームをリセット
        team_a_copy = team_a.copy()
        team_b_copy = team_b.copy()
        team_c_copy = team_c.copy()
        team_d_copy = team_d.copy()

        current_round_matches = []
        for j in range(team_mem):
            table_output = f" {j + 1}番卓 : "
            match = generate_match(team_a_copy, team_b_copy, team_c_copy, team_d_copy, match_history)
            
            # 対戦カードを作成出来なかった場合
            if match is None:
                retry += 1
                break
            player1, player2, player3, player4 = match
            table_output += f"\t{player1}\t{player2}\t{player3}\t{player4}"
            round_output.append(table_output)
            current_round_matches.extend([(player1, player2), (player1, player3), (player1, player4), (player2, player3), (player2, player4), (player3, player4)])
        else:
            for output in round_output:
                print(output)
            match_history.extend(current_round_matches)
            retry = 0
            i += 1
            
        # リトライが一定数を超えたら、もう一度全て最初からやり直す。リトライ数は挙動を見ながら変えてもよい
        if retry > 100:
            break   
    
    # 5戦目まで作成が成功した場合、プログラムを終了する
    if i == 5:
        break
