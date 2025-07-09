from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

from analytics import applications_by_priority
from analytics import average_exam_score
from analytics import neediness_in_dormitory
from analytics import unique_students
from utils.scheduler import get_last_update

FACULTY_CODES = {
    '01.03.02': 'Прикладная математика и информатика',
    '13.03.02.03': 'Электроника и технологии сенсорики', 
    '13.03.03': 'Энергетическое машиностроение',
    '15.03.03': 'Прикладная механика',
    '23.03.02': 'Наземные транспортно-технологические комплексы',
    '23.03.03.01': 'Автомобили и транспортно-логистические системы',
    '23.03.03.02': 'Инжиринг и эксплуатация транспортных систем',
    '23.05.01.01': 'Спортивные транспортные средства',
    '23.05.01.02': 'Электромобили',
    '23.05.01.03': 'Автомобили и автомобильный сервис',
    '23.05.01.04': 'Компьютерный инжиринг в автомобилестроении',
    '54.03.01.01': 'Транспортный и промышленный дизайн',
}

MAIN_MENU = {
    'applications_by_priority': '📊 Распределение по приоритетам',
    'neediness_in_dormitory': '🏠 Необходимость в общежитии',
    'average_exam_score': '📈 Средний балл ЕГЭ',
    'unique_students': '👤 Уникальные студенты',
}

ANALYSIS_MAP = {
    MAIN_MENU['applications_by_priority']: applications_by_priority.run_analysis,
    MAIN_MENU['average_exam_score']: average_exam_score.run_analysis,
    MAIN_MENU['neediness_in_dormitory']: neediness_in_dormitory.run_analysis,
    # MAIN_MENU['unique_students']: unique_studens.run_analysis,
}


def get_faculty_keyboard(selected: list = None) -> InlineKeyboardMarkup:
    """Generate inline keyboard with faculty selection."""
    
    selected = selected or []
    keyboard = []
    
    for code, name in FACULTY_CODES.items():
        emoji = "✅" if code in selected else ""
        keyboard.append([InlineKeyboardButton(f"{emoji} {code} {name}", callback_data=f"faculty_{code}")])

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
            count = len(selected)
            if len(selected):
                await query.edit_message_text(text=f"Выбранное число факультетов: {count}")
            else:
                await query.edit_message_text(text="Вы не выбрали факультеты.")
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
        "/faculty — выбор факультетов\n"
        "/update — время последнего обновления данных",
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

    if user_input not in ANALYSIS_MAP:
        await update.message.reply_text("Неизвестная команда.")
        return

    analysis_func = ANALYSIS_MAP[user_input]

    for faculty in selected_faculties:
        file_path = f"data/csv/mpu/{faculty}.csv"
        text, image = analysis_func(file_path)
        await update.message.reply_text(f"\n📊 Факультет: {faculty}\n{text}")
        if image:
            await update.message.reply_photo(photo=image)


async def update_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    update_time = get_last_update()
    await update.message.reply_text(f"Последнее обновление: \n{update_time}")