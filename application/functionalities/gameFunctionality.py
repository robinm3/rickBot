import random
import emojis
from application.dbAccess.pyMongo import setInDB, getInDB
from application.functionalities.functionality import Functionality


class GameFunctionality(Functionality):
    def __init__(self, senderId, bot, categories, payload):
        super().__init__(senderId, bot, categories)
        self.payload = payload
        if getInDB(self.senderId, "state"):
            self.state = getInDB(self.senderId, "state")
        else:
            self.state = {}

    def setResponse(self):
        try:
            self.messageToSend = self.getMessageToSend()
        except Exception as err:
            self.messageToSend = str(err)
        self.messageType = "text_message"

    def getMessageToSend(self):
        if self.state.get("game") or (
            "game" in self.categories
            and (
                "rematch" in self.categories["game"]
                or "rejouer" in self.categories["game"]
            )
        ):
            if (
                getInDB(self.senderId, "play")
                or self.gotResponse()
                or (
                    "game" in self.categories
                    and (
                        "rematch" in self.categories["game"]
                        or "rejouer" in self.categories["game"]
                    )
                )
            ):
                setInDB(
                    self.senderId,
                    {
                        "state": {"game": "tic-tac-toe"},
                        "game": "tic-tac-toe",
                        "play": True,
                    },
                )
                messageToSend = self.continuePlayingTicTacToe()
            else:
                setInDB(self.senderId, {"state": None, "play": False, "game": None})
                messageToSend = "ok, let's stop for now"
        elif "game" in self.categories:
            print(self.state)
            messageToSend = "Tu veux jouer au tic-tac-toe?"
            setInDB(
                self.senderId,
                {
                    "state": {"game": "tic-tac-toe"},
                    "game": "tic-tac-toe",
                    "play": False,
                },
            )
        else:
            setInDB(self.senderId, {"state": None, "play": False, "game": None})
            messageToSend = "nuh"
        return messageToSend

    def continuePlayingTicTacToe(self):
        messageToSend = "À toi de jouer"
        grid = [["0", "1", "2"], ["3", "4", "5"], ["6", "7", "8"]]
        if not getInDB(self.senderId, "play"):
            messageToSend = "Tu as les x, j'ai les o. Donne un chiffre entre 8 et 0"
            if not getInDB(self.senderId, "IStart"):
                setInDB(self.senderId, {"IStart": True})
            else:
                setInDB(self.senderId, {"IStart": False})
                messageToSend += ". Je commence "
                move = computerPlayTicTacToe(grid)
                grid = self.makeTicTacToeMove(grid, move, "o")
                setInDB(self.senderId, {"play": True, "grid": grid})
        else:
            if getInDB(self.senderId, "grid"):
                grid = getInDB(self.senderId, "grid")
            move = self.getTicTacToeMove(grid)
            if move not in listTicTacToeMovesAvailable(grid):
                messageToSend = "Tu ne peux pas faire ça! Je joue quand même là"
            else:
                grid = self.makeTicTacToeMove(grid, move, "x")
                setInDB(self.senderId, {"play": True, "grid": grid})
            if checkIfTicTacToeWin(grid):
                messageToSend = "Tu as gagné!! Bravo" + emojis.PARTY_POPPER + " !"
                setInDB(
                    self.senderId,
                    {"state": None, "play": False, "game": None, "grid": None},
                )
            elif len(listTicTacToeMovesAvailable(grid)) == 0:
                messageToSend = "Égalité! Bonne partie"
                setInDB(
                    self.senderId,
                    {"state": None, "play": False, "game": None, "grid": None},
                )
            else:
                move = computerPlayTicTacToe(grid)
                grid = self.makeTicTacToeMove(grid, move, "o")
                setInDB(self.senderId, {"play": True, "grid": grid})
                if checkIfTicTacToeWin(grid):
                    messageToSend = "J'ai gagné!! Haha!" + emojis.PARTY_FACE
                    setInDB(
                        self.senderId,
                        {"state": None, "play": False, "game": None, "grid": None},
                    )
                elif len(listTicTacToeMovesAvailable(grid)) == 0:
                    messageToSend = "Égalité! Bonne partie" + emojis.THUMBS_UP
                    setInDB(
                        self.senderId,
                        {"state": None, "play": False, "game": None, "grid": None},
                    )
        textGrid = "\n"
        for i in grid:
            textGrid += "|"
            for j in i:
                textGrid += j + "|"
            textGrid += "\n"
        messageToSend += textGrid
        return messageToSend

    def getTicTacToeMove(self, grid):
        try:
            move = "0"
            if self.payload:
                move = str(self.payload)
            else:
                if self.categories["number"]:
                    move = int(self.categories["number"])
                    if move not in range(9) or move == 0:
                        move = "0"
            return str(move)
        except Exception as err:
            raise TypeError("Mais ce n'est pas un numéro ça!")

    def gotResponse(self):
        gotResponse = False
        try:
            if self.categories["response"] in (
                "oui",
                "correct",
                "bien sûr",
                "Yep",
                "yep",
                "Oui",
            ):
                gotResponse = True
        except KeyError:
            gotResponse = False
        except TypeError:
            gotResponse = False
        return gotResponse

    def makeTicTacToeMove(self, grid, move, player):
        if player == "o":
            competitor = "x"
        else:
            competitor = "o"
        try:
            indiceI = 0
            for i in grid:
                indiceJ = 0
                for j in i:
                    if move == str(j) and grid[indiceI][indiceJ] != competitor:
                        grid[indiceI][indiceJ] = player
                    indiceJ += 1
                indiceI += 1
        except Exception as err:
            raise TypeError("makeTicTacToeMove" + str(err))
        return grid


