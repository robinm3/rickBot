import unittest

from pymessenger import Bot
import app
from application.dbAccess.pyMongo import setInDB, deleteFromDB
from application.functionalities.newsFunctionality import NewsFunctionality


class TestNewsFunctionality(unittest.TestCase):
    """
    Tests the NewsFunctionality class
    """
    SENDER_ID = '1'
    bot = Bot(app.PAGE_ACCESS_TOKEN)
    categories = {"newsType": "coronavirus", "frequence": "jour"}
    functionality = NewsFunctionality(SENDER_ID, bot, categories)

    def test_getResponse(self):
        # check default message and type
        deleteFromDB(self.SENDER_ID)
        response = self.functionality.getResponse()
        self.assertEqual("generic_message", response['type'])
        self.assertTrue(len(response['message']) != 0)

    def test_getResponseRecurrence(self):
        deleteFromDB(self.SENDER_ID)
        response = self.functionality.getResponse()
        self.assertEqual("generic_message", response['type'])
        self.assertTrue(len(response['message']) != 0)
        setInDB(self.SENDER_ID, {"newsRecurrence": None})


if __name__ == '__main__':
    unittest.main()
