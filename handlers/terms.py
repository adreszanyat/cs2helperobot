from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import random

from database import db

router = Router()

class TermStates(StatesGroup):
    waiting_term = State()

@router.callback_query(F.data == "menu_terms")
async def menu_terms(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "📚 <b>Словарь терминов CS2</b>\n\n"
        "Введите термин для поиска:\n"
        "<i>Например: пик, холд, кемп, эко, клатч</i>",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="🎲 Случайный термин", callback_data="term_random")]
        ]),
        parse_mode="HTML"
    )
    await state.set_state(TermStates.waiting_term)


# Also handle text menu button
@router.message(F.text == "📚 Словарь")
async def text_menu_terms(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "📚 <b>Словарь терминов CS2</b>\n\n"
        "Введите термин для поиска:\n"
        "<i>Например: пик, холд, кемп, эко, клатч</i>",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="🎲 Случайный термин", callback_data="term_random")]
        ]),
        parse_mode="HTML"
    )
    await state.set_state(TermStates.waiting_term)
@router.callback_query(F.data == "term_random")
async def random_term(callback: types.CallbackQuery, state: FSMContext):
    """Выбирает случайный термин из базы"""
    import sqlite3
    from config import DB_PATH

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM terms ORDER BY RANDOM() LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row:
        term = dict(row)
        text = f"""
<b>📖 {term['term'].upper()}</b>
<i>{term['category'] or 'Общий термин'}</i>

<b>Значение:</b>
{term['definition']}

<b>Пример:</b>
<i>{term['example'] or '—'}</i>
"""
    else:
        text = "😕 В словаре пока нет терминов."

    await callback.message.edit_text(
        text,
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="🎲 Еще раз", callback_data="term_random")]
        ]),
        parse_mode="HTML"
    )
    await state.clear()

@router.message(TermStates.waiting_term)
async def process_term(message: types.Message, state: FSMContext):
    term = message.text.lower().strip()
    result = db.get_term(term)

    await state.clear()

    if result:
        text = f"""<b>📖 {result['term'].upper()}</b>
<i>{result['category'] or 'Общий термин'}</i>

<b>Значение:</b>
{result['definition']}

<b>Пример:</b>
<i>{result['example'] or '—'}</i>"""
    
        kb = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="🎲 Случайный термин", callback_data="term_random")],
            [types.InlineKeyboardButton(text="🔍 Новый поиск", callback_data="menu_terms")]
        ])
    else:
        similar = db.search_terms(term)
        if similar:
            text = f"😕 '<b>{term}</b>' не найден.\n\n<b>Похожие:</b>\n" + "\n".join([f"• {s['term']}" for s in similar[:5]])
        else:
            text = f"😕 '<b>{term}</b>' не найден в словаре."
        
        kb = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="🎲 Случайный термин", callback_data="term_random")],
            [types.InlineKeyboardButton(text="🔍 Попробовать снова", callback_data="menu_terms")]
        ])

    await message.answer(text, reply_markup=kb, parse_mode="HTML")