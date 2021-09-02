from viberbot import API
from viberbot.api.bot_configuration import BotConfiguration

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