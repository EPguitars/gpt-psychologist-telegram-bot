# pylint: disable=unused-argument
"""
Main script for ai-psychologist bot.

Coded by Eugene Poluyakhtov
Idea by Ilya Lisov and Eugene Poluyakhtov

"""
import logging
import sqlite3
import json
import ast

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    filters,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler)

import gpt_logic

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = open("tg_TOKEN.txt", "r", encoding="utf-8").read()
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()


first_data = [
    {"role": "system", "content": """You are psychologist assistant.
                                    You never recommending me go to doctor.
                                    You using a gestalt therapy.
                                    """
     },
    {"role": "user", "content": "Здравствуйте, меня что-то тревожит!"},
    {"role": "assistant",
     "content": "Я с радостью окажу вам психологическую помощь, опишите ваши чувства"},
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """First executed function"""
    message = """Привет!
    Я искусственный интелект обладающий навыками психолога.
    Я оказываю бесплатную психологическую помощь всем кто в этом нуждается.
    Хотите начать сеанс?"""
    keyboard = [
        [
            InlineKeyboardButton("Давайте, начнём.", callback_data="yes"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(message, reply_markup=reply_markup)
    return 1


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """This function parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    await query.edit_message_text(text="Расскажите что Вас беспокоит!")
    return 2


async def get_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """This function sends question to api and prints answer"""
    question = update.message.text
    user_id = update.message.from_user.id
    data = current_data(user_id)
    data, answer = gpt_logic.get_result(data, question)
    data_size = gpt_logic.num_tokens_from_messages(data)

    while data_size > 3596:
        data.pop(3)
        data_size = gpt_logic.num_tokens_from_messages(data)

    update_db(user_id, data)
    await update.message.reply_text(answer)


def current_data(user_id) -> list:
    """This function gets users data from db"""

    dbdata = json.dumps(first_data)
    cursor.execute("SELECT * FROM user WHERE id=?", (user_id,))

    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO user (id, data) VALUES (?, ?)", (user_id, dbdata))

    dbdata = cursor.execute("SELECT data FROM user WHERE id=?", (user_id,))
    conn.commit()

    data = ast.literal_eval(*dbdata.fetchone())

    return data


def update_db(user_id, data):
    """This function updates db with new dialogue"""
    cursor.execute("""
    UPDATE user
    SET data = ?
    WHERE id = ?""",
                   (json.dumps(data), user_id))

    conn.commit()


def main():
    """This is a main function of the bot"""
    application = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [CallbackQueryHandler(button)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_answer)]
        },
        fallbacks=[CommandHandler('start', start)]
    )

    application.add_handler(conv_handler)

    application.run_polling()



if __name__ == '__main__':
    main()
