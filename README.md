# Game of Verbs Telegram and VK Bots

Game of Verbs bots for answering most common customers' questions
Examples: 
Telegram: https://t.me/game_of_verbs_helper_bot
VKontakte: https://vk.com/public218877484

## Prerequisites

Virtual environment needs to be:

```
python==3.10
```
## Installing

First, you need to clone the code:

```
git clone https://github.com/EshiNanase/game_of_verbs_chatbot.git
```
Second, you need to install requirements.txt:

```
pip install -r requirements.txt
```
Third, you need to install gcloud following these instructions:
```
https://cloud.google.com/sdk/docs/install
```
Fourth, you need to login in gcloud:
```
gcloud auth login
```
## Environment variables

The code needs .env file with such environment variables as:

```
TELEGRAM_TOKEN = token of your Telegram bot, text https://t.me/BotFather to create one
TELEGRAM_CHAT_ID = needed for logger you can find it here https://t.me/userinfobot
VK_TOKEN = token of your VK group, follow these instructions to create https://habr.com/ru/company/vk/blog/570486/
SESSION_ID = can be anything
```
## Running

The code should be ran in cmd like so:

```
python telegram_chatbot.py & python vk_chatbot.py
```
![](https://github.com/EshiNanase/game_of_verbs_chatbot/blob/main/gif.gif)
