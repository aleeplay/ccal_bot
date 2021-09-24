import yaml
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import CallbackContext, Updater, Filters, MessageHandler
from pprint import pprint
from user_handler import UserHandler, User

with open('config.yaml') as f:
	config = yaml.safe_load(f)

TOKEN = config['telegram_token']
users = UserHandler()


def message_handler(update: Update, context: CallbackContext):
	text = update.message.text
	user_id = update.message.chat_id

	user = users.get_user(user_id)

	user.user_message(text)
	reply, markup_buttons = user.bot_message()
	buttons = ReplyKeyboardMarkup([[button] for button in markup_buttons]) if markup_buttons else False

	update.message.reply_text(
		text=f'{reply}',
		reply_markup=buttons if buttons else ReplyKeyboardRemove()
	)


def main() -> None:
	updater = Updater(
		token=TOKEN,
		use_context=True
	)
	updater.dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=message_handler))
	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
	main()
