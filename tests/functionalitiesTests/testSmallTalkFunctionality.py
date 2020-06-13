import unittest

from pymessenger import Bot
import constants
from application.dbAccess.pyMongo import setInDB, getInDB
from application.functionalities.smallTalkFunctionality import SmallTalkFunctionality


class TestSmallTalkFunctionality(unittest.TestCase):
    """
    Tests the SmallTalkFunctionality class
    """
    SENDER_ID = '1'
    bot = Bot(constants.PAGE_ACCESS_TOKEN)
    categories = {"greetings": "Hey", "response": "bien"}
    functionality = SmallTalkFunctionality(SENDER_ID, bot, categories)

    def test_getResponse(self):
        # check default message and type
        response = self.functionality.getResponse()
        self.assertEqual("text_message", response['type'])
        self.assertEqual("text_message", response['type'])
        self.assertTrue(response['message'])

    def test_getMessageToSend(self):
        messageToSend = self.functionality.getMessageToSend()
        self.assertTrue(messageToSend)
        print(self.categories)
        self.assertNotEqual("ah, ok", messageToSend)

    def test_getMessageToSendIfQuestion(self):
        setInDB(self.SENDER_ID, {"question": "howAreYou"})
        messageToSend = self.functionality.getMessageToSend()
        self.assertFalse(getInDB(self.SENDER_ID, "question"))
        self.assertIn(messageToSend, ['Tant mieux!', 'Et ben. Ça va bien aller, comme on dit',
                                      'Tout va bien alors!'])


if __name__ == '__main__':
    unittest.main()
