from typing import Callable
import telegram.ext as ext

from chatbot import Chatbot


with open("token.txt", 'r') as f:
    token = f.read()

def start(update, context):
    update.message.reply_text("Hello! Welcome to ArthurBot")

def content(update, context):
    update.message.reply_text("I am A bot made by aiwizzard, Thank you for using me")

def contact(update, context):
    update.message.reply_text("You can see him in git")

chatbot = Chatbot()

# add conversational ai here
def handle_message(update, context):
    response = chatbot.chat(user_id=update.message.from_user["id"], msg=update.message.text, )
    update.message.reply_text(response)

updater = ext.Updater(token, use_context=True)
disp = updater.dispatcher

disp.add_handler(ext.CommandHandler("start", start))
disp.add_handler(ext.CommandHandler("content", content))
disp.add_handler(ext.CommandHandler("contact", contact))
disp.add_handler(ext.MessageHandler(ext.Filters.text, handle_message))

updater.start_polling()
updater.idle()
