from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# ============ ГЛАВНОЕ МЕНЮ (Reply Keyboard) ============
def main_menu_reply():
    """Главное меню с Reply клавиатурой - 4 ряда по 2 кнопки"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗺️ Раскидки"), KeyboardButton(text="⚙️ Настройки")],
            [KeyboardButton(text="📊 Мета"), KeyboardButton(text="🎯 Тренировки")],
            [KeyboardButton(text="📚 Словарь"), KeyboardButton(text="🎮 Тактика")],
            [KeyboardButton(text="⭐ Избранное"), KeyboardButton(text="🔍 Поиск")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите раздел...",
        one_time_keyboard=False  
    )
def admin_menu():
    """Админ меню"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить гранату", callback_data="admin_add_nade"),
         InlineKeyboardButton(text="📋 Список гранат", callback_data="admin_list_nades")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")]
    ])

def maps_menu():
    """Меню карт"""
    maps = [("Mirage", "map_mirage"), ("Inferno", "map_inferno"), ("Nuke", "map_nuke"),
            ("Ancient", "map_ancient"), ("Anubis", "map_anubis"), ("Vertigo", "map_vertigo"),
            ("Overpass", "map_overpass"), ("Dust2", "map_dust2")]
    buttons = []
    for i in range(0, len(maps), 2):
        row = [InlineKeyboardButton(text=name, callback_data=cb) for name, cb in maps[i:i+2]]
        buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def side_menu(map_name: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔴 T сторона", callback_data=f"side_{map_name}_t"),
         InlineKeyboardButton(text="🔵 CT сторона", callback_data=f"side_{map_name}_ct")],
        [InlineKeyboardButton(text="← Назад", callback_data="menu_nades")]
    ])

def nade_types_menu(map_name: str, side: str):
    types = [("💨 Смоки", f"type_{map_name}_{side}_smoke"), ("⚡ Флешки", f"type_{map_name}_{side}_flash"),
             ("🔥 Молотовы", f"type_{map_name}_{side}_molotov"), ("💣 HE", f"type_{map_name}_{side}_he")]
    buttons = []
    for i in range(0, len(types), 2):
        row = [InlineKeyboardButton(text=name, callback_data=cb) for name, cb in types[i:i+2]]
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="← Назад", callback_data=f"map_{map_name}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def nades_list_menu(nades: list, map_name: str, nade_type: str, side: str):
    buttons = []
    for nade in nades:
        diff_emoji = {1: "🟢", 2: "🟡", 3: "🔴"}.get(nade['difficulty'], "⚪")
        buttons.append([InlineKeyboardButton(text=f"{diff_emoji} {nade['name']}", callback_data=f"nade_{nade['id']}")])
    buttons.append([InlineKeyboardButton(text="← Назад", callback_data=f"back_type_{map_name}_{side}_{nade_type}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def nade_detail_menu(nade_id: int, is_fav: bool):
    fav_text = "❌ Убрать" if is_fav else "⭐ В избранное"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=fav_text, callback_data=f"fav_{nade_id}"),
         InlineKeyboardButton(text="← Назад", callback_data=f"back_nade_{nade_id}")]
    ])

# ============ НАСТРОЙКИ ============
def settings_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Параметры запуска", callback_data="settings_launch"),
         InlineKeyboardButton(text="💻 Оптимизация ПК", callback_data="settings_fps")],
        [InlineKeyboardButton(text="🎯 Прицелы про игроков", callback_data="settings_crosshairs"),
         InlineKeyboardButton(text="⌨️ Бинды про игроков", callback_data="settings_binds")],
        [InlineKeyboardButton(text="📥 Конфиги про игроков", callback_data="settings_pro_configs")]
    ])

def fps_tier_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🖥️ Слабый ПК", callback_data="tier_low"),
         InlineKeyboardButton(text="💻 Средний ПК", callback_data="tier_mid")],
        [InlineKeyboardButton(text="🖥️ Киберспорт", callback_data="tier_high"),
         InlineKeyboardButton(text="← Назад", callback_data="back_to_settings")]  # Исправлено
    ])

def console_tier_menu(tier: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📥 Скачать autoexec.cfg", callback_data=f"download_tier_{tier}")],
        [InlineKeyboardButton(text="← Назад", callback_data="settings_fps")]
    ])

# ============ ПРО ИГРОКИ ============
def crosshairs_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="s1mple", callback_data="crosshair_simple"),
         InlineKeyboardButton(text="ZywOo", callback_data="crosshair_zywoo")],
        [InlineKeyboardButton(text="NiKo", callback_data="crosshair_niko"),
         InlineKeyboardButton(text="m0NESY", callback_data="crosshair_monesy")],
        [InlineKeyboardButton(text="donk", callback_data="crosshair_donk"),
         InlineKeyboardButton(text="sh1ro", callback_data="crosshair_shiro")],
        [InlineKeyboardButton(text="f0rest", callback_data="crosshair_forest"),
         InlineKeyboardButton(text="olofmeister", callback_data="crosshair_olof")],
        [InlineKeyboardButton(text="← Назад", callback_data="back_to_settings")]
    ])

