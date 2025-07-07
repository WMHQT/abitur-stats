from dotenv import load_dotenv
import os
from telegram.ext import Application, CommandHandler

from analytics.anal1 import run_anal1
from analytics.anal3 import run_anal3
from analytics.anal4 import run_anal4


# Bot's token
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


# Обработчик команды /start
async def start(update, context):
    await update.message.reply_text(
        "Привет! Я бот, который показывает статистику заявлений. "
        "Используй команду /stats, чтобы получить инфографику и текстовые результаты."
    )

# Обработчик команды /stats
async def stats(update, context):
    await update.message.reply_text("Генерирую статистику, подождите...")

    # Запуск скриптов и сбор результатов
    results = []
    images = []

    # anal1: Количество заявлений по приоритетам 1–25
    text, image = run_anal1()
    results.append(text)
    if image and os.path.exists(image):
        images.append((image, "Распределение заявлений по приоритетам"))

    # anal3: Средний балл ЕГЭ для приоритетов 1 и 2
    text, image = run_anal3()
    results.append(text)
    # anal3 не генерирует изображение

    # anal4: Разбивка по общежитию для приоритетов 1 и 2
    text, image = run_anal4()
    results.append(text)
    if image and os.path.exists(image):
        images.append((image, "Разбивка заявлений по приоритетам и общежитию"))

    # Отправка текстовых результатов
    await update.message.reply_text("\n\n".join(results))

    # Отправка изображений
    for image_path, caption in images:
        with open(image_path, 'rb') as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=caption
            )

# Основная функция
def main():
    # Инициализация бота
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавление обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", stats))

    # Запуск бота
    print("Бот запущен!")
    application.run_polling()

if __name__ == "__main__":
    main()
