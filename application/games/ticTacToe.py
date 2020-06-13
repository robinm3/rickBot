def tic_tac_toe(sender_id, bot):
    """sends tic tac toe message
    :param sender_id: number containing user id
    :param bot: pymessenger bot created
    :return messageToSend
    """
    messageToSend = ""
    for i in range(3):
        messageToSend += "|"
        for j in range(3):
            messageToSend += str(j) + "|"
        messageToSend += "\n"
    buttons = []
    for i in range(9):
        buttons.append({"type": "postback", "title": i, "payload": str(i)})
    bot.send_button_message(sender_id, "Sur quelle case tu commence?", buttons)
    return messageToSend


# if getInDB(senderId, "grilleTicTacToe"):
#     oldTicTacToe = getInDB(senderId, "grilleTicTacToe")
# else:
#     oldTicTacToe = {"lol": "nah"}
# newTicTacToe = oldTicTacToe.update({str(payload): "X"})
# setInDB(senderId, {"grilleTicTacToe": newTicTacToe})
# bot.send_text_message(senderId, str(getInDB(senderId, "grilleTicTacToe")))
