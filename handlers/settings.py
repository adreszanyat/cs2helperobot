from aiogram import Router, F, types, Bot
from aiogram.types import FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.exceptions import TelegramBadRequest
import os

from keyboards import (
    settings_menu, fps_tier_menu, console_tier_menu,
    crosshairs_menu, pro_configs_menu, pro_binds_menu,
    crosshair_detail_menu
)
from config import MEDIA_DIR

router = Router()

async def safe_edit_or_send(callback: types.CallbackQuery, bot: Bot, text: str, reply_markup, **kwargs):
    """Безопасно редактирует или отправляет новое сообщение"""
    try:
        await callback.message.edit_text(text, reply_markup=reply_markup, **kwargs)
    except TelegramBadRequest as e:
        error_msg = str(e).lower()
        if "message is not modified" in error_msg:
            await callback.answer("Уже отображено", show_alert=False)
        elif "there is no text" in error_msg or "not found" in error_msg:
            try:
                await callback.message.delete()
            except:
                pass
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text=text,
                reply_markup=reply_markup,
                **kwargs
            )
        else:
            raise

FPS_TIERS = {
    "low": {
        "name": "🖥️ Слабый ПК (60-100 FPS)",
        "commands": """
fps_max 0
cl_showfps 1
r_dynamic 0
mat_queue_mode 2
cl_forcepreload 1
r_drawtracers_firstperson 0
muzzleflash_light 0
func_break_max_pieces 0
r_eyegloss 0
r_eyemove 0
r_eyeshift_x 0
r_eyeshift_y 0
r_eyeshift_z 0
r_eyesize 0""",
        "settings": "Все настройки графики на MINIMUM, разрешение 1024x768 или ниже"
    },
    "mid": {
        "name": "💻 Средний ПК (100-200 FPS)",
        "commands": """
fps_max 300
cl_showfps 1
r_dynamic 1
mat_queue_mode 2
cl_forcepreload 1
r_drawtracers_firstperson 1
muzzleflash_light 1""",
        "settings": "Средние настройки, тени HIGH (для видимости), разрешение 1280x960"
    },
    "high": {
        "name": "🖥️ Киберспорт (200+ FPS)",
        "commands": """
fps_max 400
cl_showfps 1
net_graph 1
r_dynamic 1
mat_queue_mode -1
cl_forcepreload 0
rate 786432
cl_cmdrate 128
cl_updaterate 128
cl_interp 0
cl_interp_ratio 1""",
        "settings": "Оптимальные настройки для минимального input lag, 128 tick mindset"
    }
}

