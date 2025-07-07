import os
from telegram import Update
from telegram.ext import ContextTypes

from analytics.applications_by_priority import run_anal1
from analytics.average_exam_score import run_anal3
from analytics.neediness_in_dormitory import run_anal4


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот, который показывает статистику заявлений. "
        "Используй команду /stats, чтобы получить инфографику и текстовые результаты."
    )


async def stats_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Генерирую статистику, подождите...")

    results = []
    images = []

    # anal1: Количество заявлений по приоритетам 1–25
    text, image = run_anal1()
    results.append(text)
    if image and os.path.exists(image):
        images.append((image, "Распределение заявлений по приоритетам"))

    # anal3: Средний балл ЕГЭ для приоритетов 1 и 2
    text, _ = run_anal3()
    results.append(text)

    # anal4: Разбивка по общежитию для приоритетов 1 и 2
    text, image = run_anal4()
    results.append(text)
    if image and os.path.exists(image):
        images.append((image, "Разбивка заявлений по приоритетам и общежитию"))

    # Отправить текстовые результаты
    await update.message.reply_text("\n\n".join(results))

    # Отправить изображения
    for image_path, caption in images:
        with open(image_path, 'rb') as photo:
            await update.message.reply_photo(photo=photo, caption=caption)
