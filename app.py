import sys
import constants
from flask import Flask, request
from application.utils import Utils

app = Flask(__name__)
PAGE_ACCESS_TOKEN = constants.PAGE_ACCESS_TOKEN


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
                    senderId = messagingEvent['sender']['id']
                    utilities = Utils(senderId, messagingEvent)
                    utilities.process()
            except Exception as err:
                log(err)

    return "ok", 200


def log(message):
    print(message)
    sys.stdout.flush()


if __name__ == "__main__":
    app.run(debug=True, port=80)

