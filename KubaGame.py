# Author:
# Date:
# Description:

class KubaGame:
    """A class representing a Kuba game

    Data Members (private):
        _players :
        _board :
        _valid_directions :
        _winner :
        _current_turn :

    Methods:


    """

    def __init__(self, player_one, player_two):
        """Initialize the KubaGame data members

        Parameters:
            player_one : ('Player One Name', 'W')
            player_two : ('Player Two Name', 'B')

        Returns:
            None
        """
        self._players = {player_one[0]: {"name": player_one[0],
                                         "color": player_one[1],
                                         "capture count": 0},
                         player_two[0]: {"name": player_two[0],
                                         "color": player_two[1],
                                         "capture count": 0}}
        self._board = [["W", "W", "X", "X", "X", "B", "B"],
                       ["W", "W", "X", "R", "X", "B", "B"],
                       ["X", "X", "R", "R", "R", "X", "X"],
                       ["X", "R", "R", "R", "R", "R", "X"],
                       ["X", "X", "R", "R", "R", "X", "X"],
                       ["B", "B", "X", "R", "X", "W", "W"],
                       ["B", "B", "X", "X", "X", "W", "W"]]
        self._valid_directions = ["L", "R", "F", "B"]  # Left, Right, Forward, Back
        self._winner = None
        self._current_turn = None

    def get_current_turn(self):
        """Returns the player name corresponding to who's turn it is, or None if game hasn't started yet"""
        return self._current_turn

    def set_current_turn(self, playername):
        """Sets the value of _current_turn to playername"""
        self._current_turn = playername

    def make_move(self, playername, coordinates, direction):
        """Attempts to make a move for playername by pushing marble at coordinates in the given direction.

        Parameters:
            playername : name of player attempting to make move
            coordinates : coordinates of marble to be pushed as a tuple (X, Y)
            direction : one index in _valid_directions

        Returns:
            A boolean value based on if move was actually made
        """
        if not self.is_valid_move(playername, coordinates, direction):
            return False

        self.switch_turns()
        self.check_for_winner()

    def is_valid_move(self, playername, coordinates, direction):
        """"""
        # Validate Inputs
        if not (self.is_valid_playername(playername) and self.is_valid_coordinates(
                coordinates) and self.is_valid_direction(direction)):
            return False

        # Validate no rules are broken

        # Players may not move if game is over
        if self.get_winner() is not None:
            return False

        # Players may only move their own color
        if self.get_marble(coordinates) != self._players[playername]["color"]:
            return False

        # Players may only move on their turn
        if self.get_current_turn() is not None and self.get_current_turn() != playername:
            return False

        # Players may not push their pieces off the board

        return True

    def is_valid_playername(self, playername):
        """"""
        if playername in self._players:
            return True

        return False

    def is_valid_coordinates(self, coordinates):
        """"""
        if not isinstance(coordinates, tuple):
            return False

        if len(coordinates) != 2:
            return False

        if not isinstance(coordinates[0], int) or not isinstance(coordinates[1], int):
            return False

        if coordinates[0] < 0 or coordinates[0] > 6:
            return False

        if coordinates[1] < 0 or coordinates[1] > 6:
            return False

        return True

    def is_valid_direction(self, direction):
        """Checks if a given direction is a valid input"""
        if direction not in self._valid_directions:
            return False

        return True

    def is_game_over(self):
        """Returns a boolean value based on if the game is over."""
        self.check_for_winner()

        if self.get_winner() is None:
            return False

        return True

    def get_winner(self):
        """Returns the name of the winner or None if no winner"""
        return self._winner

    def check_for_winner(self):
        """"""
        players = self._players.keys()
        # Has any player captured 7 red pieces?
        for playername in players:
            if self.get_captured(playername) >= 7:
                self._winner = playername
                return None

        # Does one player have zero pieces?
        pieces_on_board = self.get_marble_count()
        white_piece_count = pieces_on_board[0]
        black_piece_count = pieces_on_board[1]

        if white_piece_count == 0:

            for playername in players:
                if self._players[playername]["color"] == "B":
                    self._winner = playername
                    return None

        if black_piece_count == 0:

            for playername in players:
                if self._players[playername]["color"] == "W":
                    self._winner = playername
                    return None

    # Can both players still move?

    def switch_turns(self):
        """If _current_turn is not None, switches _current_turn to opposite player"""
        if self._current_turn is not None:
            playernames = self.get_playernames()
            if self._current_turn == playernames[0]:
                self.set_current_turn(playernames[1])
                return None

            self.set_current_turn(playernames[1])
            return None

    def get_playernames(self):
        """Returns a list of playernames in _players"""
        players = self._players.keys()
        playernames = []
        for name in players:
            playernames.append(name)

        return playernames

    def get_captured(self, playername):
        """Returns the number of red marbles captured by playername"""
        if self.is_valid_playername(playername):
            return self._players[playername]["capture count"]

        # If playername is not valid, return 0
        return 0

    def increment_captured(self, playername):
        """Increments the number of red marbles captured by playername"""

    def get_marble(self, coordinates):
        """Returns the color of the marble ["W", "B", "R"] at the coordinates (row, column) or "X" if None"""
        if self.is_valid_coordinates(coordinates):
            row = coordinates[0]
            column = coordinates[1]
            return self._board[row][column]

    def get_marble_count(self):
        """Returns the number of White, Black, and Red marbles on the board as a tuple in the order (W,B,R)"""

        num_white = 0
        num_black = 0
        num_red = 0

        for row in range(7):
            for column in range(7):

                if self._board[row][column] == "W":
                    num_white += 1
                    continue

                if self._board[row][column] == "B":
                    num_black += 1
                    continue

                if self._board[row][column] == "R":
                    num_red += 1
                    continue

        return (num_white, num_black, num_red)


def main():
    game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))
    print(game.get_marble_count())  # returns (8,8,13)
    game.get_captured('PlayerA')  # returns 0

    game.get_winner()  # returns None
    game.make_move('PlayerA', (6, 5), 'F')
    game.make_move('PlayerA', (6, 5), 'L')  # Cannot make this move
    print(game.get_current_turn())  # returns 'PlayerB' because PlayerA has just played.
    game.get_marble((5, 5))  # returns 'W'


if __name__ == "__main__":
    main()