PRO_CROSSHAIRS = {
    "simple": {
        "name": "s1mple (BC.Game)",
        "code": "CSGO-E8xcE-27Lmw-2ipNt-3HZvp-pevvE",
        "style": "5 (Динамический с разделением)",
        "color": "Голубой (Cyan)",
        "size": "1",
        "thickness": "0",
        "gap": "-2",
        "dot": "Да",
        "outline": "Нет",
        "alpha": "255",
        "console": "cl_crosshairgap -2;cl_crosshair_outlinethickness 0;cl_crosshaircolor_r 0;cl_crosshaircolor_g 255;cl_crosshaircolor_b 255;cl_crosshairalpha 255;cl_crosshair_dynamic_splitdist 7;cl_crosshair_recoil false;cl_fixedcrosshairgap 3;cl_crosshaircolor 4;cl_crosshair_drawoutline false;cl_crosshair_dynamic_splitalpha_innermod 1;cl_crosshair_dynamic_splitalpha_outermod 0.5;cl_crosshair_dynamic_maxdist_splitratio 0.3;cl_crosshairthickness 0;cl_crosshairdot true;cl_crosshairgap_useweaponvalue false;cl_crosshairusealpha true;cl_crosshair_t false;cl_crosshairstyle 5;cl_crosshairsize 1"
    },
    "zywoo": {
        "name": "ZywOo (Vitality)",
        "code": "CSGO-cNkTP-CTzr2-G23Ua-4wLnf-7ywPB",
        "style": "4 (Классический статический)",
        "color": "Зеленый (Green)",
        "size": "1.7",
        "thickness": "0.1",
        "gap": "-2.2",
        "dot": "Нет",
        "outline": "Нет",
        "alpha": "255",
        "console": "cl_crosshairgap -2.2;cl_crosshair_outlinethickness 1;cl_crosshaircolor_r 0;cl_crosshaircolor_g 255;cl_crosshaircolor_b 255;cl_crosshairalpha 255;cl_crosshair_dynamic_splitdist 3;cl_crosshair_recoil false;cl_fixedcrosshairgap 3;cl_crosshaircolor 5;cl_crosshair_drawoutline false;cl_crosshair_dynamic_splitalpha_innermod 0;cl_crosshair_dynamic_splitalpha_outermod 1;cl_crosshair_dynamic_maxdist_splitratio 1;cl_crosshairthickness 0.1;cl_crosshairdot false;cl_crosshairgap_useweaponvalue false;cl_crosshairusealpha true;cl_crosshair_t false;cl_crosshairstyle 4;cl_crosshairsize 1.7"
    },
    "niko": {
        "name": "NiKo (Falcons)",
        "code": "CSGO-td8s8-kfyi5-PtiK2-A8kVS-JNeZH",
        "style": "4 (Классический статический)",
        "color": "Зеленый (Green)",
        "size": "1",
        "thickness": "1",
        "gap": "-4",
        "dot": "Нет",
        "outline": "Нет",
        "alpha": "255",
        "console": "cl_crosshairgap -4;cl_crosshair_outlinethickness 0;cl_crosshaircolor_r 0;cl_crosshaircolor_g 255;cl_crosshaircolor_b 145;cl_crosshairalpha 255;cl_crosshair_dynamic_splitdist 3;cl_crosshair_recoil false;cl_fixedcrosshairgap 0;cl_crosshaircolor 5;cl_crosshair_drawoutline false;cl_crosshair_dynamic_splitalpha_innermod 0;cl_crosshair_dynamic_splitalpha_outermod 1;cl_crosshair_dynamic_maxdist_splitratio 1;cl_crosshairthickness 1;cl_crosshairdot false;cl_crosshairgap_useweaponvalue false;cl_crosshairusealpha true;cl_crosshair_t false;cl_crosshairstyle 4;cl_crosshairsize 1"
    },
    "monesy": {
        "name": "m0NESY (Falcons)",
        "code": "CSGO-VHcPj-yPL6x-NAHqX-s2yyW-o2OtQ",
        "style": "4 (Классический статический)",
        "color": "Голубой (Cyan)",
        "size": "1",
        "thickness": "0",
        "gap": "-4",
        "dot": "Нет",
        "outline": "Нет",
        "alpha": "255",
        "console": "cl_crosshairgap -4;cl_crosshair_outlinethickness 1;cl_crosshaircolor_r 0;cl_crosshaircolor_g 255;cl_crosshaircolor_b 255;cl_crosshairalpha 255;cl_crosshair_dynamic_splitdist 3;cl_crosshair_recoil false;cl_fixedcrosshairgap 3;cl_crosshaircolor 4;cl_crosshair_drawoutline false;cl_crosshair_dynamic_splitalpha_innermod 0;cl_crosshair_dynamic_splitalpha_outermod 1;cl_crosshair_dynamic_maxdist_splitratio 1;cl_crosshairthickness 0;cl_crosshairdot false;cl_crosshairgap_useweaponvalue false;cl_crosshairusealpha true;cl_crosshair_t false;cl_crosshairstyle 4;cl_crosshairsize 1"
    },
    "donk": {
        "name": "donk (Team Spirit)",
        "code": "CSGO-LdXHk-hatWX-JjEa8-tuLDN-5tbJD",
        "style": "4 (Классический статический)",
        "color": "Белый (White)",
        "size": "1",
        "thickness": "1",
        "gap": "-4",
        "dot": "Нет",
        "outline": "Нет",
        "alpha": "255",
        "console": "cl_crosshairgap -4;cl_crosshair_outlinethickness 1;cl_crosshaircolor_r 255;cl_crosshaircolor_g 255;cl_crosshaircolor_b 255;cl_crosshairalpha 255;cl_crosshair_dynamic_splitdist 7;cl_crosshair_recoil false;cl_fixedcrosshairgap 3;cl_crosshaircolor 5;cl_crosshair_drawoutline false;cl_crosshair_dynamic_splitalpha_innermod 1;cl_crosshair_dynamic_splitalpha_outermod 0.5;cl_crosshair_dynamic_maxdist_splitratio 0.3;cl_crosshairthickness 1;cl_crosshairdot false;cl_crosshairgap_useweaponvalue false;cl_crosshairusealpha true;cl_crosshair_t false;cl_crosshairstyle 4;cl_crosshairsize 1"
    },
    "shiro": {
        "name": "sh1ro (Team Spirit)",
        "code": "CSGO-u2H9q-R3KDb-ijHuY-Bfizr-J9T8N",
        "style": "4 (Классический статический)",
        "color": "Зеленый (Green)",
        "size": "1",
        "thickness": "1",
        "gap": "-4",
        "dot": "Нет",
        "outline": "Нет",
        "alpha": "200",
        "console": "cl_crosshairgap -4;cl_crosshair_outlinethickness 1;cl_crosshaircolor_r 0;cl_crosshaircolor_g 255;cl_crosshaircolor_b 0;cl_crosshairalpha 200;cl_crosshair_dynamic_splitdist 3;cl_crosshair_recoil false;cl_fixedcrosshairgap 3;cl_crosshaircolor 5;cl_crosshair_drawoutline false;cl_crosshair_dynamic_splitalpha_innermod 0;cl_crosshair_dynamic_splitalpha_outermod 1;cl_crosshair_dynamic_maxdist_splitratio 1;cl_crosshairthickness 1;cl_crosshairdot false;cl_crosshairgap_useweaponvalue false;cl_crosshairusealpha true;cl_crosshair_t false;cl_crosshairstyle 4;cl_crosshairsize 1"
    }
}

