import json
from telegram.ext import Dispatcher, InlineQueryHandler, CommandHandler, MessageHandler, Filters
from telegram import Update, Bot
import boto3
import os
import emoji
from datetime import datetime
from TelegramTasweerBot_TelegramHandlers import health, image, emoji_handler, vid, url_handler

def lambda_handler(event, context):
    TelegramBotToken = os.environ['TelegramBotToken']
    bot = Bot(token=TelegramBotToken)
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

