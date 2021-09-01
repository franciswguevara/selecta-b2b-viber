from flask import Flask, request, Response
from dotenv import load_dotenv
import os
from pyngrok import ngrok
# from viberbot import Api
# from viberbot.api.bot_configuration import BotConfiguration
# from viberbot.api.messages import (
#   TextMessage,
#   ContactMessage,
#   PictureMessage,
#   VideoMessage
# )
# from viberbot.api.viber_requests import ViberMessageRequest, ViberSubscribedRequest

load_dotenv()
access_token = os.getenv("CHATBOT_TOKEN")

# #Start Flask
app = Flask(__name__)
http_tunnel = ngrok.connect(port = '80',bind_tls=True)
print(http_tunnel.public_url,'========')

@app.route("/", methods = ['GET','POST'])
def hello_world():
  try:
    if request.method =='GET':  
      return "<p>Hello, World!</p>"
    elif request.method =='POST':
      return "<p>I want to die</p>"
    return 'TANGINA NITO'
  except Exception as e:
    return str(e)


if __name__ == "__main__":
  app.run(port = 80,debug = True)


  


# viber = Api(BotConfiguration(
#     name='Selecta B2B',
#     avatar='',
#     auth_token= access_token
# ))


#viber.set_webhook(http_tunnel.public_url)

# @app.route('/', methods=['POST'])
# def incoming():
#   # this library supplies a simple way to receive a request object
#   viber_request = viber.parse_request(request.get_data())

#   if isinstance(viber_request, ViberMessageRequest):
#     # lets echo back
#     viber.send_messages(viber_request.sender.id, [
#         TextMessage(text="Your id is: " + str(viber_request.sender.id))
#     ])
#   elif isinstance(viber_request, ViberSubscribedRequest):
#     viber.send_messages(viber_request.get_user.id, [
#         TextMessage(text="You're subscribed!")
#     ])

#   return Response(status=200)

