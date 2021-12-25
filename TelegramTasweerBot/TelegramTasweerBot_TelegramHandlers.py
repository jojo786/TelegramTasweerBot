from telegram.ext import Dispatcher, Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
import boto3
import os
import emoji
from datetime import datetime
#import MessageEntity

bot_table = boto3.resource("dynamodb", region_name="eu-west-1").Table(os.environ["TelegramBotDynamoTable"])
s3 = boto3.client('s3')

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

    found_face = str({len(response['FaceDetails'])})
    if response['FaceDetails']: #and (chat_user.username not in admin_list): #if there was a face found, and the person posting is NOT an admin, then delete
        print(date + " - Found " + found_face + " faces in image from user " + str(chat_user.username) + " in group " + str(chat_group) + ", going to delete")
        #context.bot.send_message(chat_id=chat_id, text="Found " + found_face + " faces, deleting...")
        context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
        update_db(chat_group, dynamodb=None)

        response = s3.upload_file('/tmp/image.jpg', 'face-blur-in-bucket', 'image.jpg')

        context.bot.sendPhoto(chat_id=chat_id, photo=image_face, caption="Message from " + str(chat_user.first_name) + " " +  chat_user.last_name)
        print (date + " - AFTER blurring image and resending: ")
        
    else:
        print(date + " - Found " + found_face + " faces in image from user " + str(chat_user.username) + " in group " + str(chat_group) + ", NOT going to delete")
        #context.bot.send_message(chat_id=chat_id, text="Found " + found_face + " faces, NOT deleting...")

    os.remove("/tmp/image.jpg") #delete the file once its already processed

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

    table = bot_table

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