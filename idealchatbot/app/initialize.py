from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration

#Start Flask
app = Flask(__name__)

viber = Api(BotConfiguration(
    name='Selecta B2B',
    avatar='https://i.imgur.com/YxAFDbx.png',
    auth_token = access_token
))

if __name__ == '__main__':
    app.run(threaded=True, debug = True)