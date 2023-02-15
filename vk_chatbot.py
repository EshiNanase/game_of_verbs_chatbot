from vk_api.longpoll import VkLongPoll, VkEventType
import os
import dotenv
import vk_api as vk
from telegram_chatbot import ask_dialogflow, ChatbotLogsHandler
import requests
import logging
import time


logger = logging.getLogger(__file__)


def answer(event, vk_api):
    dialogflow_answer = ask_dialogflow(event.text)
    if not dialogflow_answer.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=dialogflow_answer.query_result.fulfillment_text,
            random_id=0)


def main() -> None:
    dotenv.load_dotenv()

    logger.addHandler(ChatbotLogsHandler(os.environ['TELEGRAM_CHAT_ID']))

    vk_session = vk.VkApi(token=os.environ['VK_TOKEN'])
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    answer(event, vk_api)

        except requests.exceptions.ReadTimeout as err:
            logger.warning('Боту прилетело:')
            logger.warning(err, exc_info=True)

        except requests.exceptions.ConnectionError as err:
            logger.warning('Боту прилетело:')
            logger.warning(err, exc_info=True)
            time.sleep(5)


if __name__ == '__main__':
    main()
