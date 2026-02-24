from aiogram import Router, F, types, Bot
from aiogram.types import FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.exceptions import TelegramBadRequest
import os

from keyboards import meta_menu
from config import MEDIA_DIR

router = Router()

# ============ ДАННЫЕ ============

WEAPON_STATS = {
    # Пистолеты
    "glock": {
        "name": "Glock-18",
        "price": "$200",
        "kill_reward": "$300",
        "damage": 30,
        "recoil": "84%",
        "fire_rate": "400 / 1200",
        "range": "20 м",
        "armor_penetration": "47%",
        "reload": "2.2 сек",
        "ammo": "20/120",
        "move_speed": 240,
        "headshot_armored": 55,
        "headshot_unarmored": 118,
        "description": "Стартовый пистолет для T. Высокая скорострельность в режиме очереди."
    },
    "usp": {
        "name": "USP-S",
        "price": "$200",
        "kill_reward": "$300",
        "damage": 35,
        "recoil": "69%",
        "fire_rate": 352,
        "range": "21 м",
        "armor_penetration": "50.5%",
        "reload": "2.2 сек",
        "ammo": "12/24",
        "move_speed": 240,
        "headshot_armored": 70,
        "headshot_unarmored": 140,
        "description": "Стартовый пистолет для CT. Тихий, точный, с глушителем."
    },
    "p2000": {
        "name": "P2000",
        "price": "$200",
        "kill_reward": "$300",
        "damage": 35,
        "recoil": "73%",
        "fire_rate": 352,
        "range": "22 м",
        "armor_penetration": "50.5%",
        "reload": "2.2 сек",
        "ammo": "13/52",
        "move_speed": 240,
        "headshot_armored": 70,
        "headshot_unarmored": 140,
        "description": "Альтернатива USP-S. Больше патронов в магазине."
    },
    "p250": {
        "name": "P250",
        "price": "$300",
        "kill_reward": "$300",
        "damage": 38,
        "recoil": "69%",
        "fire_rate": 400,
        "range": "14 м",
        "armor_penetration": "64%",
        "reload": "2.2 сек",
        "ammo": "13/26",
        "move_speed": 240,
        "headshot_armored": 96,
        "headshot_unarmored": 151,
        "description": "Бюджетный пистолет с хорошим пробитием брони."
    },
    "dual_berettas": {
        "name": "Dual Berettas",
        "price": "$300",
        "kill_reward": "$300",
        "damage": 38,
        "recoil": "69%",
        "fire_rate": 500,
        "range": "24 м",
        "armor_penetration": "57.5%",
        "reload": "3.8 сек",
        "ammo": "30/120",
        "move_speed": 240,
        "headshot_armored": 79,
        "headshot_unarmored": 152,
        "description": "Двойные пистолеты. Много патронов, но низкая точность."
    },
    "cz75": {
        "name": "CZ75-Auto",
        "price": "$500",
        "kill_reward": "$300",
        "damage": 31,
        "recoil": "65%",
        "fire_rate": 600,
        "range": "11 м",
        "armor_penetration": "77.65%",
        "reload": "2.7 сек",
        "ammo": "12/12",
        "move_speed": 240,
        "headshot_armored": 95,
        "headshot_unarmored": 123,
        "description": "Автоматический пистолет. Высокая скорострельность, мало патронов."
    },
    "tec9": {
        "name": "Tec-9",
        "price": "$500",
        "kill_reward": "$300",
        "damage": 33,
        "recoil": "65%",
        "fire_rate": 500,
        "range": "19 м",
        "armor_penetration": "90.15%",
        "reload": "2.5 сек",
        "ammo": "18/90",
        "move_speed": 240,
        "headshot_armored": 119,
        "headshot_unarmored": 132,
        "description": "Мощный пистолет для T. One-shot headshot в упор."
    },
    "fiveseven": {
        "name": "Five-SeveN",
        "price": "$500",
        "kill_reward": "$300",
        "damage": 32,
        "recoil": "65%",
        "fire_rate": 400,
        "range": "22 м",
        "armor_penetration": "91%",
        "reload": "2.2 сек",
        "ammo": "20/100",
        "move_speed": 240,
        "headshot_armored": 112,
        "headshot_unarmored": 123,
        "description": "Аналог Tec-9 для CT. Точный с хорошим пробитием."
    },
    "r8": {
        "name": "Револьвер R8",
        "price": "$600",
        "kill_reward": "$300",
        "damage": 86,
        "recoil": "4%",
        "fire_rate": "85 / 150",
        "range": "60 м",
        "armor_penetration": "93.2%",
        "reload": "2.3 сек",
        "ammo": "8/8",
        "move_speed": "220 / 180",
        "headshot_armored": "One-shot",
        "headshot_unarmored": "One-shot",
        "description": "Медленный, но мощный. Альтернатива Desert Eagle."
    },
    "deagle": {
        "name": "Desert Eagle",
        "price": "$700",
        "kill_reward": "$300",
        "damage": 73,
        "recoil": "12%",
        "fire_rate": 267,
        "range": "35 м",
        "armor_penetration": "93.2%",
        "reload": "2.2 сек",
        "ammo": "7/35",
        "move_speed": 230,
        "headshot_armored": 231,
        "headshot_unarmored": 250,
        "description": "One-shot potential за $700. Требует идеальной точности."
    },
    # SMG
    "mac10": {
        "name": "MAC-10",
        "price": "$1,050",
        "kill_reward": "$600",
        "damage": 29,
        "recoil": "80%",
        "fire_rate": 800,
        "range": "15 м",
        "armor_penetration": "57.5%",
        "reload": "2.6 сек",
        "ammo": "30/100",
        "move_speed": 240,
        "headshot_armored": 65,
        "headshot_unarmored": 114,
        "description": "Бюджетный SMG для T. Отличен для форс-баев."
    },
    "ump45": {
        "name": "UMP-45",
        "price": "$1,200",
        "kill_reward": "$600",
        "damage": 35,
        "recoil": "76%",
        "fire_rate": 666,
        "range": "11 м",
        "armor_penetration": "65%",
        "reload": "3.5 сек",
        "ammo": "25/100",
        "move_speed": 230,
        "headshot_armored": 90,
        "headshot_unarmored": 140,
        "description": "SMG с характеристиками винтовки. Хорошее пробитие брони."
    },
    "mp9": {
        "name": "MP9",
        "price": "$1,250",
        "kill_reward": "$600",
        "damage": 26,
        "recoil": "80%",
        "fire_rate": 857,
        "range": "16 м",
        "armor_penetration": "60%",
        "reload": "2.1 сек",
        "ammo": "30/120",
        "move_speed": 240,
        "headshot_armored": 61,
        "headshot_unarmored": 104,
        "description": "Самый быстрый SMG для CT. Идеален для анти-эко."
    },
    "bizon": {
        "name": "ПП-19 Бизон",
        "price": "$1,400",
        "kill_reward": "$600",
        "damage": 27,
        "recoil": "80%",
        "fire_rate": 750,
        "range": "14 м",
        "armor_penetration": "57.5%",
        "reload": "2.4 сек",
        "ammo": "64/120",
        "move_speed": 240,
        "headshot_armored": 61,
        "headshot_unarmored": 108,
        "description": "Большой магазин на 64 патрона. Слабое пробитие брони."
    },
    "mp7": {
        "name": "MP7",
        "price": "$1,500",
        "kill_reward": "$600",
        "damage": 29,
        "recoil": "84%",
        "fire_rate": 800,
        "range": "14 м",
        "armor_penetration": "62.5%",
        "reload": "3.1 сек",
        "ammo": "30/120",
        "move_speed": 220,
        "headshot_armored": 71,
        "headshot_unarmored": 110,
        "description": "Сбалансированный SMG. Хорошая точность на средней дистанции."
    },
    "mp5sd": {
        "name": "MP5-SD",
        "price": "$1,500",
        "kill_reward": "$600",
        "damage": 27,
        "recoil": "85%",
        "fire_rate": 750,
        "range": "15 м",
        "armor_penetration": "62.5%",
        "reload": "2.97 сек",
        "ammo": "30/120",
        "move_speed": 235,
        "headshot_armored": 66,
        "headshot_unarmored": 107,
        "description": "Тихий SMG с глушителем. Альтернатива MP7."
    },
    "p90": {
        "name": "P90",
        "price": "$2,350",
        "kill_reward": "$300",
        "damage": 26,
        "recoil": "61%",
        "fire_rate": 857,
        "range": "15 м",
        "armor_penetration": "69%",
        "reload": "3.3 сек",
        "ammo": "50/100",
        "move_speed": 230,
        "headshot_armored": 71,
        "headshot_unarmored": 103,
        "description": "Бег и стрельба. Большой магазин, но низкая награда."
    },
    # Дробовики
    "nova": {
        "name": "Nova",
        "price": "$1,050",
        "kill_reward": "$900",
        "damage": "234 (картечь)",
        "recoil": "4%",
        "fire_rate": 68,
        "range": "3 м",
        "armor_penetration": "50%",
        "reload": "3.7 сек",
        "ammo": "8/32",
        "move_speed": 220,
        "headshot_armored": 52,
        "headshot_unarmored": 106,
        "description": "Бюджетный дробовик. Эффективен в упор."
    },
    "sawedoff": {
        "name": "Sawed-Off",
        "price": "$1,100",
        "kill_reward": "$900",
        "damage": "256 (картечь)",
        "recoil": "3%",
        "fire_rate": 71,
        "range": "2 м",
        "armor_penetration": "75%",
        "reload": "3.2 сек",
        "ammo": "7/32",
        "move_speed": 210,
        "headshot_armored": 96,
        "headshot_unarmored": 128,
        "description": "Дробовик для T. Высокий урон, но малая дальность."
    },
    "mag7": {
        "name": "MAG-7",
        "price": "$1,300",
        "kill_reward": "$900",
        "damage": "240 (картечь)",
        "recoil": "4%",
        "fire_rate": 71,
        "range": "5 м",
        "armor_penetration": "75%",
        "reload": "2.4 сек",
        "ammo": "5/32",
        "move_speed": 225,
        "headshot_armored": 90,
        "headshot_unarmored": 120,
        "description": "Дробовик для CT. Перезарядка по одному патрону."
    },
    "xm1014": {
        "name": "XM1014",
        "price": "$2,000",
        "kill_reward": "$900",
        "damage": 120,
        "recoil": "4%",
        "fire_rate": 171,
        "range": "3 м",
        "armor_penetration": "80%",
        "reload": "2.8 сек",
        "ammo": "7/32",
        "move_speed": 215,
        "headshot_armored": 64,
        "headshot_unarmored": 80,
        "description": "Полуавтоматический дробовик. Высокая скорострельность."
    },
    # Пулемёты
    "negev": {
        "name": "Негев",
        "price": "$1,700",
        "kill_reward": "$300",
        "damage": 35,
        "recoil": "76%",
        "fire_rate": 800,
        "range": "13 м",
        "armor_penetration": "75%",
        "reload": "5.7 сек",
        "ammo": "150/300",
        "move_speed": 150,
        "headshot_armored": 105,
        "headshot_unarmored": 140,
        "description": "Бюджетный пулемёт. Долго разгоняется, но точен."
    },
    "m249": {
        "name": "M249",
        "price": "$5,200",
        "kill_reward": "$300",
        "damage": 32,
        "recoil": "73%",
        "fire_rate": 750,
        "range": "16 м",
        "armor_penetration": "80%",
        "reload": "5.7 сек",
        "ammo": "100/200",
        "move_speed": 195,
        "headshot_armored": 102,
        "headshot_unarmored": 128,
        "description": "Полноценный пулемёт. Редко используется из-за цены."
    },
    # Винтовки
    "galil": {
        "name": "Galil AR",
        "price": "$1,800",
        "kill_reward": "$300",
        "damage": 30,
        "recoil": "76%",
        "fire_rate": 666,
        "range": "23 м",
        "armor_penetration": "77.5%",
        "reload": "3 сек",
        "ammo": "35/90",
        "move_speed": 215,
        "headshot_armored": 92,
        "headshot_unarmored": 119,
        "description": "Эконом-винтовка для T. Хороший выбор на форс-бае."
    },
    "famas": {
        "name": "FAMAS",
        "price": "$2,050",
        "kill_reward": "$300",
        "damage": 30,
        "recoil": "80%",
        "fire_rate": "666 / 800",
        "range": "21 м",
        "armor_penetration": "70%",
        "reload": "3.3 сек",
        "ammo": "25/90",
        "move_speed": 220,
        "headshot_armored": 84,
        "headshot_unarmored": 120,
        "description": "Эконом-винтовка для CT. Режим очереди по 3 патрона."
    },
    "ak47": {
        "name": "AK-47",
        "price": "$2,700",
        "kill_reward": "$300",
        "damage": 36,
        "recoil": "69%",
        "fire_rate": 600,
        "range": "36 м",
        "armor_penetration": "77.5%",
        "reload": "2.5 сек",
        "ammo": "30/90",
        "move_speed": 215,
        "headshot_armored": 111,
        "headshot_unarmored": 143,
        "description": "Лучшая винтовка террористов. One-shot headshot делает её мета-выбором."
    },
    "m4a1s": {
        "name": "M4A1-S",
        "price": "$2,900",
        "kill_reward": "$300",
        "damage": 33,
        "recoil": "73%",
        "fire_rate": 600,
        "range": "28 м",
        "armor_penetration": "70%",
        "reload": "3.1 сек",
        "ammo": "20/80",
        "move_speed": 225,
        "headshot_armored": 92,
        "headshot_unarmored": 132,
        "description": "Тише, точнее, дешевле. 20 патронов — главный минус."
    },
    "sg553": {
        "name": "SG 553",
        "price": "$3,000",
        "kill_reward": "$300",
        "damage": 30,
        "recoil": "69%",
        "fire_rate": 666,
        "range": "36 м",
        "armor_penetration": "100%",
        "reload": "2.8 сек",
        "ammo": "30/90",
        "move_speed": 210,
        "headshot_armored": 120,
        "headshot_unarmored": 120,
        "description": "Винтовка с прицелом для T. 100% пробитие брони."
    },
    "m4a4": {
        "name": "M4A4",
        "price": "$3,100",
        "kill_reward": "$300",
        "damage": 33,
        "recoil": "76%",
        "fire_rate": 666,
        "range": "28 м",
        "armor_penetration": "70%",
        "reload": "3.1 сек",
        "ammo": "30/90",
        "move_speed": 225,
        "headshot_armored": 92,
        "headshot_unarmored": 131,
        "description": "Высокая скорострельность, больше патронов. Лучше для спрея."
    },
    "aug": {
        "name": "AUG",
        "price": "$3,300",
        "kill_reward": "$300",
        "damage": 28,
        "recoil": "73%",
        "fire_rate": 666,
        "range": "49 м",
        "armor_penetration": "90%",
        "reload": "3.8 сек",
        "ammo": "30/90",
        "move_speed": 220,
        "headshot_armored": 101,
        "headshot_unarmored": 112,
        "description": "Винтовка с прицелом для CT. Высокая точность на дистанции."
    },
    # Снайперские винтовки
    "ssg08": {
        "name": "SSG 08",
        "price": "$1,700",
        "kill_reward": "$300",
        "damage": 88,
        "recoil": "46%",
        "fire_rate": 48,
        "range": "47 м",
        "armor_penetration": "85%",
        "reload": "3.7 сек",
        "ammo": "10/90",
        "move_speed": 230,
        "headshot_armored": 299,
        "headshot_unarmored": 352,
        "description": "Бюджетная снайперская винтовка. Быстрая передвижение."
    },
    "awp": {
        "name": "AWP",
        "price": "$4,750",
        "kill_reward": "$100",
        "damage": 115,
        "recoil": "3%",
        "fire_rate": 41,
        "range": "96 м",
        "armor_penetration": "97.5%",
        "reload": "3.6 сек",
        "ammo": "5/30",
        "move_speed": 200,
        "headshot_armored": 448,
        "headshot_unarmored": 460,
        "description": "One-shot body shot. Медленная, рискованная, но эффективная."
    },
    "scar20": {
        "name": "SCAR-20",
        "price": "$5,000",
        "kill_reward": "$300",
        "damage": 80,
        "recoil": "65%",
        "fire_rate": 240,
        "range": "66 м",
        "armor_penetration": "82.5%",
        "reload": "3.1 сек",
        "ammo": "20/90",
        "move_speed": 215,
        "headshot_armored": 263,
        "headshot_unarmored": 319,
        "description": "Полуавтоматическая снайперская винтовка для CT."
    },
    "g3sg1": {
        "name": "G3SG1",
        "price": "$5,000",
        "kill_reward": "$300",
        "damage": 80,
        "recoil": "65%",
        "fire_rate": 240,
        "range": "92 м",
        "armor_penetration": "82.5%",
        "reload": "4.7 сек",
        "ammo": "20/90",
        "move_speed": "215 / 150",
        "headshot_armored": 263,
        "headshot_unarmored": 319,
        "description": "Полуавтоматическая снайперская винтовка для T."
    },
    # Специальное
    "zeus": {
        "name": "Зевс x27",
        "price": "$200",
        "kill_reward": "$100",
        "damage": 500,
        "recoil": "N/A",
        "fire_rate": "Одноразовый",
        "range": "2 м",
        "armor_penetration": "100%",
        "reload": "30 сек",
        "ammo": "1/∞",
        "move_speed": 230,
        "headshot_armored": "One-shot",
        "headshot_unarmored": "One-shot",
        "description": "Электрошокер. One-shot в упор, перезарядка 30 сек."
    }
}

