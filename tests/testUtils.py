import unittest
from application.dbAccess.pyMongo import setInDB, deleteFromDB
from application.utils import Utils
from application.functionalities.singFunctionality import putNotesEmojisAround


class TestUtils(unittest.TestCase):
    """
    Tests the Utils class
    """

    SENDER_ID = "1"
    someTextSent = "Hey"
    MESSAGING_EVENT_EXAMPLE = {
        "sender": {"id": "1"},
        "recipient": {"id": "1"},
        "timestamp": 1589741756249,
        "message": {
            "mid": "m_tNQZfCSPWbqdyv51mNsIHJ5LlpwnCaIRAbkiYStxbpo2G8q06-WX5lQ8OanDJnrFFQb50H0KPmqlksVml-ybQw",
            "text": someTextSent,
        },
    }
    utilities = Utils(SENDER_ID, MESSAGING_EVENT_EXAMPLE)

    def test_process_NewsType(self):
        self.utilities.resetValues()
        self.utilities.witCategories = {"newsType"}
        response = self.utilities.process()
        self.assertEqual("text_message", response["type"])

    def test_process_Question(self):
        self.utilities.resetValues()
        someTextSent = "Vrai ou faux?"
        MESSAGING_EVENT_EXAMPLE = {
            "sender": {"id": "1"},
            "recipient": {"id": "1"},
            "timestamp": 1589741756249,
            "message": {
                "mid": "m_tNQZfCSPWbqdyv51mNsIHJ5LlpwnCaIRAbkiYStxbpo2G8q06-WX5lQ8OanDJnrFFQb50H0KPmqlksVml-ybQw",
                "text": someTextSent,
            },
        }
        utilities = Utils(self.SENDER_ID, MESSAGING_EVENT_EXAMPLE)
        response = utilities.process()
        self.assertEqual("text_message", response["type"])
        self.assertIn(response["message"], ["Vrai", "faux"])

    def test_witCategories_NewsType(self):
        self.utilities.resetValues()
        self.utilities.messageFromUser = "nouvelles"
        self.utilities.setWitCategories()
        self.assertIn("newsType", self.utilities.witCategories)

    def test_witCategories_Question(self):
        self.utilities.resetValues()
        self.utilities.messageFromUser = "ça va?"
        self.utilities.setWitCategories()
        self.assertIn("question", self.utilities.witCategories)

    def test_getMessageResponse_NewsType(self):
        self.utilities.resetValues()
        self.utilities.witCategories = {"newsType"}
        response = self.utilities.getMessageResponse()
        self.assertEqual("generic_message", response["type"])

    def test_getMessageResponse_Sing(self):
        deleteFromDB(self.SENDER_ID)
        self.utilities.resetValues()
        self.utilities.witCategories = {"rickSong": "We're no strangers to love"}
        response = self.utilities.getMessageResponse()
        self.assertEqual("text_message", response["type"])
        self.assertEqual(
            putNotesEmojisAround("You know the rules and so do I"), response["message"]
        )

    def test_getMessageResponse_ChoiceQuestions(self):
        self.utilities.resetValues()
        self.utilities.witCategories = {"question": ["Quelle", "?"]}
        response = self.utilities.getMessageResponse()
        self.assertEqual("text_message", response["type"])
        self.assertIn(
            response["message"],
            [
                "Je dirais exactement comme la jument blanche de Napoléon",
                "La 4e à ta gauche",
                "Hmmm. Bonne question. Si j'avais le choix, je pense que je choisirais celle qui est la même que le "
                "fils unique de la fille unique de ma grand-mère",
                "La patate à Mononc' Serge",
            ],
        )

    def test_getMessageResponse_ToughQuestions(self):
        self.utilities.resetValues()
        self.utilities.witCategories = {"choice": ["no", "yes"]}
        response = self.utilities.getMessageResponse()
        self.assertEqual("text_message", response["type"])
        self.assertIn(
            response["message"], ["no", "yes", "Trop difficile comme choix, ça!"]
        )

    def test_getMessageResponse_Games(self):
        self.utilities.resetValues()
        self.utilities.witCategories = {"game": "tic-tac-toe"}
        response = self.utilities.getMessageResponse()
        self.assertEqual("text_message", response["type"])
        setInDB(self.SENDER_ID, {"state": None, "play": False, "game": None})

    def test_getMessageResponse_GamesAcceptStart(self):
        self.utilities.resetValues()
        self.utilities.witCategories = {"response": "oui"}
        setInDB(self.SENDER_ID, {"state": {"game": "ticTacToe"}})
        response = self.utilities.getMessageResponse()
        self.assertEqual("text_message", response["type"])
        setInDB(self.SENDER_ID, {"state": None, "play": False, "game": None})

    def test_getMessageResponse_GamesAlreadyStarted(self):
        self.utilities.resetValues()
        self.utilities.witCategories = {"game": "tic-tac-toe"}
        setInDB(self.SENDER_ID, {"state": {"game": "ticTacToe"}})
        response = self.utilities.getMessageResponse()
        self.assertEqual("text_message", response["type"])
        setInDB(self.SENDER_ID, {"state": None, "play": False, "game": None})

    def test_getMessageResponse_WhatCanYouDo(self):
        self.utilities.resetValues()
        self.utilities.witCategories = {
            "whatCanYouDo": "faire",
            "question": "qu'est-ce que tu peux faire?",
        }
        response = self.utilities.getMessageResponse()
        self.assertEqual("text_message", response["type"])

    def test_setMessageFromUser(self):
        self.utilities.resetValues()
        self.assertNotEqual("Hey", self.utilities.messageFromUser)
        self.utilities.setMessageFromUser()
        self.assertEqual("Hey", self.utilities.messageFromUser)

    def test_getEventType(self):
        self.utilities.resetValues()
        self.assertEqual("message", self.utilities.getEventType())

    def test_getResponseToSend(self):
        self.utilities.resetValues()
        response = self.utilities.getResponseToSend("message")
        self.assertEqual("text_message", response["type"])
        self.assertIsInstance(response["message"], str)


if __name__ == "__main__":
    unittest.main()
