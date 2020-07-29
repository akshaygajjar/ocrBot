
"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging
import os
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import cloudmersive_ocr_api_client
from cloudmersive_ocr_api_client.rest import ApiException

KEY = "8c78f9d3-8848-48d3-86ba-a7aaf8ab9796"
configuration = cloudmersive_ocr_api_client.Configuration()
configuration.api_key['Apikey'] = KEY

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(f'\nHi !!! \n{update.effective_user.full_name} \nWelcome to Optical Character Recognizer Bot.\nJust send a clear image to the bot and it will recognize the text in the image and send it as a message!\nTo get my contact details tap /contact \nTo get donation details tap /donate\n')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

    
def contact(update, context):
    """Send a message when the command /contact is issued."""
    # update.message.reply_text('contact details soon !!')
    update.message.reply_text("Hey!! You can find me on \n[Telegram](https://telegram.me/akshay_gajjar)\n[Facebook](https://facebook.com/akshuu.prajapati)\n[Instagram](https://instagram.com/_akshay_gajjar)\n[Twitter](https://twitter.com/imakshaygajjar)", parse_mode=ParseMode.MARKDOWN)

def donate(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Thanks for hitting donate button')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)
    
    
def convert_image(update, context):
    """Convert image into text(Image as photo)"""
    filename = 'Ocr.jpg'
    file_id = update.message.photo[-1].file_id
    newFile = context.bot.get_file(file_id)
    newFile.download(filename)

    #we have access to the photo file till here 
    update.message.reply_text('Yeah ! I got image and Downloaded it !')

    api_instance = cloudmersive_ocr_api_client.ImageOcrApi()
    api_instance.api_client.configuration.api_key = {}
    api_instance.api_client.configuration.api_key['Apikey'] = KEY
    try:
        api_response = api_instance.image_ocr_post(filename)
        confidence = api_response.mean_confidence_level
        update.message.reply_text(f"Confidence : {confidence}\nExtracted Text is : {api_response.text_result}")
        os.remove(filename)
    except Exception as e: 
        update.message.reply_text("Error Occured " + e)    
        try:
            os.remove(filename)
        except Exception:
            pass

def convert_file(update, context):
    """Convert image file into text(Iamge as a file)"""
    file = 'Ocr.jpg'
    fileID = update.message.document.file_id
    new = context.bot.get_file(fileID)
    new.download(file)

    #we have access to the photo file till here 
    update.message.reply_text('Yeah ! I got image and Downloaded it !')

    api_instance = cloudmersive_ocr_api_client.ImageOcrApi()
    api_instance.api_client.configuration.api_key = {}
    api_instance.api_client.configuration.api_key['Apikey'] = KEY
    try:
        api_response = api_instance.image_ocr_post(file)
        confidence = api_response.mean_confidence_level
        update.message.reply_text(f"Confidence : {confidence}\nExtracted Text is : {api_response.text_result}")
        os.remove(file)
    except Exception as e: 
        update.message.reply_text("Error Occured " + e)    
        try:
            os.remove(file)
        except Exception:
            pass
        
def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1011780131:AAFbABXZDSS1WXu-ng7EZqR_ajKrVGGfJxo", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("contact", contact))
    dp.add_handler(CommandHandler("donate", donate))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dp.add_handler(MessageHandler(Filters.photo & ~Filters.command, convert_image)) 
    dp.add_handler(MessageHandler(Filters.document & ~Filters.command, convert_file)) 
    

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()