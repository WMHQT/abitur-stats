from telegram.ext import Application, CommandHandler
from .handlers import (
    start_handler,
    stats_handler
)


def create_bot(token: str) -> Application:
    """Creates and configures the Telegram bot."""

    application = Application.builder().token(token).build()

    # Command handlers registration
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("stats", stats_handler))

    return application