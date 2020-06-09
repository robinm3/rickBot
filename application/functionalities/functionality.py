from application.dbAccess.pyMongo import setInDB


class Functionality:
    def __init__(self, senderId, bot, categories):
        self.senderId = senderId
        self.bot = bot
        self.categories = categories
        self.state = ""
        self.messageToSend = "nah"
        self.messageType = "text_message"

    def getResponse(self):
        self.setResponse()
        return {"message": self.messageToSend, "type": self.messageType}

    def setResponse(self):
        self.messageToSend = "huh!?"
        self.messageType = "text_message"
        if self.state:
            setInDB(self.senderId, {"state": self.state})

    def getCategoryValue(self, category):
        categories = self.categories
        try:
            value = categories[category]
        except KeyError:
            value = []
        return value
