import dotenv
import os
from telegram import Update, ForceReply
from telegram.ext import Updater, CallbackContext
import logging
from logger_and_dialogflow import ask_dialogflow, ChatbotLogsHandler


logger = logging.getLogger(__file__)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_markdown_v2(
        'Здравствуйте! Добро пожаловать в наш диалог!',
        reply_markup=ForceReply(selective=True),
    )


def answer(update: Update, context: CallbackContext) -> None:
    dialogflow_answer = ask_dialogflow(update.message.text, os.environ['SESSION_ID'])
    update.message.reply_text(dialogflow_answer.query_result.fulfillment_text)


def main() -> None:
    dotenv.load_dotenv()

    telegram_token = os.environ['TELEGRAM_TOKEN']
    telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']

    logging.basicConfig(level=logging.WARNING)
    logger.addHandler(ChatbotLogsHandler(telegram_chat_id, telegram_token))

    updater = Updater(telegram_token, use_context=True)
    updater.start_polling()


if __name__ == '__main__':
    main()
