import unittest

from pymessenger import Bot

import app
from application.dbAccess.pyMongo import setInDB
from application.functionalities.gameFunctionality import GameFunctionality


class TestGameFunctionality(unittest.TestCase):
    """
    Tests the GameFunctionality class
    """
    SENDER_ID = '1'
    bot = Bot(app.PAGE_ACCESS_TOKEN)
    categories = {"number": str(2)}
    payload = None
    functionality = GameFunctionality(SENDER_ID, bot, categories, payload)

    def test_TicTacToe(self):
        # check default message and type
        setInDB(self.SENDER_ID, {"grid": [["0", "1", "2"], ["3", "4", "5"], ["6", "7", "8"]]})
        response = self.functionality.continuePlayingTicTacToe()
        print(response)
        self.assertIsInstance(response, str)

        setInDB(self.SENDER_ID, {"grid": None})
