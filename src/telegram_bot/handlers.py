from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

from analytics import applications_by_priority
from analytics import average_exam_score
from analytics import neediness_in_dormitory

FACULTY_CODES = [
    "01.03.02",
    "15.03.03",
]

MAIN_MENU = {
    'applications_by_priority': '📊 Распределение по приоритетам',
    'neediness_in_dormitory': '🏠 Необходимость в общежитии',
    'average_exam_score': '📈 Средний балл ЕГЭ',
    'unique_students': '👤 Уникальные студенты',
}


def get_faculty_keyboard(selected: list = None) -> InlineKeyboardMarkup:
    """Generate inline keyboard with faculty selection."""
    
    selected = selected or []
    keyboard = []
    
    for code in FACULTY_CODES:
        emoji = "✅" if code in selected else ""
        keyboard.append([InlineKeyboardButton(f"{emoji} {code}", callback_data=f"faculty_{code}")])

    keyboard.append([InlineKeyboardButton("Готово", callback_data="faculty_done")])

    return InlineKeyboardMarkup(keyboard)


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(text)] for text in MAIN_MENU.values()]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def faculty_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data
    selected = context.user_data.get("selected_faculties", [])

    if data.startswith("faculty_"):
        code = data.replace("faculty_", "")

        if code == "done":
            await query.edit_message_text(text="Факультеты выбраны.")
            return

        if code in selected:
            selected.remove(code)
        else:
            selected.append(code)

        context.user_data["selected_faculties"] = selected
        await query.edit_message_reply_markup(reply_markup=get_faculty_keyboard(selected))


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "/menu — выбор статистики\n"
        "/faculty — выбор факультетов",
    )


async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Выберите статистику, которая вам интересна.",
        reply_markup=get_main_menu_keyboard()
    )


async def faculty_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start faculty selection process."""
    
    context.user_data["selected_faculties"] = context.user_data.get("selected_faculties", [])
    await update.message.reply_text("Выберите факультеты:", reply_markup=get_faculty_keyboard(context.user_data["selected_faculties"]))


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text
    selected_faculties = context.user_data.get("selected_faculties")

    if not selected_faculties:
        await update.message.reply_text("Выберите сначала хотя бы один факультет через /faculty")
        return

    if user_input == MAIN_MENU['applications_by_priority']:
        for faculty in selected_faculties:
            file_path = f"data/csv/mpu/{faculty}.csv"
            text, image = applications_by_priority.run_analysis(file_path)
            await update.message.reply_text(f"\n📊 Факультет: {faculty}\n{text}")
            await update.message.reply_photo(photo=image)

    elif user_input == MAIN_MENU['average_exam_score']:
        await update.message.reply_text("...")

    elif user_input == MAIN_MENU['neediness_in_dormitory']:
        await update.message.reply_text("...")

    else:
        await update.message.reply_text("Неизвестная команда.")