ECONOMY_GUIDE = {
    "full_buy": {
        "name": "💰 Полный закуп (Full Buy)",
        "money": "$4,500+",
        "equipment": "Винтовка + Броня + Гранаты + Defuse Kit (CT)",
        "when": "Когда у всей команды достаточно денег"
    },
    "force_buy": {
        "name": "⚡ Форс-бай (Force Buy)",
        "money": "$2,000 - $4,500",
        "equipment": "SMG / Shotgun / Deagle + Лёгкая броня + Флешки",
        "when": "После проигранного пистолетного раунда или когда нужно сломать экономику врага"
    },
    "eco": {
        "name": "🌱 Эко-раунд (Eco)",
        "money": "$0 - $2,000",
        "equipment": "Только пистолеты или ничего",
        "when": "Когда нет денег на нормальный закуп. Цель — сохранить оружие для следующего раунда"
    },
    "semi_eco": {
        "name": "🌿 Полу-эко (Semi-Eco)",
        "money": "$1,500 - $3,000",
        "equipment": "Deagle / P250 + Броня или гранаты",
        "when": "Компромисс между эко и форсом"
    },
    "anti_eco": {
        "name": "🛡️ Анти-эко",
        "money": "$5,000+",
        "equipment": "SMG для фарма денег + полная броня",
        "when": "Когда знаете что у врага эко. SMG дают $600 за убийство!"
    }
}

