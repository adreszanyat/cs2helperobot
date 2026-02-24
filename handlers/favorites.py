from aiogram import Router, F, types

from database import db

router = Router()

@router.callback_query(F.data == "menu_favorites")
async def show_favorites(callback: types.CallbackQuery):
    favorites = db.get_favorites(callback.from_user.id)

    if not favorites:
        await callback.answer("У вас пока нет избранных гранат!", show_alert=True)
        return

    buttons = []
    for nade in favorites:
        buttons.append([types.InlineKeyboardButton(
            text=f"🗺️ {nade['map_name'].title()}: {nade['name']}",
            callback_data=f"nade_{nade['id']}"
        )])

    await callback.message.edit_text(
        f"⭐ <b>Ваши избранные гранаты</b> ({len(favorites)}):",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("fav_"))
async def toggle_favorite(callback: types.CallbackQuery):
    nade_id = int(callback.data.replace("fav_", ""))
    user_id = callback.from_user.id

    if db.is_favorite(user_id, nade_id):
        db.remove_favorite(user_id, nade_id)
        await callback.answer("❌ Удалено из избранного")
    else:
        if db.add_favorite(user_id, nade_id):
            await callback.answer("⭐ Добавлено в избранное!")
        else:
            await callback.answer("Уже в избранном!")