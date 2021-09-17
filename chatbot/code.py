from viberbot.api.bot_configuration import BotConfiguration
from viberbot import Api
from viberbot.api.message_sender import MessageSender

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