MAP_POOL = {
    "active_duty": ["Mirage", "Inferno", "Nuke", "Ancient", "Anubis", "Vertigo", "Dust2"],
    "premier": ["Mirage", "Inferno", "Nuke", "Ancient", "Anubis", "Vertigo", "Overpass"],
    "removed": ["Train", "Cobblestone", "Cache"]
}

# ============ ОБРАБОТЧИКИ ============

@router.callback_query(F.data == "menu_meta")
async def menu_meta(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass
    
    await callback.message.answer(
        "📊 <b>Мета-гейм CS2</b>\n\n"
        "Актуальная информация об оружии, экономике и игровом балансе.",
        reply_markup=meta_menu(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "back_to_meta")
async def back_to_meta(callback: types.CallbackQuery):
    """Возврат в меню меты"""
    await callback.message.edit_text(
        "📊 <b>Мета-гейм CS2</b>\n\n"
        "Актуальная информация об оружии, экономике и игровом балансе.",
        reply_markup=meta_menu(),
        parse_mode="HTML"
    )

def find_image_file(base_path: str):
    """Ищет файл с любым поддерживаемым расширением"""
    extensions = ['.jpg', '.jpeg', '.png']
    for ext in extensions:
        full_path = base_path + ext
        if os.path.exists(full_path):
            return full_path
    return None

async def safe_edit_or_send(callback: types.CallbackQuery, text: str, reply_markup, parse_mode="HTML"):
    """Безопасно редактирует или отправляет новое сообщение если редактирование невозможно"""
    try:
        await callback.message.edit_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
    except TelegramBadRequest as e:
        error_msg = str(e).lower()
        if "there is no text" in error_msg or "message is not modified" in error_msg:
            try:
                await callback.message.delete()
            except:
                pass
            await callback.message.answer(text, reply_markup=reply_markup, parse_mode=parse_mode)
        else:
            raise

@router.callback_query(F.data == "meta_weapons")
async def meta_weapons(callback: types.CallbackQuery, bot: Bot):
    base_path = os.path.join(MEDIA_DIR, "meta", "weapon_tierlist")
    tierlist_img = find_image_file(base_path)
    has_image = tierlist_img is not None
    
    text = """
<b>🔫 Тир-лист оружия CS2</b>
<i>Актуально на текущий патч</i>

<b>🟦 S-Tier (Мета):</b>
• <b>AK-47</b> — Лучший выбор для T, one-shot headshot
• <b>M4A4/M4A1-S</b> — Зависит от стиля (A4 для спрея, A1-S для тапов)
• <b>AWP</b> — Ситуативно, доминирует на длинных дистанциях

<b>🟩 A-Tier (Сильные):</b>
• <b>MP9/Mac-10</b> — Лучшие SMG для форс-баев
• <b>Galil/FAMAS</b> — Эконом-вариант винтовок
• <b>Desert Eagle</b> — One-shot potential, но требует скилла

<b>🟨 B-Tier (Ситуативные):</b>
• <b>Scout</b> — Бюджетная альтернатива AWP
• <b>MP7/UMP-45</b> — Альтернативы MP9/Mac-10
• <b>P250/CZ75</b> — Ситуативные пистолеты

<b>💡 Советы:</b>
• M4A1-S популярнее из-за точности первого выстрела
• На форс-бае берите SMG для бонуса к деньгам
• AWP — высокий риск, высокая награда
"""
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📈 Статистика оружия", callback_data="meta_weapon_stats")],
    [InlineKeyboardButton(text="← Назад", callback_data="menu_meta")]
    ])
    if has_image:
        await callback.message.delete()
        await bot.send_photo(
            chat_id=callback.message.chat.id,
            photo=FSInputFile(tierlist_img),
            caption=text,
            reply_markup=kb,
            parse_mode="HTML"
        )
    else:
        await safe_edit_or_send(callback, text, kb, parse_mode="HTML")

