import unittest
import emojis
from pymessenger import Bot
import constants
from application.dbAccess.pyMongo import setInDB
from application.functionalities.favoriteThingFunctionality import (
    FavoriteThingFunctionality,
)


class TestFavoriteThingFunctionality(unittest.TestCase):
    """
    Tests the FavoriteThingFunctionality class
    """

    SENDER_ID = "1"
    bot = Bot(constants.PAGE_ACCESS_TOKEN)
    categories = {"favoriteType": "Animal", "favorite": "Chien"}
    functionality = FavoriteThingFunctionality(SENDER_ID, bot, categories)

    def test_getResponse_whenNewFavorite(self):
        setInDB(self.SENDER_ID, {"question": None})
        setInDB(self.SENDER_ID, {"favorite": {"Animal": "Chat"}})
        response = self.functionality.getResponse()
        self.assertEqual(
            "Hmmm...si je me souviens bien...Animal préféré(e) pour l'instant est Chat! Est-ce que tu veux changer?",
            response["message"],
        )
        self.assertEqual("text_message", response["type"])

    def test_getResponse_whenNotChangingFavorite(self):
        setInDB(self.SENDER_ID, {"question": None})
        setInDB(self.SENDER_ID, {"favorite": {"Animal": "Chien"}})
        response = self.functionality.getResponse()
        self.assertEqual(
            "Ok, donc je garde Chien en note pour Animal préféré(e)!",
            response["message"],
        )
        self.assertEqual("text_message", response["type"])

    def test_getResponse_whenChangingFavorite(self):
        categories = {"response": "oui"}
        functionality = FavoriteThingFunctionality(self.SENDER_ID, self.bot, categories)
        setInDB(
            self.SENDER_ID,
            {"question": "favorite", "type": "Animal", "response": "Chat"},
        )
        response = functionality.getResponse()
        self.assertEqual(
            "Ok, donc je garde Chat en note pour Animal préféré(e)!",
            response["message"],
        )
        self.assertEqual("text_message", response["type"])

    def test_getResponse_whenAskingFavorite(self):
        categories = {"favoriteType": "Animal"}
        functionality = FavoriteThingFunctionality(self.SENDER_ID, self.bot, categories)
        setInDB(
            self.SENDER_ID, {"favorite": {"Animal": "chien"}},
        )
        response = functionality.getResponse()
        self.assertEqual(
            "Hmmm...si je me souviens bien...Animal préféré(e) pour l'instant est chien! Est-ce que tu veux changer?",
            response["message"],
        )
        self.assertEqual("text_message", response["type"])


if __name__ == "__main__":
    unittest.main()
