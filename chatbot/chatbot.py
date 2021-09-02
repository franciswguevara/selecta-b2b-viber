from flask import Flask, request, Response
from dotenv import load_dotenv
import logging
import os
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import *
from viberbot.api.viber_requests import (
  ViberConversationStartedRequest,
  ViberMessageRequest, 
  ViberSubscribedRequest,
  ViberFailedRequest,
  ViberUnsubscribedRequest
)

load_dotenv()
access_token = os.getenv("CHATBOT_TOKEN")

#Start Flask
app = Flask(__name__)

viber = Api(BotConfiguration(
    name='Selecta B2B',
    avatar='https://i.imgur.com/YxAFDbx.png',
    auth_token = access_token
))

@app.route('/', methods=['POST'])
def incoming():
  
  #logger.debug("received request. post data: {0}".format(request.get_data()))
  
  # every viber message is signed, you can verify the signature using this method
  if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
    return Response(status=403)

  # this library supplies a simple way to receive a request object
  viber_request = viber.parse_request(request.get_data())

  if isinstance(viber_request, ViberMessageRequest):
    message = viber_request.message
    
    # if message.lower() == 'order':
    #   viber.send_messages(viber_request.sender.id, [TextMessage(text='What do you want to order?')])
    # elif message.lower() == '2 vanilla':

    # lets echo back
    print(type(message))
    print(message)
    print(help(message))
    
    viber.send_messages(viber_request.sender.id, [message])

  elif isinstance(viber_request, ViberSubscribedRequest):
    viber.send_messages(viber_request.get_user.id, [
        TextMessage(text="thanks for subscribing!")
    ])
  elif isinstance(viber_request, ViberFailedRequest):
    #logger.warn("client failed receiving message. failure: {0}".format(viber_request))
    pass

  return Response(status=200)