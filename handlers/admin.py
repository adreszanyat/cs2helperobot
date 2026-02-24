import os
from aiogram import Router, F, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import MEDIA_DIR, ADMIN_IDS
from database import db
from keyboards import admin_menu 

router = Router()

class AddNadeStates(StatesGroup):
    map_name = State()
    nade_type = State()
    name = State()
    side = State()
    difficulty = State()
    position_desc = State()
    aim_desc = State()
    throw_desc = State()
    result_desc = State()
    confirm = State()

class UploadStates(StatesGroup):
    waiting_position_img = State()
    waiting_aim_img = State()
    waiting_result_img = State()
    waiting_video = State()

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

# ============ ГЛАВНОЕ МЕНЮ АДМИНА ============

@router.message(Command("admin"))
async def cmd_admin(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет доступа к админ-панели!")
        return
    
    await message.answer(
        "🔧 <b>Админ-панель CS2 Helper</b>\n\n"
        "Выберите действие:",
        reply_markup=admin_menu(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "admin_panel")
async def admin_panel(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа!", show_alert=True)
        return
    
    await callback.message.edit_text(
        "🔧 <b>Админ-панель</b>",
        reply_markup=admin_menu(),
        parse_mode="HTML"
    )

# ============ ДОБАВЛЕНИЕ ГРАНАТЫ (Текст) ============

@router.callback_query(F.data == "admin_add_nade")
async def start_add_nade(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа!", show_alert=True)
        return
    
    await state.set_state(AddNadeStates.map_name)
    
    maps_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=m.title(), callback_data=f"add_map_{m}")]
        for m in ["mirage", "inferno", "nuke", "ancient", "anubis", "vertigo"]
    ] + [[InlineKeyboardButton(text="← Отмена", callback_data="admin_panel")]])
    
    await callback.message.edit_text(
        "➕ <b>Добавление гранаты</b>\n\n"
        "Шаг 1/8: Выберите карту",
        reply_markup=maps_kb,
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("add_map_"))
async def process_map(callback: types.CallbackQuery, state: FSMContext):
    map_name = callback.data.replace("add_map_", "")
    await state.update_data(map_name=map_name)
    await state.set_state(AddNadeStates.nade_type)
    
    types_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💨 Смок", callback_data="add_type_smoke")],
        [InlineKeyboardButton(text="⚡ Флеш", callback_data="add_type_flash")],
        [InlineKeyboardButton(text="🔥 Молотов", callback_data="add_type_molotov")],
        [InlineKeyboardButton(text="💣 HE", callback_data="add_type_he")]
    ])
    
    await callback.message.edit_text(
        f"🗺️ Карта: <b>{map_name.title()}</b>\n\n"
        f"Шаг 2/8: Выберите тип гранаты",
        reply_markup=types_kb,
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("add_type_"))
async def process_type(callback: types.CallbackQuery, state: FSMContext):
    nade_type = callback.data.replace("add_type_", "")
    await state.update_data(nade_type=nade_type)
    await state.set_state(AddNadeStates.name)
    
    await callback.message.edit_text(
        "Шаг 3/8: Введите название гранаты\n\n"
        "<i>Например: Window Smoke (T Spawn)</i>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="← Отмена", callback_data="admin_panel")]
        ]),
        parse_mode="HTML"
    )

@router.message(AddNadeStates.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddNadeStates.side)
    
    side_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔴 T сторона", callback_data="add_side_t")],
        [InlineKeyboardButton(text="🔵 CT сторона", callback_data="add_side_ct")],
    ])
    
    await message.answer(
        "Шаг 4/8: Выберите сторону",
        reply_markup=side_kb,
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("add_side_"))
async def process_side(callback: types.CallbackQuery, state: FSMContext):
    side = callback.data.replace("add_side_", "")
    await state.update_data(side=side)
    await state.set_state(AddNadeStates.difficulty)
    
    diff_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 Легко", callback_data="add_diff_1")],
        [InlineKeyboardButton(text="🟡 Средне", callback_data="add_diff_2")],
        [InlineKeyboardButton(text="🔴 Сложно", callback_data="add_diff_3")]
    ])
    
    await callback.message.edit_text(
        "Шаг 5/8: Выберите сложность",
        reply_markup=diff_kb,
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("add_diff_"))
async def process_difficulty(callback: types.CallbackQuery, state: FSMContext):
    difficulty = int(callback.data.replace("add_diff_", ""))
    await state.update_data(difficulty=difficulty)
    await state.set_state(AddNadeStates.position_desc)
    
    await callback.message.edit_text(
        "Шаг 6/8: Опишите позицию (где стоять)\n\n"
        "<i>Например: Упритесь в угол у выхода с T Spawn</i>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="← Отмена", callback_data="admin_panel")]
        ]),
        parse_mode="HTML"
    )

