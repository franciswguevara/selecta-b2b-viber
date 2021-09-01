from flask import Flask, request, Response
import os
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import (
  TextMessage,
  ContactMessage,
  PictureMessage,
  VideoMessage
)
from viberbot.api.viber_requests import ViberMessageRequest, ViberSubscribedRequest

access_token = os.getenv("CHATBOT_TOKEN")

# #Start Flask
app = Flask(__name__)

viber = Api(BotConfiguration(
    name='Selecta B2B',
    avatar='',
    auth_token= access_token
))

viber.set_webhook('http://172.18.0.14:443/')

@app.route('/', methods=['POST'])
def incoming():
  # this library supplies a simple way to receive a request object
  viber_request = viber.parse_request(request.get_data())

  if isinstance(viber_request, ViberMessageRequest):
    # lets echo back
    viber.send_messages(viber_request.sender.id, [
        TextMessage(text="Your id is: " + str(viber_request.sender.id))
    ])
  elif isinstance(viber_request, ViberSubscribedRequest):
    viber.send_messages(viber_request.get_user.id, [
        TextMessage(text="You're subscribed!")
    ])

  return Response(status=200)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port = 443, debug=True)