import random
from collections import Counter

class Card:

    PAYOUTS = {
        'life':       0.1,
        'super_life': 0.5,
        'wild':       0.2,
        'super_wild': 1.0,
        'death':      0.0,
        'super_death':0.0
    }

    def __init__(self, suit=None, card_type=None):
        assert card_type in ['life', 'super_life', 'wild', 'super_wild', 'death', 'super_death']
        self.suit = suit
        self.card_type = card_type
        self.payout = self.PAYOUTS[card_type]
        self.is_life = True if card_type == 'life' or card_type == 'super_life' else False
        self.is_suit = True if self.is_life or card_type == 'death' else False
        self.is_wild = True if card_type == 'wild' or card_type == 'super_wild' else False
        self.is_super = True if card_type == 'super_life' or card_type == 'super_wild' or card_type == 'super_death' else False
        self.is_death = True if card_type == 'death' or card_type == 'super_death' else False
        self.is_super_death = True if card_type == 'super_death' else False

    def __repr__(self):
        return f"{self.card_type}{self.suit if self.suit else ''}"

    def __str__(self):
        return self.__repr__()


class Deck:
    SUITS = 10
    def __init__(self):
        self.cards = self._build_deck()
        self.drawn = []
        self.card_stacks = {}
        self.death_drawn = False
        self.super_death_drawn = False
        self.wilds_drawn = 0
        self.lifes_drawn = 0

    def _build_deck(self, shuffle=True):
        # initialize deck
        cards = []
        
        # create suit cards
        for suit in range(1, self.SUITS + 1):
            life = Card(suit, 'life')
            super_life = Card(suit, 'super_life')
            death = Card(suit, 'death')
            cards += [life] * 3 + [super_life, death]

        # create wild cards
        wild = Card(None, 'wild')
        super_wild = Card(None, 'super_wild')
        super_death = Card(None, 'super_death')
        cards += [wild] * 3 + [super_wild, super_death]

        # shuffle deck
        if shuffle:
            random.shuffle(cards)
        return cards

    def new_deck(self):
        self.__init__()

    def draw(self):
        card = self.cards.pop()
        if card.is_life:
            self.lifes_drawn += 1
        elif card.is_wild:
            self.wilds_drawn += 1
        elif card.is_death:
            self.death_drawn = True
            if card.is_super_death:
                self.super_death_drawn = True
        self.drawn.append(card)
        self._create_stacks()
        return card

    def _create_stacks(self):
        self.card_stacks = {}
        self.card_stacks['suits'] = {suit:[] for suit in range(1, self.SUITS + 1)}
        # add all drawn cards with a suit (not wild or super death) into their corresponding suit array
        for card in self.drawn:
            if card.is_suit:
                self.card_stacks['suits'][card.suit].append(card)

        # create array of the suit of each card drawn and array of wild cards
        suits_drawn = list(map(lambda x: x.suit, filter(lambda x: x.is_life, self.drawn)))
        wilds = list(filter(lambda x: x.is_wild, self.drawn))
        if wilds:
            # get top N where N = number of wilds drawn
            modes = Counter(suits_drawn).most_common()
            for m in modes:
                if len(wilds) == 0:
                    break
                if len(self.card_stacks['suits'][m[0]]) >= 1:
                    self.card_stacks['suits'][m[0]].append(wilds[0])
                    wilds.pop(0)

        self.card_stacks['wilds'] = wilds
        self.card_stacks['super_death'] = list(filter(lambda x: x.is_super_death, self.drawn))

    def get_stack_as_string(self):
        card_stack_str = {}
        for card_type in self.card_stacks:
            if card_type == 'suits':
                card_stack_str[card_type] = {}
                for suit in self.card_stacks[card_type]:
                    card_stack_str[card_type][suit] = list(map(lambda x: str(x), self.card_stacks[card_type][suit]))
            else:
                card_stack_str[card_type] = list(map(lambda x: str(x), self.card_stacks[card_type]))

        return card_stack_str

    def get_drawn_as_string(self):
        return list(map(lambda x: str(x), self.drawn))


    def __len__(self):
        return len(self.cards)
