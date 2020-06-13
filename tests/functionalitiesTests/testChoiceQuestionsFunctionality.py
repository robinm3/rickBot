import unittest

from pymessenger import Bot
import constants
from application.functionalities.choiceQuestionsFunctionality import (
    ChoiceQuestionsFunctionality,
)


class TestWeirdQuestionsFunctionality(unittest.TestCase):
    """
    Tests the NewsFunctionality class
    """

    SENDER_ID = "1"
    bot = Bot(constants.PAGE_ACCESS_TOKEN)
    categories = {"choice": ["vrai", "faux"]}
    functionality = ChoiceQuestionsFunctionality(SENDER_ID, bot, categories)

    def test_getResponse(self):
        response = self.functionality.getResponse()
        self.assertEqual("text_message", response["type"])
        self.assertIn(
            response["message"], ["vrai", "faux", "Trop difficile comme choix, ça!"]
        )

    def test_getResponseWithOnlyOneChoice(self):
        newCategories = {"choice": "pas de choix"}
        functionality = ChoiceQuestionsFunctionality(
            self.SENDER_ID, self.bot, newCategories
        )
        response = functionality.getResponse()
        self.assertEqual("text_message", response["type"])
        self.assertIn(
            response["message"], ["pas de choix", "Trop difficile comme choix, ça!"]
        )


if __name__ == "__main__":
    unittest.main()
