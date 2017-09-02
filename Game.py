from enum import Enum
import random


class Card(object):

    def __init__(self, suit, value):
        self.suit: Suit = suit
        self.value = value

        # Set to red, and then if it isn't red, set to black
        self.color = Color.RED
        self.color = (suit == Suit.HEARTS or suit == Suit.DIAMONDS) or Color.BLACK

    # Return a unique hash for each card
    def get_hash(self):
        return (self.suit.value - 1) * 13 + self.value


class Suit(Enum):
    HEARTS = 1
    DIAMONDS = 2
    SPADES = 3
    CLUBS = 4


class Color(Enum):
    RED = 1
    BLACK = 2


class Game(object):

    def __init__(self, iterations, deck):
        self.iterations = iterations
        self.deck: [Card] = deck
        self.revealed_cards: [Card] = []

        self.player1_pairs: [(Card, Card)] = []
        self.player2_pairs: [(Card, Card)] = []

    def play_game(self):

        player1_wins = 0
        player2_wins = 0
        ties = 0

        for i in range(0, self.iterations):

            # Reset the game deck
            game_deck = list(self.deck)

            # Used to check if game is finished
            winning_player = None

            # Used to keep track of turns
            player_turn = 1

            # Used to track the previous player's card 2, if it matches something
            previous_card_match = False

            # Reset arrays
            self.revealed_cards = []
            self.player1_pairs = []
            self.player2_pairs = []

            while winning_player is None:

                # If there was a match that the previous player couldn't grab
                if previous_card_match is not False:

                    if player_turn == 1:
                        self.player1_pairs.append(previous_card_match)

                        # Check if the game has been won
                        winning_player = self.check_for_win()

                    elif player_turn == 2:
                        self.player2_pairs.append(previous_card_match)

                        # Check if the game has been won
                        winning_player = self.check_for_win()

                    # Reset the boolean
                    previous_card_match = False

                    # Take another turn
                    continue

                # Take a random card from the remaining cards
                revealed_card: Card = random.choice(game_deck)

                pair_found = self.check_for_pair(revealed_card)

                if pair_found[0] is True:

                    # Check whose turn it is, and add the pair to their list
                    if player_turn == 1:
                        self.player1_pairs.append((revealed_card, pair_found[1]))

                        # Check if the game has been won
                        winning_player = self.check_for_win()

                    elif player_turn == 2:
                        self.player2_pairs.append((revealed_card, pair_found[1]))

                        # Check if the game has been won
                        winning_player = self.check_for_win()

                    # Remove new revealed card from game (other card has already been removed)
                    game_deck.remove(revealed_card)

                    # Skip player change if pair found
                    continue

                #
                # At this point, the first card has been drawn, and it wasn't a match
                # So the second card will be drawn
                #

                # Remove first card from deck before checking second card
                game_deck.remove(revealed_card)

                # Get second card
                another_revealed_card = random.choice(game_deck)

                # If the second and first card match
                if revealed_card.value == another_revealed_card.value and revealed_card.color == another_revealed_card.color:

                    if player_turn == 1:

                        self.player1_pairs.append((revealed_card, another_revealed_card))

                        # Check if the game has been won
                        winning_player = self.check_for_win()

                    elif player_turn == 2:

                        self.player2_pairs.append((revealed_card, another_revealed_card))

                        # Check if the game has been won
                        winning_player = self.check_for_win()

                    # Remove second card from deck (first card has already been removed)
                    game_deck.remove(another_revealed_card)

                    continue

                #
                # At this point, no matches have been found, even after the second card
                #

                # Remove card 2 from deck, as the computer will not choose it again
                game_deck.remove(another_revealed_card)

                # For the next player's sake, check if card 2 matches any previous card
                pair_found = self.check_for_pair(another_revealed_card)

                # If card 2 matches a previous card
                if pair_found[0] is True:

                    # Set the pair for the next player to use
                    previous_card_match = (another_revealed_card, pair_found[1])

                    # Only add the first card to revealed cards as it is still unmatched
                    self.revealed_cards.append(revealed_card)

                else:

                    # Add both revealed cards to revealed card deck, if there are absolutely no matches
                    self.revealed_cards.append(revealed_card)
                    self.revealed_cards.append(another_revealed_card)

                # If no pairs found, next player's turn
                if player_turn == 1:
                    player_turn = 2
                elif player_turn == 2:
                    player_turn = 1

            if winning_player == 1:
                player1_wins += 1
            elif winning_player == 2:
                player2_wins += 1
            elif winning_player == 0:
                ties += 1

        # This is just to show the "results" of the simulation
        # You can change this if you like
        print(player1_wins)
        print(player2_wins)

        print("Player 1 Wins: " + str(round((player1_wins / self.iterations), 3) * 100) + "%")
        print("Player 2 Wins: " + str(round((player2_wins / self.iterations), 3) * 100) + "%")
        print("Ties: " + str(round((ties / self.iterations), 3) * 100) + "%")

    def check_for_pair(self, card):

        for revealed_card in self.revealed_cards:

            # If there is a match that was previously revealed
            if card.value == revealed_card.value and card.color == revealed_card.color:

                # Remove match from memory (for efficiency)
                self.revealed_cards.remove(revealed_card)

                return [True, revealed_card]

        # If there is no match
        return [False]

    def check_for_win(self):

        # Check if the game has been won
        if len(self.player1_pairs) > len(self.deck) / 4:
            # Player 1 wins
            return 1
        elif len(self.player2_pairs) > len(self.deck) / 4:
            # Players 2 wins
            return 2
        elif len(self.player1_pairs) == len(self.deck) / 4 and len(self.player2_pairs) == len(self.deck) / 4:
            # Tie
            return 0
        else:
            return None


