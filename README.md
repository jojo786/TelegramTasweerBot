# TelegramTasweerBot
Telegram Bot that detects and deletes representations of animate objects.
Its written in python, using the [python-telegram-bot](https://pypi.org/project/python-telegram-bot/) telegram bot framework. 

# Islamic ruling regarding photography
Representations of animate objects are impermissible in Islam. This Bot can be used in your Telegram groups and channels to remove pictures and videos of animate objects.
The following list contains information from reliable and authentic Ulema regarding photography:
- [Is photos permissible in any madhab?](http://muftionline.co.za/node/2245)
- [Photography & Modern Challenges](http://alhaadi.org.za/articles-publications/books/60-taleemuddeen-publications/1966-photography-a-modern-challenges.html)
- [The Orchards of Love – Part Ten](https://ihyaauddeen.co.za/?p=16922)
- [Joint Statement regarding the viewing and usage of TV for propagation purposes](https://sites.google.com/site/duzakpdfs/duzakpdfs/Join_Statement_regarding_TV.pdf?attredirects=0&d=1)
- [Letter pertaining to the television Issue](https://sites.google.com/site/duzakpdfs/duzakpdfs/letter%20pertaining%20to%20the%20television%20Issue.pdf?attredirects=0&d=1)
- [Evil Effects of Television](https://www.dua.org.za/content/evil-effects-television)
- [Television - Root of Many Evil](https://www.dua.org.za/content/television-root-many-evils)
- [2014 - Announcement regarding Photography](https://ia802506.us.archive.org/7/items/Madraasah_Taaleemuddeen_Jalsa_2014/03_Important_Anouncemnet_Regarding_Photography.mp3)
- [2015 - Announcement regarding Photography](https://ia800507.us.archive.org/3/items/Madrasah_Taleemuddeen_Jalsa_2015/03_Important_Anouncement_Regarding_Photography.mp3)
- [2016 - Announcement regarding Photography](https://ia800408.us.archive.org/21/items/Madrasah_Taleemuddeen_Jalsa_2016/03_Important_Announcement.mp3)
- [2017 - Announcement regarding Photography](https://ia801602.us.archive.org/35/items/Madrasah_Taleemuddeen_Jalsa_2017/04_Important_Announcement.mp3)
- [2018 - Announcement regarding Photography](https://ia803107.us.archive.org/24/items/Madrasah_Taleemuddeen_Jalsa_2018/03_Important_Announcement.mp3)
- [2019 - Announcement regarding Photography](https://ia803006.us.archive.org/35/items/Madrasah_Taleemudden_Jalsah_2019/03_Important_Announcement_Ml_Ismail_Bayat.mp3)
- [2021 - Announcement regarding Photography](https://ia801507.us.archive.org/11/items/madrasah_taleemudden_jalsah_2021/08_Important_Announcement.mp3)
- [Wifaq ul Ulema SA - Photography](https://github.com/jojo786/TelegramPrivacyBot/blob/main/Photography%20-%20Wifaqul%20Ulama%20SA.jpg)
- [Wifaqul Madaaris - Announcement](https://github.com/jojo786/TelegramPrivacyBot/blob/main/Photography%20announcement-3.pdf)
- [Using Emojis](http://muftionline.co.za/node/32294)


It detects these types of objects in a telegram channel/group:
## Images
It uses AWS Rekognition to detect faces in an image, and then deletes.

## Videos
Once the filter picks up a video, it deletes it

## Emojis
Emoji is part of messages, but we did'nt want the bot to access all messages, so we used a Telegram Message Handler with a regex to catch only blacklisted emojis. This ensures that that the bot does not access most messages, and lowers the amount of times Telegram will invoke the bot (which will also keep the cost of running the bot low). The bot uses a blacklist/blocklist of emojis that are to be removed. Only messages with those emojis will be send to the bot, which will repalce the emoji image with its text short code, which is sometimes called [CLDR](http://cldr.unicode.org/translation/characters-emoji-symbols/short-names-and-keywords). E.g. a smiling face emoji will be replaced by `:grinning_face_with_big_eyes:`. The [python emoji library](https://github.com/carpedm20/emoji) is used, by calling the `demojize` method on the message. [Emojipedia](https://emojipedia.org/folded-hands-light-skin-tone/) as well as the [Unicode emoji list](https://unicode.org/emoji/charts/full-emoji-list.html). [Emojibase](https://www.emojibase.com/) is usefull as well. At the moment, the blocklist includes only the [U1F600 range](https://unicode.org/charts/PDF/U1F600.pdf), which is the most commonly used emojis, but it exludes the last few characters, so as to not block the hands emoji. The intention currently is not be an exhauustive blocklist of every haraam emoji. 
Other usefull resouces is [this]9https://stackoverflow.com/questions/31430587/how-to-send-emoji-with-telegram-bot-api) and [this](https://stackoverflow.com/questions/24840667/what-is-the-regex-to-extract-all-the-emojis-from-a-string), as well as this [regex tester](https://www.regextester.com/106421). It would be usefull if you could simply block emojis by these [categories](https://github.com/shanraisshan/EmojiCodeSheet). This bot uses a blocklist regex to catch emojis, but you could modify it to block all emojis, and exclude certain allowed ones but a [regex not operator](https://stackoverflow.com/questions/7317043/regex-not-operator), but the negative lookahead did not work with the Telegram filter.

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
10. Detect and delete emojis 

# Other AWS Options
1. [Image Moderation Chatbot](https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:426111819794:applications~image-moderation-chatbot)
2. [Serverless Image Handler](https://aws.amazon.com/about-aws/whats-new/2021/02/introducing-serverless-image-handler-v5-2/)

