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

    def test_get_current_turn(self):
        """TBD"""
        self.assertIsNone(self.kg.get_current_turn())
        self.kg._current_turn = "W"
        self.assertEqual(self.kg.get_current_turn(), "W")
        self.kg._current_turn = "B"
        self.assertEqual(self.kg.get_current_turn(), "B")

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


if __name__ == '__main__':
    unittest.main()
