#TODO: 
# control URLs, like youtube, and images from links
# Dont save image to file: https://stackoverflow.com/questions/59876271/how-to-process-images-from-telegram-bot-without-saving-to-file
# Fix/correct faces in images: https://aws.amazon.com/blogs/compute/creating-a-serverless-face-blurring-service-for-photos-in-amazon-s3/

from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
import boto3
import os
import emoji
from datetime import datetime
from TelegramTasweerBot_TelegramHandlers import health, image, emoji_handler, vid, url_handler
#import MessageEntity


def main():
    TELEGRAM_BOT = os.environ['TELEGRAM_BOT']
    emoji_blocklist = "[\U0001F600-\U0001F64B|\U0001F610-\U0001F61F|\U0001F937|\U0001F483|\U0001F435|\U0001F412|\U0001F920-\U0001F92F|\U0001F910-\U0001F917]" #Catches most of the F600 faces-range (except the last few which is the hands emojis). F937 is person shrugging, 1F483 is woman dancing, 1F435 and 1F412 are monkey. Catches some parts of the 1F900 range
    #emoji_blocklist = "[\U0001F300-\U0001F5FF|\U0001F600-\U0001F64F|\U0001F680-\U0001F6FF|\u2600-\u26FF\u2700-\u27BF]" #almost the full emoji range - but this will block hands, etc
    updater = Updater(TELEGRAM_BOT)
    dp = updater. dispatcher
    dp.add_handler(MessageHandler(Filters.photo | Filters.document.image | Filters.document.jpg, image)) #to catch inline photos, and photos as attachements/files
    dp.add_handler(MessageHandler(Filters.video | Filters.document.mime_type("video/mp4"), vid)) #to catch inline vidoes, and videos as attachements/files
    dp.add_handler(CommandHandler("health", health))
    dp.add_handler(MessageHandler(Filters.regex(emoji_blocklist), emoji_handler))
    dp.add_handler(MessageHandler(Filters.entity("youtube.com"), url_handler))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
