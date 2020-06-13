import unittest

from pymessenger import Bot
import constants
from application.dbAccess.pyMongo import setInDB, deleteFromDB
from application.functionalities.singFunctionality import (
    SingFunctionality,
    putNotesEmojisAround,
)


class TestSingFunctionality(unittest.TestCase):
    """
    Tests the NewsFunctionality class
    """

    SENDER_ID = "1"
    bot = Bot(constants.PAGE_ACCESS_TOKEN)
    categories = {"rickSong": "We're no strangers to love"}
    functionality = SingFunctionality(SENDER_ID, bot, categories)

    def test_getResponse(self):
        deleteFromDB(self.SENDER_ID)
        response = self.functionality.getResponse()
        self.assertEqual("text_message", response["type"])
        self.assertEqual(
            putNotesEmojisAround("You know the rules and so do I"), response["message"]
        )

    def test_getResponseWithDatabase(self):
        deleteFromDB(self.SENDER_ID)
        setInDB(self.SENDER_ID, {"rickPartLastLyrics": 5})
        response = self.functionality.getResponse()
        self.assertEqual("text_message", response["type"])
        self.assertEqual(
            putNotesEmojisAround("Never gonna let you down"), response["message"]
        )


if __name__ == "__main__":
    unittest.main()
