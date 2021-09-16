from flask import Flask, request, Response
from dotenv import load_dotenv
import logging
import os
import time
from viberbot.api.bot_configuration import BotConfiguration
from viberbot import Api
from viberbot.api.message_sender import MessageSender
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

class New_BotConfiguration(BotConfiguration):
  def __init__(self, min_api_version=7,*args, **kwargs):
    super(New_BotConfiguration, self).__init__(*args, **kwargs)
    self._min_api_version=min_api_version
  
  @property
  def min_api_version(self):
    return self._min_api_version

class New_MessageSender(MessageSender):
  def __init__(self, *args, **kwargs):
    super(New_MessageSender, self).__init__(*args, **kwargs)

  def _prepare_payload(self, message, sender_name, sender_avatar, sender=None, receiver=None, chat_id=None):
    payload = message.to_dict()
    payload.update(
      {
        'auth_token': self._bot_configuration.auth_token,
        'from': sender,
        'receiver': receiver,
        'sender': {
          'name': sender_name,
          'avatar': sender_avatar},
        "chat_id": chat_id,
        "min_api_version": self._bot_configuration.min_api_version
      })
    return self._remove_empty_fields(payload)

class New_Api(Api):
  def __init__(self, *args, **kwargs):
    super(New_Api, self).__init__(*args, **kwargs)
    self._message_sender = New_MessageSender(self._logger, self._request_sender, self._bot_configuration)

