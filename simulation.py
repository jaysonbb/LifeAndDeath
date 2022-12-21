from modules import Player, Game, Simulation
import pandas as pd
import time

Game.LIFESTYLE_BONUSES[5] = 5

players = [
    Player('p10', 10000, 10),
    Player('p20', 10000, 20),
    Player('p50', 10000, 50),
    Player('p100', 10000, 100),
    Player('p250', 10000, 250),
]

game_data, player_data = Simulation(players).run(plays=20000, verbose=True)

game_df = pd.DataFrame(game_data['data'], columns=game_data['headers'])
player_df = pd.DataFrame(player_data['data'], columns=player_data['headers'])

game_df.to_csv('data/game_data.csv', index=False)
player_df.to_csv('data/player_data.csv', index=False)
