import random
import emojis
from application.dbAccess.pyMongo import setInDB, getInDB
from application.functionalities.functionality import Functionality


class SmallTalkFunctionality(Functionality):
    def setResponse(self):
        self.messageToSend = self.getMessageToSend()
        self.messageType = "text_message"

    def getMessageToSend(self):
        messageToSend = ""
        categories = self.categories
        if getInDB(self.senderId, "question") or (
            "response" in self.categories
            and self.categories["response"]
            in ("correct", "bof", "je ne sais pas", "non", "pas bien", "mal")
        ):
            messageToSend = self.getResponseContinueWithQuestion()
            if (
                getInDB(self.senderId, "question") == "howAreYou2"
                and "question" in categories
            ):
                messageToSend += random.choice(
                    [
                        "Ça va, merci",
                        "Je sais pas trop, il y a rien de facile ces temps-ci. ",
                        "Je vais bien. Ça va bien aller.",
                        "Ça va correct, merci",
                    ]
                )
        elif "lifeIsDead" in categories:
            messageToSend = "Tout à fait d'accord avec toi"
        elif "greetings" in categories:
            messageToSend = self.getGreetingsResponse()
        elif "response" in categories:
            messageToSend = self.getContinueHowAreYouQuestion()
        if "whatCanYouDo" in categories:
            messageToSend = ""
            if (
                "es-tu" in categories["whatCanYouDo"]
                or "es tu" in categories["whatCanYouDo"]
            ):
                messageToSend = "Je suis RickBot! "
            if random.choice([True, False]):
                messageToSend = {
                    "RICKROLL": ["Voici ce que je peux faire: ", "Clique ici"]
                }
            else:
                messageToSend += getWhatCanYouDoResponse()
        elif getInDB(self.senderId, "question2") and "response" in self.categories:
            setInDB(self.senderId, {"question": "howAreYou"})
            messageToSend = self.getResponseContinueWithQuestion()
            if "question" in categories:
                messageToSend += ". De mon côté, "
                messageToSend += random.choice(
                    [
                        "ça va, merci",
                        "je sais pas trop, il y a rien de facile ces temps-ci. ",
                        "je vais bien. Ça va bien aller.",
                        "ça va correct, merci",
                    ]
                )
            setInDB(self.senderId, {"question2": None})
        elif "question" in categories:
            if (
                "?" in categories.get("question")
                and len(categories.get("question")) == 1
            ):
                messageToSend = random.choice(
                    ["oui", "non", "je sais pas", "peut-être"]
                )
            elif "vie" in categories.get("question"):
                messageToSend = "la vie est morte, voilà la vérité"
            else:
                messageToSend += random.choice(
                    [
                        "Ça va, toi?",
                        "Je sais pas trop, il y a rien de facile ces temps-ci"
                        + emojis.SWEAT_SMILE
                        + ". Toi?",
                        "Je vais bien. Ça va bien aller"
                        + emojis.RAINBOW
                        + ". Toi, comment tu "
                        "vas?",
                        "Ça va correct, toi?",
                    ]
                )
                setInDB(self.senderId, {"question": "howAreYou"})
        elif not messageToSend:
            messageToSend = random.choice(
                [
                    "ah, ok",
                    "hahaha, quoi!?" + emojis.SURPRISED_MONKEY,
                    "je comprends pas ce que tu veux dire" + emojis.SWEAT_SMILE,
                    "ah ben là là" + emojis.SWEAT_SMILE,
                    emojis.THUMBS_UP,
                ]
            )
        return messageToSend

    def getResponseContinueWithQuestion(self):
        getInDB(self.senderId, "question")
        if "response" in self.categories:
            setInDB(self.senderId, {"question": None})
            messageToSend = self.getContinueHowAreYouQuestion()
        else:
            setInDB(self.senderId, {"question": None})
            messageToSend = {"RICKROLL": ["hmm, ok", "voici ce que je pense"]}
        return messageToSend

    def getGreetingsResponse(self):
        value = self.categories["greetings"]
        if value == "wazza":
            messageToSend = "wazzaa \n wazzaaaa"
        else:
            messageToSend = random.choice(
                [value, "Yo!", "Salut!", "Hey! "]
            ) + random.choice([" ça va?", " comment tu vas?", " what's up?"])
            setInDB(self.senderId, {"question2": "howAreYou2"})
        return messageToSend

    def getContinueHowAreYouQuestion(self):
        if self.categories["response"] in (
            "correct",
            "je ne sais pas",
            "non",
            "pas bien",
            "mal",
        ):
            messageToSend = random.choice(
                [
                    "Ah, dsl" + emojis.SWEAT_SMILE + ". J'espère que tu iras mieux",
                    "Ah" + emojis.CRYING_FACE + "J'espère que ça ira mieux",
                ]
            )
        elif self.categories["response"] in ("pas grand chose", "nothing much", "meh"):
            messageToSend = random.choice(["Same", "Pareil pour moi"])
        else:
            messageToSend = random.choice(
                [
                    "Tant mieux!",
                    "Et ben. Ça va bien aller " + emojis.RAINBOW + ", comme on dit",
                    "Tout va bien alors " + emojis.HAPPY_FACE + "!",
                ]
            )
        return messageToSend


def getWhatCanYouDoResponse():
    return (
        "Je peux t'envoyer des nouvelles du COVID-19, te parler un peu, jouer au tic tac toe avec toi, chanter "
        "'Never gonna give you up', répondre à tes questions, tout aussi étranges soit-elles, et même choisir pour "
        "toi(si tu me donnes des choix, évidemment) " + emojis.SMILEY_FACE + " !"
    )
