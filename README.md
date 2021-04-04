Photos of animate objects are impermissible in Islam. This Bot can be used in your Telegram groups and channels to remove pictures and videos of animate objects.
The following contains more information of the rulings regaring photography:
- [Is photos permissible in any madhab?](http://muftionline.co.za/node/2245)
- [Photography & Modern Challenges](http://alhaadi.org.za/articles-publications/books/60-taleemuddeen-publications/1966-photography-a-modern-challenges.html)
- [The Orchards of Love – Part Ten](https://ihyaauddeen.co.za/?p=16922)
- [Joint Statement regarding the viewing and usage of TV for propagation purposes](https://sites.google.com/site/duzakpdfs/duzakpdfs/Join_Statement_regarding_TV.pdf?attredirects=0&d=1)
- [Letter pertaining to the television Issue](https://sites.google.com/site/duzakpdfs/duzakpdfs/letter%20pertaining%20to%20the%20television%20Issue.pdf?attredirects=0&d=1)

# TelegramMooratyBot
Telegram Bot that detects and deletes representations of animate objects.
Its written in python, using the [python-telegram-bot](https://pypi.org/project/python-telegram-bot/) telegram bot framework. 

It detects these types:
## Images
It uses AWS Rekognition to detect faces in an image, and then deletes.

## Videos
Once the filter picks up a video, it deletes it

# Privacy
This bot does not access any text messages. It only has handlers for video and images

# How to run it
Install the python requirements with pip, and then run it with python.
It picks up your telegram bot token from environment variables. AWS credentials also picked up from environment variables.
Add the bot to your groups/channels, then make it an Admin to manage PII in your channels/groups

# TODO: 
1. Dont use polling, so it can deployed as a Lambda
2. Dont save image to file: https://stackoverflow.com/questions/59876271/how-to-process-images-from-telegram-bot-without-saving-to-file
3. Store telegram bot credentials in config
4. Deploy to AWS; Lambda and API GW
5. Detect cartoon images
6. Instead of deleting, remove/obscurre faces in images
7. Detect and remove images sent as file
8. Filter and detect a list of URLs, e.g youtube.com
9. Analyse inline images that accompany URLs/links

# Other AWS Options
1. [Image Moderation Chatbot](https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:426111819794:applications~image-moderation-chatbot)
2. [Serverless Image Handler](https://aws.amazon.com/about-aws/whats-new/2021/02/introducing-serverless-image-handler-v5-2/)

