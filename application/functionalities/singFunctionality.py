import emojis
from application.dbAccess.pyMongo import getInDB, setInDB
from application.functionalities.functionality import Functionality


class SingFunctionality(Functionality):
    def setResponse(self):
        self.messageToSend = self.getMessageToSend()
        self.messageType = "text_message"

    def getMessageToSend(self):
        messageToSend = putNotesEmojisAround(self.nextLyrics())
        return messageToSend

    def nextLyrics(self):
        lyricFromUser = self.categories.get("rickSong")
        nextLyrics = "We're no strangers to love"
        lyricIndice = 0
        if getInDB(self.senderId, "rickPartLastLyrics"):
            if int(getInDB(self.senderId, "rickPartLastLyrics") + 2) < len(
                neverGonnaGiveYouUp
            ):
                nextLyrics = neverGonnaGiveYouUp[
                    int(getInDB(self.senderId, "rickPartLastLyrics") + 2)
                ]
                lyricIndice = getInDB(self.senderId, "rickPartLastLyrics")
        for i in range(lyricIndice, len(neverGonnaGiveYouUp)):
            if neverGonnaGiveYouUp[i] == lyricFromUser:
                nextLyrics = neverGonnaGiveYouUp[i + 1]
                setInDB(self.senderId, {"rickPartLastLyrics": i + 1})
                break
        return nextLyrics


neverGonnaGiveYouUp = [
    "We're no strangers to love",
    "You know the rules and so do I",
    "A full commitment's what I'm thinking of",
    "You wouldn't get this from any other guy",
    "I just wanna tell you how I'm feeling",
    "Gotta make you understand",
    "Never gonna give you up",
    "Never gonna let you down",
    "Never gonna run around and desert you",
    "Never gonna make you cry",
    "Never gonna say goodbye",
    "Never gonna tell a lie and hurt you",
    "We've known each other for so long",
    "Your heart's been aching but you're too shy to say it",
    "Inside we both know what's been going on",
    "We know the game and we're gonna play it",
    "And if you ask me how I'm feeling",
    "Don't tell me you're too blind to see",
    "Never gonna give you up",
    "Never gonna let you down",
    "Never gonna run around and desert you",
    "Never gonna make you cry",
    "Never gonna say goodbye",
    "Never gonna tell a lie and hurt you",
    "Never gonna give you up",
    "Never gonna let you down",
    "Never gonna run around and desert you",
    "Never gonna make you cry",
    "Never gonna say goodbye",
    "Never gonna tell a lie and hurt you",
    "Never gonna give, never gonna give",
    "(Give you up)",
    "Never gonna give",
    "Never gonna give",
    "(Give you up)",
    "We've known each other for so long",
    "Your heart's been aching but you're too shy to say it",
    "Inside we both know what's been going on",
    "We know the game and we're gonna play it",
    "I just wanna tell you how I'm feeling",
    "Gotta make you understand",
    "Never gonna give you up",
    "Never gonna let you down",
    "Never gonna run around and desert you",
    "Never gonna make you cry",
    "Never gonna say goodbye",
    "Never gonna tell a lie and hurt you",
    "Never gonna give you up",
    "Never gonna let you down",
    "Never gonna run around and desert you",
    "Never gonna make you cry",
    "Never gonna say goodbye",
    "Never gonna tell a lie and hurt you",
    "Never gonna give you up",
    "Never gonna let you down",
    "Never gonna run around and desert you",
    "Never gonna make you cry",
]


def putNotesEmojisAround(text):
    return emojis.MUSICAL_NOTES + text + emojis.MUSICAL_NOTE
