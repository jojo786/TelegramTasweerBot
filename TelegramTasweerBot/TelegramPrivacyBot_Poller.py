from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import boto3
import os
import emoji
from datetime import datetime
from TelegramTasweerBot_TelegramHandlers import health, image, emoji_handler, vid, url_handler


def main():
    TelegramBotToken = os.environ['TelegramBotToken']
    application = ApplicationBuilder().token('TelegramBotToken').build()

    #emoji_blocklist = "[\U0001F600-\U0001F64B|\U0001F610-\U0001F61F|\U0001F937|\U0001F483|\U0001F435|\U0001F412|\U0001F920-\U0001F92F|\U0001F910-\U0001F917]" #Catches most of the F600 faces-range (except the last few which is the hands emojis). F937 is person shrugging, 1F483 is woman dancing, 1F435 and 1F412 are monkey. Catches some parts of the 1F900 range
    emoji_blocklist  = "([\U0001F600-\U0001F64B])" #F600-F64B: Emoticons and pictographs, including various facial expressions - https://unicode.org/charts/PDF/U1F600.pdf
    emoji_blocklist += "|([\U0001F910-\U0001F96B])" #F910-F96B: Additional emoticons and pictographs, including various facial expressions, hand gestures, and objects - https://unicode.org/charts/PDF/U1F900.pdf
    emoji_blocklist += "|([\U0001F980-\U0001F991])" #F980-F991: Animal emojies - https://unicode.org/charts/PDF/U1F900.pdf
    emoji_blocklist += "|([\U0001FAE0-\U0001FAE8])" #FAE0-FAE8: faces 
    emoji_blocklist += "|([\U0001F466-\U0001F478])" #Various person emojis, such as man, woman, boy, girl, princess, baby                  
    emoji_blocklist += "|([\U0001F481-\U0001F483])" #Dancer emojis, including woman dancing, man dancing, and people with bunny ears.
    emoji_blocklist += "|([\U0001F486-\U0001F487])" #Various person emojis, such as woman getting haircut, man getting haircut, and person getting massage.
    emoji_blocklist += "|([\U0001F645-\U0001F647])" #Various gesture emojis, such as person gesturing OK, person shrugging, and person tipping hand.
    emoji_blocklist += "|([\U0001F648-\U0001F649])" #No-evil monkeys
    emoji_blocklist += "|([\U0001F937])|([\U0001F483])|([\U0001F435])|([\U0001F412])|([\U0001F6A3])"  #F937 is person shrugging, F483 is woman dancing, F435 and F412 are monkeys, F6A3: Rowboat emoji 
    print(emoji_blocklist)

    application.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE | filters.Document.JPG, image)) #to catch inline photos, and photos as attachements/files
    application.add_handler(MessageHandler(filters.VIDEO | filters.Document.MimeType('video/mp4'), vid)) #to catch inline vidoes, and videos as attachements/files
    application.add_handler(CommandHandler('health', health))
    application.add_handler(MessageHandler(filters.Regex(emoji_blocklist), emoji_handler))
    application.add_handler(MessageHandler(filters.Entity('youtube.com'), url_handler)) #Not working

    application.run_polling()

if __name__ == '__main__':
    main()
