import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_TOKEN
from database import db
from handlers import register_handlers
from keyboards import main_menu_reply

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Регистрация всех обработчиков
register_handlers(dp)

# Контакты для обратной связи
SUPPORT_USERNAME = "username"  
SUPPORT_CHANNEL = "username"  
SUPPORT_CHAT = "username"

STICKER_FILE_ID = "CAACAgIAAxkBAAEQmcZpnQNKPps-kReyTtp8n9gK9wedcQACNAEAAlKJkSMTzddv9RwHWDoE" # можете заменить на свой @idstickerbot

@dp.message(Command("start"))
async def cmd_start(message: Message):
    db.update_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name
    )

    try:
        await message.answer_sticker(
            STICKER_FILE_ID,
            reply_markup=main_menu_reply()
        )
    except Exception as e:
        logging.error(f"Ошибка отправки стикера: {e}")
        await message.answer(
            "👇 <b>Главное меню:</b>",
            reply_markup=main_menu_reply(),
            parse_mode="HTML"
        )
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🔍 Открыть поиск", 
            switch_inline_query_current_chat=""
        )]
    ])

    await message.answer(
        "🎯 <b>CS2 Helper Pro</b>\n\n"
        "Привет, стрелок! Я — твой помощник по Counter-Strike 2.\n\n"
        "<b>🗺️ Раскидки</b> — Гранаты с позициями, прицелами и видео\n"
        "<b>⚙️ Настройки</b> — Прицелы, бинды и конфиги про игроков, оптимизация ПК\n"
        "<b>📊 Мета</b> — Актуальные тир-листы оружия, экономика, пул карт\n"
        "<b>🎯 Тренировки</b> — Паттерны спрея и лучшие карты для практики\n"
        "<b>📚 Словарь</b> — Термины и сленг CS2\n"
        "<b>🎮 Тактика</b> — Стратегии и коллы для командной игры\n"
        "<b>⭐ Избранное</b> — Сохраняй гранаты в избранное\n"
        "<b>🔍 Поиск</b> — Быстрый поиск гранат и терминов\n\n"
        "<i>Нажми кнопку ниже для поиска или используй меню 👇</i>\n\n"
        "ℹ️ <code>/help</code> — Помощь и контакты",
        reply_markup=inline_kb,
        parse_mode="HTML"
    )

@dp.message(Command("help"))
async def cmd_help(message: Message):
    """Команда помощи с контактами для обратной связи"""
    
    contact_buttons = []
    
    contact_buttons.append([
        InlineKeyboardButton(
            text="💬 Написать разработчику", 
            url=f"tg://user?id={SUPPORT_USERNAME}" if SUPPORT_USERNAME.isdigit() else f"https://t.me/{SUPPORT_USERNAME.replace('@', '')}"
        )
    ])
    
    if SUPPORT_CHANNEL:
        contact_buttons.append([
            InlineKeyboardButton(
                text="📢 Канал с новостями", 
                url=f"https://t.me/{SUPPORT_CHANNEL}"
            )
        ])
    
    if SUPPORT_CHAT:
        contact_buttons.append([
            InlineKeyboardButton(
                text="👥 Чат поддержки", 
                url=f"https://t.me/{SUPPORT_CHAT}"
            )
        ])
    
    help_kb = InlineKeyboardMarkup(inline_keyboard=contact_buttons)

    help_text = f"""
❓ <b>Помощь и поддержка CS2 Helper</b>

<b>🤖 Команды бота:</b>
<code>/start</code> — Главное меню
<code>/help</code> — Эта справка

<b>💡 Как пользоваться:</b>
• Выбирай разделы через меню ниже
• Используй <code>@cs2helperobot</code> в любом чате для поиска
• Сохраняй гранаты в ⭐ Избранное
• Смотри прицелы и конфиги про игроков

<b>🐞 Нашли баг или есть идея?</b>
Напиши разработчику — мы всё исправим и улучшим!

<b>📊 Статистика:</b>
В базе: гранаты, термины, прицелы про игроков
Карты: Mirage, Inferno, Nuke, Ancient, Anubis, Vertigo, Overpass, Dust2

<i>Спасибо, что используешь CS2 Helper! 🎯</i>
"""

    await message.answer(help_text, reply_markup=help_kb, parse_mode="HTML")

