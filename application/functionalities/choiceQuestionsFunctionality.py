import random
from application.functionalities.functionality import Functionality


class ChoiceQuestionsFunctionality(Functionality):
    def setResponse(self):
        self.messageToSend = self.getMessageToSend()
        self.messageType = "text_message"

    def getMessageToSend(self):
        choices = []
        if type(self.categories.get("choice")) != list:
            choices = [self.categories.get("choice")]
        else:
            for choice in self.categories.get("choice"):
                choices.append(choice)
        print(choices)
        choice = random.choice(list(choices))
        print(choice)
        return choice
