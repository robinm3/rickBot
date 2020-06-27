from application.dbAccess.pyMongo import getInDB, setInDB
from application.functionalities.functionality import Functionality
import emojis


class FavoriteThingFunctionality(Functionality):
    def __init__(self, senderId, bot, categories):
        super().__init__(senderId, bot, categories)
        self.newFavorite = ""
        self.oldFavorite = ""
        self.newFavoriteType = ""

    def setResponse(self):
        self.messageToSend = self.getMessageToSend()
        self.messageType = "text_message"

    def getMessageToSend(self):
        categories = self.categories
        senderId = self.senderId
        question = []
        if getInDB(senderId, "question"):
            question = getInDB(senderId, "question")
        setInDB(senderId, {"question": None})
        if "favorite" in question:
            messageToSend = self.continueQuestion()
        else:
            self.newFavorite = str(categories.get("favorite"))
            self.newFavoriteType = str(categories.get("favoriteType"))
            if (type(getInDB(senderId, "favorite")) == dict) and (
                getInDB(senderId, "favorite").get(self.newFavoriteType)
                != self.newFavorite
            ):
                messageToSend = self.askToChangeFavorite()
            elif "favorite" in categories and "favoriteType" in categories:
                messageToSend = self.setNewFavoriteInDb()
            else:
                messageToSend = self.continueQuestion()
        return messageToSend

    def askToChangeFavorite(self):
        newFavorite = self.newFavorite
        newFavoriteType = self.newFavoriteType
        senderId = self.senderId
        if (type(getInDB(senderId, "favorite")) == dict) and (
            getInDB(senderId, "favorite").get(self.newFavoriteType)
        ):
            oldFavorite = getInDB(senderId, "favorite").get(self.newFavoriteType)
        else:
            oldFavorite = "inconnue"
        messageToSend = str(
            "Hmmm...si je me souviens bien...{0} préféré(e) pour l'instant est {1}! "
            "Est-ce que tu veux changer?"
        ).format(newFavoriteType, oldFavorite)
        if newFavorite:
            setInDB(
                senderId,
                {
                    "question": "favorite",
                    "type": newFavoriteType,
                    "response": newFavorite,
                },
            )
        return messageToSend

    def setNewFavoriteInDb(self):
        newFavorite = self.newFavorite
        newFavoriteType = self.newFavoriteType
        senderId = self.senderId
        setInDB(
            senderId,
            {
                "favorite": {self.newFavoriteType: newFavorite},
                "response": None,
                "question": None,
                "type": None,
            },
        )
        return "Ok, donc je garde {0} en note pour {1} préféré(e)!".format(
            newFavorite, newFavoriteType
        )

    def continueQuestion(self):
        senderId = self.senderId
        self.newFavorite = getInDB(senderId, "response")
        self.newFavoriteType = getInDB(senderId, "type")
        if self.acceptNewFavorite() and self.newFavorite and self.newFavorite != "None":
            messageToSend = self.setNewFavoriteInDb()
        elif (
            self.newFavoriteType
            and self.newFavoriteType != "None"
            and self.categories.get("favorite")
        ):
            self.newFavorite = self.categories.get("favorite")
            messageToSend = self.setNewFavoriteInDb()
        elif (
            self.newFavoriteType
            and self.newFavoriteType != "None"
            and self.categories.get("response")
            and "oui" not in self.getCategoryValue("response")
            and "correct" not in self.getCategoryValue("response")
            and "bien sûr" not in self.getCategoryValue("response")
            and "non" not in self.getCategoryValue("response")
        ):
            self.newFavorite = self.categories.get("response")
            messageToSend = self.setNewFavoriteInDb()
        elif self.acceptNewFavorite():
            messageToSend = self.askNewFavorite()
        else:
            messageToSend = "Ah, ok. Donc on ne change pas"
            setInDB(senderId, {"response": None, "question": None, "type": None})
        return messageToSend

    def acceptNewFavorite(self):
        acceptFavorite = False
        for i in ("oui", "correct", "bien sûr"):
            if i in self.getCategoryValue("response"):
                acceptFavorite = True
        return acceptFavorite or self.categories.get("favorite") == self.newFavorite

    def askNewFavorite(self):
        messageToSend = "Good! Donc, quel est ton/ta {0} préféré(e)?".format(
            self.newFavoriteType
        )
        setInDB(
            self.senderId,
            {"question": "favorite", "type": self.newFavoriteType, "response": None,},
        )
        return messageToSend