@router.callback_query(F.data == "menu_settings")
async def menu_settings(callback: types.CallbackQuery, bot: Bot):
    text = (
        "⚙️ <b>Настройки CS2</b>\n\n"
        "Здесь вы найдете:\n"
        "🚀 Параметры запуска\n"
        "💻 Оптимизацию под ваш ПК\n"
        "🎯 Прицелы про игроков\n"
        "⌨️ Бинды про игроков\n"
        "📥 Полные конфиги про игроков"
    )
    await safe_edit_or_send(callback, bot, text, settings_menu(), parse_mode="HTML")

@router.callback_query(F.data == "back_to_settings")
async def back_to_settings(callback: types.CallbackQuery, bot: Bot):
    """Возврат в главное меню настроек"""
    text = (
        "⚙️ <b>Настройки CS2</b>\n\n"
        "Здесь вы найдете:\n"
        "🚀 Параметры запуска\n"
        "💻 Оптимизацию под ваш ПК\n"
        "🎯 Прицелы про игроков\n"
        "⌨️ Бинды про игроков\n"
        "📥 Полные конфиги про игроков"
    )
    await safe_edit_or_send(callback, bot, text, settings_menu(), parse_mode="HTML")

@router.callback_query(F.data == "settings_crosshairs")
async def settings_crosshairs(callback: types.CallbackQuery, bot: Bot):
    text = (
        "🎯 <b>Прицелы про игроков</b>\n\n"
        "Актуальные прицелы с <a href='https://procrosshairs.com/'>procrosshairs.com</a>:\n"
        "Выберите игрока для просмотра настроек:"
    )
    await safe_edit_or_send(
        callback, bot, text, crosshairs_menu(), 
        parse_mode="HTML", disable_web_page_preview=True
    )

def find_image_file(base_path: str):
    """Ищет файл с любым поддерживаемым расширением"""
    extensions = ['.jpg', '.jpeg', '.png', '.gif']
    for ext in extensions:
        full_path = base_path + ext
        if os.path.exists(full_path):
            return full_path
    return None

