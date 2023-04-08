# pylint: disable=unused-argument, disable=import-error
"""
Main script for ai-psychologist bot.

Coded by Eugene Poluyakhtov
Idea by Ilya Lisov and Eugene Poluyakhtov

"""
import logging
import sqlite3
import json
import os
from warnings import filterwarnings

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    filters,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler)
from telegram.warnings import PTBUserWarning
from dotenv import load_dotenv

import gpt_operations
from db_operations import current_data, update_db
from behavior import start, button


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

load_dotenv()
TOKEN_LIMIT = 3596
TGTOKEN = os.getenv("TG_TOKEN")
with open("behavior_prompts.json", "r", encoding="utf-8") as prompts:
    first_data = json.load(prompts)

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)


async def get_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This function sends question to api and prints answer to user
    """

    question = update.message.text
    user_id = update.message.from_user.id
    data = current_data(user_id)
    data, answer = gpt_operations.get_result(data, question)
    data_size = gpt_operations.num_tokens_from_messages(data)

    while data_size > TOKEN_LIMIT:
        data.pop(3)
        data_size = gpt_operations.num_tokens_from_messages(data)

    update_db(user_id, data)
    await update.message.reply_text(answer)


def main():
    """This is a main function of the bot"""

    application = ApplicationBuilder().token(TGTOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
          # 1: Open input for gpt prompts
            1: [CallbackQueryHandler(button)],
          # 2: Submit gpt prompt
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_answer)]
        },
        fallbacks=[CommandHandler('start', start)]
    )

    application.add_handler(conv_handler)

    application.run_polling()



if __name__ == '__main__':
    main()
