from application.dbAccess.pyMongo import getInDB, setInDB
from application.functionalities.functionality import Functionality


class LocationFunctionality(Functionality):
    def __init__(self, senderId, bot, categories):
        super().__init__(senderId, bot, categories)
        self.newLocation = ""
        self.oldLocation = ""

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
        if "location" in question:
            messageToSend = self.continueQuestion()
        else:
            self.newLocation = str(categories["location"])
            if getInDB(senderId, "location") != self.newLocation:
                messageToSend = self.askToChangeLocation()
            else:
                messageToSend = self.setNewLocationInDb()
        return messageToSend

    def askToChangeLocation(self):
        newLocation = self.newLocation
        senderId = self.senderId
        oldLocation = getInDB(senderId, "location")
        if not oldLocation:
            oldLocation = "inconnue"
        messageToSend = (
            "Ta localisation jusqu'à maintenant était {0}"
            ", est-ce que tu veux la changer?".format(oldLocation)
        )
        setInDB(senderId, {"question": "location", "response": newLocation})
        return messageToSend

    def setNewLocationInDb(self):
        newLocation = self.newLocation
        senderId = self.senderId
        setInDB(senderId, {"location": newLocation})
        return "Ok, donc je garde {0} en note comme étant ta localisation!".format(
            newLocation
        )

    def continueQuestion(self):
        senderId = self.senderId
        self.newLocation = getInDB(senderId, "response")
        if self.acceptNewLocation():
            messageToSend = self.setNewLocationInDb()
        else:
            messageToSend = "Ah, ok. Donc on ne change pas"
        setInDB(senderId, {"response": None})
        return messageToSend

    def acceptNewLocation(self):
        acceptLocation = False
        for i in ("oui", "correct", "bien sûr"):
            if i in self.getCategoryValue("response"):
                acceptLocation = True
        return acceptLocation or self.categories.get("location") == self.newLocation
