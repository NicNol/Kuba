# Author: Nic Nolan
# Date: 05/27/2021
# Description: Unit Tests for KubaGame.py

from KubaGame import KubaGame
import unittest


class TestKubaGame(unittest.TestCase):
    """Contains unit tests for KubaGame.py"""

    def setUp(self):
        """TBD"""
        self.kg = KubaGame(("player1", "W"), ("player2", "B"))

    def tearDown(self):
        """TBD"""
        del self.kg

    def test_make_move(self):
        """TBD"""
        self.assertTrue(self.kg.make_move("player1", (0, 0), "R"))
        self.assertTrue(self.kg.make_move("player2", (0, 6), "B"))
        self.assertTrue(self.kg.make_move("player1", (6, 6), "L"))
        self.assertTrue(self.kg.make_move("player2", (6, 0), "F"))

        self.assertFalse(self.kg.make_move("player2", (5, 0), "R"))  # Repeat Turn
        self.assertFalse(self.kg.make_move("player1", (-1, 0), "R"))  # Coordinates Out of Bounds
        self.assertFalse(self.kg.make_move("player1", (7, 0), "R"))  # Coordinates Out of Bounds
        self.assertFalse(self.kg.make_move("player1", (0, -1), "R"))  # Coordinates Out of Bounds
        self.assertFalse(self.kg.make_move("player1", (0, 7), "R"))  # Coordinates Out of Bounds
        self.assertFalse(self.kg.make_move("player1", (1, 0), "N"))  # Invalid Direction
        self.assertFalse(self.kg.make_move("player3", (1, 0), "R"))  # Invalid player name

    def test_push_marble(self):
        """TBD"""
        self.kg.make_move("player1", (0, 0), "R")
        board = [["X", "W", "W", "X", "X", "B", "B"],
                 ["W", "W", "X", "R", "X", "B", "B"],
                 ["X", "X", "R", "R", "R", "X", "X"],
                 ["X", "R", "R", "R", "R", "R", "X"],
                 ["X", "X", "R", "R", "R", "X", "X"],
                 ["B", "B", "X", "R", "X", "W", "W"],
                 ["B", "B", "X", "X", "X", "W", "W"]]
        self.assertEqual(self.kg._board, board)

        self.kg.make_move("player2", (1, 6), "L")
        board = [["X", "W", "W", "X", "X", "B", "B"],
                 ["W", "W", "X", "R", "B", "B", "X"],
                 ["X", "X", "R", "R", "R", "X", "X"],
                 ["X", "R", "R", "R", "R", "R", "X"],
                 ["X", "X", "R", "R", "R", "X", "X"],
                 ["B", "B", "X", "R", "X", "W", "W"],
                 ["B", "B", "X", "X", "X", "W", "W"]]
        self.assertEqual(self.kg._board, board)

        self.kg.make_move("player1", (1, 0), "B")
        board = [["X", "W", "W", "X", "X", "B", "B"],
                 ["X", "W", "X", "R", "B", "B", "X"],
                 ["W", "X", "R", "R", "R", "X", "X"],
                 ["X", "R", "R", "R", "R", "R", "X"],
                 ["X", "X", "R", "R", "R", "X", "X"],
                 ["B", "B", "X", "R", "X", "W", "W"],
                 ["B", "B", "X", "X", "X", "W", "W"]]
        self.assertEqual(self.kg._board, board)

        self.kg.make_move("player2", (1, 4), "B")
        board = [["X", "W", "W", "X", "X", "B", "B"],
                 ["X", "W", "X", "R", "X", "B", "X"],
                 ["W", "X", "R", "R", "B", "X", "X"],
                 ["X", "R", "R", "R", "R", "R", "X"],
                 ["X", "X", "R", "R", "R", "X", "X"],
                 ["B", "B", "X", "R", "R", "W", "W"],
                 ["B", "B", "X", "X", "X", "W", "W"]]
        self.assertEqual(self.kg._board, board)

    def test_is_valid_move(self):
        """TBD"""
        self.assertTrue(self.kg.is_valid_move("player1", (0, 0), "R"))
        self.assertTrue(self.kg.is_valid_move("player2", (0, 6), "B"))
        self.assertTrue(self.kg.is_valid_move("player1", (6, 6), "L"))
        self.assertTrue(self.kg.is_valid_move("player2", (6, 0), "F"))

        self.assertFalse(self.kg.is_valid_move("player1", (-1, 0), "R"))  # Coordinates Out of Bounds
        self.assertFalse(self.kg.is_valid_move("player1", (7, 0), "R"))  # Coordinates Out of Bounds
        self.assertFalse(self.kg.is_valid_move("player1", (0, -1), "R"))  # Coordinates Out of Bounds
        self.assertFalse(self.kg.is_valid_move("player1", (0, 7), "R"))  # Coordinates Out of Bounds
        self.assertFalse(self.kg.is_valid_move("player1", (1, 0), "N"))  # Invalid Direction
        self.assertFalse(self.kg.is_valid_move("player3", (1, 0), "R"))  # Invalid player name

    def test_set_forbidden_move(self):
        """TBD"""
        self.kg.set_forbidden_move((0, 0), "R")
        self.assertEqual(self.kg._forbidden_move["coordinates"], (0, 0))
        self.assertEqual(self.kg._forbidden_move["direction"], "R")

    def test_is_forbidden_move(self):
        """TBD"""
        self.kg.set_forbidden_move((0, 0), "R")
        false_1 = self.kg.is_forbidden_move((1, 0), "R")
        false_2 = self.kg.is_forbidden_move((0, 1), "R")
        false_3 = self.kg.is_forbidden_move((0, 0), "L")
        true_1 = self.kg.is_forbidden_move((0, 0), "R")

        self.assertFalse(false_1)
        self.assertFalse(false_2)
        self.assertFalse(false_3)
        self.assertTrue(true_1)

    def test_get_current_turn(self):
        """TBD"""
        self.assertIsNone(self.kg.get_current_turn())
        self.kg._current_turn = "player1"
        self.assertEqual(self.kg.get_current_turn(), "player1")
        self.kg._current_turn = "player2"
        self.assertEqual(self.kg.get_current_turn(), "player2")

    def test_is_game_over(self):
        """TBD"""
        self.assertIsNone(self.kg._winner)
        self.kg._players["player1"]["capture count"] = 7
        self.assertTrue(self.kg.is_game_over())
        self.assertEqual(self.kg._winner, "player1")
        # Tear Down
        self.kg._players["player1"]["capture count"] = 0
        self.kg._winner = None
        self.assertFalse(self.kg.is_game_over())

        self.kg._board = [["X", "X", "X", "X", "X", "B", "B"],
                          ["X", "X", "X", "R", "X", "B", "B"],
                          ["X", "X", "R", "R", "R", "X", "X"],
                          ["X", "R", "R", "R", "R", "R", "X"],
                          ["X", "X", "R", "R", "R", "X", "X"],
                          ["B", "B", "X", "R", "X", "X", "X"],
                          ["B", "B", "X", "X", "X", "X", "X"]]
        self.assertTrue(self.kg.is_game_over())
        self.assertEqual(self.kg._winner, "player2")
        # Tear Down
        self.kg._board = [["W", "W", "X", "X", "X", "B", "B"],
                          ["W", "W", "X", "R", "X", "B", "B"],
                          ["X", "X", "R", "R", "R", "X", "X"],
                          ["X", "R", "R", "R", "R", "R", "X"],
                          ["X", "X", "R", "R", "R", "X", "X"],
                          ["B", "B", "X", "R", "X", "W", "W"],
                          ["B", "B", "X", "X", "X", "W", "W"]]
        self.kg._winner = None
        self.assertFalse(self.kg.is_game_over())

        self.kg._board = [["X", "X", "X", "X", "X", "X", "X"],
                          ["X", "X", "X", "X", "X", "X", "X"],
                          ["X", "X", "X", "W", "X", "X", "X"],
                          ["X", "X", "W", "B", "W", "X", "X"],
                          ["X", "X", "X", "W", "X", "X", "X"],
                          ["X", "X", "X", "X", "X", "X", "X"],
                          ["X", "X", "X", "X", "X", "X", "X"]]
        self.kg._current_turn = "player2"
        self.assertTrue(self.kg.is_game_over())
        self.assertEqual(self.kg._winner, "player1")
        # Tear Down
        self.kg._board = [["W", "W", "X", "X", "X", "B", "B"],
                          ["W", "W", "X", "R", "X", "B", "B"],
                          ["X", "X", "R", "R", "R", "X", "X"],
                          ["X", "R", "R", "R", "R", "R", "X"],
                          ["X", "X", "R", "R", "R", "X", "X"],
                          ["B", "B", "X", "R", "X", "W", "W"],
                          ["B", "B", "X", "X", "X", "W", "W"]]
        self.kg._winner = None
        self.assertFalse(self.kg.is_game_over())


if __name__ == '__main__':
    unittest.main()
