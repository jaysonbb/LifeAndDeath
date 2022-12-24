from modules import Player, Game, Simulation
import pandas as pd

# cards of a kind : bonus,
Game.LIFESTYLE_BONUSES = {
    0 :0,
    1: 0,
    2: 0.1,
    3: 0.5,
    4: 1,
    5: 5,
    6: 10
}

players = [
    # create players here separated by commas. must have at least one
    Player(name='p10',  bank=100000, bet=10),
    Player(name='p20',  bank=100000, bet=20),
    Player(name='p50',  bank=100000, bet=50),
    Player(name='p100', bank=100000, bet=100),
    Player(name='p250', bank=100000, bet=250),
]

# number of games to simulate 
plays = 20000

# data file destinations (must be .csv file)
game_data_file_name =   'data/game_data.csv'
player_data_file_name = 'data/player_data.csv'


# don't change anything here
game_data, player_data = Simulation(players).run(plays=plays, verbose=True)
game_df = pd.DataFrame(game_data['data'], columns=game_data['headers'])
player_df = pd.DataFrame(player_data['data'], columns=player_data['headers'])
game_df.to_csv(game_data_file_name, index=False)
player_df.to_csv(player_data_file_name, index=False)