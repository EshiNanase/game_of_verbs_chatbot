import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import os
import dotenv
import random


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=0
    )

dotenv.load_dotenv()

vk_session = vk_api.VkApi(token=os.environ['VK_TOKEN'])
vk_api = vk_session.get_api()

longpoll = VkLongPoll(vk_session)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        echo(event, vk_api)
