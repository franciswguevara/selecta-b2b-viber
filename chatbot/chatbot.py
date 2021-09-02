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
    
    if message.text.lower() == 'order':
      viber.send_messages(viber_request.sender.id, [TextMessage(text='What do you want to order?')])
    elif message.text.lower() == 'Vanilla':
      viber.send_messages(viber_request.sender.id, [PictureMessage(media='https://i.imgur.com/MFZcVom.jpg',text='Confirming your order of 1 Tub of SELECTA IH CLSC VANILLA 1X1.5L')])
      viber.send_messages(viber_request.sender.id, [TextMessage(text='Your total is PHP 100.00 and your order is on its way!')])
    elif message.text.lower() == 'Chocolate':
      viber.send_messages(viber_request.sender.id, [PictureMessage(media='https://i.imgur.com/c7MZgVK.jpg',text='Confirming your order of 1 Tub of SELECTA IH CLSC SUPER CHOCOLATE 1X1.5L')])
      viber.send_messages(viber_request.sender.id, [TextMessage(text='Your total is PHP 100.00 and your order is on its way!')])
    elif message.text.lower() == 'rich':
      SAMPLE_RICH_MEDIA = {
        "BgColor": "#69C48A",
        "Buttons": [
          {
            "Columns": 6,
            "Rows": 1,
            "BgColor": "#454545",
            "BgMediaType": "jpg",
            "BgMedia": "https://i.imgur.com/YxAFDbx.png",
            "BgLoop": "true",
            "ActionType": "open-url",
            "Silent": "true",
            "ActionBody": "www.i.imgur.com",
            "Image": "https://i.imgur.com/YxAFDbx.png",
            "TextVAlign": "middle",
            "TextHAlign": "left",
            "Text": "<b>example</b> button",
            "TextOpacity": 10,
            "TextSize": "regular"
          }
        ]
      }

      SAMPLE_ALT_TEXT = "Buy now!"

      message = RichMediaMessage(rich_media=SAMPLE_RICH_MEDIA, alt_text=SAMPLE_ALT_TEXT)
      viber.send_messages(viber_request.sender.id, [message])
    elif message.text.lower() == 'keyboard':
      SAMPLE_KEYBOARD = {
        "Type": "keyboard",
        "Buttons": [
          {
          "Columns": 3,
          "Rows": 2,
          "BgColor": "#e6f5ff",
          "BgMedia": "https://i.imgur.com/MFZcVom.jpg",
          "BgMediaType": "picture",
          "BgLoop": True,
          "ActionType": "reply",
          "ActionBody": "2 Vanilla",
          "ReplyType": "message",
          "Text": "2 Vanilla",
          "TextSize": "medium",
		      "TextHAlign": "center"
          },
          {
          "Columns": 3,
          "Rows": 2,
          "BgColor": "#e6f5ff",
          "BgMedia": "https://i.imgur.com/c7MZgVK.jpg",
          "BgMediaType": "picture",
          "BgLoop": True,
          "ActionType": "reply",
          "ActionBody": "2 Chocolate",
          "ReplyType": "message",
          "Text": "2 Chocolate",
          "TextSize": "medium",
		      "TextHAlign": "center"
            ]
          }
        }

      message = KeyboardMessage(tracking_data='tracking_data', keyboard=SAMPLE_KEYBOARD)
      viber.send_messages(viber_request.sender.id, [message])
    else:
      #echo bot
      viber.send_messages(viber_request.sender.id, [message])
  elif isinstance(viber_request, ViberSubscribedRequest):
    viber.send_messages(viber_request.get_user.id, [
        TextMessage(text="thanks for subscribing!")
    ])
  elif isinstance(viber_request, ViberFailedRequest):
    #logger.warn("client failed receiving message. failure: {0}".format(viber_request))
    pass

  return Response(status=200)