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
    #emoji regex has most of F4*, F6*, F9* and FA*
    emoji_blocklist  = "([\U0001F466-\U0001F479])" #Various person emojis, such as man, woman, boy, girl, princess, baby        
    emoji_blocklist += "|([\U0001F400-\U0001F416])" #F400 (rat) to F416 (pig)
    emoji_blocklist += "|([\U0001F47A-\U0001F47F])" #goblin, ghost           
    emoji_blocklist += "|([\U0001F481-\U0001F483])" #Dancer emojis, including woman dancing, man dancing, and people with bunny ears.
    emoji_blocklist += "|([\U0001F486-\U0001F487])" #Various person emojis, such as woman getting haircut, man getting haircut, and person getting massage.
    emoji_blocklist += "|([\U0001F600-\U0001F64B])" #F600-F64B: Emoticons and pictographs, including various facial expressions - https://unicode.org/charts/PDF/U1F600.pdf
    emoji_blocklist += "|([\U0001F648-\U0001F649])" #No-evil monkeys
    emoji_blocklist += "|([\U0001F645-\U0001F647])" #Various gesture emojis, such as person gesturing OK, person shrugging, and person tipping hand.
    emoji_blocklist += "|([\U0001F6B4-\U0001F6B6])" #Various person emojis, such as person biking, person mountain biking, and person walking.
    emoji_blocklist += "|([\U0001F910-\U0001F929])" #F910-F920: Additional emoticons and pictographs, including various facial expressions, hand gestures, and objects - https://unicode.org/charts/PDF/U1F900.pdf
    emoji_blocklist += "|([\U0001F930-\U0001F931])" #Various person: Pregnat women, breastfeeding
    emoji_blocklist += "|([\U0001F934-\U0001F939])" #Various person: Prince, tux, claus, shrugging, cartwheeling, juggling
    emoji_blocklist += "|([\U0001F980-\U0001F991])" #F980-F991: Animal emojies - https://unicode.org/charts/PDF/U1F900.pdf
    emoji_blocklist += "|([\U0001F9A0-\U0001F9A9])" #F980-F991: animals
    emoji_blocklist += "|([\U0001F9AA-\U0001F9AE])" #F980-F991: animals
    emoji_blocklist += "|([\U0001F9B0-\U0001F9B9])" #F980-F991: animals
    emoji_blocklist += "|([\U0001F9BA-\U0001F9BE])" #F980-F991: body parts
    emoji_blocklist += "|([\U0001F9CC-\U0001F9CF])" #F980-F991: animals
    emoji_blocklist += "|([\U0001F9D0-\U0001F9D9])" #F980-F991: animals
    emoji_blocklist += "|([\U0001F9DA-\U0001F9DE])" #F980-F991: body parts
    emoji_blocklist += "|([\U0001FAE0-\U0001FAE8])" #FAE0-FAE8: faces 
    

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

