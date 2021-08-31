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

@app.route('/', methods = ['POST'])
def incoming():
  viber_request = viber.parse_request(request.get_data())

  if isinstance(viber_request, ViberMessageRequest):
    #
  return Response(status = 200)