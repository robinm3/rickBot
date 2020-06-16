import constants
from pymessenger import Bot
from wit import Wit
import time
from gnewsclient import gnewsclient
from application.dbAccess.pyMongo import findAllInDB, setInDB
from application.functionalities.newsFunctionality import chooseCovidImage, newElement

wit_access_token = constants.WIT_ACCESS_TOKEN
client = Wit(access_token=wit_access_token)

PAGE_ACCESS_TOKEN = constants.PAGE_ACCESS_TOKEN
bot = Bot(PAGE_ACCESS_TOKEN)


def recurrencePosting():
    currentHour = time.struct_time.tm_hour
    currentDay = time.struct_time.tm_wday
    newsEveryDay(currentHour)
    newsEveryWeek(currentHour, currentDay)


def newsEveryDay(currentHour):
    if currentHour == 10:
        setInDB(1, {"newsRecurrence": "jour"})
        elements = getCoronaNewsElements(1)
        for sender in findAllInDB("recurrence", "jour"):
            senderId = sender.get("_id")
            bot.send_generic_message(senderId, elements)
        return elements
    return None


def newsEveryWeek(currentHour, currentDay):
    if currentHour == 10 and currentDay == 0:
        setInDB(1, {"newsRecurrence": "semaine"})
        elements = getCoronaNewsElements(1)
        for sender in findAllInDB("recurrence", "semaine"):
            senderId = sender.get("_id")
            bot.send_generic_message(senderId, elements)
        return elements
    return None


def getCoronaNewsElements(senderId):
    location = "Canada"
    newsClient = gnewsclient.NewsClient(
        language="french", location=location, topic="Health", max_results=9
    )
    newsClient.query = ""
    newsItems = newsClient.get_news()
    elements = []

    for item in newsItems:
        if not item["media"]:
            image = chooseCovidImage()
        else:
            image = item["media"]
        wordsInTitle = (item["title"]).split()
        if (
            ("COVID-19" in wordsInTitle)
            or ("COVID" in wordsInTitle)
            or ("Coronavirus" in wordsInTitle)
        ):
            element = newElement(item, image)
            elements.insert(0, element)
        else:
            element = newElement(item, image)
            elements.append(element)
    return elements