def pro_configs_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="s1mple", callback_data="config_pro_simple"),
         InlineKeyboardButton(text="ZywOo", callback_data="config_pro_zywoo")],
        [InlineKeyboardButton(text="NiKo", callback_data="config_pro_niko"),
         InlineKeyboardButton(text="m0NESY", callback_data="config_pro_monesy")],
        [InlineKeyboardButton(text="ropz", callback_data="config_pro_ropz"),
         InlineKeyboardButton(text="b1t", callback_data="config_pro_bit")],
        [InlineKeyboardButton(text="← Назад", callback_data="back_to_settings")]
    ])

def pro_binds_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="s1mple", callback_data="binds_simple"),
         InlineKeyboardButton(text="ZywOo", callback_data="binds_zywoo")],
        [InlineKeyboardButton(text="NiKo", callback_data="binds_niko"),
         InlineKeyboardButton(text="ropz", callback_data="binds_ropz")],
        [InlineKeyboardButton(text="← Назад", callback_data="back_to_settings")]
    ])

def crosshair_detail_menu(player: str, has_image: bool):
    """Меню детального просмотра прицела"""
    buttons = []
    if has_image:
        buttons.append([InlineKeyboardButton(text="📥 Скачать прицел", callback_data=f"download_crosshair_{player}")])
    buttons.append([InlineKeyboardButton(text="📋 Код прицела", callback_data=f"code_crosshair_{player}")])
    buttons.append([InlineKeyboardButton(text="⌨️ Консоль", callback_data=f"console_crosshair_{player}")])
    buttons.append([InlineKeyboardButton(text="← Назад", callback_data="settings_crosshairs")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# ============ ТАКТИКИ ============
def tactics_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Коллы на раунд", callback_data="tactics_calls")]
    ])

def tactics_maps_menu():
    maps = ["mirage", "inferno", "nuke", "ancient", "anubis"]
    buttons = []
    for i in range(0, len(maps), 2):
        row = [InlineKeyboardButton(text=m.title(), callback_data=f"tactic_map_{m}") for m in maps[i:i+2]]
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="← Назад", callback_data="back_to_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# ============ МЕТА ============
def meta_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔫 Тир-лист оружия", callback_data="meta_weapons"),
         InlineKeyboardButton(text="📈 Статистика оружия", callback_data="meta_weapon_stats")],
        [InlineKeyboardButton(text="💰 Экономика", callback_data="meta_economy"),
         InlineKeyboardButton(text="🗺️ Пул карт", callback_data="meta_maps")],
        [InlineKeyboardButton(text="← Назад", callback_data="back_to_main")]  
    ])


# ============ ТРЕНИРОВКИ ============
def training_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 Контроль спрея", callback_data="training_spray")],
        [InlineKeyboardButton(text="🗺️ Карты тренировок", callback_data="training_maps")],
        [InlineKeyboardButton(text="← Назад", callback_data="back_to_main")]  
    ])

def spray_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="AK-47", callback_data="spray_ak47"),
         InlineKeyboardButton(text="M4A4", callback_data="spray_m4a4")],
        [InlineKeyboardButton(text="M4A1-S", callback_data="spray_m4a1s"),
         InlineKeyboardButton(text="← Назад", callback_data="back_to_training")]
    ])

def training_maps_menu():
    """Меню карт для тренировок с ссылками"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 Aim Botz", url="https://steamcommunity.com/sharedfiles/filedetails/?id=243702660")],
        [InlineKeyboardButton(text="🔫 Fast Aim/Reflex", url="https://steamcommunity.com/sharedfiles/filedetails/?id=647772286")],
        [InlineKeyboardButton(text="💨 Yprac Hub", url="https://steamcommunity.com/sharedfiles/filedetails/?id=3070715607")],
        [InlineKeyboardButton(text="🏃 Refrag Prefire", url="https://refrag.gg")],
        [InlineKeyboardButton(text="← Назад", callback_data="back_to_training")]
    ])

# ============ ПОИСК ============
def search_results_menu(results: list, page: int = 0, query: str = ""):
    buttons = []
    start, end = page * 5, (page + 1) * 5
    for nade in results[start:end]:
        buttons.append([InlineKeyboardButton(text=f"🗺️ {nade['map_name'].title()}: {nade['name']}", callback_data=f"nade_{nade['id']}")])
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="⬅️", callback_data=f"search_page_{page-1}_{query}"))
    if end < len(results):
        nav.append(InlineKeyboardButton(text="➡️", callback_data=f"search_page_{page+1}_{query}"))
    if nav:
        buttons.append(nav)
    return InlineKeyboardMarkup(inline_keyboard=buttons)