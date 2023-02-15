import dotenv
import os
from telegram import Update, ForceReply, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from google.cloud import dialogflow


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_markdown_v2(
        'Здравствуйте! Добро пожаловать в наш диалог!',
        reply_markup=ForceReply(selective=True),
    )


def echo(update: Update, context: CallbackContext) -> None:
    answer = ask_dialogflow(update.message.text)
    update.message.reply_text(answer)


def ask_dialogflow(text):

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(os.environ['PROJECT_ID'], os.environ['SESSION_ID'])

    text_input = dialogflow.TextInput(text=text, language_code='ru-RU')
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    print("Query text: {}".format(response.query_result.query_text))
    print(
        "Detected intent: {} (confidence: {})\n".format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        )
    )
    print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))

    return response.query_result.fulfillment_text


def main() -> None:
    dotenv.load_dotenv()

    telegram_token = os.environ['TELEGRAM_TOKEN']
    updater = Updater(telegram_token, use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()


if __name__ == '__main__':
    main()
