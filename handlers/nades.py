from aiogram import Router, F, types, Bot
from aiogram.types import FSInputFile, InputMediaPhoto
import os

from database import db
from keyboards import maps_menu, side_menu, nade_types_menu, nades_list_menu, nade_detail_menu

router = Router()

def format_nade_text(nade: dict) -> str:
    diff_map = {1: "🟢 Легко", 2: "🟡 Средне", 3: "🔴 Сложно"}
    side_map = {"t": "🔴 T сторона", "ct": "🔵 CT сторона", "both": "⚪ Обе стороны"}
    
    type_emoji = {"smoke": "💨", "flash": "⚡", "molotov": "🔥", "he": "💣"}

    text = f"""
<b>{type_emoji.get(nade['nade_type'], '💨')} {nade['name']}</b>
{diff_map.get(nade['difficulty'], '❓')} | {side_map.get(nade['side'], '❓')} | <i>{nade['map_name'].title()}</i>

📍 <b>Позиция:</b>
{nade['position_desc']}

🎯 <b>Прицел:</b> 
{nade['aim_desc']}

👋 <b>Бросок:</b> <code>{nade['throw_desc']}</code>

✅ <b>Результат:</b>
{nade['result_desc']}
"""
    return text

@router.callback_query(F.data == "menu_nades")
async def menu_nades(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🗺️ <b>Раскидки гранат</b>\n\n"
        "Выберите карту для просмотра позиций:",
        reply_markup=maps_menu(),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("map_"))
async def select_map(callback: types.CallbackQuery):
    map_name = callback.data.replace("map_", "")
    await callback.message.edit_text(
        f"🗺️ <b>{map_name.title()}</b>\n\n"
        f"Выберите сторону:",
        reply_markup=side_menu(map_name),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("side_"))
async def select_side(callback: types.CallbackQuery):
    parts = callback.data.replace("side_", "").split("_")
    map_name, side = parts[0], parts[1]
    side_name = "🔴 Terrorist" if side == "t" else "🔵 Counter-Terrorist"

    await callback.message.edit_text(
        f"🗺️ <b>{map_name.title()}</b>\n"
        f"{side_name}\n\n"
        f"Выберите тип гранаты:",
        reply_markup=nade_types_menu(map_name, side),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("type_"))
async def select_nade_type(callback: types.CallbackQuery):
    parts = callback.data.replace("type_", "").split("_")
    map_name, side, nade_type = parts[0], parts[1], parts[2]

    nades = db.get_nades(map_name, nade_type, side)
    if not nades:
        await callback.answer("Пока нет гранат для этой стороны!", show_alert=True)
        return

    type_names = {"smoke": "💨 Смоки", "flash": "⚡ Флешки", "molotov": "🔥 Молотовы", "he": "💣 HE"}
    side_name = "🔴 T" if side == "t" else "🔵 CT"

    await callback.message.edit_text(
        f"🗺️ <b>{map_name.title()}</b> — {side_name}\n"
        f"{type_names.get(nade_type)}\n"
        f"Найдено: <b>{len(nades)}</b>\n\n"
        f"🟢 Легко | 🟡 Средне | 🔴 Сложно",
        reply_markup=nades_list_menu(nades, map_name, nade_type, side),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("nade_"))
async def show_nade(callback: types.CallbackQuery, bot: Bot):
    nade_id = int(callback.data.replace("nade_", ""))
    nade = db.get_nade_by_id(nade_id)

    if not nade:
        await callback.answer("Граната не найдена!", show_alert=True)
        return

    is_fav = db.is_favorite(callback.from_user.id, nade_id)
    text = format_nade_text(nade)

    media_files = []
    if nade.get('position_img') and os.path.exists(nade['position_img']):
        media_files.append(FSInputFile(nade['position_img']))
    if nade.get('aim_img') and os.path.exists(nade['aim_img']):
        media_files.append(FSInputFile(nade['aim_img']))
    if nade.get('result_img') and os.path.exists(nade['result_img']):
        media_files.append(FSInputFile(nade['result_img']))

    try:
        if media_files:
            await callback.message.delete()
            
            if len(media_files) > 1:
                await bot.send_media_group(
                    chat_id=callback.message.chat.id,
                    media=[InputMediaPhoto(media=f) for f in media_files]
                )
            else:
                await bot.send_photo(chat_id=callback.message.chat.id, photo=media_files[0])
                
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text=text,
                reply_markup=nade_detail_menu(nade_id, is_fav),
                parse_mode="HTML"
            )
        else:
            await callback.message.edit_text(
                text + "\n\n<i>📸 Изображения пока не добавлены</i>",
                reply_markup=nade_detail_menu(nade_id, is_fav),
                parse_mode="HTML"
            )
    except Exception as e:
        print(f"Ошибка при отправке изображений: {e}")
        await callback.message.answer(
            "❌ Ошибка при отправке изображений. Попробуйте позже.",
            reply_markup=nade_detail_menu(nade_id, is_fav)
        )

@router.callback_query(F.data.startswith("back_type_"))
async def back_to_type(callback: types.CallbackQuery):
    parts = callback.data.replace("back_type_", "").split("_")
    map_name, side, nade_type = parts[0], parts[1], parts[2]

    nades = db.get_nades(map_name, nade_type, side)
    type_names = {"smoke": "💨 Смоки", "flash": "⚡ Флешки", "molotov": "🔥 Молотовы", "he": "💣 HE"}
    side_name = "🔴 T" if side == "t" else "🔵 CT"

    text = (
        f"🗺️ <b>{map_name.title()}</b> — {side_name}\n"
        f"{type_names.get(nade_type)}\n"
        f"Найдено: <b>{len(nades)}</b>\n\n"
        f"🟢 Легко | 🟡 Средне | 🔴 Сложно"
    )
    
    current_text = callback.message.text or callback.message.caption or ""
    
    if current_text == text:
        await callback.answer("✅ Список гранат", show_alert=False)
        return
        
    try:
        await callback.message.edit_text(
            text,
            reply_markup=nades_list_menu(nades, map_name, nade_type, side),
            parse_mode="HTML"
        )
    except Exception as e:
        if "message is not modified" in str(e).lower():
            await callback.answer("✅ Список гранат", show_alert=False)
        else:
            raise

@router.callback_query(F.data.startswith("back_nade_"))
async def back_to_nade_list(callback: types.CallbackQuery):
    nade_id = int(callback.data.replace("back_nade_", ""))
    nade = db.get_nade_by_id(nade_id)

    if nade:
        map_name = nade['map_name']
        side = nade.get('side', 'both')
        nade_type = nade['nade_type']

        nades = db.get_nades(map_name, nade_type, side)
        type_names = {"smoke": "💨 Смоки", "flash": "⚡ Флешки", "molotov": "🔥 Молотовы", "he": "💣 HE"}
        side_name = "🔴 T" if side == "t" else "🔵 CT"

        text = (
            f"🗺️ <b>{map_name.title()}</b> — {side_name}\n"
            f"{type_names.get(nade_type)}\n"
            f"Найдено: <b>{len(nades)}</b>\n\n"
            f"🟢 Легко | 🟡 Средне | 🔴 Сложно"
        )
        
        try:
            await callback.message.edit_text(
                text,
                reply_markup=nades_list_menu(nades, map_name, nade_type, side),
                parse_mode="HTML"
            )
        except Exception as e:
            if "message is not modified" in str(e).lower():
                await callback.answer("✅ Список гранат", show_alert=False)
            else:
                raise
    else:
        await menu_nades(callback)

