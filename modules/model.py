from .game import Game
from .player import Player
from collections.abc import Iterable

class SimulationBasic:
    
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
                if i % 1000 == 0 or i == plays - 1:
                    print(i + 1 if i == plays - 1 else i)

            game = Game(game_number=i)
            game.play()
            self.game_data['data'].append(game.get_data(format=data_format))
            for player in active_players:
                player.settle_bet(game)
                self.player_data['data'].append(player.get_data(format=data_format))
                if player.bank < player.bet:
                    active_players.remove(player)

        return (self.game_data, self.player_data)


class SimulationCheater(SimulationBasic):
    
    PLAYER_DATA_HEADERS = Player.DATA_HEADERS + ['simulation_payout',
                                                 'simulation_return',
                                                 'simulation_bank']

    def run(self, plays:int, players=None, data_format='array', verbose=False):
        if not isinstance(plays, int):
            raise ValueError(f'Cannot use {type(plays)}. Must be a non-negative integer.')
        if players:
            self.players = players

        for player in self.players:
            player.best_bank = player.bank
        
        active_players = self.players
        for i in range(plays):
            if len(active_players) == 0:
                break
            if verbose:
                if i % 1000 == 0 or i == plays - 1:
                    print(i + 1 if i == plays - 1 else i)
            
            game = Game(game_number=i)
            best_payout = 0
            while game.is_active:
                game.next()
                if game.deck.cards[-1].is_death:
                    best_payout = game.total_payout

            if game.total_payout > best_payout:
                best_payout = game.total_payout
            if best_payout == 0 and game.total_payout == -1:
                best_payout = -1

            self.game_data['data'].append(game.get_data(format=data_format))

            for player in self.players:
                player.settle_bet(game)
                best_return = best_payout * player.bet
                player.best_bank += best_return
                p_data = player.get_data(format=data_format)
                if data_format == 'dict':
                    p_data['player']['simulation_payout'] = best_payout
                    p_data['player']['simulation_return'] = best_return
                    p_data['player']['simulation_bank'] = player.best_bank
                else:
                    p_data += [best_payout, best_return, player.best_bank]
            
                self.player_data['data'].append(p_data)
                if player.best_bank < player.bet:
                    active_players.remove(player)
            
        return (self.game_data, self.player_data)