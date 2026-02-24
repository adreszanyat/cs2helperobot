from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import db
from keyboards import search_results_menu 

router = Router()

class SearchStates(StatesGroup):
    waiting_query = State()

# Словарь переводов для поиска
TRANSLATIONS = {
    # Карты
    "мираж": "mirage", "mirage": "mirage",
    "инферно": "inferno", "inferno": "inferno",
    "ньюк": "nuke", "nuke": "nuke",
    "эншент": "ancient", "ancient": "ancient",
    "анубис": "anubis", "anubis": "anubis",
    "вертиго": "vertigo", "vertigo": "vertigo",
    "оверпасс": "overpass", "overpass": "overpass",
    "даст": "dust2", "dust2": "dust2", "дуст": "dust2",

    # Типы гранат
    "смок": "smoke", "дым": "smoke", "smoke": "smoke",
    "флеш": "flash", "вспышка": "flash", "flash": "flash",
    "молотов": "molotov", "огонь": "molotov", "molotov": "molotov",
    "хе": "he", "граната": "he", "he": "he", "взрыв": "he",

    # Позиции (Mirage)
    "окно": "window", "window": "window",
    "коннектор": "connector", "connector": "connector",
    "джангл": "jungle", "jungle": "jungle",
    "палас": "palace", "palace": "palace",
    "тикет": "ticket", "ticket": "ticket",
    "сити": "city", "city": "city",
    "рампа": "ramp", "ramp": "ramp",
    "апарты": "apartments", "apartments": "apartments",

    # Позиции (Inferno)
    "банан": "banana", "banana": "banana",
    "ковры": "carpet", "carpet": "carpet",
    "квартира": "apartment", "apartment": "apartment",
    "пит": "pit", "pit": "pit",
    "мото": "moto", "moto": "moto",
}

def translate_query(query: str) -> str:
    """Переводит запрос с русского на английский и наоборот"""
    words = query.lower().split()
    translated = []

    for word in words:
        base_word = word.rstrip('еуойаяи')
        if word in TRANSLATIONS:
            translated.append(TRANSLATIONS[word])
        elif base_word in TRANSLATIONS:
            translated.append(TRANSLATIONS[base_word])
        else:
            translated.append(word)

    return " ".join(translated)

