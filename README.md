# TelegramPrivacyBot
Telegram Bot that detects and deletes Personally identifiable information (PII). For now, it delete images that contain faces
Its written in Python, using the [python-telegram-bot](https://pypi.org/project/python-telegram-bot/) telegram bot framework. 
When it detects:
## Images
It uses AWS Rekognition to detect faces in the image, and then deletes.
## Videos
Once the filter picks up a video, it deletes it


# To run it
Install the python requirements with pip, and then run it with python.
It picks up your telegram bot token from environment variables. AWS credentials also picked up from environment variables.
Add the bot to your groups to manage PII.

#TODO: 
1. Dont use polling, so it can deployed as a Lambda
2. Dont save image to file: https://stackoverflow.com/questions/59876271/how-to-process-images-from-telegram-bot-without-saving-to-file
3. Dont store telegram bot credentials in source code
4. Deploy to AWS; Lambda and API GW
5. Detect cartoon images
