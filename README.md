## 麻雀大会用プログラム(Create takugumi_4team_pivot.py　の解説)

### 概要

このプログラムは、麻雀大会の対戦組み合わせを自動的に生成するためのものです。プログラムは、指定された参加者数とゲーム数に基づいて各プレイヤーの対戦組み合わせを決定し、最終的な対戦表を出力します。各ゲームごとにプレイヤーが異なる組み合わせで対戦するように配慮されています。

### 使用方法

1. プログラムの実行開始時に、全体の参加者数 (`member`) とゲーム数 (`game_count`) を設定します。
2. プログラムは、各チームのプレイヤーを均等に分け、ゲームごとにランダムにプレイヤーを選びます。
3. 各ゲームごとに対戦組み合わせを生成し、対戦履歴に基づいて過去に対戦したことのないプレイヤーを選択します。
4. 各プレイヤーがどのテーブルで対戦したかの記録を保持し、最終的に各プレイヤーごとの対戦履歴をテーブル形式で出力します。
5. 実行時間を計算し、表示します。

### プログラムの詳細

#### インポートと初期設定

```python
import random
import os
import time
import pandas as pd
```

- 必要なライブラリをインポートします。
- `member`、`game_count`、`team_mem` などの設定を行います。

#### プレイヤーの初期化

```python
players = list(range(1, member + 1))
team_a = players[:team_mem]
team_b = players[team_mem:team_mem*2]
team_c = players[team_mem*2:team_mem*3]
team_d = players[team_mem*3:]
```

- プレイヤーリストを作成し、各チームに均等に分割します。

#### 対戦組み合わせ生成関数

```python
def generate_match(team1, team2, team3, team4, match_history):
    # 対戦組み合わせを生成するための関数
    # 各チームから1人ずつプレイヤーを選びますが、過去に対戦したことのあるプレイヤーは除外します
```

- 各チームから1人ずつプレイヤーを選び、過去に対戦したことのないプレイヤーを組み合わせます。

#### メインループ

```python
while True:
    # 対戦履歴とリトライカウントをリセット
    # 各ゲームの対戦組み合わせを生成
    # リトライ回数が一定数を超えた場合はやり直し
```

- 各ゲームの対戦組み合わせを生成し、成功するまで繰り返します。

#### 結果の出力と実行時間の計算

```python
# ピボット解除して再ピボットするためのデータフレームを作成
columns = ['Game', 'Table', 'Player']
df = pd.DataFrame(game_records, columns=columns)

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

# 表示
print(df_pivot)
```

- 各プレイヤーの各ゲームごとの対戦テーブルを記録し、再ピボットして最終的な対戦表を生成します。
- プレイヤーを昇順にソートして表示します。

```python
# 実行時間を計算し、表示
elapsed_time = end_time - start_time
hours, rem = divmod(elapsed_time, 3600)
minutes, seconds = divmod(rem, 60)
print(f"実行時間: {int(hours)}時間{int(minutes):02d}分{seconds:02.0f}秒")
```

- プログラムの実行時間を計算し、表示します。

### 注意事項

- `member` は4の倍数で設定してください。そうしないと、チーム分けが均等に行われません。
- プログラムは、各プレイヤーが他の全プレイヤーと対戦することを保証するものではありませんが、可能な限り多様な対戦組み合わせを生成します。

このプログラムを使用することで、麻雀大会の対戦組み合わせを自動的に生成し、公平で効率的な大会運営が可能になります。