@router.callback_query(F.data == "meta_weapon_stats")
async def meta_weapon_stats(callback: types.CallbackQuery):
    """Статистика оружия - меню категорий"""
    text = """
<b>📈 Статистика оружия CS2</b>

Выберите категорию:
"""
    buttons = [
        [InlineKeyboardButton(text="🔫 Пистолеты", callback_data="weapon_cat_pistols")],
        [InlineKeyboardButton(text="🔫 SMG", callback_data="weapon_cat_smg")],
        [InlineKeyboardButton(text="🔫 Дробовики", callback_data="weapon_cat_shotguns")],
        [InlineKeyboardButton(text="🔫 Винтовки", callback_data="weapon_cat_rifles")],
        [InlineKeyboardButton(text="🔫 Снайперские винтовки", callback_data="weapon_cat_snipers")],
        [InlineKeyboardButton(text="🔫 Пулемёты и специальное", callback_data="weapon_cat_heavy")],
        [InlineKeyboardButton(text="← Назад", callback_data="back_to_meta")]
    ]
    
    await safe_edit_or_send(callback, text, InlineKeyboardMarkup(inline_keyboard=buttons), parse_mode="HTML")

@router.callback_query(F.data.startswith("weapon_cat_"))
async def show_weapon_category(callback: types.CallbackQuery):
    """Показать оружие по категориям"""
    category = callback.data.replace("weapon_cat_", "")
    
    category_map = {
        "pistols": ["glock", "usp", "p2000", "p250", "dual_berettas", "cz75", "tec9", "fiveseven", "r8", "deagle"],
        "smg": ["mac10", "ump45", "mp9", "bizon", "mp7", "mp5sd", "p90"],
        "shotguns": ["nova", "sawedoff", "mag7", "xm1014"],
        "rifles": ["galil", "famas", "ak47", "m4a1s", "sg553", "m4a4", "aug"],
        "snipers": ["ssg08", "awp", "scar20", "g3sg1"],
        "heavy": ["negev", "m249", "zeus"]
    }
    
    weapons = category_map.get(category, [])
    buttons = []
    
    for weapon_id in weapons:
        weapon = WEAPON_STATS.get(weapon_id)
        if weapon:
            buttons.append([InlineKeyboardButton(
                text=f"{weapon['name']} ({weapon['price']})", 
                callback_data=f"weapon_stat_{weapon_id}"
            )])
    
    buttons.append([InlineKeyboardButton(text="← К категориям", callback_data="meta_weapon_stats")])
    
    category_names = {
        "pistols": "Пистолеты",
        "smg": "SMG",
        "shotguns": "Дробовики",
        "rifles": "Винтовки",
        "snipers": "Снайперские винтовки",
        "heavy": "Пулемёты и специальное"
    }
    
    await safe_edit_or_send(
        callback,
        f"<b>📈 {category_names.get(category, 'Оружие')}</b>\n\nВыберите оружие:",
        InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("weapon_stat_"))
