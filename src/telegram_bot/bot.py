import asyncio
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
from telegram_bot.handlers import (
    start_handler,
    menu_handler,
    faculty_handler,
    update_handler,
    button_handler,
    faculty_button_handler,
)

from utils.scheduler import periodic_update


async def post_init(application: Application) -> None:
    """Start background task after bot starts."""
    application.bot_data["background_task"] = asyncio.create_task(periodic_update())


def create_bot(token: str) -> Application:
    application = Application.builder().token(token).post_init(post_init).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("menu", menu_handler))
    application.add_handler(CommandHandler("faculty", faculty_handler))
    application.add_handler(CommandHandler("update", update_handler))

    # Button click handler (for inline faculty selection)
    application.add_handler(CallbackQueryHandler(faculty_button_handler))

    # General message handler (for main menu buttons)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))

    return application