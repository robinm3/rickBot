import unittest

from pymessenger import Bot
import constants
from application.dbAccess.pyMongo import setInDB
from application.functionalities.locationFunctionality import LocationFunctionality


class TestLocationFunctionality(unittest.TestCase):
    """
    Tests the LocationFunctionality class
    """

    SENDER_ID = "1"
    bot = Bot(constants.PAGE_ACCESS_TOKEN)
    categories = {"location": "Canada"}
    functionality = LocationFunctionality(SENDER_ID, bot, categories)

    def test_getResponse_whenNotChangingLocation(self):
        # check default message and type
        setInDB(self.SENDER_ID, {"question": None})
        setInDB(self.SENDER_ID, {"location": "Canada"})
        response = self.functionality.getResponse()
        self.assertEqual(
            "Ok, donc je garde Canada en note comme étant ta localisation!",
            response["message"],
        )
        self.assertEqual("text_message", response["type"])

    def test_getResponse_whenNewLocation(self):
        # check default message and type
        setInDB(self.SENDER_ID, {"question": None})
        setInDB(self.SENDER_ID, {"location": "India"})
        response = self.functionality.getResponse()
        self.assertEqual(
            "Ta localisation jusqu'à maintenant était India"
            ", est-ce que tu veux la changer?",
            response["message"],
        )
        self.assertEqual("text_message", response["type"])
        setInDB(self.SENDER_ID, {"location": "Canada"})

    def test_getResponse_whenChangingLocation(self):
        # check default message and type
        setInDB(
            self.SENDER_ID,
            {"question": "location", "response": "Canada", "location": "India"},
        )
        response = self.functionality.getResponse()
        self.assertEqual(
            "Ok, donc je garde Canada en note comme étant ta localisation!",
            response["message"],
        )
        self.assertEqual("text_message", response["type"])
        setInDB(self.SENDER_ID, {"location": "Canada"})

    def test_getResponse_whenNotChangingLocation(self):
        # check default message and type
        setInDB(
            self.SENDER_ID,
            {"question": "location", "response": "India", "location": "India"},
        )
        response = self.functionality.getResponse()
        self.assertEqual("Ah, ok. Donc on ne change pas", response["message"])
        self.assertEqual("text_message", response["type"])
        setInDB(self.SENDER_ID, {"location": "Canada"})

    def test_getCategoryValue(self):
        # get the value for a category
        value = self.functionality.getCategoryValue("location")
        self.assertEqual("Canada", value)


if __name__ == "__main__":
    unittest.main()