@router.callback_query(F.data.startswith("crosshair_"))
async def show_crosshair(callback: types.CallbackQuery, bot: Bot):
    player = callback.data.replace("crosshair_", "")
    data = PRO_CROSSHAIRS.get(player)

    if not data:
        await callback.answer("Игрок не найден!", show_alert=True)
        return

    base_path = os.path.join(MEDIA_DIR, "crosshairs", player)
    crosshair_img = find_image_file(base_path)
    has_image = crosshair_img is not None

    text = f"""<b>🎯 Прицел {data['name']}</b>

<b>⚙️ Параметры:</b>
• Стиль: <code>{data['style']}</code>
• Цвет: <code>{data['color']}</code>
• Размер: <code>{data['size']}</code>
• Толщина: <code>{data['thickness']}</code>
• Gap: <code>{data['gap']}</code>
• Точка: <code>{data['dot']}</code>
• Обводка: <code>{data['outline']}</code>
• Прозрачность: <code>{data['alpha']}</code>

<i>Настройки → Прицел → Поделиться/Импортировать → Вставить код</i>"""

    try:
        await callback.message.delete()
    except:
        pass
    
    if has_image:
        await bot.send_photo(
            chat_id=callback.message.chat.id,
            photo=FSInputFile(crosshair_img),  
            caption=text,
            reply_markup=crosshair_detail_menu(player, True),
            parse_mode="HTML"
        )
    else:
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text + "\n\n<i>📸 Изображение прицела не найдено.</i>",
            reply_markup=crosshair_detail_menu(player, False),
            parse_mode="HTML"
        )

@router.callback_query(F.data.startswith("code_crosshair_"))
async def copy_crosshair_code(callback: types.CallbackQuery):
    player = callback.data.replace("code_crosshair_", "")
    data = PRO_CROSSHAIRS.get(player)

    if data:
        await callback.message.answer(
            f"<b>🎯 {data['name']}</b>\n\n"
            f"<code>{data['code']}</code>",
            parse_mode="HTML"
        )

@router.callback_query(F.data.startswith("console_crosshair_"))
async def copy_crosshair_console(callback: types.CallbackQuery):
    player = callback.data.replace("console_crosshair_", "")
    data = PRO_CROSSHAIRS.get(player)

    if data:
        await callback.message.answer(
            f"<b>⌨️ Консольные команды {data['name']}</b>\n\n"
            f"<code>{data['console']}</code>\n\n"
            f"<i>Вставьте в консоль CS2 (клавиша Ё)</i>",
            parse_mode="HTML"
        )

@router.callback_query(F.data.startswith("download_crosshair_"))
async def download_crosshair_config(callback: types.CallbackQuery):
    player = callback.data.replace("download_crosshair_", "")
    data = PRO_CROSSHAIRS.get(player)

    if not data:
        return

    crosshair_cfg = f"""// Прицел {data['name']}
// Сайт: https://procrosshairs.com/
// Импортируйте через: exec {player}_crosshair

{data['console']}
"""

    filename = f"{player}_crosshair.cfg"
    filepath = os.path.join(MEDIA_DIR, "configs", filename)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(crosshair_cfg)

    await callback.message.answer_document(
        FSInputFile(filepath),
        caption=f"🎯 <b>Прицел {data['name']}</b>\n\nВведите в консоли: <code>exec {player}_crosshair</code>",
        parse_mode="HTML"
    )

