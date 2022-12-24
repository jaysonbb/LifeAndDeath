from .game import Game
from .player import Player
from collections.abc import Iterable

class Simulation:
    
    GAME_DATA_HEADERS = Game.DATA_HEADERS
    PLAYER_DATA_HEADERS = Player.DATA_HEADERS

    def __init__(self, players):
        self.players = players
        self.game_data = {'headers':self.GAME_DATA_HEADERS, 'data':[]}
        self.player_data = {'headers':self.PLAYER_DATA_HEADERS, 'data':[]}
    
    @property
    def players(self):
        return self._players
    
    @players.setter
    def players(self, obj):
        if not isinstance(obj, Iterable):
            obj = [obj]
        for player in obj:
            if type(player) != Player:
                raise ValueError(f'Cannot use {type(obj)} as Player.')
        self._players = obj

    def reset(self):
        self.__init__(self.players)

    def run(self, plays:int, players=None, data_format='array', verbose=False):
        if not isinstance(plays, int):
            raise ValueError(f'Cannot use {type(plays)}. Must be a non-negative integer.')
        if players:
            self.players = players
        
        active_players = self.players
        for i in range(plays):
            if len(active_players) == 0:
                break
            if verbose and i > 0:
                if i % 1000 == 0 or i == plays-1:
                    if i == plays - 1:
                        print(i + 1)
                    else:
                        print(i)
            game = Game(game_number=i)
            game.play()
            self.game_data['data'].append(game.get_data(format=data_format))
            for player in active_players:
                player.settle_bet(game)
                self.player_data['data'].append(player.get_data(format=data_format))
                if player.bank < player.bet:
                    active_players.remove(player)

        return (self.game_data, self.player_data)


# class SimulationBestCase(Simulation):
    
#     GAME_DATA_HEADERS = Game.DATA_HEADERS + ['best_case_payout']
#     PLAYER_DATA_HEADERS = Player.DATA_HEADERS + ['best_case_payout',
#                                                  'best_case_return', 
#                                                  'best_case_bank']

#     def run(self, plays:int, players=None, data_format='array', verbose=False):
#         pass



# def simulation_best_case(players, plays, data_format='array', verbose=False):
#     if not isinstance(players, Iterable):
#         players = [players]
#     for player in players:
#         if type(player) != Player:
#             raise ValueError(f'Cannot use {type(player)} as Player.')

#     game_headers = Game.DATA_HEADERS.append('best_case_payout')
#     player_headers = Player.DATA_HEADERS + ['best_case_payout', 'best_case_return', 'best_case_bank']
#     game_data = {'headers':game_headers, 'data':[]}
#     player_data = {'headers':player_headers, 'data':[]}

#     best_case_payout = 0
#     for i in range(plays):
#         if len(players) == 0:
#             break
#         if verbose and i > 0:
#             if i % 10000 == 0:
#                 print(i)
#         for i in range(plays):
#             game = Game(game_number=i)
#             while game.is_active:
#                 game.next()
#                 if game.deck.cards[-1].is_death:
#                     best_exit_payout = game.total_payout

#             if game.total_payout > best_exit_payout:
#                 best_case_payout = game.total_payout

#             g_data = game.get_data()
#             g_data['payout']['best_case_payout'] = best_case_payout
#             game_data['data'].append(g_data)

#             for player in players:
#                 player.settle_bet(game)
#                 p_data = player.get_data()
#                 p_data['payout']['best_case_payout'] = best_case_payout
#                 best_case_return = -player.bet if best_case_payout == 0 else best_case_payout * player.bet
#                 player.best_case_bank += best_case_return
#                 p_data['player']['best_case_return'] = best_case_return
#                 p_data['player']['best_case_bank'] = player.best_case_bank
#                 player_data['data'].append(p_data)












            
            