# pylint: disable=unused-argument
""" Start and send button """
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from telegram.ext import (
    ContextTypes
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Executing bot behavior, print first message
    """

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
    """
    This function parses the CallbackQuery and updates the message text.
    """

    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    await query.edit_message_text(text="Расскажите что Вас беспокоит!")
    return 2
