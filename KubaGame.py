# Author: Nic Nolan
# Date: 05/20/2021
# Description: The game Kuba represented as a class KubaGame that is playable with various commands.

class KubaGame:
    """A class representing a Kuba game.

    Data Members (private):
        _players : dict, with playername as key. Key value is a dict with 'name', 'color', and 'capture count'
        _board : holds the state of the board in string representation
        _valid_directions : lists the valid directions a player can push ['L', 'R', 'F', 'B']
        _winner : the winner of the game; initialized as None
        _current_turn : the player who is allowed to make a move; initialized as None
        _forbidden_move : dict with 'coordinates' and 'direction' as keys; an illegal move that repeats last position

    Methods:
        get_current_turn() --> playername
        make_move(playername, coordinates, direction) --> boolean
        push_marble(coordinates, direction)
        push_marble_horizontal(coordinates, direction)
        push_marble_vertical(coordinates, direction)
        is_valid_move(playername, coordinates, direction) --> boolean
        is_valid_playername(playername) --> boolean
        is_valid_coordinates(coordinates) --> boolean
        is_valid_direction(direction) --> boolean
        set_forbidden_move(coordinates, direction)
        is_forbidden_move(coordinates, direction) --> boolean
        is_game_over() --> boolean
        get_winner() --> playername
        check_for_winner() --> boolean
        check_for_player_with_7_captures() --> boolean
        check_for_player_with_no_pieces() --> boolean
        check_for_player_that_cannot_move() --> boolean
        can_current_player_move() --> boolean
        can_marble_be_pushed(coordinates, direction) --> boolean
        can_marble_be_pushed_horizontal(coordinates, direction, marble_color) --> boolean
        can_marble_be_pushed_vertical(coordinates, direction, marble_color) --> boolean
        switch_turns()
        get_playernames()
        get_captured(playername) --> captured pieces as int
        handle_captured_piece(captured_piece_color)
        get_marble(coordinates) --> marble color ["W", "B", "R"]
        get_marble_count() --> tuple of ints (num_white, num_black, num_red)
    """

    def __init__(self, player_one, player_two):
        """Initialize the KubaGame data members
        Parameters:
            player_one : ('Player One Name', 'W')
            player_two : ('Player Two Name', 'B')
        Returns:
            None
        """
        self._players = {
            player_one[0]: {
                "name": player_one[0],
                "color": player_one[1],
                "capture count": 0
            },
            player_two[0]: {
                "name": player_two[0],
                "color": player_two[1],
                "capture count": 0
            }
        }
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
        # Forbidden move is an illegal move that repeats the previous position
        self._forbidden_move = {"coordinates": (),
                                "direction": ""}

    def get_current_turn(self):
        """Returns the player name corresponding to who's turn it is, or None if game hasn't started yet

        Parameters:
            N/A
        Returns:
            string value playername stored in _current_turn, or None if game hasn't started
        """
        return self._current_turn

    def make_move(self, playername, coordinates, direction):
        """Attempts to make a move for playername by pushing marble at coordinates in the given direction.

        Parameters:
            playername : name of player attempting to make move
            coordinates : coordinates of marble to be pushed as a tuple (row, column)
            direction : one index in _valid_directions

        Returns:
            A boolean value based on if move was actually made
        """
        if not self.is_valid_move(playername, coordinates, direction):
            return False

        self._current_turn = playername  # Needed for the first turn only
        self.push_marble(coordinates, direction)
        self.switch_turns()
        self.check_for_winner()

        return True

    def push_marble(self, coordinates, direction):
        """Pushes marble at 'coordinates' in 'direction' on _board

        Parameters:
            coordinates : coordinates of marble to be pushed as a tuple (row, column)
            direction : one index in _valid_directions

        Returns:
            None
        """
        if direction == "L" or direction == "R":
            self.push_marble_horizontal(coordinates, direction)

        if direction == "F" or direction == "B":
            self.push_marble_vertical(coordinates, direction)

    def push_marble_horizontal(self, coordinates, direction):
        """Pushes marble at 'coordinates' in direction 'L' or 'R' on _board

        Parameters:
            coordinates : coordinates of marble to be pushed as a tuple (row, column)
            direction : 'L' or 'R'

        Returns:
            None
        """
        row = coordinates[0]
        column = coordinates[1]
        pointer = column
        variable_dict = {
            "L": {
                "step": -1,
                "boundary": 0,
                "forbidden direction": "R"
            },
            "R": {
                "step": 1,
                "boundary": 6,
                "forbidden direction": "L"
            }
        }
        step = variable_dict[direction]["step"]
        boundary = variable_dict[direction]["boundary"]

        while 0 <= pointer <= 6:
            pointer += step
            if self._board[row][pointer] == "X":
                self._board[row].pop(pointer)
                self._board[row].insert(column, "X")
                self.set_forbidden_move((row, pointer), variable_dict[direction]["forbidden direction"])
                return None

            if pointer == boundary:
                captured_piece_color = self.get_marble((row, pointer))
                self.handle_captured_piece(captured_piece_color)
                self._board[row].pop(pointer)
                self._board[row].insert(column, "X")
                self.set_forbidden_move((), "")  # No forbidden moves, piece can not come back
                return None

    def push_marble_vertical(self, coordinates, direction):
        """Pushes marble at 'coordinates' in direction 'F' or 'B' on _board

        Parameters:
            coordinates : coordinates of marble to be pushed as a tuple (row, column)
            direction : 'F' or 'B'

        Returns:
            None
        """
        row = coordinates[0]
        column = coordinates[1]
        pointer = row
        variable_dict = {
            "F": {
                "step": -1,
                "boundary": 0,
                "forbidden direction": "B"
            },
            "B": {
                "step": 1,
                "boundary": 6,
                "forbidden direction": "F"
            }
        }
        step = variable_dict[direction]["step"]
        boundary = variable_dict[direction]["boundary"]

        while 0 <= pointer <= 6:
            pointer += step
            if self._board[pointer][column] == "X":
                self.set_forbidden_move((pointer, column), variable_dict[direction]["forbidden direction"])
                while pointer != row:
                    self._board[pointer][column] = self._board[pointer - step][column]
                    pointer -= step
                self._board[row][column] = "X"
                return None

            if pointer == boundary:
                captured_piece_color = self.get_marble((pointer, column))
                self.handle_captured_piece(captured_piece_color)  # fix this to handle all captured pieces
                self.set_forbidden_move((), "")  # No forbidden moves, piece can not come back
                while pointer != row:
                    self._board[pointer][column] = self._board[pointer - step][column]
                    pointer -= step
                self._board[row][column] = "X"
                return None

    def is_valid_move(self, playername, coordinates, direction):
        """Checks the validity of a potential move by checking parameters and game rules

        Parameters:
            playername : name of player attempting to make move
            coordinates : coordinates of marble to be pushed as a tuple (row, column)
            direction : one index in _valid_directions

        Returns:
            A boolean value based on if move is valid (input is acceptable and does not violate game rules)
        """
        # Validate Inputs
        if not (self.is_valid_playername(playername)
                and self.is_valid_coordinates(coordinates)
                and self.is_valid_direction(direction)):
            return False

        # Validate no rules are broken
        # Players may not move if game is over
        if self.get_winner() is not None:
            return False

        # Players may only move their own color
        if self.get_marble(coordinates) != self._players[playername]["color"]:
            return False

        # Players may only move on their turn
        if self.get_current_turn(
        ) is not None and self.get_current_turn() != playername:
            return False

        # Players may not push their pieces off the board or repeat the previous position
        if not self.can_marble_be_pushed(coordinates, direction):
            return False

        return True

    def is_valid_playername(self, playername):
        """Verifies that one of the two given player names is being called

        Parameters:
            playername : name of player we want to validate

        Returns:
            a boolean value based on if playername is one of the players
        """
        if playername in self._players:
            return True

        return False

    def is_valid_coordinates(self, coordinates):
        """Verifies that the given coordinates are integers in the correct range, nested in a tuple

        Parameters:
            coordinates : coordinates of marble as a tuple (row, column)

        Returns:
            a boolean value based on if the coordinates are integers in the correct range, nested in a tuple
        """
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
        """Checks if a given direction is a valid input based on _valid_directions

        Parameters:
            direction : one index in _valid_directions

        Returns:
            a boolean value based on if the given direction is in _valid_directions
        """
        if direction in self._valid_directions:
            return True

        return False

    def set_forbidden_move(self, coordinates, direction):
        """Sets the value of _forbidden_move

        Parameters:
            coordinates : coordinates of marble that may not be pushed, as a tuple (row, column)
            direction : one index in _valid_directions
        Returns:
            None
        """
        self._forbidden_move["coordinates"] = coordinates
        self._forbidden_move["direction"] = direction

    def is_forbidden_move(self, coordinates, direction):
        """Returns a boolean based on if the coordinates and direction are the forbidden_move

        Parameters:
            coordinates : coordinates of marble to be checked, as a tuple (row, column)
            direction : one index in _valid_directions

        Returns:
            A boolean based on if the coordinates and direction are the _forbidden_move
        """
        if coordinates == self._forbidden_move["coordinates"] and direction == self._forbidden_move["direction"]:
            return True
        return False

    def is_game_over(self):
        """Returns a boolean value based on if the game is over

        Parameters:
            N/A
        Returns:
            A boolean value based on if the game is over
        """
        self.check_for_winner()

        if self.get_winner() is None:
            return False

        return True

    def get_winner(self):
        """Returns the name of the winner or None if no winner

        Parameters:
            N/A

        Returns:
            _winner (playername string)
        """
        return self._winner

    def check_for_winner(self):
        """Checks for all possible win conditions and sets _winner if win condition is met

        Note: runs after a move is played and turn has been switched.

        Parameters:
            N/A

        Returns:
            None
        """
        if self.check_for_player_with_7_captures():
            return True

        if self.check_for_player_with_no_pieces():
            return True

        if self.check_for_player_that_cannot_move():
            return True

    def check_for_player_with_7_captures(self):
        """Determines if a player has captured 7 pieces and sets _winner if so

        Parameters
            N/A

        Returns:
            a boolean value based on if a player has won or not
        """
        players = self.get_playernames()
        for playername in players:
            if self.get_captured(playername) >= 7:
                self._winner = playername
                return True
        return False

    def check_for_player_with_no_pieces(self):
        """Determines if a player has no pieces on the board and sets _winner if so

        Parameters
            N/A

        Returns:
            a boolean value based on if a player has won or not
        """
        players = self.get_playernames()
        pieces_on_board = self.get_marble_count()
        white_piece_count = pieces_on_board[0]
        black_piece_count = pieces_on_board[1]

        if white_piece_count == 0:  # Black Wins
            for playername in players:
                if self._players[playername]["color"] == "B":
                    self._winner = playername
                    return True

        if black_piece_count == 0:  # White Wins
            for playername in players:
                if self._players[playername]["color"] == "W":
                    self._winner = playername
                    return True

        return False

    def check_for_player_that_cannot_move(self):
        """Determines if _current_turn player cannot move and sets _winner if so

        Parameters
            N/A

        Returns:
            a boolean value based on if a player has won or not
        """
        players = self.get_playernames()
        # Can current_player move? Verify after we know both players have pieces on the board
        if not self.can_current_player_move():
            for playername in players:
                if playername != self.get_current_turn():
                    self._winner = playername
                    return True
        return False

    def can_current_player_move(self):
        """Determines if _current_turn player has any legal moves

        Parameters
            N/A

        Returns:
            a boolean value based on if _current_turn player has any legal moves
        """
        if self._current_turn is None:
            return True

        current_turn_color = self._players[self._current_turn]["color"]
        for row in range(7):
            for column in range(7):
                if self._board[row][column] == current_turn_color:
                    for direction in self._valid_directions:
                        if self.can_marble_be_pushed((row, column), direction):
                            return True
        return False

    def can_marble_be_pushed(self, coordinates, direction):
        """Determines if marble at 'coordinates' can be pushed in 'direction'

        Parameters
            coordinates : coordinates of marble as a tuple (row, column)
            direction : one index in _valid_directions

        Returns:
            a boolean value based on if the marble at 'coordinates' can be pushed in 'direction'
        """
        if not self.is_valid_coordinates(coordinates) or not self.is_valid_direction(direction):
            return False

        if self.is_forbidden_move(coordinates, direction):
            return False

        marble_color = self.get_marble(coordinates)
        if direction == "L" or direction == "R":
            return self.can_marble_be_pushed_horizontal(coordinates, direction, marble_color)

        if direction == "F" or direction == "B":
            return self.can_marble_be_pushed_vertical(coordinates, direction, marble_color)

    def can_marble_be_pushed_horizontal(self, coordinates, direction, marble_color):
        """Determines if marble at 'coordinates' can be pushed in the given horizontal 'direction' ('L' or 'R' only)

        Parameters
            coordinates : coordinates of marble as a tuple (row, column)
            direction : 'L' or 'R' (Left or Right) direction of push
            marble_color : the color of the marble at 'coordinates'

        Returns:
            a boolean value based on if the marble at 'coordinates' can be pushed in the given horizontal direction
        """
        row = coordinates[0]
        column = coordinates[1]
        variable_dict = {
            "L": {
                "step": -1,
                "boundary": 0,
                "opposite boundary": 6
            },
            "R": {
                "step": 1,
                "boundary": 6,
                "opposite boundary": 0
            }
        }
        step = variable_dict[direction]["step"]
        boundary = variable_dict[direction]["boundary"]
        opposite_boundary = variable_dict[direction]["opposite boundary"]

        # Checks the opposite direction of the push for the board edge (boundary) or an empty adjacent space
        if column == opposite_boundary or self._board[row][column - step] == "X":

            # Check that we're not pushing our own piece off the board in the direction of the push
            pointer = column + step
            while 0 <= pointer <= 6:

                # If we find a blank space in the push direction, we can push the stack of marbles this direction
                if self._board[row][pointer] == "X":
                    return True

                # If we reach the edge of the board and the edge marble isn't the current_player's color,
                # Then we can push the stack of marbles this direction
                if pointer == boundary and self._board[row][pointer] != marble_color:
                    return True

                pointer += step
        return False

    def can_marble_be_pushed_vertical(self, coordinates, direction, marble_color):
        """Determines if marble at 'coordinates' can be pushed in the given vertical 'direction' ('F' or 'B' only)

        Parameters
            coordinates : coordinates of marble as a tuple (row, column)
            direction : 'F' or 'B' (Forward or Backward) direction of push
            marble_color : the color of the marble at 'coordinates'

        Returns:
            a boolean value based on if the marble at 'coordinates' can be pushed in the given vertical direction
        """
        row = coordinates[0]
        column = coordinates[1]
        variable_dict = {
            "F": {
                "step": -1,
                "boundary": 0,
                "opposite boundary": 6
            },
            "B": {
                "step": 1,
                "boundary": 6,
                "opposite boundary": 0
            }
        }
        step = variable_dict[direction]["step"]
        boundary = variable_dict[direction]["boundary"]
        opposite_boundary = variable_dict[direction]["opposite boundary"]

        # Checks the opposite direction of the push for the board edge (boundary) or an empty adjacent space
        if row == opposite_boundary or self._board[row - step][column] == "X":

            # Check that we're not pushing our own piece off the board in the direction of the push
            pointer = row + step
            while 0 <= pointer <= 6:

                # If we find a blank space in the push direction, we can push the stack of marbles this direction
                if self._board[pointer][column] == "X":
                    return True

                # If we reach the edge of the board and the edge marble isn't the current_player's color,
                # Then we can push the stack of marbles this direction
                if pointer == boundary and self._board[pointer][column] != marble_color:
                    return True

                pointer += step
        return False

    def switch_turns(self):
        """Switches _current_turn to opposite player

        Parameters:
            N/A

        Returns:
            None
        """
        playernames = self.get_playernames()
        if self._current_turn == playernames[0]:
            self._current_turn = playernames[1]
            return None

        self._current_turn = playernames[0]
        return None

    def get_playernames(self):
        """Returns a list of playernames in _players

        Parameters:
            N/A

        Returns:
            a list of playernames ["player 1", "player 2"]
        """
        players = self._players.keys()
        playernames = []
        for name in players:
            playernames.append(name)

        return playernames

    def get_captured(self, playername):
        """Returns the number of red marbles captured by 'playername'

        Parameters:
            playername : name of a player in _players

        Returns:
            int representing number of red marbles captured by 'playername'
        """
        if self.is_valid_playername(playername):
            return self._players[playername]["capture count"]

        # If playername is not valid, return 0
        return 0

    def handle_captured_piece(self, captured_piece_color):
        """Increments the number of red marbles captured by _current_turn player

        Parameters:
            captured_piece_color : the color of the captured piece ['W', 'B', 'R']

        Returns:
            None
        """
        if captured_piece_color == "R":
            current_turn = self.get_current_turn()
            self._players[current_turn]["capture count"] += 1

    def get_marble(self, coordinates):
        """Returns the color of the marble ['W', 'B', 'R'] at the coordinates (row, column) or "X" if None

        Parameters:
            coordinates : coordinates of board where piece may be, as a tuple (row, column)

        Returns:
            a string representing a piece ['W', 'B', 'R'] or an empty square ['X']
        """
        if self.is_valid_coordinates(coordinates):
            row = coordinates[0]
            column = coordinates[1]
            return self._board[row][column]

    def get_marble_count(self):
        """Returns the number of white, black, and red marbles on the board as a tuple in the order (W, B, R)

        Parameters:
            N/A

        Returns:
            a tuple representing the int number of white, black, and red marbles (W, B, R)
        """
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
    """The main function for KubaGame.py"""
    game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))
    game.get_marble_count()  # returns (8,8,13)
    game.get_captured('PlayerA')  # returns 0

    game.get_winner()  # returns None
    game.make_move('PlayerA', (6, 5), 'L')  # Cannot make this move
    game.get_current_turn()  # returns 'PlayerB' because PlayerA has just played.
    game.get_marble((5, 5))  # returns 'W'


if __name__ == "__main__":
    main()