# If you alter anything above this comment, there is a high chance the program won't work properly again

# Below I populate the deck. Feel free to change the composition of the deck

deck: [Card] = []
deck.append(Card(Suit.HEARTS, 1))
deck.append(Card(Suit.HEARTS, 2))
deck.append(Card(Suit.HEARTS, 3))
deck.append(Card(Suit.HEARTS, 4))
deck.append(Card(Suit.HEARTS, 5))
deck.append(Card(Suit.HEARTS, 6))
deck.append(Card(Suit.HEARTS, 7))
deck.append(Card(Suit.HEARTS, 8))
deck.append(Card(Suit.HEARTS, 9))
deck.append(Card(Suit.HEARTS, 10))
deck.append(Card(Suit.HEARTS, 11))
deck.append(Card(Suit.HEARTS, 12))
deck.append(Card(Suit.HEARTS, 13))
deck.append(Card(Suit.CLUBS, 1))
deck.append(Card(Suit.CLUBS, 2))
deck.append(Card(Suit.CLUBS, 3))
deck.append(Card(Suit.CLUBS, 4))
deck.append(Card(Suit.CLUBS, 5))
deck.append(Card(Suit.CLUBS, 6))
deck.append(Card(Suit.CLUBS, 7))
deck.append(Card(Suit.CLUBS, 8))
deck.append(Card(Suit.CLUBS, 9))
deck.append(Card(Suit.CLUBS, 10))
deck.append(Card(Suit.CLUBS, 11))
deck.append(Card(Suit.CLUBS, 12))
deck.append(Card(Suit.CLUBS, 13))
deck.append(Card(Suit.SPADES, 1))
deck.append(Card(Suit.SPADES, 2))
deck.append(Card(Suit.SPADES, 3))
deck.append(Card(Suit.SPADES, 4))
deck.append(Card(Suit.SPADES, 5))
deck.append(Card(Suit.SPADES, 6))
deck.append(Card(Suit.SPADES, 7))
deck.append(Card(Suit.SPADES, 8))
deck.append(Card(Suit.SPADES, 9))
deck.append(Card(Suit.SPADES, 10))
deck.append(Card(Suit.SPADES, 11))
deck.append(Card(Suit.SPADES, 12))
deck.append(Card(Suit.SPADES, 13))
deck.append(Card(Suit.DIAMONDS, 1))
deck.append(Card(Suit.DIAMONDS, 2))
deck.append(Card(Suit.DIAMONDS, 3))
deck.append(Card(Suit.DIAMONDS, 4))
deck.append(Card(Suit.DIAMONDS, 5))
deck.append(Card(Suit.DIAMONDS, 6))
deck.append(Card(Suit.DIAMONDS, 7))
deck.append(Card(Suit.DIAMONDS, 8))
deck.append(Card(Suit.DIAMONDS, 9))
deck.append(Card(Suit.DIAMONDS, 10))
deck.append(Card(Suit.DIAMONDS, 11))
deck.append(Card(Suit.DIAMONDS, 12))
deck.append(Card(Suit.DIAMONDS, 13))

# Here I run the simulation. You can check the number of iterations by changing the number below
game = Game(100000, deck)
game.play_game()