PRO_BINDS = {
    "simple": {
        "name": "s1mple",
        "description": "Агрессивные бинды для AWP и рантаймов",
        "binds": """bind mouse4 "+jump; -jump; +duck; -duck"  // Jumpthrow
bind mouse5 "use weapon_knife; use weapon_awp"  // Быстрая смена на AWP
bind v "+voicerecord"  // Голосовой чат на V
bind shift "+speed; r_cleardecals"  // Очистка декалей при ходьбе
bind f "use weapon_flashbang"  // Быстрая флешка
bind c "use weapon_smokegrenade"  // Быстрый смок
bind x "use weapon_molotov; use weapon_incgrenade"  // Быстрый молотов"""
    },
    "zywoo": {
        "name": "ZywOo",
        "description": "Бинды для комфортной игры на всех оружиях",
        "binds": """bind mouse4 "+jump; -jump; +duck; -duck"  // Jumpthrow
bind mouse5 "+lookatweapon"  // Осмотр оружия
bind v "+voicerecord"
bind shift "+speed; r_cleardecals"
bind f "use weapon_flashbang"
bind c "use weapon_smokegrenade"
bind x "use weapon_molotov; use weapon_incgrenade"
bind z "use weapon_hegrenade"""
    },
    "niko": {
        "name": "NiKo",
        "description": "Бинды для точной стрельбы и контроля",
        "binds": """bind mouse4 "+jump; -jump; +duck; -duck"
bind mouse5 "slot8"  // Бомба на mouse5
bind v "+voicerecord"
bind shift "+speed; r_cleardecals"
bind f "use weapon_flashbang"
bind c "use weapon_smokegrenade"
bind x "use weapon_molotov; use weapon_incgrenade"
bind mouse3 "slot7"  // Молотов на колесико"""
    },
    "ropz": {
        "name": "ropz",
        "description": "Минималистичные бинды для чистой игры",
        "binds": """bind mouse4 "+jump; -jump; +duck; -duck"
bind mouse5 "+klook"  // Старый бинд ropz
bind v "+voicerecord"
bind shift "+speed; r_cleardecals"
bind f "use weapon_flashbang"
bind c "use weapon_smokegrenade"
bind x "use weapon_molotov; use weapon_incgrenade"
bind m "showmouse"  // Показать мышь в меню"""
    }
}

@router.callback_query(F.data == "settings_binds")
async def settings_binds(callback: types.CallbackQuery, bot: Bot):
    text = (
        "⌨️ <b>Бинды про игроков</b>\n\n"
        "Уникальные бинды топовых игроков:"
    )
    await safe_edit_or_send(callback, bot, text, pro_binds_menu(), parse_mode="HTML")

@router.callback_query(F.data.startswith("binds_"))
async def show_binds(callback: types.CallbackQuery, bot: Bot): 
    player = callback.data.replace("binds_", "")
    data = PRO_BINDS.get(player)

    if not data:
        await callback.answer("Бинды не найдены!", show_alert=True)
        return

    text = f"""<b>⌨️ Бинды {data['name']}</b>
<i>{data['description']}</i>

<pre>{data['binds']}</pre>

<b>💡 Как использовать:</b>
1. Создайте файл <code>{player}_binds.cfg</code>
2. Вставьте бинды выше
3. В консоли CS2: <code>exec {player}_binds</code>"""

    filename = f"{player}_binds.cfg"
    filepath = os.path.join(MEDIA_DIR, "configs", filename)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(f"// Бинды {data['name']}\n")
        f.write(f"// {data['description']}\n\n")
        f.write(data['binds'])

    await safe_edit_or_send(
        callback, bot, text,
        InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📥 Скачать .cfg", callback_data=f"download_binds_{player}")],
            [InlineKeyboardButton(text="← Назад", callback_data="settings_binds")]
        ]),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("download_binds_"))
async def download_binds(callback: types.CallbackQuery):
    player = callback.data.replace("download_binds_", "")
    filename = f"{player}_binds.cfg"
    filepath = os.path.join(MEDIA_DIR, "configs", filename)

    if os.path.exists(filepath):
        await callback.message.answer_document(
            FSInputFile(filepath),
            caption=f"⌨️ <b>Бинды {player}</b>",
            parse_mode="HTML"
        )

