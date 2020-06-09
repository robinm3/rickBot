import gnewsclient
from gnewsclient import gnewsclient
import random
from pymessenger import Bot
from application.dbAccess.pyMongo import getInDB, setInDB
from application.functionalities.functionality import Functionality

PAGE_ACCESS_TOKEN = "EAAJtOhvTldQBAOL2pxcIraYCU5p4a2BTKL3FxwReAGsm5RkoJqn3xfi4V2J3AZC4EEHg4yd1aj0FYNCdIZCgkmGLoxfuqrVBABH5ucBFRJZCnKfTaCIMoRr3YWYTyZAzuhmZBR7KsBIzz0nvFpqdrMfqubhbwPFEPp1M5lK9cJAZDZD"
bot = Bot(PAGE_ACCESS_TOKEN)


class NewsFunctionality(Functionality):

    def setResponse(self):
        if not (getInDB(self.senderId, "question")):
            response = self.getCoronaNewsElements()
        else:
            response = self.setNewsRecurrence()
        self.messageToSend = response["message"]
        self.messageType = response["type"]

    def setNewsRecurrence(self):
        if 'frequence' in self.categories:
            frequence = self.categories.get('frequence')
            if 'jour' in frequence:
                setInDB(self.senderId, {"newsRecurrence": "jour"})
                messageToSend = "C'est noté! Toutefois, cette fonction ne marche pas présentement, dsl"
                setInDB(self.senderId, {"question": None})
            elif 'semaine' in frequence:
                setInDB(self.senderId, {"newsRecurrence": "semaine"})
                messageToSend = "C'est noté! Toutefois, cette fonction ne marche pas présentement, dsl"
                setInDB(self.senderId, {"question": None})
            else:
                messageToSend = "Je ne sais pas trop quelle est cette fréquence, désolé"
        else:
            messageToSend = "D'accord, tu me demanderas des nouvelles quand tu en veux!"
            setInDB(self.senderId, {"newsRecurrence": None})
        return {"message": messageToSend, "type": "text_message"}

    def getCoronaNewsElements(self):
        location = 'Canada'
        newsClient = gnewsclient.NewsClient(language='french', location=location, topic='Health', max_results=5)
        newsItems = newsClient.get_news()
        senderId = self.senderId
        elements = []

        for item in newsItems:
            if not item['media']:
                image = chooseCovidImage()
            else:
                image = item['media']
            element = newElement(item, image)
            elements.append(element)
        response = {'message': elements, 'type': 'generic_message'}
        # if not getInDB(senderId, "newsRecurrence"):
        #     bot.send_generic_message(senderId, elements)
        #     response = {'message': 'Voulez-vous des nouvelles chaque jour ou chaque semaine?', 'type': 'text_message'}
        #     setInDB(senderId, {"question": "newsRecurrence"})
        return response


def chooseCovidImage():
    return random.choice(['https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimages.newscientist'
                          '.com%2Fwp-content%2Fuploads%2F2020%2F02%2F11165812%2Fc0481846'
                          '-wuhan_novel_coronavirus_illustration-spl.jpg&f=1&nofb=1',
                          'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth'
                          '%3Fid%3DOIP.Zg1gYnsydFQpMiYhWWMSGAEsDU%26pid%3DApi&f=1 ',
                          'https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.fda.gov%2Ffiles'
                          '%2Fcoronavirus-graphic-web-feature.jpg&f=1&nofb=1',
                          'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth'
                          '%3Fid%3DOIP.7Izen4eW-VuoBZxSPKeVMgHaEo%26pid%3DApi&f=1'])


def newElement(item, image):
    return {
        'title': item['title'],
        'buttons': [{
            'type': 'web_url',
            'title': "Read more",
            'url': item['link']
        }],
        'image_url': image}
