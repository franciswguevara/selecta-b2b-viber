from dotenv import load_dotenv
from flask import Flask, request, Response
import os
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_messages import TextMessage 
from viberbot.api.viber_request import ViberMessageRequest, ViberSubscribedRequest

#Start Flask
app = Flask(__name__)

#Load Environmental Variables
load_dotenv()
access_token = os.environ['CHATBOT_TOKEN']

bot_configuration = BotConfiguration(
  name='Selecta B2B',
	avatar='',
	auth_token= access_token
)

viber = Api(bot_configuration)
viber.set_webhook('https://selecta-b2b-viber.herokuapp.com/')

@app.route('/', methods = ['POST'])
def incoming():

  logger.debug("received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
  if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
      return Response(status=403)

  #Parse the request object
  viber_request = viber.parse_request(request.get_data())

  if isinstance(viber_request, ViberMessageRequest):
    message = viber_request.message
    # lets echo back
    viber.send_messages(viber_request.sender.id, [
        message
    ])
  elif isinstance(viber_request, ViberSubscribedRequest):
    viber.send_messages(viber_request.get_user.id, [
        TextMessage(text="thanks for subscribing!")
    ])
  elif isinstance(viber_request, ViberFailedRequest):
    logger.warn("client failed receiving message. failure: {0}".format(viber_request))
	
  return Response(status=200)

app.run(host = 'https://selecta-b2b-viber.herokuapp.com/', port = 443, debug = True)