async def show_weapon_stat(callback: types.CallbackQuery):
    """Показать детальную статистику оружия"""
    weapon_id = callback.data.replace("weapon_stat_", "")
    weapon = WEAPON_STATS.get(weapon_id)
    
    if not weapon:
        await callback.answer("Оружие не найдено!", show_alert=True)
        return
    
    category_map = {
        "pistols": ["glock", "usp", "p2000", "p250", "dual_berettas", "cz75", "tec9", "fiveseven", "r8", "deagle"],
        "smg": ["mac10", "ump45", "mp9", "bizon", "mp7", "mp5sd", "p90"],
        "shotguns": ["nova", "sawedoff", "mag7", "xm1014"],
        "rifles": ["galil", "famas", "ak47", "m4a1s", "sg553", "m4a4", "aug"],
        "snipers": ["ssg08", "awp", "scar20", "g3sg1"],
        "heavy": ["negev", "m249", "zeus"]
    }
    
    back_category = "meta_weapon_stats"
    for cat, weapons in category_map.items():
        if weapon_id in weapons:
            back_category = f"weapon_cat_{cat}"
            break
    
    text = f"""
<b>🔫 {weapon['name']}</b>

<b>💰 Цена:</b> {weapon['price']}
<b>💵 Награда за убийство:</b> {weapon['kill_reward']}

<b>⚔️ Характеристики:</b>
• Урон: <code>{weapon['damage']}</code>
• Отдача: <code>{weapon['recoil']}</code> (выше = лучше контроль)
• Скорострельность: <code>{weapon['fire_rate']}</code>
• Дальность: <code>{weapon['range']}</code>
• Пробитие брони: <code>{weapon['armor_penetration']}</code>
• Перезарядка: <code>{weapon['reload']}</code>
• Патроны: <code>{weapon['ammo']}</code>
• Скорость передвижения: <code>{weapon['move_speed']}</code>

<b>🎯 Урон в голову:</b>
• В броне: <code>{weapon['headshot_armored']}</code>
• Без брони: <code>{weapon['headshot_unarmored']}</code>

<b>📝 Описание:</b>
<i>{weapon['description']}</i>
"""
    
    await safe_edit_or_send(
        callback,
        text,
        InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="← К списку", callback_data=back_category)]
        ]),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "meta_economy")
