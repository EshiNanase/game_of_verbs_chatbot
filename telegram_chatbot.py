import dotenv
import os

import telegram
from telegram import Update, ForceReply
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from google.cloud import dialogflow
import logging
import requests
import time

GOOGLE_APPLICATION_CREDENTIALS = 'credentials.json'


class ChatbotLogsHandler(logging.Handler):

    def __init__(self, telegram_chat_id):
        super(ChatbotLogsHandler, self).__init__()
        self.bot = telegram.Bot(token=os.environ['TELEGRAM_TOKEN'])
        self.chat_id = telegram_chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


logger = logging.getLogger(__file__)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_markdown_v2(
        'Здравствуйте! Добро пожаловать в наш диалог!',
        reply_markup=ForceReply(selective=True),
    )


def answer(update: Update, context: CallbackContext) -> None:
    dialogflow_answer = ask_dialogflow(update.message.text)
    update.message.reply_text(dialogflow_answer.query_result.fulfillment_text)


def ask_dialogflow(text):

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(os.environ['PROJECT_ID'], os.environ['SESSION_ID'])

    text_input = dialogflow.TextInput(text=text, language_code='ru-RU')
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response


def main() -> None:
    dotenv.load_dotenv()

    telegram_token = os.environ['TELEGRAM_TOKEN']
    updater = Updater(telegram_token, use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))

    telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']
    logging.basicConfig(level=logging.WARNING)
    logger.addHandler(ChatbotLogsHandler(telegram_chat_id))

    try:
        updater.start_polling()

    except requests.exceptions.ReadTimeout as err:
        logger.warning('Боту прилетело:')
        logger.warning(err, exc_info=True)

    except requests.exceptions.ConnectionError as err:
        logger.warning('Боту прилетело:')
        logger.warning(err, exc_info=True)
        time.sleep(5)


if __name__ == '__main__':
    main()