@router.callback_query(F.data == "menu_search")
async def start_search(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(SearchStates.waiting_query)
    await callback.message.edit_text(
        "🔍 <b>Поиск по боту</b>\n\n"
        "Введите запрос:\n"
        "<i>Примеры:\n"
        "• 'раскид на мираж' — найдет гранаты\n"
        "• 'что такое холдить' — найдет термины\n"
        "• 'смок в окно' — поиск по позициям\n\n"
        "Работает на русском и английском!</i>",
        parse_mode="HTML"
    )

@router.message(SearchStates.waiting_query)
async def process_search(message: types.Message, state: FSMContext):
    query = message.text.lower().strip()
    original_query = query

    query = translate_query(query)

    is_term_query = any(phrase in original_query for phrase in ['что такое', 'кто такой', 'значение', 'термин'])

    if is_term_query:
        search_term = original_query.replace('что такое', '').replace('кто такой', '').replace('значение', '').replace('термин', '').strip()
        term = db.get_term(search_term)

        if term:
            text = f"""
            <b>📖 {term['term'].upper()}</b>
            <i>{term['category'] or 'Общий термин'}</i>

            <b>Значение:</b>
            {term['definition']}

            <b>Пример:</b>
            <i>{term['example'] or '—'}</i>
            """
            await message.answer(text, parse_mode="HTML")
        else:
            similar = db.search_terms(search_term)
            if similar:
                text = f"😕 '<b>{search_term}</b>' не найден.\n\n<b>Похожие термины:</b>\n" + "\n".join([f"• {s['term']}" for s in similar[:5]])
            else:
                text = f"😕 '<b>{search_term}</b>' не найден в словаре."
            await message.answer(text, parse_mode="HTML")
    else:
        results = db.search_nades(query)

        if not results:
            similar_maps = [m for m in ["mirage", "inferno", "nuke", "ancient", "anubis", "vertigo", "overpass", "dust2"] if m in query or any(t in query for t in TRANSLATIONS if TRANSLATIONS[t] == m)]

            suggestions = []
            if "smoke" in query or any(t in query for t in ["смок", "дым"]):
                suggestions.append("смок")
            if "window" in query or "окно" in original_query:
                suggestions.append("в окно")
            if similar_maps:
                suggestions.append(f"на {similar_maps[0]}")

            if suggestions:
                suggestion_text = " ".join(suggestions)
                text = (
                    f"😕 '<b>{original_query}</b>' не найдено.\n\n"
                    f"<b>Попробуйте:</b>\n"
                    f"• {suggestion_text}\n"
                    f"• смок на мираже\n"
                    f"• флешка инферно\n"
                    f"• molotov banana"
                )
            else:
                text = (
                    f"😕 '<b>{original_query}</b>' не найдено.\n\n"
                    f"<b>Попробуйте искать:</b>\n"
                    f"• Название карты (mirage, inferno, мираж)\n"
                    f"• Тип гранаты (smoke, flash, смок, флеш)\n"
                    f"• Позицию (window, connector, окно)"
                )

            await message.answer(text, parse_mode="HTML")
            return

        await state.update_data(search_results=results, search_query=original_query, search_page=0)
        await message.answer(
            f"🔍 Найдено <b>{len(results)}</b> по запросу '<b>{original_query}</b>':",
            reply_markup=search_results_menu(results, 0, original_query),
            parse_mode="HTML"
        )

@router.message(Command("search"))
async def search_command(message: types.Message, state: FSMContext):
    args = message.text.replace("/search", "").strip()
    
    if not args:
        await state.set_state(SearchStates.waiting_query)
        await message.answer(
            "🔍 <b>Поиск по боту</b>\n\nВведите запрос:",
            parse_mode="HTML"
        )
        return
    
    message.text = args
    await process_search(message, state)

@router.callback_query(F.data.startswith("search_page_"))
async def change_search_page(callback: types.CallbackQuery, state: FSMContext):
    """Пагинация результатов поиска"""
    parts = callback.data.replace("search_page_", "").split("_")
    page = int(parts[0])
    query = "_".join(parts[1:]) if len(parts) > 1 else ""

    data = await state.get_data()
    results = data.get('search_results', [])

    if not results:
        results = db.search_nades(translate_query(query))
        await state.update_data(search_results=results)

    await callback.message.edit_text(
        f"🔍 Найдено <b>{len(results)}</b> по запросу '<b>{query}</b>':",
        reply_markup=search_results_menu(results, page, query),
        parse_mode="HTML"
    )

# ============ INLINE MODE ============

from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

@router.inline_query()
async def inline_search(inline_query: InlineQuery):
    """Обработчик inline поиска"""
    query = inline_query.query.lower().strip()
    
    if not query or len(query) < 2:
        await inline_query.answer([], cache_time=300)
        return
    
    results = []
    
    translated = translate_query(query)
    nades = db.search_nades(translated)[:5] 
    
    for nade in nades:
        type_emoji = {"smoke": "💨", "flash": "⚡", "molotov": "🔥", "he": "💣"}
        emoji = type_emoji.get(nade['nade_type'], '💨')
        
        content = f"""{emoji} <b>{nade['name']}</b>
🗺️ Карта: {nade['map_name'].title()}
📍 Позиция: {nade['position_desc']}
🎯 Прицел: {nade['aim_desc']}
👋 Бросок: {nade['throw_desc']}
✅ Результат: {nade['result_desc']}"""
        
        results.append(
            InlineQueryResultArticle(
                id=f"nade_{nade['id']}",
                title=f"{nade['map_name'].title()}: {nade['name']}",
                description=f"{nade['nade_type']} | {nade['position_desc'][:50]}...",
                input_message_content=InputTextMessageContent(
                    message_text=content,
                    parse_mode="HTML"
                )
            )
        )
    
    terms = db.search_terms(query)[:3] 
    
    for term in terms:
        content = f"""<b>📖 {term['term'].upper()}</b>
<i>{term['category'] or 'Общий термин'}</i>

<b>Значение:</b>
{term['definition']}

<b>Пример:</b>
<i>{term['example'] or '—'}</i>"""
        
        results.append(
            InlineQueryResultArticle(
                id=f"term_{term['id']}",
                title=f"📚 {term['term'].title()}",
                description=f"{term['definition'][:60]}...",
                input_message_content=InputTextMessageContent(
                    message_text=content,
                    parse_mode="HTML"
                )
            )
        )
    
    if not results:
        results.append(
            InlineQueryResultArticle(
                id="no_results",
                title="😕 Ничего не найдено",
                description=f"По запросу '{query}' нет результатов. Попробуйте: смок окно мираж, флеш инферно...",
                input_message_content=InputTextMessageContent(
                    message_text=f"😕 По запросу '<b>{query}</b>' ничего не найдено.\n\nПопробуйте искать:\n• Название карты (mirage, inferno)\n• Тип гранаты (smoke, flash)\n• Позицию (window, banana)",
                    parse_mode="HTML"
                )
            )
        )
    
    await inline_query.answer(results, cache_time=300)