# Обработчики текстовых команд меню
@dp.message(lambda message: message.text == "🗺️ Раскидки")
async def text_menu_nades(message: Message):
    maps = [("Mirage", "map_mirage"), ("Inferno", "map_inferno"), ("Nuke", "map_nuke"),
            ("Ancient", "map_ancient"), ("Anubis", "map_anubis"), ("Vertigo", "map_vertigo"),
            ("Overpass", "map_overpass"), ("Dust2", "map_dust2")]
    buttons = []
    for i in range(0, len(maps), 2):
        row = [InlineKeyboardButton(text=name, callback_data=cb) for name, cb in maps[i:i+2]]
        buttons.append(row)
    
    await message.answer(
        "🗺️ <b>Раскидки гранат</b>\n\n"
        "Выберите карту для просмотра позиций:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )

@dp.message(lambda message: message.text == "⚙️ Настройки")
async def text_menu_settings(message: Message):
    buttons = [
        [InlineKeyboardButton(text="🚀 Параметры запуска", callback_data="settings_launch"),
         InlineKeyboardButton(text="💻 Оптимизация ПК", callback_data="settings_fps")],
        [InlineKeyboardButton(text="🎯 Прицелы про игроков", callback_data="settings_crosshairs"),
         InlineKeyboardButton(text="⌨️ Бинды про игроков", callback_data="settings_binds")],
        [InlineKeyboardButton(text="📥 Конфиги про игроков", callback_data="settings_pro_configs")]
    ]
    
    await message.answer(
        "⚙️ <b>Настройки CS2</b>\n\n"
        "Здесь вы найдете:\n"
        "🚀 Параметры запуска\n"
        "💻 Оптимизацию под ваш ПК\n"
        "🎯 Прицелы про игроков\n"
        "⌨️ Бинды про игроков\n"
        "📥 Полные конфиги про игроков",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )

@dp.message(lambda message: message.text == "📊 Мета")
async def text_menu_meta(message: Message):
    buttons = [
        [InlineKeyboardButton(text="🔫 Тир-лист оружия", callback_data="meta_weapons"),
         InlineKeyboardButton(text="📈 Статистика оружия", callback_data="meta_weapon_stats")],
        [InlineKeyboardButton(text="💰 Экономика", callback_data="meta_economy"),
         InlineKeyboardButton(text="🗺️ Пул карт", callback_data="meta_maps")]
    ]
    
    await message.answer(
        "📊 <b>Мета-гейм CS2</b>\n\n"
        "Актуальная информация об оружии, экономике и игровом балансе.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )

@dp.message(lambda message: message.text == "🎯 Тренировки")
async def text_menu_training(message: Message):
    buttons = [
        [InlineKeyboardButton(text="🎯 Контроль спрея", callback_data="training_spray")],
        [InlineKeyboardButton(text="🗺️ Карты тренировок", callback_data="training_maps")]
    ]
    
    await message.answer(
        "🎯 <b>Тренировки CS2</b>\n\n"
        "Выберите тип тренировки:\n\n"
        "<b>🎯 Контроль спрея</b> — паттерны отдачи оружий\n"
        "<b>🗺️ Карты тренировок</b> — лучшие workshop карты",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )

@dp.message(lambda message: message.text == "📚 Словарь")
async def text_menu_terms(message: Message):
    await message.answer(
        "📚 <b>Словарь терминов CS2</b>\n\n"
        "Введите термин для поиска:\n"
        "<i>Например: пик, холд, кемп, эко, клатч</i>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎲 Случайный термин", callback_data="term_random")]
        ]),
        parse_mode="HTML"
    )

@dp.message(lambda message: message.text == "🎮 Тактика")
async def text_menu_tactics(message: Message):
    maps = ["mirage", "inferno", "nuke", "ancient", "anubis"]
    buttons = []
    for i in range(0, len(maps), 2):
        row = [InlineKeyboardButton(text=m.title(), callback_data=f"tactic_map_{m}") for m in maps[i:i+2]]
        buttons.append(row)
    
    await message.answer(
        "🗺️ <b>Выберите карту для тактики:</b>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )

@dp.message(lambda message: message.text == "⭐ Избранное")
async def text_menu_favorites(message: Message):
    from database import db
    
    favorites = db.get_favorites(message.from_user.id)

    if not favorites:
        await message.answer(
            "⭐ <b>Избранное</b>\n\n"
            "У вас пока нет избранных гранат!\n"
            "Добавляйте гранаты в избранное при просмотре раскидок.",
            parse_mode="HTML"
        )
        return

    buttons = []
    for nade in favorites:
        buttons.append([InlineKeyboardButton(
            text=f"🗺️ {nade['map_name'].title()}: {nade['name']}",
            callback_data=f"nade_{nade['id']}"
        )])

    await message.answer(
        f"⭐ <b>Ваши избранные гранаты</b> ({len(favorites)}):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )

@dp.message(lambda message: message.text == "🔍 Поиск")
async def text_menu_search(message: Message):
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🔍 Открыть поиск гранат", 
            switch_inline_query_current_chat=""
        )]
    ])
    
    await message.answer(
        "🔍 <b>Поиск по боту</b>\n\n"
        "Нажми кнопку ниже, чтобы открыть inline-поиск прямо здесь!\n\n"
        "<i>Или в любом другом чате начни печатать:</i> <code>@cs2helperobot смок мираж</code>",
        reply_markup=inline_kb,
        parse_mode="HTML"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен пользователем")
    except Exception as e:
        print(f"Произошла ошибка: {e}")