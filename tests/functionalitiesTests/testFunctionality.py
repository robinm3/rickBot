import unittest

from application.functionalities.functionality import Functionality
from pymessenger import Bot
import constants


class TestFunctionality(unittest.TestCase):
    """
    Tests the Utils class
    """
    SENDER_ID = '1'
    bot = Bot(constants.PAGE_ACCESS_TOKEN)
    categories = {"newsType": "coronavirus"}
    functionality = Functionality(SENDER_ID, bot, categories)

    def test_getResponse(self):
        # check default message and type
        response = self.functionality.getResponse()
        self.assertEqual("huh!?", response['message'])
        self.assertEqual("text_message", response['type'])

    def test_getCategoryValue(self):
        # get the value for a category
        value = self.functionality.getCategoryValue("newsType")
        self.assertEqual("coronavirus", value)


if __name__ == '__main__':
    unittest.main()
