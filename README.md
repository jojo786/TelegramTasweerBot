# TelegramPrivacyBot
Telegram Bot that detects and deletes Personally Identifiable Information (PII).
Its written in python, using the [python-telegram-bot](https://pypi.org/project/python-telegram-bot/) telegram bot framework. 

It detects these potential sources of PII:
## Images
It uses AWS Rekognition to detect faces in an image, and then deletes.

## Videos
Once the filter picks up a video, it deletes it

# Privacy
This bot does not access any text messages. It only has handlers for video and images

# How to run it
Install the python requirements with pip, and then run it with python.
It picks up your telegram bot token from environment variables. AWS credentials also picked up from environment variables.
Add the bot to your groups/channels, then make it an Admin to manage PII in your channels/groups

# TODO: 
1. Dont use polling, so it can deployed as a Lambda
2. Dont save image to file: https://stackoverflow.com/questions/59876271/how-to-process-images-from-telegram-bot-without-saving-to-file
3. Store telegram bot credentials in config
4. Deploy to AWS; Lambda and API GW
5. Detect cartoon images
6. Add methods to query health status
7. Instead of deleting, remove/obscurre faces in images