@router.message(AddNadeStates.position_desc)
async def process_position(message: types.Message, state: FSMContext):
    await state.update_data(position_desc=message.text)
    await state.set_state(AddNadeStates.aim_desc)
    
    await message.answer(
        "Шаг 7/8: Опишите куда целиться\n\n"
        "<i>Например: На пересечение белой линии и темного пятна</i>",
        parse_mode="HTML"
    )

@router.message(AddNadeStates.aim_desc)
async def process_aim(message: types.Message, state: FSMContext):
    await state.update_data(aim_desc=message.text)
    await state.set_state(AddNadeStates.throw_desc)
    
    throw_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ЛКМ", callback_data="throw_left")],
        [InlineKeyboardButton(text="ПКМ", callback_data="throw_right")],
        [InlineKeyboardButton(text="ЛКМ+ПКМ", callback_data="throw_both")],
        [InlineKeyboardButton(text="Jump Throw", callback_data="throw_jump")],
        [InlineKeyboardButton(text="Run Throw", callback_data="throw_run")]
    ])
    
    await message.answer(
        "Выберите тип броска:",
        reply_markup=throw_kb,
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("throw_"))
async def process_throw_type(callback: types.CallbackQuery, state: FSMContext):
    throw_map = {
        "throw_left": "ЛКМ (Left Click)",
        "throw_right": "ПКМ (Right Click)",
        "throw_both": "ЛКМ + ПКМ",
        "throw_jump": "Jump Throw",
        "throw_run": "Run Throw"
    }
    throw_desc = throw_map[callback.data]
    await state.update_data(throw_desc=throw_desc)
    await state.set_state(AddNadeStates.result_desc)
    
    await callback.message.edit_text(
        "Шаг 8/8: Опишите результат (куда упадет граната)\n\n"
        "<i>Например: Глубокий смок в Window, блокирует полностью</i>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="← Отмена", callback_data="admin_panel")]
        ]),
        parse_mode="HTML"
    )

@router.message(AddNadeStates.result_desc)
async def process_result(message: types.Message, state: FSMContext):
    await state.update_data(result_desc=message.text)
    data = await state.get_data()
    
    # Сохраняем в БД
    nade_id = db.add_nade({
        'map_name': data['map_name'],
        'nade_type': data['nade_type'],
        'name': data['name'],
        'side': data['side'],
        'difficulty': data['difficulty'],
        'position_desc': data['position_desc'],
        'aim_desc': data['aim_desc'],
        'throw_desc': data['throw_desc'],
        'result_desc': message.text,
        'position_img': None,
        'aim_img': None,
        'result_img': None,
        'result_video': None,
        'tags': []
    })
    
    await state.clear()
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📸 Добавить изображения", callback_data=f"upload_{nade_id}")],
        [InlineKeyboardButton(text="✅ Готово", callback_data="admin_panel")]
    ])
    
    await message.answer(
        f"✅ <b>Граната добавлена!</b>\n\n"
        f"ID: <code>{nade_id}</code>\n"
        f"Название: {data['name']}\n\n"
        f"Хотите добавить изображения?",
        reply_markup=kb,
        parse_mode="HTML"
    )

# ============ ЗАГРУЗКА ИЗОБРАЖЕНИЙ ============

