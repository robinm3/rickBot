import unittest

from pymessenger import Bot
import constants
from application.functionalities.toughQuestionsFunctionality import (
    ToughQuestionsFunctionality,
)


class TestWeirdQuestionsFunctionality(unittest.TestCase):
    """
    Tests the NewsFunctionality class
    """

    SENDER_ID = "1"
    bot = Bot(constants.PAGE_ACCESS_TOKEN)
    categories = {"question": ["Quelle", "?"]}
    functionality = ToughQuestionsFunctionality(SENDER_ID, bot, categories)

    def test_getResponse(self):
        response = self.functionality.getResponse()
        self.assertEqual("text_message", response["type"])
        self.assertIn(
            response["message"],
            [
                "Je dirais exactement comme la jument blanche de Napoléon",
                "La 4e à ta gauche",
                "Hmmm. Bonne question. Si j'avais le choix, je pense que je choisirais celle qui est la même que le "
                "fils unique de la fille unique de ma grand-mère",
                "La même que la patate à Mononc' Serge",
            ],
        )

    def test_getResponseWithOnlyOneChoice(self):
        newCategories = {"question": ["qui", "?"], "whatCanYouDo": "faire"}
        functionality = ToughQuestionsFunctionality(
            self.SENDER_ID, self.bot, newCategories
        )
        response = functionality.getResponse()
        self.assertTrue(response["type"])
        self.assertTrue(response["message"])


if __name__ == "__main__":
    unittest.main()