PRO_CONFIGS = {
    "simple": {
        "name": "s1mple",
        "team": "BC.Game",
        "role": "AWPer / Star",
        "sens": "3.09 @ 400 DPI (eDPI: 1236)",
        "resolution": "1280x960 (4:3 stretched)",
        "viewmodel": "Классический",
        "zoom_sens": "1.0",
        "description": "Самая известная конфигурация в CS. Высокая сенса для быстрых фликов."
    },
    "zywoo": {
        "name": "ZywOo",
        "team": "Vitality",
        "role": "AWPer / Star",
        "sens": "2.0 @ 400 DPI (eDPI: 800)",
        "resolution": "1280x960 (4:3 stretched)",
        "viewmodel": "Классический",
        "zoom_sens": "1.0",
        "description": "Сбалансированная сенса для rifle и AWP."
    },
    "niko": {
        "name": "NiKo",
        "team": "Falcons",
        "role": "Rifler / Entry",
        "sens": "1.4 @ 400 DPI (eDPI: 560)",
        "resolution": "1280x960 (4:3 stretched)",
        "viewmodel": "Классический",
        "zoom_sens": "1.0",
        "description": "Очень низкая сенса для идеального контроля спрея."
    },
    "monesy": {
        "name": "m0NESY",
        "team": "Falcons",
        "role": "AWPer",
        "sens": "2.0 @ 400 DPI (eDPI: 800)",
        "resolution": "1280x960 (4:3 stretched)",
        "viewmodel": "Классический",
        "zoom_sens": "1.0",
        "description": "Стандартная сенса для молодых AWPеров."
    },
    "ropz": {
        "name": "ropz",
        "team": "Vitality",
        "role": "Rifler / Lurker",
        "sens": "1.77 @ 400 DPI (eDPI: 708)",
        "resolution": "1920x1080 (16:9)",
        "viewmodel": "Классический",
        "zoom_sens": "1.0",
        "description": "Единственный топовый игрок на 16:9. Чистая картинка."
    },
    "bit": {
        "name": "b1t",
        "team": "NAVI",
        "role": "Rifler",
        "sens": "1.42 @ 400 DPI (eDPI: 568)",
        "resolution": "1280x1024 (5:4 stretched)",
        "viewmodel": "Классический",
        "zoom_sens": "1.0",
        "description": "Уникальное разрешение 5:4 для широких моделек."
    }
}

@router.callback_query(F.data == "settings_pro_configs")
async def settings_pro_configs(callback: types.CallbackQuery, bot: Bot):
    text = (
        "📥 <b>Конфиги про игроков</b>\n\n"
        "Полные конфигурации с настройками сенсы, биндов и видео:"
    )
    await safe_edit_or_send(callback, bot, text, pro_configs_menu(), parse_mode="HTML")

@router.callback_query(F.data.startswith("config_pro_"))
async def show_pro_config(callback: types.CallbackQuery, bot: Bot):
    player = callback.data.replace("config_pro_", "")
    data = PRO_CONFIGS.get(player)

    if not data:
        await callback.answer("Конфиг не найден!", show_alert=True)
        return

    text = f"""<b>📥 Конфиг {data['name']}</b>
<b>{data['team']}</b> — {data['role']}

<b>🎯 Настройки мыши:</b>
• Сенса: <code>{data['sens']}</code>
• Zoom sens: <code>{data['zoom_sens']}</code>

<b>🖥️ Видео:</b>
• Разрешение: <code>{data['resolution']}</code>
• Вьюмодель: <code>{data['viewmodel']}</code>

<i>{data['description']}</i>

<b>⚠️ Внимание:</b> Полный конфиг включает прицел, бинды, настройки видео и мыши."""

    config_path = os.path.join(MEDIA_DIR, "configs", f"{player}_full.cfg")
    has_config = os.path.exists(config_path)

    buttons = [
        [InlineKeyboardButton(text="🎯 Прицел этого игрока", callback_data=f"crosshair_{player}")]
    ]
    
    if has_config:
        buttons.append([InlineKeyboardButton(text="📥 Скачать полный конфиг", callback_data=f"download_full_config_{player}")])
    else:
        buttons.append([InlineKeyboardButton(text="⏳ Конфиг в разработке", callback_data="noop")])

    buttons.append([InlineKeyboardButton(text="← Назад", callback_data="settings_pro_configs")])

    await safe_edit_or_send(
        callback, bot, text,
        InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("download_full_config_"))
