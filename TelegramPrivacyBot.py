#TODO: 
# Dont use polling, so it can deployed as a Lambda
# Deploy to AWS; Lambda and API GW
# Dont save image to file: https://stackoverflow.com/questions/59876271/how-to-process-images-from-telegram-bot-without-saving-to-file
# Detect cartoon images
# Fix/correct faces in images

from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
from pprint import pprint
import requests
import re
import boto3
import os

def image(update, context):
    print("Start processing image")

    chat_id = update.message.chat_id
    chat_user = update.message.from_user
    chat_group = update.message.chat.title
    #context.bot.send_message(chat_id=chat_id, text="Detected image")

    file = context.bot.getFile(update.message.photo[-1].file_id)
    file.download('image.jpg')
    with open("image.jpg", 'rb') as image_file:
            image_face = {'Bytes': image_file.read()}
    rekognition = boto3.client('rekognition')
    response = rekognition.detect_faces(Image=image_face, Attributes=['DEFAULT'])
    
    found_face = str({len(response['FaceDetails'])})
    if response['FaceDetails']:
        print("Found " + found_face + " faces in image from user " + str(chat_user.username) + " in group " + str(chat_group) + ", going to delete")
        #context.bot.send_message(chat_id=chat_id, text="Found " + found_face + " faces, deleting...")
        context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
        update_db(chat_group, dynamodb=None)
    else:
        print("Found " + found_face + " faces in image, NOT going to delete")
        #context.bot.send_message(chat_id=chat_id, text="Found " + found_face + " faces, NOT deleting...")

def vid(update, context):
    print("Start processing video")
    chat_id = update.message.chat_id
    chat_user = update.message.from_user
    chat_group = update.message.chat.title

    print("Found video from user " + str(chat_user.username) + " in group " + str(chat_group) + ", going to delete")
    context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
    update_db(chat_group, dynamodb=None)

def health(update, context):
    print("Start health command")
    update.message.reply_text('Someone called?')

def update_db(group, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', 'eu-west-1')

    table = dynamodb.Table('MuslimPrivacyBot')

    try:
        response = table.update_item(
        Key={
            'group': group
        },
        UpdateExpression="set blocked = blocked + :val",
        ExpressionAttributeValues={
            ':val': 1
        },
        ReturnValues="UPDATED_NEW"
        )
    except:
        response = table.put_item(
        Item={
            'group': group,
            'blocked': 1
       }
    )


def main():
    TELEGRAM_BOT = os.environ['TELEGRAM_BOT'] 
    updater = Updater(TELEGRAM_BOT)
    dp = updater. dispatcher
    dp.add_handler(MessageHandler(Filters.photo, image))
    dp.add_handler(MessageHandler(Filters.video, vid))
    dp.add_handler(CommandHandler("health", health))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
