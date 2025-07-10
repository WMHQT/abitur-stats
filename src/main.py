import os
from dotenv import load_dotenv
from telegram_bot.bot import create_bot

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


def main() -> None:
    if not BOT_TOKEN:
        raise ValueError("Missing BOT_TOKEN in environment variables.")

    bot = create_bot(BOT_TOKEN)
    print("Bot is up.")
    bot.run_polling()


if __name__ == "__main__":
    main()