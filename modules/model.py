from .game import Game
from .player import Player
from collections.abc import Iterable

def simulator_basic(players, plays, data_format='array', verbose=False):
    if not isinstance(players, Iterable):
        players = [players]
    for player in players:
        if type(player) != Player:
            raise ValueError(f'Cannot use {type(player)} as Player.')

    game_data = {'headers':Game.DATA_HEADERS, 'data':[]}
    player_data = {'headers':Player.DATA_HEADERS, 'data':[]}

    for i in range(plays):
        if len(players) == 0:
            break
        if verbose and i > 0:
            if i % 1000 == 0:
                print(i)

        game = Game(game_number=i)
        game.play()
        game_data['data'].append(game.get_data(format=data_format))
        for player in players:
            player.settle_bet(game)
            player_data['data'].append(player.get_data(format=data_format))
            if player.bank < 10:
                players.remove(player)
    
    return (game_data, player_data)