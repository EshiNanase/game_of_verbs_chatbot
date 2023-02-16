import logging
import telegram
from google.cloud import dialogflow


class ChatbotLogsHandler(logging.Handler):

    def __init__(self, telegram_chat_id, token):
        super(ChatbotLogsHandler, self).__init__()
        self.bot = telegram.Bot(token=token)
        self.chat_id = telegram_chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def ask_dialogflow(text, session_id):

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project='bold-streamer-1337', session=session_id)

    text_input = dialogflow.TextInput(text=text, language_code='ru-RU')
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response
