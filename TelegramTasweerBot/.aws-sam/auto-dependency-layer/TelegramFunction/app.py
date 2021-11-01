import json
from telegram.ext import Dispatcher, InlineQueryHandler, CommandHandler, MessageHandler, Filters
from telegram import Update, Bot
import boto3
import os
import emoji
from datetime import datetime


def health(update, context):
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(date + " - Start health command")
    update.message.reply_text('Was-salaam')

def image(update, context):
    admin_list = ['jojo786', 'Muaaza'] #List of telegram users that can bypass the rules and still post
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(date + " - Start processing image:")

    chat_id = update.message.chat_id
    chat_user = update.message.from_user
    chat_group = update.message.chat.title
    #context.bot.send_message(chat_id=chat_id, text="Detected image")

    if (update.message.photo): # a photo, not a document
        file = context.bot.getFile(update.message.photo[-1].file_id)
    
    if (update.message.document): # a document, not a photo
        file = context.bot.getFile(update.message.document.file_id)
    
    file.download(f'/tmp/image.jpg')
    with open("/tmp/image.jpg", 'rb') as image_file:
            image_face = {'Bytes': image_file.read()}
    print(date + " - Saved image, now going to Rekcognition:")
    rekognition = boto3.client('rekognition')
    response = rekognition.detect_faces(Image=image_face, Attributes=['DEFAULT'])

    os.remove("/tmp/image.jpg") #delete the file once its already processed
    
    found_face = str({len(response['FaceDetails'])})
    if response['FaceDetails'] and (chat_user.username not in admin_list): #if there was a face found, and the person posting is NOT an admin, then delete
        print(date + " - Found " + found_face + " faces in image from user " + str(chat_user.username) + " in group " + str(chat_group) + ", going to delete")
        #context.bot.send_message(chat_id=chat_id, text="Found " + found_face + " faces, deleting...")
        context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
        update_db(chat_group, dynamodb=None)
    else:
        print(date + " - Found " + found_face + " faces in image from user " + str(chat_user.username) + " in group " + str(chat_group) + ", NOT going to delete")
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

    if (len(chat_text) > 1): #if len = 1, then this is only an emoji, so no need to repost it, as there is no message text
        chat_text_noemoji = emoji.demojize(chat_text)
        last_name = str(chat_user.last_name) 
        if (last_name == "None"): # some users dont have a Last Name set in Telegram, so it displays as None. In which case, instead of showing None, just blank it out
            last_name = ""
        context.bot.send_message(chat_id=chat_id, text= "Message from " + str(chat_user.first_name) + " " +  last_name + ": \n " + chat_text_noemoji)
        print (date + " - AFTER removing emoji: " + chat_text_noemoji)

    update_db(chat_group, dynamodb=None)

def url_handler(update, context):
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(date + " - Start processing URL links")


def lambda_handler(event, context):
    bot = Bot(token='2024083896:AAHWyb50jf8_8ICVlFzQfOR7cN4u9paryEA')
    dispatcher = Dispatcher(bot, None, use_context=True)
    
    emoji_blocklist = "[\U0001F600-\U0001F64B|\U0001F610-\U0001F61F|\U0001F937|\U0001F483|\U0001F435|\U0001F412|\U0001F920-\U0001F92F|\U0001F910-\U0001F917]" #Catches most of the F600 faces-range (except the last few which is the hands emojis). F937 is person shrugging, 1F483 is woman dancing, 1F435 and 1F412 are monkey. Catches some parts of the 1F900 range
    
    dispatcher.add_handler(MessageHandler(Filters.photo | Filters.document.image | Filters.document.jpg, image)) #to catch inline photos, and photos as attachements/files
    dispatcher.add_handler(MessageHandler(Filters.video | Filters.document.mime_type("video/mp4"), vid)) #to catch inline vidoes, and videos as attachements/files
    dispatcher.add_handler(CommandHandler("health", health))
    dispatcher.add_handler(MessageHandler(Filters.regex(emoji_blocklist), emoji_handler))
    dispatcher.add_handler(MessageHandler(Filters.entity("youtube.com"), url_handler))

    try:
        dispatcher.process_update(
            Update.de_json(json.loads(event["body"]), bot)
        )

    except Exception as e:
        print(e)
        return {"statusCode": 500}

    return {"statusCode": 200}

