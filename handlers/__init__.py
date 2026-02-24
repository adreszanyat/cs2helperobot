from aiogram import Dispatcher, F, types
from aiogram.filters import Command

from database import db

from handlers import (
    admin, nades, settings, meta, training, 
    terms, tactics, favorites, search
)

def register_handlers(dp: Dispatcher):
    """Регистрация всех обработчиков"""
    dp.include_router(admin.router)
    dp.include_router(nades.router)
    dp.include_router(settings.router)
    dp.include_router(meta.router)
    dp.include_router(training.router)
    dp.include_router(terms.router)
    dp.include_router(tactics.router)
    dp.include_router(favorites.router)
    dp.include_router(search.router)