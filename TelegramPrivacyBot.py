#TODO: 
# Dont use polling, so it can deployed as a Lambda
# Dont save image to file: https://stackoverflow.com/questions/59876271/how-to-process-images-from-telegram-bot-without-saving-to-file
# Dont store telegram bot credentials in source code
# Deploy to AWS; Lambda and API GW
# Detect cartoon images
# Detect videos

from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
import requests
import re
import boto3
import os

def image(update, context):
    print("Start processing image")

    chat_id = update.message.chat_id
    #context.bot.send_message(chat_id=chat_id, text="Detected image")

    file = context.bot.getFile(update.message.photo[-1].file_id)
    file.download('image.jpg')
    with open("image.jpg", 'rb') as image_file:
            image_face = {'Bytes': image_file.read()}
    rekognition = boto3.client('rekognition')
    response = rekognition.detect_faces(Image=image_face, Attributes=['DEFAULT'])
    
    found_face = str({len(response['FaceDetails'])})
    if response['FaceDetails']:
        print("Found " + found_face + " faces in image, going to delete")
        #context.bot.send_message(chat_id=chat_id, text="Found " + found_face + " faces, deleting...")
        context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
    else:
        print("Found " + found_face + " faces in image, NOT going to delete")
        #context.bot.send_message(chat_id=chat_id, text="Found " + found_face + " faces, NOT deleting...")

def vid(update, context):
    print("Start processing video")
    chat_id = update.message.chat_id
    print("Found video, going to delete")
    context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)


def main():
    TELEGRAM_BOT = os.environ['TELEGRAM_BOT'] 
    updater = Updater(TELEGRAM_BOT)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.photo, image))
    dp.add_handler(MessageHandler(Filters.video, vid))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
