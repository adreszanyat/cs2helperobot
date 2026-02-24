from aiogram import Router, F, types, Bot
from aiogram.types import FSInputFile
import os

from keyboards import training_menu, spray_menu, training_maps_menu
from config import MEDIA_DIR

router = Router()

SPRAY_PATTERNS = {
    "ak47": {
        "name": "AK-47",
        "pattern": "Вниз-влево, затем вправо",
        "tip": "Тяните вниз сильно на первые 10 пуль, затем контролируйте горизонт",
        "pattern_path": os.path.join(MEDIA_DIR, "pattern", "ak47_pattern"),
        "spray_path": os.path.join(MEDIA_DIR, "sprays", "ak47_spray")
    },
    "m4a4": {
        "name": "M4A4", 
        "pattern": "Вверх с отклонением вправо",
        "tip": "Тяните вниз и чуть вправо, первые 10 пуль критичны",
        "pattern_path": os.path.join(MEDIA_DIR, "pattern", "m4a4_pattern"),
        "spray_path": os.path.join(MEDIA_DIR, "sprays", "m4a4_spray")
    },
    "m4a1s": {
        "name": "M4A1-S",
        "pattern": "Вертикальный с легким отклонением",
        "tip": "Легкий спрей вниз, проще чем M4A4",
        "pattern_path": os.path.join(MEDIA_DIR, "pattern", "m4a1s_pattern"),
        "spray_path": os.path.join(MEDIA_DIR, "sprays", "m4a1s_spray")
    }
}

TRAINING_MAPS = {
    "aim_botz": {
        "name": "🎯 Aim Botz",
        "code": "steam://rungame/730/76561202255233023/+cs2_workshop_map 243702660",
        "url": "https://steamcommunity.com/sharedfiles/filedetails/?id=243702660",
        "description": "Классическая карта для тренировки аима. Статичные боты, настройка сложности.",
        "best_for": "Теппинг, флики, префаер"
    },
    "fast_aim": {
        "name": "🔫 Fast Aim/Reflex",
        "code": "steam://rungame/730/76561202255233023/+cs2_workshop_map 647772286",
        "url": "https://steamcommunity.com/sharedfiles/filedetails/?id=647772286",
        "description": "Быстрая тренировка рефлексов. Боты появляются со всех сторон.",
        "best_for": "Реакция, флики на 180°"
    },
    "yprac": {
        "name": "💨 Yprac Hub",
        "code": "steam://rungame/730/76561202255233023/+cs2_workshop_map 3070715607",
        "url": "https://steamcommunity.com/sharedfiles/filedetails/?id=3070715607",
        "description": "Серия карт для каждой карты с позициями раскидок и префаерами.",
        "best_for": "Изучение раскидок, префаеры"
    },
    "prefire": {
        "name": "🏃 Refrag Prefire",
        "code": "https://refrag.gg",
        "url": "https://refrag.gg",
        "description": "Онлайн-сервис для тренировки префаеров на всех картах.",
        "best_for": "Префаеры, чек углов"
    }
}

@router.callback_query(F.data == "menu_training")
async def menu_training(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🎯 <b>Тренировки CS2</b>\n\n"
        "Выберите тип тренировки:\n\n"
        "<b>🎯 Контроль спрея</b> — паттерны отдачи оружий\n"
        "<b>🗺️ Карты тренировок</b> — лучшие workshop карты",
        reply_markup=training_menu(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "back_to_training")
async def back_to_training(callback: types.CallbackQuery):
    """Возврат в главное меню тренировок"""
    await callback.message.edit_text(
        "🎯 <b>Тренировки CS2</b>\n\n"
        "Выберите тип тренировки:\n\n"
        "<b>🎯 Контроль спрея</b> — паттерны отдачи оружий\n"
        "<b>🗺️ Карты тренировок</b> — лучшие workshop карты",
        reply_markup=training_menu(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "training_spray")
async def training_spray(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🎯 <b>Контроль спрея</b>\n\n"
        "Выберите оружие для просмотра паттерна отдачи:",
        reply_markup=spray_menu(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "training_maps")
async def training_maps(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🗺️ <b>Карты для тренировок</b>\n\n"
        "Подпишитесь на карты в Steam Workshop и тренируйтесь перед матчмейкингом!",
        reply_markup=training_maps_menu(),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("map_"))
async def show_training_map(callback: types.CallbackQuery):
    map_key = callback.data.replace("map_", "")
    data = TRAINING_MAPS.get(map_key)
    
    if not data:
        await callback.answer("Карта не найдена!", show_alert=True)
        return
    
    text = f"""
<b>{data['name']}</b>

<b>📝 Описание:</b>
{data['description']}

<b>⭐ Лучше всего для:</b>
{data['best_for']}

<b>🔗 Код в Workshop:</b>
<code>{data['code']}</code>

<i>Откройте CS2 → Играть → Практика с ботами → Мастерская</i>
"""
    
    await callback.message.edit_text(
        text,
        reply_markup=training_maps_menu(),
        parse_mode="HTML"
    )

def find_media_file(base_path: str):
    """Ищет файл с любым поддерживаемым расширением"""
    extensions = ['.gif', '.png', '.jpg', '.jpeg', '.mp4', '.webm']
    for ext in extensions:
        full_path = base_path + ext
        if os.path.exists(full_path):
            return full_path
    return None

@router.callback_query(F.data.startswith("spray_"))
async def show_spray(callback: types.CallbackQuery, bot: Bot):
    weapon = callback.data.replace("spray_", "")
    data = SPRAY_PATTERNS.get(weapon)

    if not data:
        await callback.answer("Оружие не найдено!", show_alert=True)
        return

    pattern_file = find_media_file(data['pattern_path']) if data.get('pattern_path') else None
    spray_file = find_media_file(data['spray_path']) if data.get('spray_path') else None

    has_pattern = pattern_file is not None
    has_spray = spray_file is not None

    menu_text = f"""🎯 <b>Контроль спрея — {data['name']}</b>

<b>🎯 Паттерн:</b> {data['pattern']}
<b>💡 Совет:</b> {data['tip']}

<i>Изображения отправлены ниже ↓</i>"""
    
    await callback.message.edit_text(
        menu_text,
        reply_markup=spray_menu(),
        parse_mode="HTML"
    )
    
    if has_pattern:
        await bot.send_photo(
            chat_id=callback.message.chat.id,
            photo=FSInputFile(pattern_file),
            caption=f"🎯 <b>{data['name']}</b> — Паттерн отдачи (куда тянуть мышь)",
            parse_mode="HTML"
        )
    
    if has_spray:
        await bot.send_animation(
            chat_id=callback.message.chat.id,
            animation=FSInputFile(spray_file),
            caption=f"🔫 <b>{data['name']}</b> — Анимация спрея в игре",
            parse_mode="HTML"
        )
    
    if not has_pattern and not has_spray:
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=f"⚠️ <i>Изображения для {data['name']} не найдены.\nДобавьте файлы в папку media/</i>",
            parse_mode="HTML"
        )