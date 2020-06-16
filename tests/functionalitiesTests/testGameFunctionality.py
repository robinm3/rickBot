import unittest

from pymessenger import Bot

import constants
from application.dbAccess.pyMongo import setInDB, deleteFromDB, getInDB
from application.functionalities.gameFunctionality import GameFunctionality


class TestGameFunctionality(unittest.TestCase):
    """
    Tests the GameFunctionality class
    """

    SENDER_ID = "1"
    bot = Bot(constants.PAGE_ACCESS_TOKEN)
    categories = {"number": str(2)}
    payload = None
    functionality = GameFunctionality(SENDER_ID, bot, categories, payload)

    def test_TicTacToeResponse(self):
        categories = {"response": "oui"}
        functionality = GameFunctionality(
            self.SENDER_ID, self.bot, categories, self.payload
        )
        deleteFromDB(self.SENDER_ID)
        setInDB(self.SENDER_ID, {"game": "ticTacToe"})
        response = functionality.getResponse()
        self.assertEqual("text_message", response["type"])
        self.assertIsInstance(response["message"], str)
        self.assertIsNotNone(getInDB(self.SENDER_ID, "grid"))

    def test_TicTacToeGameStarted(self):
        deleteFromDB(self.SENDER_ID)
        setInDB(
            self.SENDER_ID,
            {"grid": [["0", "1", "2"], ["3", "4", "5"], ["6", "7", "8"]]},
        )
        response = self.functionality.continuePlayingTicTacToe()
        self.assertIsInstance(response, str)

        setInDB(self.SENDER_ID, {"grid": None})
