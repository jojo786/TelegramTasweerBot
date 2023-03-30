import boto3
import os
import emoji
from datetime import datetime
import time
from telegram import Update
from telegram.ext import ContextTypes

stage = os.environ['stage']

s3 = boto3.client('s3')

async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_list = ['Muaaza', 'LambdaYusufBot'] #List of telegram users that can bypass the rules and still post
    print("Start processing image:")

    chat_id = update.effective_chat.id
    chat_user = update.effective_message.from_user
    chat_group = update.effective_message.chat.title
    #context.bot.send_message(chat_id=chat_id, text="Detected image")

    if (update.effective_message.photo): # a photo, not a document
        file = await context.bot.getFile(update.effective_message.photo[-1].file_id)
    
    if (update.message.document): # a document, not a photo
        file = await context.bot.getFile(update.effective_message.document.file_id)
    
    file.download_to_drive(f'/tmp/image.jpg')
    with open("/tmp/image.jpg", 'rb') as image_file:
            image_face = {'Bytes': image_file.read()}
    print("Saved image, now going to Rekognition:")
    rekognition = boto3.client('rekognition')
    response = rekognition.detect_faces(Image=image_face, Attributes=['DEFAULT'])

    found_face = str({len(response['FaceDetails'])})
    if response['FaceDetails'] and (chat_user.username not in admin_list): #if there was a face found, and the person posting is NOT an admin, then delete
        print("Found " + found_face + " faces in image from user " + str(chat_user.username) + " in group " + str(chat_group) + ", going to delete")
        #context.bot.send_message(chat_id=chat_id, text="Found " + found_face + " faces, deleting...")
        await context.bot.delete_message(chat_id=chat_id, message_id=update.effective_message.message_id)
        # invoke the blurring service by uploading the image to S3 - in bucket
        print ("send to image blurring bucket")
        response = s3.upload_file('/tmp/image.jpg', 'telegramtasweerbot-'+stage+'-faceblur-in', 'image'+str(chat_id)+'-'+str(chat_user.first_name)+'-'+str(chat_user.last_name)+'.jpg')
        
    else:
        print("Found " + found_face + " faces in image from user " + str(chat_user.username) + " in group " + str(chat_group) + ", NOT going to delete")
        #context.bot.send_message(chat_id=chat_id, text="Found " + found_face + " faces, NOT deleting...")

async def vid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Start processing video")
    chat_id = update.effective_chat.id
    chat_user = update.effective_message.from_user
    chat_group = update.effective_message.chat.title

    print("Found video from user " + str(chat_user.username) + " in group " + str(chat_group) + ", going to delete")
    await context.bot.delete_message(chat_id=chat_id, message_id=update.effective_message.message_id)

async def health(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Start health command")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Was-salaam")

async def emoji_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Start processing emoji")

    chat_id = update.effective_message.chat_id
    chat_user = update.effective_message.from_user
    chat_group = update.effective_message.chat.title
    chat_text = update.effective_message.text
    
    #print ("BEFORE: " + chat_text)
    print("Found emoji from user " + str(chat_user.username) + " in group " + str(chat_group) + ", going to delete")
    await context.bot.delete_message(chat_id=chat_id, message_id=update.effective_message.message_id)

    if (len(chat_text) > 1): #if len = 1, then this is only an emoji, so no need to repost it, as there is no message text
        chat_text_noemoji = emoji.demojize(chat_text)
        last_name = str(chat_user.last_name) 
        if (last_name == "None"): # some users dont have a Last Name set in Telegram, so it displays as None. In which case, instead of showing None, just blank it out
            last_name = ""
        await context.bot.send_message(chat_id=chat_id, text= "Message from " + str(chat_user.first_name) + " " +  last_name + ": \n " + chat_text_noemoji)
        print ("AFTER removing emoji: " + chat_text_noemoji)

def url_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Start processing URL links")