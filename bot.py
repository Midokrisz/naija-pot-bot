hereimport random
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

POTS = {
    "500": [],
    "1000": [],
    "2000": [],
    "5000": []
}

MAX_PLAYERS = 5

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Join ₦500 Pot", callback_data="500")],
        [InlineKeyboardButton("Join ₦1000 Pot", callback_data="1000")],
        [InlineKeyboardButton("Join ₦2000 Pot", callback_data="2000")],
        [InlineKeyboardButton("Join ₦5000 Pot", callback_data="5000")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "🎰 Welcome to Naija Pot Game!\nChoose a pot to join:",
        reply_markup=reply_markup
    )

def join_pot(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    pot = query.data
    user = query.from_user.username or query.from_user.first_name

    if user in POTS[pot]:
        query.message.reply_text("You already joined this pot!")
        return

    POTS[pot].append(user)

    players_list = "\n".join(POTS[pot])

    query.message.reply_text(
        f"💰 ₦{pot} Pot\n"
        f"Players ({len(POTS[pot])}/{MAX_PLAYERS}):\n{players_list}"
    )

    if len(POTS[pot]) == MAX_PLAYERS:
        winner = random.choice(POTS[pot])

        query.message.reply_text(
            f"🎉 ₦{pot} POT FULL!\n\n"
            f"Players:\n{players_list}\n\n"
            f"🏆 Winner: {winner}"
        )

        POTS[pot] = []

TOKEN = os.getenv("BOT_TOKEN")

updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(join_pot))

print("Bot is running...")
updater.start_polling()
updater.idle()
