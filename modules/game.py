from .cards import Deck

class Game:

    LIFESTYLE_BONUSES = {
        0:0,
        1:0,
        2:.1,
        3:.5,
        4:1,
        5:2,
        6:10
    }

    DATA_HEADERS = [
        'game_number',
        'payout',
        'lifestyle_bonus',
        'total_payout',
        'lifestyle_bonuses',
        'cards_drawn',
        'draw_order',
        'card_stack',
        'suit_counts',
        'life',
        'wild',
        'death',
        'super_death',
        'longest_suit_count'
    ]

    def __init__(self, game_number=None):
        self.deck = Deck()
        self.game_number = game_number
        self.is_active = True
        self.suits_drawn = {}
        self.payout = 0
        self.lifestyle_bonus = 0
        self.total_payout = 0

    def calculate_payouts(self):
        self.payout = 0
        self.lifestyle_bonus = 0
        self.total_payout = 0

        # no payouts of super death drawn
        if self.deck.super_death_drawn:
            return

        # calculate payout form cards
        for card in self.deck.drawn:
            self.payout += card.payout

        # calculate lifestyle bonus
        # top N suits drawn where N = wilds drawn
        for suit in self.deck.card_stacks['suits']:
            card_count = len(self.deck.card_stacks['suits'][suit])
            self.lifestyle_bonus += self.LIFESTYLE_BONUSES[card_count]
            
        # calculate total payout (%)
        self.total_payout = self.payout
        if self.deck.death_drawn:
            self.total_payout += self.lifestyle_bonus
        self.lifestyle_bonus = round(self.lifestyle_bonus, 1)
        self.payout = round(self.payout, 1)
        self.total_payout = round(self.total_payout, 1)

    def next(self):
        if self.is_active:
            card = self.deck.draw()
            if card.is_death:
                self.is_active = False
        self.calculate_payouts()

    def play(self):
        while self.is_active:
            self.next()

    def reset_game(self):
        self.__init__()

    def get_data(self, format='dict'):
        if format not in ('dict', 'array'):
            raise ValueError(f"'{format}' is not an acceptable format. Format must be dict or array.")

        suit_counts = {suit:len(self.deck.card_stacks['suits'][suit]) for suit in self.deck.card_stacks['suits']}
        drawn_str = self.deck.get_drawn_as_string()
        card_stacks_str = self.deck.get_stack_as_string()
        lifestyle_bonuses = 0
        longest = 0
        for sc in suit_counts:
            if suit_counts[sc] > 1:
                lifestyle_bonuses += 1
            if suit_counts[sc] > longest:
                longest = suit_counts[sc]

        if format == 'dict':
            data = {}
            data['cards'] = {
                'card_stack':card_stacks_str,
                'suit_counts':suit_counts,
                'draw_order':drawn_str,
                'cards_drawn':len(self.deck.drawn),
                'life':self.deck.lifes_drawn,
                'wild':self.deck.wilds_drawn,
                'death':1 if self.deck.death_drawn else 0,
                'super_death':1 if self.deck.super_death_drawn else 0,
                'longest_suit_count':longest,
            }
            data['payouts'] = {
                'payout':self.payout,
                'lifestyle_bonus':self.lifestyle_bonus,
                'total_payout':self.total_payout,
                'lifestyle_bonuses':lifestyle_bonuses,
            }
            data['meta'] = {
                'game_number':self.game_number
            }
        
        elif format == 'array':
            data = [
                self.game_number,
                self.payout, 
                self.lifestyle_bonus, 
                self.total_payout, 
                lifestyle_bonuses,
                len(self.deck.drawn),
                drawn_str, 
                card_stacks_str, 
                suit_counts,
                self.deck.lifes_drawn,
                self.deck.wilds_drawn,
                1 if self.deck.death_drawn else 0,
                1 if self.deck.super_death_drawn else 0,
                longest
                ]

        return data