# TelegramPrivacyBot
Telegram Bot that detects and deletes Personally identifiable information (PII). For now, it delete images that contain faces
Its written in Python, using the https://pypi.org/project/python-telegram-bot/. The bot only runs on images. It uses AWS Rekognition to detect faces in the image, and then deletes.

Add the bot to your groups to manage PII.

#TODO: 
# Dont use polling, so it can deployed as a Lambda
# Dont save image to file: https://stackoverflow.com/questions/59876271/how-to-process-images-from-telegram-bot-without-saving-to-file
# Dont store telegram bot credentials in source code
# Deploy to AWS; Lambda and API GW
# Detect cartoon images
# Detect videos
