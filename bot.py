import random
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

POTS = {
    "500": [],
    "1000": [],
    "2000": [],
    "5000": []
}

MAX_PLAYERS = 5

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Join ₦500 Pot", callback_data="500")],
        [InlineKeyboardButton("Join ₦1000 Pot", callback_data="1000")],
        [InlineKeyboardButton("Join ₦2000 Pot", callback_data="2000")],
        [InlineKeyboardButton("Join ₦5000 Pot", callback_data="5000")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🎰 Welcome to Naija Pot Game!\nChoose a pot to join:",
        reply_markup=reply_markup
    )

async def join_pot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    pot = query.data
    user = query.from_user.username or query.from_user.first_name

    if pot not in POTS:
        await query.message.reply_text("Invalid pot selected.")
        return

    if user in POTS[pot]:
        await query.message.reply_text("You already joined this pot!")
        return

    POTS[pot].append(user)

    players_list = "\n".join(POTS[pot])

    await query.message.reply_text(
        f"💰 ₦{pot} Pot\n"
        f"Players ({len(POTS[pot])}/{MAX_PLAYERS}):\n{players_list}"
    )

    if len(POTS[pot]) == MAX_PLAYERS:
        winner = random.choice(POTS[pot])

        await query.message.reply_text(
            f"🎉 ₦{pot} POT FULL!\n\n"
            f"Players:\n{players_list}\n\n"
            f"🏆 Winner: {winner}"
        )

        POTS[pot] = []

def main():
    TOKEN = os.getenv("BOT_TOKEN")

    if not TOKEN:
        print("Error: BOT_TOKEN not set")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(join_pot))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
