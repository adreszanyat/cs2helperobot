from aiogram import Router, F, types

router = Router()

TACTICS = {
    "mirage": {
        "a_execute": {
            "name": "🔴 Полный выход на A (A Execute)",
            "difficulty": "Средне",
            "description": "Захват точки A с полным набором гранат, перекрытие ключевых позиций защиты.",
            "when_to_use": [
                "Против команд, сильно укрепляющих мид",
                "Когда A не в глубокой обороне",
                "Против игроков на позициях без укрытия (Ticket, Default, Jungle)",
                "При полном наборе гранат и хорошей координации"
            ],
            "roles": {
                "T1 (Коннектор)": "Контролит мид → заходит через Коннектор → давление на защиту",
                "T2 (Палас)": "Ждет сигнала → выходит из Palace → контролит Тикет",
                "T3, T4, T5 (Рампа)": "Кидают гранаты → выходят на A → один ставит бомбу"
            },
            "nades": {
                "T1": "Смок 'Окно' (если нет контроля мида) + Молотов 'Джангл'",
                "T2": "Молотов за Default + Флешка в сайт",
                "T3": "Смок 'Сити' + Флешка на выход",
                "T4": "Смок 'Тикет' + Молотов 'Ниндзя'",
                "T5": "Смок 'Коннектор' + HE под Тикет"
            },
            "timing": "Все гранаты кидаются одновременно, выход через 2 секунды после флешек"
        },
        "b_split": {
            "name": "🔴 Сплит на B (B Split)",
            "difficulty": "Легко",
            "description": "Атака B с двух сторон: через Апартаменты и с Т-спавна.",
            "when_to_use": [
                "Против агрессивных CT на миду",
                "Когда B играет в одиночку",
                "Для растягивания защиты"
            ],
            "roles": {
                "T1, T2 (Апарты)": "Контроль Апартов → смоки на Ван и Сайт",
                "T3, T4, T5 (Рампа)": "Выход с Т-спавна → флешки для апартовцев"
            },
            "nades": {
                "T1": "Смок 'Ван' + Молотов 'Сайт'",
                "T2": "Смок 'Двери' + HE на Сайт",
                "T3": "Флешка для апартовцев",
                "T4": "Флешка на выход",
                "T5": "Бомба + резервная граната"
            },
            "timing": "Апартовцы начинают первыми, рамповцы выходят на звук дымов"
        }
    },
    "inferno": {
        "b_execute": {
            "name": "🔴 Полный выход на B (B Execute)",
            "difficulty": "Средне",
            "description": "Массированная атака на B с полным контролем CT и Сайта.",
            "when_to_use": [
                "Против пассивной защиты B",
                "Когда есть контроль мид/банана",
                "Для быстрого раунда"
            ],
            "roles": {
                "T1, T2 (Банан)": "Контроль банана → смоки на CT и Сайт",
                "T3 (Ковры)": "Заход через Ковры → флешки на Сайт",
                "T4, T5 (Банан)": "Выход с бомбой → установка"
            },
            "nades": {
                "T1": "Смок 'CT' + Молотов 'Новая Коробка'",
                "T2": "Смок 'Сайт' + HE на 'Пулю'",
                "T3": "Флешка на Сайт из Ковров",
                "T4": "Флешка на выход",
                "T5": "Молотов 'Темница' + бомба"
            },
            "timing": "Одновременный выход с банана и ковров через 3 секунды после смоков"
        }
    }
}

@router.callback_query(F.data == "menu_tactics")
async def menu_tactics(callback: types.CallbackQuery):
    from keyboards import tactics_maps_menu
    await callback.message.edit_text(
        "🗺️ <b>Выберите карту для тактики:</b>",
        reply_markup=tactics_maps_menu(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "back_to_tactics")
async def back_to_tactics(callback: types.CallbackQuery):
    """Возврат в меню выбора карт для тактик"""
    from keyboards import tactics_maps_menu
    await callback.message.edit_text(
        "🗺️ <b>Выберите карту для тактики:</b>",
        reply_markup=tactics_maps_menu(),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("tactic_map_"))
async def show_tactics_for_map(callback: types.CallbackQuery):
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    map_name = callback.data.replace("tactic_map_", "")
    tactics = TACTICS.get(map_name, {})

    if not tactics:
        await callback.answer("Тактики для этой карты пока не добавлены!", show_alert=True)
        return

    buttons = []
    for tactic_id, tactic_data in tactics.items():
        buttons.append([InlineKeyboardButton(
            text=tactic_data["name"], 
            callback_data=f"tactic_view_{map_name}_{tactic_id}"
        )])

    buttons.append([InlineKeyboardButton(text="← К картам", callback_data="menu_tactics")])

    await callback.message.edit_text(
        f"🗺️ <b>{map_name.title()}</b> — доступные коллы:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("tactic_view_"))
async def show_tactic_detail(callback: types.CallbackQuery):
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    parts = callback.data.replace("tactic_view_", "").split("_")
    map_name = parts[0]
    tactic_id = "_".join(parts[1:])

    tactic = TACTICS.get(map_name, {}).get(tactic_id)
    if not tactic:
        await callback.answer("Тактика не найдена!", show_alert=True)
        return

    roles_text = "\n".join([f"<b>{role}:</b> {action}" for role, action in tactic["roles"].items()])
    nades_text = "\n".join([f"<b>{player}:</b> {nade}" for player, nade in tactic["nades"].items()])
    when_text = "\n• ".join([""] + tactic["when_to_use"])

    text = f"""
<b>{tactic['name']}</b>
Сложность: {tactic['difficulty']}

<b>🎯 Цель:</b>
{tactic['description']}

<b>📋 Когда использовать:</b>
• {when_text}

<b>👥 Роли и действия:</b>
{roles_text}

<b>💣 Гранаты:</b>
{nades_text}

<b>⏱ Тайминг:</b>
<i>{tactic['timing']}</i>
"""

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← К тактикам", callback_data=f"tactic_map_{map_name}")]
    ])

    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")