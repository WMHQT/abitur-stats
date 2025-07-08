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
    button_handler,
    faculty_button_handler,
)


def create_bot(token: str):
    application = Application.builder().token(token).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("menu", menu_handler))
    application.add_handler(CommandHandler("faculty", faculty_handler))

    # Button click handler (for inline faculty selection)
    application.add_handler(CallbackQueryHandler(faculty_button_handler))

    # General message handler (for main menu buttons)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))

    return application