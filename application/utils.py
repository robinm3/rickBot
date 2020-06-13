import wit
import constants
from pymessenger import Bot
from wit import Wit
from application.dbAccess.pyMongo import getInDB, deleteFromDB
from application.functionalities.gameFunctionality import GameFunctionality
from application.functionalities.locationFunctionality import LocationFunctionality
from application.functionalities.newsFunctionality import NewsFunctionality
from application.functionalities.singFunctionality import SingFunctionality
from application.functionalities.smallTalkFunctionality import SmallTalkFunctionality
from application.functionalities.weirdQuestionsFunctionality import WeirdQuestionsFunctionality

client = Wit(access_token=constants.WIT_ACCESS_TOKEN)
bot = Bot(constants.PAGE_ACCESS_TOKEN)


class Utils:
    def __init__(self, senderId, messagingEvent):
        self.senderId = senderId
        self.messagingEvent = messagingEvent
        self.messageFromUser = ""
        self.state = None
        self.payload = None
        self.witCategories = dict()
        self.responseToSend = ""

    def process(self):
        eventType = self.getEventType()
        if eventType:
            self.setResponseState("start")
            try:
                responseToSend = (self.getResponseToSend(eventType))
            except Exception as err:
                messageToSend = rickRoll("Ce n'est pas ce que tu penses", "Clique ici")
                responseToSend = {"message": messageToSend, "type": "generic_message"}
            if type(responseToSend) == list:
                for response in responseToSend:
                    self.sendMessage(response)
                responseToSend = responseToSend[0]
            else:
                self.sendMessage(responseToSend)
            self.setResponseState("stop")
            return responseToSend

    def getEventType(self):
        eventType = ""
        messagingEvent = self.messagingEvent
        if messagingEvent.get('postback'):
            eventType = "postback"
        elif messagingEvent.get('message'):
            eventType = "message"
        return eventType

    def setResponseState(self, responseState):
        if responseState == "start":
            bot.send_action(self.senderId, "mark_seen")
            bot.send_action(self.senderId, "typing_on")
        elif responseState == "stop":
            bot.send_action(self.senderId, "typing_off")

    def getResponseToSend(self, eventType):
        if eventType == "postback":
            self.state = "game"
            self.setPayload()
        elif eventType == "message":
            self.setMessageFromUser()
            self.setWitCategories()
        responseToSend = self.getMessageResponse()
        if 'RICKROLL' in responseToSend.get('message'):
            RickRoll = responseToSend.get('message').get('RICKROLL')
            messageToSend = rickRoll(RickRoll[0], RickRoll[1])
            responseToSend = {"message": messageToSend, "type": "generic_message"}
        return responseToSend

    def sendMessage(self, response):
        senderId = self.senderId
        messageType = response['type']
        messageToSend = response['message']
        if messageType == "text_message":
            bot.send_text_message(senderId, messageToSend)
        elif messageType == "generic_message":
            bot.send_generic_message(senderId, messageToSend)

    def setPayload(self):
        messagingEvent = self.messagingEvent
        if 'payload' in messagingEvent['postback']:
            self.payload = messagingEvent['postback']['payload']

    def setMessageFromUser(self):
        messagingEvent = self.messagingEvent
        if 'text' in messagingEvent['message']:
            extractedMessage = messagingEvent['message']['text']
        else:
            extractedMessage = ""
        self.messageFromUser = extractedMessage
        print(self.messageFromUser)

    def setWitCategories(self):
        witCategories = {}
        messageFromUser = self.messageFromUser
        try:
            resp = client.message(messageFromUser)
            print(resp)
            for entity in resp['entities']:
                print(entity)
                witCategories[str(entity)] = []
                for i in resp['entities'][entity]:
                    print(i)
                    witCategories[str(entity)].append(i['value'])
                if len(witCategories[str(entity)]) == 1:
                    witCategories[str(entity)] = witCategories[str(entity)][0]

        except wit.wit.WitError as err:
            print(err)
            pass
        if not witCategories:
            witCategories = {"categories": None}
        print(witCategories)
        self.witCategories = witCategories

    def getMessageResponse(self):
        categories = self.witCategories
        senderId = self.senderId
        if getInDB(senderId, "state"):
            functionality = self.continueState()
        elif (getInDB(senderId, "question")) and (
                'response' in categories or 'location' in categories or 'frequence' in categories):
            question = getInDB(senderId, "question")
            if "location" in question:
                functionality = LocationFunctionality(senderId, bot, categories)
            elif "newsRecurrence" in question:
                functionality = NewsFunctionality(senderId, bot, categories)
            else:
                functionality = SmallTalkFunctionality(senderId, bot, categories)
        elif 'choice' in categories:
            functionality = WeirdQuestionsFunctionality(senderId, bot, categories)
        elif 'rickSong' in categories:
            functionality = SingFunctionality(senderId, bot, categories)
        elif 'newsType' in categories:
            functionality = NewsFunctionality(senderId, bot, categories)
        elif 'location' in categories:
            functionality = LocationFunctionality(senderId, bot, categories)
        elif 'game' in categories:
            functionality = GameFunctionality(senderId, bot, categories, self.payload)
        else:
            functionality = SmallTalkFunctionality(senderId, bot, categories)
        if 'reset' in categories:
            deleteFromDB(senderId)
            return {"message": "ok, rebooting", "type": "text_message"}
        return functionality.getResponse()

    def resetValues(self):
        self.messageFromUser = ""
        self.state = None
        self.payload = None
        self.witCategories = dict()
        self.responseToSend = ""

    def continueState(self):
        state = getInDB(self.senderId, "state")
        if "game" in state:
            functionality = GameFunctionality(self.senderId, bot, self.witCategories, self.payload)
        else:
            functionality = SmallTalkFunctionality(self.senderId, bot, self.witCategories)
        return functionality


def rickRoll(title, buttonTitle):
    return [{
        'title': title,
        'buttons': [{
            'type': 'web_url',
            'title': buttonTitle,
            'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        }]}]
