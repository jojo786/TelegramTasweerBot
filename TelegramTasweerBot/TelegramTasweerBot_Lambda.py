import json
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import boto3
import os
import emoji
from datetime import datetime
from TelegramTasweerBot_TelegramHandlers import health, image, emoji_handler, vid, url_handler
from aws_lambda_powertools.utilities import parameters

ssm_provider = parameters.SSMProvider()

stage = os.environ['stage']
TelegramBotToken = ssm_provider.get('/telegramtasweerbot/telegram/'+stage+'/bot_token', decrypt=True)

application = ApplicationBuilder().token(TelegramBotToken).build()

def lambda_handler(event, context):
    return asyncio.get_event_loop().run_until_complete(main(event, context))

async def main(event, context):
    emoji_blocklist = "([\U0001F600-\U0001F64B])" #F600-F64B: Emoticons and pictographs, including various facial expressions - https://unicode.org/charts/PDF/U1F600.pdf
    emoji_blocklist += "|([\U0001F910-\U0001F96B])" #F910-F96B: Additional emoticons and pictographs, including various facial expressions, hand gestures, and objects - https://unicode.org/charts/PDF/U1F900.pdf
    emoji_blocklist += "|([\U0001F980-\U0001F991])" #F980-F991: Animal emojies - https://unicode.org/charts/PDF/U1F900.pdf
    emoji_blocklist += "|([\U0001FAE0-\U0001FAE8])" #FAE0-FAE8: faces 
    emoji_blocklist += "|([\U0001F466-\U0001F478])" #Various person emojis, such as man, woman, boy, girl, princess, baby                  
    emoji_blocklist += "|([\U0001F481-\U0001F483])" #Dancer emojis, including woman dancing, man dancing, and people with bunny ears.
    emoji_blocklist += "|([\U0001F486-\U0001F487])" #Various person emojis, such as woman getting haircut, man getting haircut, and person getting massage.
    emoji_blocklist += "|([\U0001F645-\U0001F647])" #Various gesture emojis, such as person gesturing OK, person shrugging, and person tipping hand.
    emoji_blocklist += "|([\U0001F937])|([\U0001F483])|([\U0001F435])|([\U0001F412])"  #F937 is person shrugging, F483 is woman dancing, F435 and F412 are monkeys. 

    #still to test
    #\U0001F645-\U0001F647: Various gesture emojis, such as person gesturing OK, person shrugging, and person tipping hand.
    #\U0001F64B-\U0001F64F: Various person emojis, such as person raising hand, person bowing, and person with folded hands.
    #\U0001F6A3: Rowboat emoji, which depicts a person rowing a boat.
    #\U0001F6B4-\U0001F6B6: Various person emojis, such as person biking, person mountain biking, and person walking.
    #\U0001F6C0: Bath emoji, which depicts a person in a bathtub.
    #\U0001F938: Prince emoji.
    #\U0001F93C: Person in lotus position emoji, which depicts a person sitting cross-legged with their eyes closed.
    #\U0001F93D: Skateboarder emoji.
    #\U0001F93E: Person surfing emoji.
    #\U0001F9D1-\U0001F9D3: Various person emojis, such as person in wheelchair, person with probing cane, and person with white cane.

    application.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE | filters.Document.JPG, image)) #to catch inline photos, and photos as attachements/files
    application.add_handler(MessageHandler(filters.VIDEO | filters.Document.MimeType('video/mp4'), vid)) #to catch inline vidoes, and videos as attachements/files
    application.add_handler(CommandHandler('health', health))
    application.add_handler(MessageHandler(filters.Regex(emoji_blocklist), emoji_handler))
    application.add_handler(MessageHandler(filters.Entity('youtube.com'), url_handler)) #Not working

    try:    
        await application.initialize()
        await application.process_update(
            Update.de_json(json.loads(event["body"]), application.bot)
        )
    
        return {
            'statusCode': 200,
            'body': 'Success'
        }

    except Exception as exc:
        return {
            'statusCode': 500,
            'body': 'Failure'
        }