async def meta_economy(callback: types.CallbackQuery):
    """Гайд по экономике"""
    text = """
<b>💰 Экономика CS2</b>

<b>🎯 Основные принципы:</b>
• Проигрыш: +$1,400 (стек до $3,400)
• Победа: +$3,250 + награды за убийства
• Закладка бомбы: +$300 (T)
• Обезвреживание: +$300 (CT)
• Спасение заложника: +$1,000 (CT)

<b>💡 Золотые правила:</b>
• Не форсьте после первой победы (враг на эко)
• Если у вас $4,500+ — закупайтесь полностью
• На эко сохраняйте оружие teammates
• SMG дают $600 за убийство (фарм против эко)
"""
    
    buttons = []
    for eco_id, eco_data in ECONOMY_GUIDE.items():
        buttons.append([InlineKeyboardButton(
            text=eco_data['name'], 
            callback_data=f"eco_{eco_id}"
        )])
    
    buttons.append([InlineKeyboardButton(text="← Назад", callback_data="back_to_meta")])
    
    await safe_edit_or_send(callback, text, InlineKeyboardMarkup(inline_keyboard=buttons), parse_mode="HTML")

@router.callback_query(F.data.startswith("eco_"))
async def show_economy_detail(callback: types.CallbackQuery):
    """Детальная информация о типе закупа"""
    eco_id = callback.data.replace("eco_", "")
    eco = ECONOMY_GUIDE.get(eco_id)
    
    if not eco:
        await callback.answer("Информация не найдена!", show_alert=True)
        return
    
    text = f"""
<b>{eco['name']}</b>

<b>💵 Деньги:</b> <code>{eco['money']}</code>
<b>🎒 Экипировка:</b> {eco['equipment']}

<b>📋 Когда использовать:</b>
<i>{eco['when']}</i>

<b>💡 Совет:</b> Координируйтесь с командой! Смешанные закупы = проигрыш.
"""

    await safe_edit_or_send(
        callback,
        text,
        InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="← К экономике", callback_data="meta_economy")]
        ]),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "meta_maps")
async def meta_maps(callback: types.CallbackQuery):
    """Актуальный пул карт"""
    text = f"""
<b>🗺️ Актуальный пул карт CS2</b>

<b>🟢 Active Duty (MM/Premier):</b>
{', '.join(MAP_POOL['active_duty'])}

<b>🔵 Premier Only:</b>
Overpass (в MM убрали)

<b>🔴 Убраны из игры:</b>
{', '.join(MAP_POOL['removed'])}

<b>💡 Советы по картам:</b>
• <b>Mirage</b> — самая популярная, учите первой
• <b>Inferno</b> — сложная тактически, много гранат
• <b>Nuke</b> — вертикальность, уникальная
• <b>Ancient</b> — новая, все учат с нуля
• <b>Anubis</b> — водная карта, специфичная
• <b>Vertigo</b> — высоты, подходит для AWP
• <b>Dust2</b> — классика, но скучная мета
"""
    
    await safe_edit_or_send(
    callback,
    text,
    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← Назад", callback_data="menu_meta")]
    ]),
    parse_mode="HTML"
)