def getTicTacToeMoveAvailability(grid, move):
    availability = True
    for i in grid:
        for j in i:
            if move == str(j) and (j == "o" or j == "x"):
                availability = False
    if move == str(8):
        availability = True
    return availability


def listTicTacToeMovesAvailable(grid):
    availableMoves = []
    for i in grid:
        for j in i:
            if j not in ["o", "x"] or j == str(0):
                availableMoves.append(str(j))
    return availableMoves


def checkIfTicTacToeWin(grid):
    ticTacToeWin = False
    for i in grid:
        if i[0] == i[1] and i[1] == i[2]:
            ticTacToeWin = True
    for i in range(3):
        if grid[0][i] == grid[1][i] and grid[1][i] == grid[2][i]:
            ticTacToeWin = True
    if grid[0][0] == grid[1][1] and grid[1][1] == grid[2][2]:
        ticTacToeWin = True
    elif grid[2][0] == grid[1][1] and grid[1][1] == grid[0][2]:
        ticTacToeWin = True
    return ticTacToeWin


def computerPlayTicTacToe(grid):
    listAvailableMoves = listTicTacToeMovesAvailable(grid)
    listGoodMoves = {"x": [], "o": []}
    for i in range(3):
        if grid[0][i] == grid[1][i] and (grid[2][i] in listAvailableMoves):
            listGoodMoves[str(grid[0][i])].append(grid[2][i])
        elif grid[0][i] == grid[2][i] and (grid[1][i] in listAvailableMoves):
            listGoodMoves[str(grid[0][i])].append(grid[1][i])
        elif grid[1][i] == grid[2][i] and (grid[0][i] in listAvailableMoves):
            listGoodMoves[str(grid[1][i])].append(grid[0][i])
        elif grid[i][0] == grid[i][1] and (grid[i][2] in listAvailableMoves):
            listGoodMoves[str(grid[i][0])].append(grid[i][2])
        elif grid[i][0] == grid[i][2] and (grid[i][1] in listAvailableMoves):
            listGoodMoves[str(grid[i][0])].append(grid[i][1])
        elif grid[i][1] == grid[i][2] and (grid[i][0] in listAvailableMoves):
            listGoodMoves[str(grid[i][1])].append(grid[i][0])
    if grid[0][0] == grid[1][1] and (grid[2][2] in listAvailableMoves):
        listGoodMoves[str(grid[0][0])].append(grid[2][2])
    elif grid[1][1] == grid[2][2] and (grid[0][0] in listAvailableMoves):
        listGoodMoves[str(grid[2][2])].append(grid[0][0])
    elif grid[0][0] == grid[2][2] and (grid[0][0] in listAvailableMoves):
        listGoodMoves[str(grid[1][1])].append(grid[0][0])
    elif grid[2][0] == grid[1][1] and (grid[0][2] in listAvailableMoves):
        listGoodMoves[str(grid[2][0])].append(grid[0][2])
    elif grid[2][0] == grid[0][2] and (grid[0][2] in listAvailableMoves):
        listGoodMoves[str(grid[1][1])].append(grid[0][2])
    elif grid[1][1] == grid[0][2] and (grid[2][0] in listAvailableMoves):
        listGoodMoves[str(grid[0][2])].append(grid[2][0])
    for i in (2, 6, 4, 0, 8):
        if str(i) in listAvailableMoves:
            move = i
            break
        else:
            move = listAvailableMoves[0]

    if 2 not in listAvailableMoves and 6 in listAvailableMoves:
        move = 6
    elif 6 not in listAvailableMoves and 2 in listAvailableMoves:
        move = 2
    elif 0 not in listAvailableMoves and 8 in listAvailableMoves:
        move = 8
    elif 8 not in listAvailableMoves and 0 in listAvailableMoves:
        move = 0
    if 2 not in listAvailableMoves and 6 not in listAvailableMoves:
        if 8 in listAvailableMoves:
            move = 8
        elif 0 in listAvailableMoves:
            move = 0
    elif 0 not in listAvailableMoves and 8 not in listAvailableMoves:
        if 6 in listAvailableMoves:
            move = 6
        elif 2 in listAvailableMoves:
            move = 2
    if len(listGoodMoves.get("o")) != 0:
        move = listGoodMoves.get("o")[0]
    elif len(listGoodMoves.get("x")) != 0:
        move = listGoodMoves.get("x")[0]
    return str(move)
