import requests
from google.cloud import dialogflow
import argparse
import os
import dotenv


def create_intent(project_id, display_name, training_phrases_parts, message_texts):

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )


def ask_dialogflow(text, project_id, session_id):

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project=project_id, session=session_id)

    text_input = dialogflow.TextInput(text=text, language_code='ru-RU')
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response


def main() -> None:
    dotenv.load_dotenv()

    project_id = os.environ['PROJECT_ID']

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', help='Link for Json file with more questions and answers for Dialogflow agent')
    args = parser.parse_args()
    url = args.url
    if not url:
        raise RuntimeError('No url provided!')

    response = requests.get(url=url)
    response.raise_for_status()
    intents = response.json()

    for topic, information in intents.items():
        questions = information['questions']
        answer = information['answer']

        create_intent(project_id, topic, questions, [answer])


if __name__ == '__main__':
    main()
