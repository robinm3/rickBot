import random
import emojis
from application.functionalities.functionality import Functionality
from application.functionalities.smallTalkFunctionality import getWhatCanYouDoResponse


class ToughQuestionsFunctionality(Functionality):
    def setResponse(self):
        self.messageToSend = self.getMessageToSend()
        self.messageType = "text_message"

    def getMessageToSend(self):
        messageToSend = "Humm, bonne question. Je ne sais pas"
        if "whatCanYouDo" in self.categories:
            messageToSend = self.respondToWhatCanYouDo()
        elif "question" in self.categories:
            question = self.categories["question"]
            if "Comment" in question:
                messageToSend = self.respondToHow()
            elif "Quand" in question:
                messageToSend = self.respondToWhen()
            elif "Quel" in question:
                messageToSend = self.respondToWhat()
            elif "Quelle" in question:
                messageToSend = self.respondToWhatFemale()
            elif "Qui" in question:
                messageToSend = self.respondToWho()
            elif "Où" in question:
                messageToSend = self.respondToWhere()
            elif "Pourquoi" in question:
                messageToSend = self.respondToWhy()
            elif "Que" in question or "Qu'" in question:
                messageToSend = self.respondToQue()
        return messageToSend

    def respondToHow(self):
        return random.choice(
            [
                "Comment!? Comme si je savais ça!",
                "Et bien, c'est facile! Tu n'as qu'à courir en rond pendant 5 minutes et ça devrait être fait "
                + emojis.LAUGHING_FACE,
                "Hum et bien je ne peux pas t'expliquer ça facilement"
                + emojis.SWEAT_SMILE
                + ", tu devrais aller chercher sur internet",
                "Wtf c'est quoi cette question?" + emojis.LAUGHING_FACE,
            ]
        )

    def respondToWhen(self):
        return random.choice(
            [
                "Lundi prochain à 2h du matin",
                "Sûrement l'année prochaine " + emojis.LAUGHING_FACE,
                "C'était hier, t'es en retard" + emojis.SWEAT_SMILE,
                "D'après mes calculs, ça devrait être dans 3 jours, 2 heures, 40 minutes et 42 secondes",
            ]
        )

    def respondToWhat(self):
        return random.choice(
            [
                "Le même que le cheval blanc de Napoléon",
                "Le 2e à ta droite",
                "Regarde devant toi, et tu devineras",
                "Tout comme le ski sur la plage de sable, bien sûr "
                + emojis.CRAZY_FACE,
            ]
        )

    def respondToWhatFemale(self):
        return random.choice(
            [
                "Je dirais exactement comme la jument blanche de Napoléon",
                "La 4e à ta gauche",
                "Hmmm. Bonne question. Si j'avais le choix, je pense que je choisirais celle qui est la même que le "
                "fils unique de la fille unique de ma grand-mère",
                "La même que la patate à Mononc' Serge",
            ]
        )

    def respondToWho(self):
        messageToSend = random.choice(
            [
                "C'est Michael Jackson réincarné",
                "Qui? Et bien c'est la même personne que celle qui joue un rôle dans le film que tu as regardé hier",
                "C'est le genre de personne qui dirais...(Lire dans la voix de Darth Vador) Je suis ton père ",
                "C'est l'enfant unique de la fille unique de ma grand-mère",
                "Tout ce que je peux te dire, c'est que dans une autre vie, c'était un ver de terre",
            ]
        )
        return messageToSend

    def respondToWhere(self):
        return random.choice(
            [
                "À St-Clin-Clin des Meuh-Meuh",
                "Juste derrière toi",
                "Dans mon bac à fleur ",
                "Pas très loin de la tour Eiffel",
                "Dans ta maison, en dessous d'un des divans",
            ]
        )

    def respondToWhy(self):
        return random.choice(
            [
                "Pourquoi pas? " + emojis.WINKING_FACE,
                "Parce qu'on a pas le choix, ça a été déterminé et on a décidé que c'était comme ça",
                "Ça n'a pas de sens. Je ne sais pas pourquoi, en fait "
                + emojis.PERSON_SHRUGGING,
                "Pour la même raison que celle qui explique pourquoi le cheval blanc de Napoléon est rose"
                + emojis.WINKING_FACE,
                "Parce que c'en est ainsi",
            ]
        )

    def respondToQue(self):
        return random.choice(
            [
                "Humm, je ne sais pas? " + emojis.PERSON_SHRUGGING,
                "Cette personne n'a pas le choix, ça a été déterminé et on a décidé que c'était comme ça pour elle",
                "Une chose insensé, c'est certain " + emojis.SURPRISED_MONKEY,
                "Hahahaha, devine toi-même! " + emojis.SWEAT_SMILE,
                "J'ai pas toute la journée, non mais " + emojis.CRYING_FACE,
            ]
        )

    def respondToWhatCanYouDo(self):
        messageToSend = ""
        if (
            "es-tu" in self.categories["whatCanYouDo"]
            or "es tu" in self.categories["whatCanYouDo"]
        ):
            messageToSend = "Je suis RickBot! "
        if random.choice([False, True, False, False]):
            messageToSend = {
                "RICKROLL": ["Je s'appelle Groot...hum, RickBot ", "Clique ici"]
            }
        else:
            messageToSend += getWhatCanYouDoResponse()
        return messageToSend
