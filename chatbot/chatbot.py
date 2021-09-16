from flask import Flask, request, Response
from dotenv import load_dotenv
import logging
import os
from .prices import *
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

skus = ['SELECTA IH SUP PISTACHIO N CASHEW 1X1.3L', 'SELECTA IH PISTACHIO & CASHEW 1X450ML', 'SELECTA IH SUP DOUBLE DUTCH 1X3.0L', 'SELECTA IH SUP DOUBLE DUTCH 1X1.3L', 'SELECTA SUPREME DOUBLE DUTCH 1X0.75L', 'SELECTA IH DOUBLE DUTCH 1X450ML', 'SELECTA IH SUP VERY ROCKY ROAD 1X3.0L', 'SELECTA IH SUP VERY ROCKY RAD 1X1.4L', 'SELECTA SUPREME ROCKY ROAD 1X0.75L', 'SELECTA IH ROCKY ROAD 1X450ML', 'SELECTA IH SUP COOKIES AND CREAM 1X3.0L', 'SELECTA IH SUP COOKIES AND CREAM 1X1.3L', 'SELECTA SUPREME COOKIES & CREAM 1X0.75L', 'SELECTA IH COOKIES & CREAM 1X450ML', 'SELECTA IH SUP CFFE CRUMBLE 1X1.4L', 'SELECTA SUPREME COFFEE CRUMBLE 1X0.75L', 'SELECTA IH COFFEE CRUMBLE 1X450ML', 'SELECTA IH SUP QUEZO REAL 1X1.3L', 'SELECTA SUPREME QUEZO REAL 1X0.75L', 'SELECTA IH SUP BF 1X 475ML', 'SELECTA IH CHOCO ALMOND FUDGE 1X1.4L', 'SELECTA IH CHOCO ALMOND FUDGE 1X750ML', 'SELECTA IH SUP CHOCO ALMOND FUDG 1X450ML', 'SELECTA IH COCONUT MANGO MOCHI 1X1.3L', 'SELECTA IH BANANA GRAHAM CRUNCH 1X1.3L', 'SELECTA IH CHOCOHAZELNUT TRUFFLE 1X1.3L', 'SELECTA IH BANANA GRAHAM CRUNCH 1X750ML', 'SELECTA IH SUP UBE MACAPUNO 1X1.3L', 'SELECTA IH SUP HALO-HALO 1X1.3L', 'SELECTA IH SUP MILK TEA 1X1.3L', 'SELECTA IH SUP MILK TEA 1X450ML', 'SELECTA IH SUP STRAW N CREAM 1X1.3L', 'SELECTA IH SUP MANGO SANSRIVAL 1X1.3L', 'SELECTA IH DSUP DDUTCH/C&CRM 1.4L', 'SELECTA DSUP DDUTCH/C&CREAM 750ML', 'SELECTA DSUP RROAD/C&CREM 1.4L', 'SELECTA DSUP RROAD/C&CREAM 750ML', 'SELECTA IH DSUP DBLDTCH/VRKYRD 1X3.0L', 'SELECTA IH DSUP DBLDCH/VRKYRD 1X1.4L', 'SELECTA IH DSUP DBLDTCH/VRKYRD 1X750ML', 'SELECTA IH DSUP CAF-CNC 1X1.3L', 'SELECTA IH SUP VERY ROCKY ROAD 1X1.3L', 'SELECTA IH SUP COFFEE CRUMBLE 1X1.3L', 'SELECTA IH SUP CHOC ALMOND FUDGE 1X1.3L', 'SELECTA IH DSUP DBLDTCH/VRKYRD 1X1.3L', 'SELECTA DSUP DDUTCH/C&CREAM 1X1.3L', 'SELECTA DSUP RROAD/C&CREAM 1X1.3L', 'SELECTA IH COB HERSHEYS MILKAMNDS 1X1.3L', 'SELECTA IH COB HERSHEYMLK&AMNDS 1X450ML', 'SELECTA IH COB HERSHEYCARAMELKISS 1X1.3L', 'SELECTA IH COB HERSHEYCRMELKISS 1X0.475L', 'SELECTA IH COB HERSHEYS C&CHOCO 1X1.3L', 'SELECTA IH COB HERSHEYS C&C 1X1.3L', 'SELECTA IH COB HERSHEYS C&C 1X475ML', 'SELECTA IH COB HERSHEYS FDGE KSS 1X1.3L', 'SELECTA IH COB HERSHEYS FDGE KSS 1X475ML', 'GROM GELATO CREMA DI GROM 1X460ML', 'GROM GELATO CIOCCOLATO 1X460ML', 'GROM GELATO STRACCIATELLA 1X460ML', 'GROM GELATO SALTED CARAMEL 1X460ML', 'GROM GELATO PISTACCHIO 1X460ML', 'GROM GELATO HAZELNUT 1X460ML', 'GROM GELATO COFFEE 1X460ML', 'GROM GELATO STRAWBERRY 1X460ML', 'MAGNUM TUBS CLASSIC 1X440ML', 'MAGNUM TUBS WHITE 1X440ML', 'MAGNUM TUBS ALMOND 1X440ML', 'MAGNUM TUBS CLASSIC ANZ 1X440ML', 'MAGNUM TUBS WHITE ANZ 1X440ML', 'MAGNUM TUBS ALMOND ANZ 1X440ML', 'MAGNUM TUBS COOKIES & CREAM 1X440ML', 'VIENNETTA VANILLA 1X650ML', 'SELECTA IH CLSC SUPER CHOCOLATE 1X3.0L', 'SELECTA IH CLSC UBE ROYALE 1X3.0L', 'SELECTA IH CLSC VANILLA 1X3.0L', 'SELECTA IH CLSC UBE MACAPUNO 1X1.3L', 'SELECTA IH CLSC BUCO MELON 1X1.3L', 'SELECTA IH CLSC MANG 1X1.4L', 'SELECTA IH CLSC STRAWBERY 1X1.4L', 'SELECTA IH CLSC SUPER CHOCLATE 1X1.4L', 'SELECTA IH CLSC UBE ROYLE 1X1.4L', 'SELECTA IH CLSC VANLLA 1X1.4L', 'SELECTA IH BIRTHDAY BASO CHOCO 1X400ML', 'SELECTA IH BIRTHDAY BASO KESO 1X400ML', 'SELECTA IH BIRTHDAY BASO UBE 1X400ML', 'SELECTA IH 3N1 CHC MANGO UBE 1X1.0L', 'SELECTA 3N1 TUBS CHOCO-KESO-UBE 1L', 'SELECTA IH 3+1 CKUM EFF 1X1.5L', 'SELECTA 2N1 ESP BPAN-MF 1X1.3L', 'SELECTA 2N1 SUP BPAN-MF 1X0.75L', 'SELECTA 2N1 ESP BRWNIE-COOKIECMBL 1X1.3L', 'SELECTA 2N1 SUP BROWNIE-CKECRMBL 1X0.75L', 'SELECTA 2IN1 CRMSUP CNC-CMALLOW 1X1.3L', 'SELECTA 2IN1 CRMSUP CNC-CMALLOW 1X750ML', 'SELECTA 2IN1 CRMSUP UBEKESO-HALO 1X1.3L', 'SELECTA 2IN1 CRMSUP UBEKESO-HALO 1X750ML', 'MAGNUM CLASSIC AMBER 24X90ML', 'MAGNUM ALMOND AMBER 24X90ML', 'MAGNUM COOKIES & CREAM 24X80ML(64G)', 'MAGNUM CHERRY BLOSSOMS E 24X80ML', 'MAGNUM DAIRY FREE ALMOND 20X90ML', 'MAGNUM MINI CLASSIC AMBER 6X(6X45ML)', 'MAGNUM MINI ALMOND AMBER 6X(6X45ML)', 'CORNETTO CHOCOLATE 24X110ML', 'CORNETTO POOH COOKIES & DREAM 24X110ML', 'CORNETTO POOH ROCKY ROAD 24X110ML', 'CORNETTO VANILLA 24X110ML', 'SELECTA CORNETTO BANANA SPLIT 24X110ML', 'CORNETTO POOH HAZELNUT 24X110ML', 'CORNETTO DISC WHITE CHOCO C&C 12X115 ML', 'CORNETTO DISC MILK TEA 12X115ML', 'CORNETTO DISC BLACK CHCO COKIE 12X115ML', 'SELECTA OOH BOOM CHOCO 12X60ML', 'SELECTA OOH BOOM COOKIESNCRM 12X60ML', 'SELECTA OOH BOOM CHOCO COOKIES 12X60ML', 'SELECTA OOH BOOM BOOM UBE 12X60ML', 'SELECTA OOH ICS COOKIES & CREAM 18X60ML', 'SELECTA OOH ICS ROCKY ROAD 18X60ML', 'SELECTA OOH ICS QUEZO REAL 18X60ML', 'SELECTA OOH MELON STICK 20X65ML', 'SELECTA OOH STRAWBERRY STICK 20X65ML', 'SELECTA OOH VANILLA MOCHI 30X(2X30ML)', 'WALLS IC SANDWICH EXP 32X80ML', 'SELECTA CUPS UBE 16X100ML', 'SELECTA CUPS CHOCO 16X100ML', 'SELECTA OOH WATERMELON SLICE 20X60ML', 'SELECTA OOH PINE APPLE STICK 15X70ML', 'SELECTA MANGO SLUSH 15X60ML', 'SELECTA OOH MELON SLICE 20X60ML', 'SELECTA OOH CORNETTO MP 4X(6X110ML)', 'SELECTA OOH FRUIT SLICE MP 6X(8X60ML)', 'SELECTA IH HRI CHOCOLATE 1X3.8L', 'SELECTA IH HRI STRAWBERRY 1X3.8L', 'SELECTA IH HRI UBE 1X3.8L', 'SELECTA IH HRI MANGO 1X3.8L', 'SELECTA IH HRI VANILLA 1X3.8L', 'SELECTA IH HRI MACAPUNO 1X3.8L']
prices = [227.27, 90.0, 440.91, 227.27, 126.35, 90.0, 440.91, 227.27, 126.35, 90.0, 440.91, 227.27, 126.35, 90.0, 227.27, 126.35, 90.0, 227.27, 126.35, 90.0, 227.27, 126.35, 90.0, 227.27, 227.27, 227.27, 126.36, 240.91, 240.91, 240.9, 95.45, 240.9, 240.9, 227.27, 126.35, 227.27, 126.35, 440.91, 227.27, 126.35, 227.27, 227.27, 227.27, 227.27, 227.27, 227.27, 227.27, 272.75, 136.36, 272.75, 136.36, 272.75, 272.75, 136.36, 272.75, 136.36, 415.83, 415.83, 415.83, 415.8, 433.33, 433.33, 433.33, 433.33, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 180.9, 409.1, 409.1, 409.1, 209.1, 209.1, 209.1, 209.1, 209.1, 209.1, 209.1, 45.45, 45.45, 45.45, 90.0, 90.0, 126.36, 150.0, 90.0, 150.0, 90.0, 150.0, 90.0, 150.0, 90.0, 1309.2, 1309.2, 1309.2, 1309.2, 1545.4, 1009.08, 1009.08, 436.36, 436.32, 436.32, 436.32, 436.32, 436.32, 272.73, 272.73, 272.73, 163.64, 163.64, 163.64, 163.64, 163.62, 163.62, 163.62, 637.0, 637.0, 955.5, 581.76, 291.2, 291.2, 181.82, 136.36, 204.6, 181.82, 418.2, 518.4, 316.7, 316.7, 316.7, 316.7, 316.7, 316.7]

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
                                                    TextMessage(text="5 SELECTA IH SUP DOUBLE DUTCH 1X1.3L\n3 MAGNUM CLASSIC AMBER 24X90ML\n2 GROM GELATO CIOCCOLATO 1X460ML\n1 SELECTA IH CLSC VANILLA 1X3.0L")])
    elif order := parse_order(message.text.upper()):
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
      key = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD)
      viber.send_messages(viber_request.sender.id, [TextMessage(text=f'Confirming your order of:'),
                                                    TextMessage(text=order[0]),
                                                    TextMessage(text=f'Your total will be {order[1]}'),
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