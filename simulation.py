from modules import Player, simulator_basic
import pandas as pd
import time

players = [
    Player('p10', 100000, 10),
    Player('p20', 100000, 20),
    Player('p50', 100000, 50),
    Player('p100', 100000, 100),
    Player('p250', 100000, 250),
]

game_data, player_data = simulator_basic(players, 100000, verbose=True)

game_df = pd.DataFrame(game_data['data'], columns=game_data['headers'])
player_df = pd.DataFrame(player_data['data'], columns=player_data['headers'])

game_df.to_csv('data/game_data.csv', index=False)
player_df.to_csv('data/player_data.csv', index=False)
