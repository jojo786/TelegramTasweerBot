# TelegramPrivacyBot
Telegram Bot that detects and deletes Personally identifiable information (PII). For now, it delete images that contain faces
Its written in Python, using the [python-telegram-bot](https://pypi.org/project/python-telegram-bot/) telegram bot framework. The bot only runs on images. It uses AWS Rekognition to detect faces in the image, and then deletes.

It picks up your telegram bot token from environment variables. AWS credentials also picked up from environment variables.
Add the bot to your groups to manage PII.

#TODO: 
1. Dont use polling, so it can deployed as a Lambda
2. Dont save image to file: https://stackoverflow.com/questions/59876271/how-to-process-images-from-telegram-bot-without-saving-to-file
3. Dont store telegram bot credentials in source code
4. Deploy to AWS; Lambda and API GW
5. Detect cartoon images
6. Detect videos
