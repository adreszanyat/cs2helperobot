import os
import json
from typing import List, Dict, Optional
from datetime import datetime

def format_number(num: int) -> str:
    """Форматирует число с разделителями"""
    return f"{num:,}".replace(",", " ")

def truncate_text(text: str, max_length: int = 100) -> str:
    """Обрезает текст до указанной длины"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def validate_image_path(path: str) -> bool:
    """Проверяет существование изображения"""
    return os.path.exists(path) and os.path.getsize(path) > 0

def generate_config_file(content: str, filename: str, directory: str = "configs") -> str:
    """Генерирует конфиг файл"""
    filepath = os.path.join(directory, filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath

def parse_search_query(query: str) -> Dict[str, str]:
    """Парсит поисковый запрос"""
    query = query.lower().strip()
    
    # Карты
    maps = ["mirage", "inferno", "nuke", "ancient", "anubis", "vertigo", "overpass", "dust2"]
    found_map = next((m for m in maps if m in query), None)
    
    # Типы гранат
    nade_types = {
        "smoke": ["smoke", "смок", "дым"],
        "flash": ["flash", "флеш", "вспышка"],
        "molotov": ["molotov", "молотов", "огонь"],
        "he": ["he", "взрыв", "грамата"]
    }
    
    found_type = None
    for type_key, aliases in nade_types.items():
        if any(alias in query for alias in aliases):
            found_type = type_key
            break
    
    return {
        "map": found_map,
        "type": found_type,
        "raw": query
    }

def calculate_edpi(sens: float, dpi: int) -> int:
    """Вычисляет eDPI"""
    return int(sens * dpi)

def format_time_ago(timestamp: datetime) -> str:
    """Форматирует время в 'N минут назад'"""
    now = datetime.now()
    diff = now - timestamp
    
    if diff.days > 0:
        return f"{diff.days} дн. назад"
    hours = diff.seconds // 3600
    if hours > 0:
        return f"{hours} ч. назад"
    minutes = diff.seconds // 60
    return f"{minutes} мин. назад"