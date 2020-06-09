import sys
from flask import Flask, request
from application.utils import Utils

app = Flask(__name__)
PAGE_ACCESS_TOKEN = "EAAJtOhvTldQBAOL2pxcIraYCU5p4a2BTKL3FxwReAGsm5RkoJqn3xfi4V2J3AZC4EEHg4yd1aj0FYNCdIZCgkmGLoxfuqrVBABH5ucBFRJZCnKfTaCIMoRr3YWYTyZAzuhmZBR7KsBIzz0nvFpqdrMfqubhbwPFEPp1M5lK9cJAZDZD"


@app.route('/', methods=['GET'])
def verify():
    """ Webhook verification
    :return: Hello world string and code 200 when verified
    """
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    """ Webhook
    :return: code 200 when ok
    """
    data = request.get_json()
    log(data)
    if data['object'] == 'page':
        for entry in data['entry']:
            try:
                for messagingEvent in entry['messaging']:
                    log(messagingEvent)
                    senderId = messagingEvent['sender']['id']
                    utilities = Utils(senderId, messagingEvent)
                    responseToSend = utilities.process()
                    log(responseToSend)
            except Exception as err:
                log(err)

    return "ok", 200


def log(message):
    print(message)
    sys.stdout.flush()


if __name__ == "__main__":
    app.run(debug=True, port=80)

