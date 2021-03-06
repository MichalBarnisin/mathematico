"""
In this file, we define the game class that will be responsible for generating
the numbers for moves, adding/removing the players and letting them know the
current number, and evaluating the positions.
"""
import random as rnd
from .player import Player
from .eval import evaluate
from .board import Board
from typing import Union


class Game:
    """
    Class Game controls all card picking, asks players about next moves and
    assigns scores at the end.

    Note: each player must conform to the interface in player.py
    Note: only handles ONE game
    """
    def __init__(self):
        self.available_cards = [i for i in range(1, 14) for _ in range(4)]
        rnd.shuffle(self.available_cards)
        self.moves_played = 0
        self.players = []

    def __str__(self):
        """
        String representation of the game with full description of the current
        state of the game, including hidden information about the deck.

        :return: string representation of the current game state
        """
        r = f"Moves played:\t{self.available_cards[:self.moves_played]}\n"
        r += "Current card:\t"
        if self.finished():
            r += "None"
        else:
            r += str(self.available_cards[self.moves_played])
        r += f"\nMove number:\t{self.moves_played}\n"
        r += f"Players:\t{self.players}"
        return r

    def take_next_card(self) -> Union[None, int]:
        """
        Picks next card randomly from available_cards.

        :return: the number of the next card or None if the number of moves is
            sufficient to fill the board
        """
        if self.finished():
            return None
        card = self.available_cards[self.moves_played]
        self.moves_played += 1
        return card

    def add_player(self, player: Player) -> int:
        """
        Adds the player to the game. If the game is in progress, throws
        ValueError. To reference the final results for the added player, returns
        the index at which the player was added.

        :param player: player to be added
        :return: index of player in the game array
        """
        if self.moves_played != 0:
            raise ValueError("Game is in progress")
        self.players.append(player)
        return len(self.players) - 1

    def finished(self) -> bool:
        """
        Checks whether the game is finished either by filling the board or by
        drawing all cards from the deck.

        :return: true if no more cards will be drawn
        """
        return self.moves_played >= Board.SIZE ** 2 \
            or self.moves_played >= len(self.available_cards)

    def start(self, verbose=False):
        """
        Simulates one game, for each round picks one card, lets players start
        their move and at the end computes final scores.

        :param verbose: if True, prints information about game
        :return: list of final scores, the index corresponds to the index return
            by <add_player>
        """
        while not self.finished():
            next_card = self.take_next_card()
            assert next_card is not None
            if verbose:
                print(self)
            for player in self.players:
                player.move(next_card)
        return [evaluate(player.get_board()) for player in self.players]
