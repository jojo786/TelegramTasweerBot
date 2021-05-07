#TODO: 
# Dont use polling, so it can deployed as a Lambda
# Deploy to AWS; Lambda and API GW
# Dont save image to file: https://stackoverflow.com/questions/59876271/how-to-process-images-from-telegram-bot-without-saving-to-file
# Detect cartoon images
# Fix/correct faces in images

from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
import boto3
import os
import emoji
from datetime import datetime

def image(update, context):
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(date + " - Start processing image:")

    chat_id = update.message.chat_id
    chat_user = update.message.from_user
    chat_group = update.message.chat.title
    #context.bot.send_message(chat_id=chat_id, text="Detected image")

    if (update.message.photo):
        file = context.bot.getFile(update.message.photo[-1].file_id)
    
    if (update.message.document):
        file = context.bot.getFile(update.message.document.file_id)
    
    file.download('image.jpg')
    with open("image.jpg", 'rb') as image_file:
            image_face = {'Bytes': image_file.read()}
    rekognition = boto3.client('rekognition')
    response = rekognition.detect_faces(Image=image_face, Attributes=['DEFAULT'])
    
    found_face = str({len(response['FaceDetails'])})
    if response['FaceDetails']:
        print(date + " - Found " + found_face + " faces in image from user " + str(chat_user.username) + " in group " + str(chat_group) + ", going to delete")
        #context.bot.send_message(chat_id=chat_id, text="Found " + found_face + " faces, deleting...")
        context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
        update_db(chat_group, dynamodb=None)
    else:
        print(date + " - Found " + found_face + " faces in image, NOT going to delete")
        #context.bot.send_message(chat_id=chat_id, text="Found " + found_face + " faces, NOT deleting...")

def vid(update, context):
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(date + " - Start processing video")
    chat_id = update.message.chat_id
    chat_user = update.message.from_user
    chat_group = update.message.chat.title

    print(date + " - Found video from user " + str(chat_user.username) + " in group " + str(chat_group) + ", going to delete")
    context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
    update_db(chat_group, dynamodb=None)

def health(update, context):
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(date + " - Start health command")
    update.message.reply_text('Was-salaam')

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

def emoji_handler(update, context):
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(date + " - Start processing emoji")

    chat_id = update.message.chat_id
    chat_user = update.message.from_user
    chat_group = update.message.chat.title
    chat_text = update.message.text
    
    #print ("BEFORE: " + chat_text)
    print(date + " - Found emoji from user " + str(chat_user.username) + " in group " + str(chat_group) + ", going to delete")
    context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)

    if (len(chat_text) > 1):
        chat_text_noemoji = emoji.demojize(chat_text)
        context.bot.send_message(chat_id=chat_id, text= "Message from " + str(chat_user.first_name) + " " +  str(chat_user.last_name) + ": \n " + chat_text_noemoji)
        print (date + " - AFTER removing emoji: " + chat_text_noemoji)

def main():
    TELEGRAM_BOT = os.environ['TELEGRAM_BOT']
    emoji_blocklist = "[\U0001F600-\U0001F64B]"

    updater = Updater(TELEGRAM_BOT)
    dp = updater. dispatcher
    dp.add_handler(MessageHandler(Filters.photo | Filters.document.image | Filters.document.jpg, image))
    dp.add_handler(MessageHandler(Filters.video | Filters.document.mime_type("video/mp4"), vid))
    dp.add_handler(CommandHandler("health", health))
    dp.add_handler(MessageHandler(Filters.regex(emoji_blocklist), emoji_handler))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