@router.callback_query(F.data.startswith("upload_"))
async def start_upload(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа!", show_alert=True)
        return
    
    nade_id = int(callback.data.replace("upload_", ""))
    await state.update_data(nade_id=nade_id)
    await state.set_state(UploadStates.waiting_position_img)
    
    await callback.message.edit_text(
        "📸 <b>Загрузка изображений</b>\n\n"
        "Шаг 1/4: Отправьте фото позиции (где стоять)\n\n"
        "<i>Или нажмите /skip чтобы пропустить</i>",
        parse_mode="HTML"
    )

@router.message(UploadStates.waiting_position_img, F.photo)
async def process_position_img(message: types.Message, state: FSMContext, bot: Bot):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    
    data = await state.get_data()
    nade_id = data['nade_id']
    
    filename = f"nade_{nade_id}_position.jpg"
    filepath = os.path.join(MEDIA_DIR, "nades", filename)
    await bot.download_file(file.file_path, filepath)
    
    db.update_nade(nade_id, {'position_img': filepath})
    
    await state.set_state(UploadStates.waiting_aim_img)
    await message.answer(
        "✅ Позиция сохранена!\n\n"
        "Шаг 2/4: Отправьте фото прицела (куда целиться)\n\n"
        "<i>Или /skip</i>",
        parse_mode="HTML"
    )

@router.message(UploadStates.waiting_aim_img, F.photo)
async def process_aim_img(message: types.Message, state: FSMContext, bot: Bot):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    
    data = await state.get_data()
    nade_id = data['nade_id']
    
    filename = f"nade_{nade_id}_aim.jpg"
    filepath = os.path.join(MEDIA_DIR, "nades", filename)
    await bot.download_file(file.file_path, filepath)
    
    db.update_nade(nade_id, {'aim_img': filepath})
    
    await state.set_state(UploadStates.waiting_result_img)
    await message.answer(
        "✅ Прицел сохранен!\n\n"
        "Шаг 3/4: Отправьте фото результата (куда упала граната)\n\n"
        "<i>Или /skip</i>",
        parse_mode="HTML"
    )

@router.message(UploadStates.waiting_result_img, F.photo)
async def process_result_img(message: types.Message, state: FSMContext, bot: Bot):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    
    data = await state.get_data()
    nade_id = data['nade_id']
    
    filename = f"nade_{nade_id}_result.jpg"
    filepath = os.path.join(MEDIA_DIR, "nades", filename)
    await bot.download_file(file.file_path, filepath)
    
    db.update_nade(nade_id, {'result_img': filepath})
    
    await state.set_state(UploadStates.waiting_video)
    await message.answer(
        "✅ Результат сохранен!\n\n"
        "Шаг 4/4 (опционально): Отправьте видео броска\n\n"
        "<i>Или /skip чтобы завершить</i>",
        parse_mode="HTML"
    )

@router.message(UploadStates.waiting_video, F.video)
async def process_video(message: types.Message, state: FSMContext, bot: Bot):
    video = message.video
    file = await bot.get_file(video.file_id)
    
    data = await state.get_data()
    nade_id = data['nade_id']
    
    filename = f"nade_{nade_id}_video.mp4"
    filepath = os.path.join(MEDIA_DIR, "nades", filename)
    await bot.download_file(file.file_path, filepath)
    
    db.update_nade(nade_id, {'result_video': filepath})
    
    await state.clear()
    await message.answer(
        "✅ <b>Граната полностью добавлена со всеми медиа!</b>",
        reply_markup=admin_menu(),
        parse_mode="HTML"
    )

@router.message(Command("skip"), UploadStates.waiting_position_img)
@router.message(Command("skip"), UploadStates.waiting_aim_img)
@router.message(Command("skip"), UploadStates.waiting_result_img)
@router.message(Command("skip"), UploadStates.waiting_video)
async def skip_upload(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    
    if current_state == UploadStates.waiting_position_img:
        await state.set_state(UploadStates.waiting_aim_img)
        await message.answer(
            "⏭ Пропущено.\n\n"
            "Шаг 2/4: Отправьте фото прицела\n\n"
            "<i>Или /skip</i>",
            parse_mode="HTML"
        )
    elif current_state == UploadStates.waiting_aim_img:
        await state.set_state(UploadStates.waiting_result_img)
        await message.answer(
            "⏭ Пропущено.\n\n"
            "Шаг 3/4: Отправьте фото результата\n\n"
            "<i>Или /skip</i>",
            parse_mode="HTML"
        )
    elif current_state == UploadStates.waiting_result_img:
        await state.set_state(UploadStates.waiting_video)
        await message.answer(
            "⏭ Пропущено.\n\n"
            "Шаг 4/4: Отправьте видео\n\n"
            "<i>Или /finish чтобы завершить</i>",
            parse_mode="HTML"
        )
    elif current_state == UploadStates.waiting_video:
        await state.clear()
        await message.answer(
            "✅ <b>Готово!</b> Граната добавлена.",
            reply_markup=admin_menu(),
            parse_mode="HTML"
        )

@router.message(Command("finish"), UploadStates.waiting_video)
async def finish_upload(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "✅ <b>Загрузка завершена!</b>",
        reply_markup=admin_menu(),
        parse_mode="HTML"
    )

# ============ УПРАВЛЕНИЕ ГРАНАТАМИ ============

@router.callback_query(F.data == "admin_list_nades")
async def list_nades(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа!", show_alert=True)
        return
    
    await callback.message.edit_text(
        "📋 <b>Список гранат</b>\n\n"
        "Функция в разработке...\n"
        "Используйте поиск для нахождения гранат.",
        reply_markup=admin_menu(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "admin_stats")
async def show_stats(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа!", show_alert=True)
        return
    
    await callback.message.edit_text(
        "📊 <b>Статистика бота</b>\n\n"
        "В разработке...",
        reply_markup=admin_menu(),
        parse_mode="HTML"
    )