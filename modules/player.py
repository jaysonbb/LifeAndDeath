class Player:

    DATA_HEADERS = [
        'player',
        'game_number',
        'bet',
        'payout',
        'lifestyle_bonus',
        'total_payout',
        'lifestyle_bonuses',
        'total_return',
        'available_bank',
        'cards_drawn',
        'draw_order',
        'card_stack',
        'suit_counts',
        'life',
        'wild',
        'death',
        'super_death',
        'longest_suit_count',
        'best_payout',
        'best_payout_card_count'
    ]

    def __init__(self, name=None, bank=0, bet=None):
        self.name = name
        self.bank = bank
        self.bet = bet
        self.is_active = True
        self.game_data = None
        
    @property
    def bet(self):
        return self._bet

    @property
    def bank(self):
        return self._bank

    @bet.setter
    def bet(self, val):
        if val and val % 10 != 0 and val < 10:
            raise ValueError(f"{val} is not valid. Player bet must be a multiple of 10 greater than 0.")
        if val and self.bank and val > self.bank:
            raise ValueError(f"{val} cannot be greater than player's available bank ({self.bank})")
        self._bet = val

    @bank.setter
    def bank(self, val):
        self._bank = val

    def settle_bet(self, game):
        self.is_active = False
        total_return = (game.total_payout * self.bet) - self.bet
        if game.is_active:
            total_return += self.bet
        self.bank += total_return
        
        self.game_data = game.get_data(format='dict')
        self.game_data['player'] = {
            'player':self.name,
            'bet':self.bet,
            'total_return':total_return,
            'bank_remaining':self.bank
        }

    def get_data(self, format='dict'):
        if format not in ('dict', 'array'):
            raise ValueError(f"'{format}' is not an acceptable format. Format must be dict or array.")
        if not self.game_data:
            raise ValueError(f'Player has no data for current game.')

        if format == 'dict':
            return self.game_data
        elif format == 'array':
            return [
                self.name,
                self.game_data['meta']['game_number'],
                self.bet,
                self.game_data['payouts']['payout'],
                self.game_data['payouts']['lifestyle_bonus'],
                self.game_data['payouts']['total_payout'],
                self.game_data['payouts']['lifestyle_bonuses'],
                self.game_data['player']['total_return'],
                self.bank,
                self.game_data['cards']['cards_drawn'],
                self.game_data['cards']['draw_order'],
                self.game_data['cards']['card_stack'],
                self.game_data['cards']['suit_counts'],
                self.game_data['cards']['life'],
                self.game_data['cards']['wild'],
                self.game_data['cards']['death'],
                self.game_data['cards']['super_death'],
                self.game_data['cards']['longest_suit_count'],
                self.game_data['cards']['best_payout'],
                self.game_data['cards']['best_payout_card_count']
            ]