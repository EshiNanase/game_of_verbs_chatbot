import requests
from google.cloud import dialogflow
import argparse


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


def main() -> None:

    parser = argparse.ArgumentParser(
        description='Script uploads more questions and answers to them'
    )
    parser.add_argument('-url', help='Link for Json file with more questions and answers for Dialogflow agent')
    args = parser.parse_args()
    url = args.url
    if not url:
        raise RuntimeError('No url provided!')

    response = requests.get(url=url)
    response.raise_for_status()
    data_for_uploading = response.json()

    for topic, information in data_for_uploading.items():
        questions = information['questions']
        answer = information['answer']

        create_intent('bold-streamer-1337', topic, questions, [answer])


if __name__ == '__main__':
    main()