async def download_full_config(callback: types.CallbackQuery, bot: Bot):
    player = callback.data.replace("download_full_config_", "")
    config_path = os.path.join(MEDIA_DIR, "configs", f"{player}_full.cfg")
    data = PRO_CONFIGS.get(player)

    if os.path.exists(config_path) and data:
        caption_text = (
            f"🎮 <b>{data['name']}</b>\n\n"
            "📁 Поместите в:\n"
            "<code>Steam\\steamapps\\common\\Counter-Strike Global Offensive\\game\\csgo\\cfg</code>\n\n"
            "🚀 В консоли: <code>exec " + player + "_full</code>"
        )
        await callback.message.answer_document(
            FSInputFile(config_path),
            caption=caption_text,
            parse_mode="HTML"
        )

@router.callback_query(F.data == "settings_launch")
async def settings_launch(callback: types.CallbackQuery, bot: Bot):
    text = """<b>🚀 Параметры запуска CS2</b>

<code>-novid</code> — Пропускает intro видео
<code>-high</code> — Высокий приоритет процесса  
<code>-threads 8</code> — Количество потоков (под ваш CPU)
<code>+fps_max 0</code> — Снятие ограничения FPS
<code>-nojoy</code> — Отключение джойстика
<code>-freq 144</code> — Частота монитора (144/240/360)
<code>-tickrate 128</code> — Тикрейт для оффлайн серверов

<b>💡 Пример для слабого ПК:</b>
<code>-novid -high -threads 4 +fps_max 60 -nojoy</code>

<b>💡 Пример для киберспорта:</b>
<code>-novid -high -threads 8 +fps_max 0 -nojoy -freq 144</code>"""

    await safe_edit_or_send(callback, bot, text, settings_menu(), parse_mode="HTML")

@router.callback_query(F.data == "settings_fps")
async def settings_fps(callback: types.CallbackQuery, bot: Bot):
    text = (
        "💻 <b>Оптимизация под ваш ПК</b>\n"
        "Выберите уровень производительности:"
    )
    try:
        await callback.message.edit_text(text, reply_markup=fps_tier_menu(), parse_mode="HTML")
    except Exception as e:
        error_msg = str(e).lower()
        if "message is not modified" in error_msg:
            await callback.answer("✅ Меню загружено", show_alert=False)
        else:
            try:
                await callback.message.delete()
            except:
                pass
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text=text,
                reply_markup=fps_tier_menu(),
                parse_mode="HTML"
            )

@router.callback_query(F.data.startswith("tier_"))
async def show_tier(callback: types.CallbackQuery, bot: Bot):
    tier = callback.data.replace("tier_", "")
    data = FPS_TIERS.get(tier)

    if not data:
        await callback.answer("Ошибка!", show_alert=True)
        return

    text = f"""<b>{data['name']}</b>

<b>🎮 Настройки:</b>
{data['settings']}

<b>⌨️ Консольные команды:</b>
<pre>{data['commands']}</pre>"""

    await safe_edit_or_send(callback, bot, text, console_tier_menu(tier), parse_mode="HTML")

@router.callback_query(F.data.startswith("download_tier_"))
async def download_tier(callback: types.CallbackQuery, bot: Bot):
    tier = callback.data.replace("download_tier_", "")
    data = FPS_TIERS[tier]

    filename = f"autoexec_{tier}.cfg"
    filepath = os.path.join(MEDIA_DIR, "configs", filename)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'w') as f:
        f.write(data['commands'])
    
    caption_text = (
    f"🎮 <b>{data['name']}</b>\n\n"
    "📁 Поместите файл в:\n"
    r"<code>Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\cfg</code>\n\n" 
    "🚀 Как использовать:\n"
    "1️⃣ Способ (через консоль):\n"
    "Запустите CS2, откройте консоль (клавиша Ё)\n"
    f"Введите: <code>exec autoexec_{tier}</code>\n\n"
    "2️⃣ Способ (автозагрузка):\n"
    "Steam → Библиотека → ПКМ по CS2 → Свойства\n"
    "В «Параметры запуска» добавьте:\n"
    f"<code>+exec autoexec_{tier}</code>"
)

    await callback.message.answer_document(
        FSInputFile(filepath),
        caption=caption_text,
        parse_mode="HTML"
    )