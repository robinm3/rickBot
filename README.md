# rickBot
Un bot messenger pour le coronavirus
## Comment l'utiliser?
Aller sur cette page et cliquez 'envoyer un message', puis commencez à lui parler directement:
https://www.facebook.com/Rickbotmarc-101108658265690/


## Fonctionalités

### Envoyer des nouvelles du COVID-19

Demandez des nouvelles et vous en recevrez. Seulement quand vous en demandez par contre. (voir [newsFunctionality](application/functionalities/newsFunctionality.py) pour le code)

<p align="center">
<img src="https://github.com/robinm3/rickBot/blob/master/images/news.png" height="400">
</p>


### Faire du small talk

Pas grand chose à dire? Parlez-lui un peu et demandez-lui comment ça va. Des conversations de base, mais nécessaires.(voir [smallTalkFunctionality](application/functionalities/smallTalkFunctionality.py) pour le code)

<p align="center">
<img src="https://github.com/robinm3/rickBot/blob/master/images/smallTalk.png" height="400">
</p>

### Le faire choisir

Vous vous demandez quoi porter entre votre camisole rose et votre cotton ouaté Supreme? Vous ne savez pas quoi choisir entre aller vous baigner sur une plage de roche, rester chez vous à regarder votre écran ou faire des roulades dans le gazon? RickBot va choisir pour vous! Plus jamais à faire de choix par vous même avec RickBot! (voir [choiceQuestionsFunctionality](application/functionalities/choiceQuestionsFunctionality.py) pour le code)

<p align="center">
<img src="https://github.com/robinm3/rickBot/blob/master/images/choices.png" height="400">
</p>

### Répondre à vos question étranges

Qui est votre père? Comment peut-on courir en rond pendant plus de 20 minutes sans s'essoufler? Pourquoi vous n'avez pas d'ami? Où est votre porte-clé des minions? Je ne sais pas, mais RickBot, lui, oui! Demandez-lui donc! (voir [toughQuestionsFunctionality](application/functionalities/toughQuestionsFunctionality.py) pour le code)


<p align="center">
<img src="https://github.com/robinm3/rickBot/blob/master/images/toughQuestions.png" height="400">
</p>

### Jouer au tic-tac-toe

Demandez-lui pour jouer au tic-tac-toe et vous ne serez pas déçus. Il est quand même bon, mais vous pouvez tout de même gagner. Essayez-donc! (voir [gameFunctionality](application/functionalities/gameFunctionality.py) pour le code)


<p align="center">
<img src="https://github.com/robinm3/rickBot/blob/master/images/ticTacToe.png" height="400">
</p>


### Chanter Never Gonna Give You Up

Il ne connait qu'une chanson, mais il la connait bien. Commencez en lui envoyant une des lignes de la chanson et vous pourrez chanter pendant longtemps! (voir [singFunctionality](application/functionalities/singFunctionality.py) pour le code)


<p align="center">
<img src="https://github.com/robinm3/rickBot/blob/master/images/sing.png" height="400">
</p>

### Se rappeler de vos trucs préférés

Une vrai conversation demande de l'écoute, et quoi de mieux pour montrer son écoute que de se rappeler des trucs préférés de l'autre? Maintenant, RickBot peut se rappeler de vos trucs préférés, que ce soit votre enfant préféré ou votre livre préféré. (voir [favoriteThingFunctionality](application/functionalities/favoriteThingFunctionality.py) pour le code)

<p align="center">
<img src="https://github.com/robinm3/rickBot/blob/master/images/favorite.png" height="400">
</p>

### Autres

Il peut aussi vous envoyez des rickrolls si ça lui tente, sauvegarder votre supposée localisation et dire n'importe quoi! Vous en serez peut-être surpris(es) (voir [functionalities](application/functionalities/))!


<p align="center">
<img src="https://github.com/robinm3/rickBot/blob/master/images/whatCanYou2.png" height="400">
</p>


## Vous avez un bug?

Rickbot n'arrête pas de vous dire la même chose ou il semble y avoir un problème quelconque? Écrivez "Reboot" à RickBot et ça risque de règler le problème temporairement.

## Architecture

Dans cette section, j'explique l'organisation de mon code. 

### app.py
(voir [app.py](app.py))
Dans ce module, on prend le message et les données qui y sont liées et on appelle utils.py pour envoyer le message.

### utils.py
(voir [utils.py](application/utils.py))
Dans ce module, on trouve les catégories(données par wit.ai), on détermine la functionality à utiliser et on envoie le message.

### Les functionalities
(voir [functionalities](application/functionalities/))

Chacunes des fonctionalités implémentées hérite de la class Functionality de base, qui initialise le senderId, le bot et les categories et peux renvoyer le message par getResponse. Plus qu'à implémenté le setResponse qui va déterminer le type(self.messageType) et contenu(self.messageToSend) du message à envoyer!

### Tests unitaires
(voir [tests](tests/))
Les tests unitaires sont séparés de l'application, mais sont organisés de la même façon que l'application
