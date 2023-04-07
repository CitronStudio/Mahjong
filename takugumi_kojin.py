import random
import console

# 参加者及び試合数を設定。mは4の倍数にすること
member = 28
game_count = 6

# m人の参加者を作成
all_players = list(range(1, member + 1))

# 動作確認の為の試行回数カウント
retry_count = -1

def generate_match(players, match_history, excluded_players):
    players = [p for p in players if p not in excluded_players]
    
    player1 = random.choice(players)
    players.remove(player1)

    players = [p for p in players if p not in match_history[player1]]
    if not players:
        return None
    player2 = random.choice(players)
    players.remove(player2)

    players = [p for p in players if p not in match_history[player1] and p not in match_history[player2]]
    if not players:
        return None
    player3 = random.choice(players)
    players.remove(player3)

    players = [p for p in players if p not in match_history[player1] and p not in match_history[player2] and p not in match_history[player3]]
    if not players:
        return None
    player4 = random.choice(players)
    players.remove(player4)

    return player1, player2, player3, player4

while True:
    # 各プレイヤーの対戦履歴を記録する辞書
    match_history = {player: set() for player in all_players}
    
    console.clear()
    retry_count += 1
    print(f"{member}人・個人戦(Retry Count : {retry_count})")
    print()
    loop_count = 0
    i = 0
    players = all_players.copy()
    
    while i < game_count:     
        round_output = []
        round_output.append(f"{i + 1}ゲーム目")
        current_round_matches = []
        excluded_players = set()
        
        for j in range(member // 4):
            table_output = f" {j + 1}番卓 : "
            if i == 0:
                match = tuple(players[0:4])
                players = players[4:]
            else:
                match = generate_match(players, match_history, excluded_players)
                if match is None:
                    loop_count += 1
                    break
            player1, player2, player3, player4 = match
            table_output += f"\t{player1}\t{player2}\t{player3}\t{player4}"
            round_output.append(table_output)
            current_round_matches.extend([(player1, player2), (player2, player1), (player1, player3), (player3, player1), (player1, player4), (player4, player1), (player2, player3), (player3, player2), (player2, player4), (player4, player2), (player3, player4), (player4, player3)])
            
            # プレイヤーを使用済みとして除外リストに追加
            excluded_players.update(match)

        else:
            for output in round_output:
                print(output)
            for match in current_round_matches:
                match_history[match[0]].add(match[1])
            loop_count = 0
            i += 1
            players = all_players.copy()

        if loop_count > 500:
            break

    if i == game_count:
        break
