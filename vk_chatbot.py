from vk_api.longpoll import VkLongPoll, VkEventType
import os
import dotenv
import vk_api as vk
from logger import ChatbotLogsHandler
from dialogflow_utils import ask_dialogflow
import requests
import logging
import time

logger = logging.getLogger(__file__)


def answer(event, vk_api, project_id, session_id):
    dialogflow_answer = ask_dialogflow(event.text, project_id, session_id)
    if not dialogflow_answer.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=dialogflow_answer.query_result.fulfillment_text,
            random_id=0)


def main() -> None:
    dotenv.load_dotenv()

    project_id = os.environ['PROJECT_ID']

    telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']
    telegram_token = os.environ['TELEGRAM_TOKEN']

    logger.addHandler(ChatbotLogsHandler(telegram_chat_id, telegram_token))

    vk_session = vk.VkApi(token=os.environ['VK_TOKEN'])
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    session_id = event.user_id
                    answer(event, vk_api, project_id, session_id)

        except requests.exceptions.ConnectionError as err:
            logger.warning('Боту прилетело:')
            logger.warning(err, exc_info=True)
            time.sleep(10)


if __name__ == '__main__':
    main()
