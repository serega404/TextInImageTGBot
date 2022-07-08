# pip install Pillow
from PIL import Image, ImageDraw, ImageFont
import requests
import time
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher

logging.basicConfig(format='%(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

updater = None

def start(update, context):
    s = "Бот служит для создания картинок с вашим текстом. Напишите боту сообщение и он прекрепит его к картинке."
    update.message.reply_text(s)

def repeater(update, context):
    image = Image.open("sample.jpg")
    W, H = image.size

    font = ImageFont.truetype("youfont.ttf", 45)
    drawer = ImageDraw.Draw(image)
    w, h = drawer.textsize(update.message.text, font=font)
    drawer.text(((W-w)/2,(H-h)-32), update.message.text, font=font, fill='white')
    
    image.save('new_img.jpg')

    f = open('user_log.txt', 'a', encoding='utf-8')
    Name = str(update.message.from_user.first_name) + " " + str(update.message.from_user.last_name);
    f.write(str(update.message.from_user.id) + " (" + Name + ")"  + ": " + str(update.message.text) + '\n')
    f.close()
    
    update.message.reply_photo(photo=open('new_img.jpg', 'rb'))
    update.message.reply_text("Ваша картинка готова")


def start_bot():
    global updater
    updater = Updater(
        'TELEGRAMbotTOKEN', use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, repeater))

    updater.start_polling()

    updater.idle()

start_bot()