viber = New_Api(New_BotConfiguration(
    name='Selecta B2B',
    avatar='https://i.imgur.com/YxAFDbx.png',
    auth_token = access_token,
    min_api_version = 7.6
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
    try:
      name = viber_request.sender.name
    except:
      pass

    if message.text.lower() == 'order':
      viber.send_messages(viber_request.sender.id, [
        TextMessage(text='Para maka-order, i-verify muna natin ang iyong Tindahan Club account'),
        TextMessage(text='Ikaw ba ay direktang nakaka-order mula sa isang Unilever distributor?')
        ])
      
      KEYBOARD = {
        "Type": "keyboard",
        "Buttons": [
          {
          "Columns": 3,
          "Rows": 2,
          "BgColor": "#e6f5ff",
          "BgLoop": True,
          "ActionType": "reply",
          "ActionBody": "YES",
          "ReplyType": "message",
          "Text": "YES",
          "TextSize": "large",
		      "TextHAlign": "center"
          },
          {
          "Columns": 3,
          "Rows": 2,
          "BgColor": "#e6f5ff",
          "BgLoop": True,
          "ActionType": "reply",
          "ActionBody": "NO (SIGN-UP)",
          "ReplyType": "message",
          "Text": "NO (SIGN-UP)",
          "TextSize": "medium",
		      "TextHAlign": "center"
          }
            ]
        }
      message = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD)
      viber.send_messages(viber_request.sender.id, [message])
    elif message.text.lower() == 'yes':
      viber.send_messages(viber_request.sender.id, [PictureMessage(media='https://i.imgur.com/PtU6k6d.jpg',text='Makikita ang inyong outlet code sa upper-left na bahagi ng inyong invoice'),TextMessage(text='Ano ang iyong outlet code?')])
    elif message.text.lower() == '1234567':
      viber.send_messages(viber_request.sender.id, [TextMessage(text='I-enter ang mobile number na ginamit sa pag register sa Tindahan Club App or binigay sa inyong Unilever Salesman (ex.0919xxxxxxx)')])
    elif message.text.lower() == '09778912017':
      KEYBOARD = {
        "Type": "keyboard",
        "Buttons": [
          {
          "Columns": 2,
          "Rows": 2,
          "BgColor": "#e6f5ff",
          "BgLoop": True,
          "ActionType": "reply",
          "ActionBody": "AGREE",
          "ReplyType": "message",
          "Text": "AGREE",
          "TextSize": "large",
		      "TextHAlign": "center"
          },
          {
          "Columns": 2,
          "Rows": 2,
          "BgColor": "#e6f5ff",
          "BgLoop": True,
          "ActionType": "reply",
          "ActionBody": "REJECT",
          "ReplyType": "message",
          "Text": "REJECT",
          "TextSize": "medium",
		      "TextHAlign": "center"
          },
          {
          "Columns": 2,
          "Rows": 2,
          "BgColor": "#e6f5ff",
          "BgLoop": True,
          "ActionType": "reply",
          "ActionBody": "TERMS AND CONDITIONS",
          "ReplyType": "message",
          "Text": "TERMS AND CONDITIONS",
          "TextSize": "medium",
		      "TextHAlign": "center"
          }
            ]
        }

      message = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD)
      viber.send_messages(viber_request.sender.id, [TextMessage(text='Mag-login sa Tindahan Club? By clicking "AGREE" below, you are agreeing to the T&Cs of Tindahan Club.'),message])
    elif message.text.lower() == 'agree':
      viber.send_messages(viber_request.sender.id, [
          TextMessage(text='Do you want to quick order or browse?')
          ])
      KEYBOARD = {
        "Type": "keyboard",
        "Buttons": [
          {
          "Columns": 3,
          "Rows": 2,
          "BgColor": "#e6f5ff",
          "BgLoop": True,
          "ActionType": "reply",
          "ActionBody": "QUICK ORDER",
          "ReplyType": "message",
          "Text": "QUICK ORDER",
          "TextSize": "large",
		      "TextHAlign": "center"
          },
          {
          "Columns": 3,
          "Rows": 2,
          "BgColor": "#e6f5ff",
          "BgLoop": True,
          "ActionType": "reply",
          "ActionBody": "BROWSE",
          "ReplyType": "message",
          "Text": "BROWSE",
          "TextSize": "medium",
		      "TextHAlign": "center"
          }
            ]
        }
      message = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD)
      viber.send_messages(viber_request.sender.id, [message])
    elif message.text.lower() == 'quick order' or message.text.lower() == 'back':
      viber.send_messages(viber_request.sender.id, [TextMessage(text='Please enter your order using the following format:\nQuantity[Space]SKU Name on Official Pricelist'), 
                                                    TextMessage(text='To enter multiple orders, please use another line'),
                                                    TextMessage(text='Example Order:'),
                                                    TextMessage(text="5 SELECTA IH DOUBLE DUTCH 1X1.4L\n3 MAGNUM CLASSIC AMBER 24X90ML\n2 GROM GELATO CIOCCOLATO 1X460ML\n1 SELECTA IH CLSC VANILLA 1X1.4L")])
    elif message.text.upper() =='5 SELECTA IH DOUBLE DUTCH 1X1.4L\n3 MAGNUM CLASSIC AMBER 24X90ML\n2 GROM GELATO CIOCCOLATO 1X460ML\n1 SELECTA IH CLSC VANILLA 1X1.4L':
      KEYBOARD = {
        "Type": "keyboard",
        "Buttons": [
          {
          "Columns": 3,
          "Rows": 2,
          "BgColor": "#e6f5ff",
          "BgLoop": True,
          "ActionType": "reply",
          "ActionBody": "CONFIRM",
          "ReplyType": "message",
          "Text": "CONFIRM",
          "TextSize": "large",
		      "TextHAlign": "center"
          },
          {
          "Columns": 3,
          "Rows": 2,
          "BgColor": "#e6f5ff",
          "BgLoop": True,
          "ActionType": "reply",
          "ActionBody": "BACK",
          "ReplyType": "message",
          "Text": "BACK",
          "TextSize": "medium",
		      "TextHAlign": "center"
          }
            ]
        }
      message = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD)
      viber.send_messages(viber_request.sender.id, [TextMessage(text="Confirming your order of:\n\n5 SELECTA IH DOUBLE DUTCH 1X1.4L\n3 MAGNUM CLASSIC AMBER 24X90ML\n2 GROM GELATO CIOCCOLATO 1X460ML\n1 SELECTA IH CLSC VANILLA 1X1.4L"),
                                                    TextMessage(text='Is this correct?'),
                                                    message])
    elif message.text.lower() == 'browse':
      SAMPLE_RICH_MEDIA = {
        "BgColor": "#69C48A",
        "Buttons": [
          {
            "Columns": 6,
            "Rows": 7,
            "BgColor": "#454545",
            "BgMediaType": "picture",
            "BgMedia": "https://i.imgur.com/YxAFDbx.png",
            "BgLoop": "true",
            "ActionType": "open-url",
            "Silent": "true",
            "ActionBody": "https://www.google.com",
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
      viber.send_messages(viber_request.sender.id, [TextMessage(text=f'Welcome {name}!'),TextMessage(text='Pumili mula sa mga product categories!'),message])
    elif message.text.lower() == 'vanilla':
      viber.send_messages(viber_request.sender.id, [PictureMessage(media='https://i.imgur.com/MFZcVom.jpg',text='Confirming your order of 1 Tub of SELECTA IH CLSC VANILLA 1X1.5L')])
      viber.send_messages(viber_request.sender.id, [TextMessage(text='Your total is PHP 100.00 and your order is on its way!')])
    elif message.text.lower() == 'chocolate':
      viber.send_messages(viber_request.sender.id, [PictureMessage(media='https://i.imgur.com/c7MZgVK.jpg',text='Confirming your order of 1 Tub of SELECTA IH CLSC SUPER CHOCOLATE 1X1.5L')])
      viber.send_messages(viber_request.sender.id, [TextMessage(text='Your total is PHP 100.00 and your order is on its way!')])
    elif message.text.lower() == 'rich':
      SAMPLE_RICH_MEDIA = {
        "BgColor": "#69C48A",
        "Buttons": [
          {
            "Columns": 6,
            "Rows": 7,
            "BgColor": "#454545",
            "BgMediaType": "picture",
            "BgMedia": "https://i.imgur.com/YxAFDbx.png",
            "BgLoop": "true",
            "ActionType": "open-url",
            "Silent": "true",
            "ActionBody": "https://www.google.com",
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
          "ActionBody": "Vanilla",
          "ReplyType": "message",
          "Text": "Vanilla",
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
          "ActionBody": "Chocolate",
          "ReplyType": "message",
          "Text": "Chocolate",
          "TextSize": "medium",
		      "TextHAlign": "center"
          }
            ]
        }

      message = KeyboardMessage(tracking_data='tracking_data', keyboard=SAMPLE_KEYBOARD)
      viber.send_messages(viber_request.sender.id, [message])
    elif message.text.lower() == 'start':
      viber.send_messages(viber_request.sender.id, [TextMessage(text=f'Hi {name}! Welcome to Tindahan Club!')])
      viber.send_messages(viber_request.sender.id, [TextMessage(text=f"Anong maitutulong namin sa'yo at sa iyong tindahan, {name}?")])

      KEYBOARD = {
        "Type": "keyboard",
        "Buttons": [
          {
          "Columns": 2,
          "Rows": 2,
          "BgColor": "#e6f5ff",
          "BgLoop": True,
          "ActionType": "reply",
          "ActionBody": "ORDER",
          "ReplyType": "message",
          "Text": "ORDER",
          "TextSize": "large",
		      "TextHAlign": "center"
          },
          {
          "Columns": 2,
          "Rows": 2,
          "BgColor": "#e6f5ff",
          "BgLoop": True,
          "ActionType": "reply",
          "ActionBody": "FAQ",
          "ReplyType": "message",
          "Text": "FAQ",
          "TextSize": "medium",
		      "TextHAlign": "center"
          },
          {
          "Columns": 2,
          "Rows": 2,
          "BgColor": "#e6f5ff",
          "BgLoop": True,
          "ActionType": "reply",
          "ActionBody": "SIGN UP",
          "ReplyType": "message",
          "Text": "SIGN UP",
          "TextSize": "medium",
		      "TextHAlign": "center"
          }
            ]
        }

      message = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD)
      viber.send_messages(viber_request.sender.id, [message])
    else:
      #echo bot
      print(message.text.split('\n'))
      viber.send_messages(viber_request.sender.id, [message])
  elif isinstance(viber_request, ViberSubscribedRequest):
    viber.send_messages(viber_request.get_user.id, [
        TextMessage(text="thanks for subscribing!")
    ])
  elif isinstance(viber_request, ViberFailedRequest):
    #logger.warn("client failed receiving message. failure: {0}".format(viber_request))
    pass

  return Response(status=200)

@app.route('/instantiate', methods=['POST'])
def start():
  pass
  return Response(status=200)

@app.route('/login', methods=['POST'])
def login():
  pass
  return Response(status=200)

@app.route('/order', methods=['POST'])
def order():
  pass
  return Response(status=200)

@app.route('/checkout', methods=['POST'])
def checkout():
  pass
  return Response(status=200)