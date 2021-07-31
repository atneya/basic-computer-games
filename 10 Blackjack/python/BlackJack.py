import random 


class Card:
    
    SUIT = ["Spades", "Clubs", "Hearts", "Diamonds"]
    NUMBER = [0, "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

    def is_ace(self):
        return self.number == 1

    def get_value(self):
        if (self.is_ace()):
            return 11
        return min(self.number, 10)
    
    def get_string(self):
        return self.NUMBER[self.number] + " of " + self.SUIT[self.suit]


class Hand:
    def __init__(self, player, bet):
        self.player = player
        self.bet = bet
        self.cards = []
        self.num_aces = 0

    def add_card(self, card):
        self.cards.append(card)
        if card.get_value() == 11:
            self.num_aces += 1
    
    def get_value(self):
        ace_ct = self.num_aces
        val = sum([card.get_value() for card in self.cards])
        while (val > 21 and ace_ct > 0):
            val -= 10
            ace_ct -= 1
        return val

    def is_blackjack(self):
        return (self.get_value() == 21 and self.num_aces == 1 and len(self.cards) == 2)    

    def is_pair(self):
        return (len(self.cards) == 2 and self.cards[0].number == self.cards[1].number)

    def is_busted(self):
        return self.get_value() > 21


class BlackJackGame:
    SHUFFLE_LIMIT = 52 * 2

    def __init__(self, numplayers):
        self._num_players = numplayers
        self._profits = [0] * (numplayers + 1) # Last index is the dealer
        self._deck = None
        self._hands = None
        self._insurance = None
        self.generate_shuffled_deck()

    def generate_shuffled_deck(self):
        print("RESHUFFLING")
        self._deck = []
        for suit in range(4):
            for number in range(1, 14): # Ace is 1, face is 11+
                self._deck.append(Card(suit, number)) # We represent cards as suit, number tuples
        self._deck = self._deck * 6 # We want a 6 card shoe
               
    def deal_card(self):
        if (len(self._deck) < self.SHUFFLE_LIMIT):
           self.generate_shuffled_deck() 
        val = self._deck.pop(0)
        return val
    def get_bets(self):
        print("BETS")
        self._hands = []
        for i in range(self._num_players):
            var = 0
            while True:
                try:
                    var = int(input("# {} ? ".format(i + 1)))
                    if (var < 0 or var > 10000):
                        raise ValueError
                    break
                except ValueError:
                    print("ENTER VALID INTEGER BETWEEN 1-10000")
            self._hands.append(Hand(i, var))
    
    def deal_cards(self):
        self._dealer_hand = Hand(self._num_players, 0)
        print("PLAYER ", end="")
        for i in range(self._num_players):
            print("{0:<15} ".format(i + 1), end = '')
        print("DEALER")
        for j in range(2):
            print("       ", end="")
            for i in range(self._num_players):
                card = self.deal_card()
                self._hands[i].add_card(card)
                print("{0: <15}".format(card.get_string()), end = ' ')
            dealer_card = self.deal_card()
            self._dealer_hand.add_card(dealer_card)
            if (j == 0):
                print("{0: <15}".format(dealer_card.get_string()))
        print("")

    def ask_insurance(self):
        self._insurance = [0] * self._num_players
        if (self._dealer_hand.cards[0].get_value() != 11):
            return
        for i in range(self._num_players):
            inp = ""
            while (not inp or (inp[0] != "Y" and inp[0] != "N" and inp[0] != "y" and inp[0] != "n")):
                inp = input("Player {} Insurance ? ".format(i + 1))
            if (inp[0] == "Y" or inp[0] == "y"):
                self._insurance[i] = self._hands[i].bet / 2
   
    def dealer_blackjack(self):
        if (self._dealer_hand.cards[0].get_value() != 11 and self._dealer_hand.cards[0].get_value() != 10):
            return
        if (self._dealer_hand.is_blackjack()):
            print("DEALER BLACKJACK!")
            for i in range(self._num_players):
                self._profits[i] += self.insurance[i] * 2 
                self._profits[self._num_players] -= self.insurance[i] * 2
            for hand in self._hands:
                if (not hand.is_blackjack()):
                    self._profits[hand.player] -= hand.bet
                    self._profits[self._num_players] += hand.bet
            for i in range(self._num_players):
                print("player {}  has {:>5}".format(i+1, self._profits))
            print("dealer's total is {}".format(self._profits[self._num_players]))
            
        else:
            print("NO DEALER BLACKJACK")

    def player_action(self, hand):
        inp = "" 
        while True:
            inp = input("Player {} ? ".format(hand.player + 1))
            if (inp != "H" and inp != "D" and inp != "S" and inp != "/"):
                print("Please enter valid input")
            else:
                if (inp == "/" and not hand.pair()):
                    print("Can only split with a pair")
                else:
                    break
        if (inp == "S"):
            print("TOTAL IS {}".format(hand.get_value()))
            return None

        if (inp == "D"):
            hand.bet *= 2
            print("Player {} doubles up to {}".format(hand.player + 1, hand.bet))
            card = self.deal_card()
            print("Recieved a {}".format(card.get_string()), end="")
            hand.add_card(card)
            if (hand.get_value() > 21):
                print(" ... BUSTED!")
            else:
                print("\nTOTAL IS {}".format(hand.get_value()))
            return None

        if (inp == "/"):
            card = hand.cards.pop()
            new_hand = Hand(hand.player, hand.bet)
            new_hand.add_card(card)
            return [hand, new_hand]
        
        while True:
            card = self.deal_card()
            print("Recieved a {}".format(card.get_string()), end="")
            hand.add_card(card)
            if (hand.get_value() > 21):
                print(" ... BUSTED!") 
                break
            else:
                print("\nTOTAL IS {}".format(hand.get_value()))
            inp = ""
            while True:
                inp = input("Player {} ? ".format(hand.player + 1))
                if (inp != "H" and inp != "S"):
                    print("Please enter valid input")
                else:
                    break
            if (inp == "S"):
                return None
    
    def player_actions(self):
        completed_splits = []
        for hand in self._hands: 
            res = self.player_action(hand)
            if res:
                hand = res.pop()
                new_splits =  self.players_action(hand)
                if not new_splits:
                    completed_splits.append(hand) 
                res += new_splits
        self._hands += completed_splits 

    def dealer_action(self):
        print("Dealer has a {} concealed for a total of {}".format(self._dealer_hand.cards[1].get_string(), self._dealer_hand.get_value()))
        while (self._dealer_hand.get_value() < 17):
            card = self.deal_card()
            print("Draws a {}".format(card.get_string()), end="")
            self._dealer_hand.add_card(card)
            if (self._dealer_hand.get_value() > 21):
                print(" ... BUSTED!") 
                break
            else:
                print("\nTOTAL IS {}".format(self._dealer_hand.get_value()))

    def close_action(self):
       
        for hand in self._hands:
            if (hand.is_blackjack()):
                self._profits[hand.player] += hand.bet * 1.5
                self._profits[self._num_players] -= hand.bet * 1.5
            elif (hand.is_busted()):
                self._profits[hand.player] -= hand.bet 
                self._profits[self._num_players] += hand.bet 
            elif (self._dealer_hand.is_busted() or hand.get_value() > self._dealer_hand.get_value()):
                self._profits[hand.player] += hand.bet 
                self._profits[self._num_players] -= hand.bet 
            elif (hand.get_value() < self._dealer_hand.get_value()):
                self._profits[hand.player] -= hand.bet 
                self._profits[self._num_players] += hand.bet 
        
        for i in range(self._num_players):
            print("player {}  has {:>5}".format(i+1, self._profits[i]))

        print("dealer's total is {}".format(self._profits[self._num_players]))
 
 

    def game_loop(self):
        self.get_bets()
        self.deal_cards()
        self.ask_insurance()
        if (self.dealer_blackjack()):
            return
        self.player_actions()
        self.dealer_action()
        self.close_action()

    
def main():
    print("                 BLACKJACK                    ")
    print("CREATIVE COMPUTING MORRISTOWN,  NEW JERSEY\n\n")
    
    inp = ""
    while (not inp or (inp[0] != "Y" and inp[0] != "N" and inp[0] != "y" and inp[0] != "n")):
        inp = input("DO YOU WANT INSTRUCTIONS?")
    
    if (inp[0] == "Y" or inp[0] == "y"):
        print("This is the game of 21. As many as 7 players may play the")
        print("game. On each deal, bets will be asked for, and the")
        print("players' bets should be typed in. The cards will then be")
        print("dealt, and each player in turn plays his hand. The")
        print("first response should be either 'D', indicating that the")
        print("player is doubling down, 'S', indicating that he is")
        print("standing, 'H', indicating he wants another card, or '/',")
        print("indicating that he wants to split his cards. After the")
        print("initial response, all further responses should be 's' or")
        print("'H', unless the cards were split, in which case doubling")
        print("down is again permitted. In order to collect for")
        print("Blackjack, the initial response should be 'S'.")
    
   
    
    while True:
        try:
            var = int(input("NUMBER OF PLAYERS?"))
            if (var < 1 or var > 6):
                raise ValueError()
            break
        except ValueError:
            print("ENTER VALID INTEGER BETWEEN 1-6")
    
    game = BlackJackGame(var)
    while True:
        game.game_loop()

if __name__ == "__main__":
    main()

