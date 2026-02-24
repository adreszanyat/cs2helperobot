import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from config import DB_PATH

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        # Гранаты
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                map_name TEXT NOT NULL,
                nade_type TEXT NOT NULL,
                name TEXT NOT NULL,
                side TEXT,
                difficulty INTEGER DEFAULT 1,
                position_desc TEXT,
                position_img TEXT,
                aim_desc TEXT,
                aim_img TEXT,
                throw_type TEXT,
                throw_desc TEXT,
                result_desc TEXT,
                result_img TEXT,
                result_video TEXT,
                tags TEXT,
                consistency INTEGER DEFAULT 90,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        """)

        # Избранное пользователей
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                nade_id INTEGER NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (nade_id) REFERENCES nades(id),
                UNIQUE(user_id, nade_id)
            )
        """)

        # Термины словаря
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS terms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                term TEXT UNIQUE NOT NULL,
                definition TEXT NOT NULL,
                category TEXT,
                example TEXT,
                added_by INTEGER,
                is_verified BOOLEAN DEFAULT 0
            )
        """)

        # Статистика пользователей
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_stats (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                favorites_count INTEGER DEFAULT 0,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Логи админа
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.conn.commit()

    # === ГРАНАТЫ ===

    def add_nade(self, data: Dict) -> int:
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO nades (
                map_name, nade_type, name, side, difficulty,
                position_desc, position_img, aim_desc, aim_img,
                throw_type, throw_desc, result_desc, result_img, result_video, tags
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['map_name'], data['nade_type'], data['name'], data.get('side'),
            data.get('difficulty', 1), data.get('position_desc'), data.get('position_img'),
            data.get('aim_desc'), data.get('aim_img'), data.get('throw_type'),
            data.get('throw_desc'), data.get('result_desc'), data.get('result_img'),
            data.get('result_video'), json.dumps(data.get('tags', []))
        ))
        self.conn.commit()
        return cursor.lastrowid

    def get_nades(self, map_name: str, nade_type: Optional[str] = None, side: Optional[str] = None) -> List[Dict]:
        """Получает гранаты с фильтром по карте, типу и стороне"""
        cursor = self.conn.cursor()

        query = "SELECT * FROM nades WHERE map_name = ? AND is_active = 1"
        params = [map_name]

        if nade_type:
            query += " AND nade_type = ?"
            params.append(nade_type)

        if side and side != "both":
            query += " AND (side = ? OR side = 'both')"
            params.append(side)

        query += " ORDER BY difficulty ASC, name ASC"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def get_nade_by_id(self, nade_id: int) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM nades WHERE id = ?", (nade_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def search_nades(self, query: str) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM nades 
            WHERE (name LIKE ? OR position_desc LIKE ? OR aim_desc LIKE ? OR tags LIKE ?)
            AND is_active = 1
            ORDER BY map_name, nade_type
        """, (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
        return [dict(row) for row in cursor.fetchall()]

    def update_nade(self, nade_id: int, data: Dict):
        cursor = self.conn.cursor()
        fields = []
        values = []
        for key, value in data.items():
            fields.append(f"{key} = ?")
            values.append(value)
        values.append(nade_id)

        cursor.execute(f"""
            UPDATE nades SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, values)
        self.conn.commit()

    def delete_nade(self, nade_id: int):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE nades SET is_active = 0 WHERE id = ?", (nade_id,))
        self.conn.commit()

    # === ИЗБРАННОЕ ===

    def add_favorite(self, user_id: int, nade_id: int) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO favorites (user_id, nade_id) VALUES (?, ?)
            """, (user_id, nade_id))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def remove_favorite(self, user_id: int, nade_id: int):
        cursor = self.conn.cursor()
        cursor.execute("""
            DELETE FROM favorites WHERE user_id = ? AND nade_id = ?
        """, (user_id, nade_id))
        self.conn.commit()

    def get_favorites(self, user_id: int) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT n.* FROM nades n
            JOIN favorites f ON n.id = f.nade_id
            WHERE f.user_id = ? AND n.is_active = 1
            ORDER BY f.added_at DESC
        """, (user_id,))
        return [dict(row) for row in cursor.fetchall()]

    def is_favorite(self, user_id: int, nade_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 1 FROM favorites WHERE user_id = ? AND nade_id = ?
        """, (user_id, nade_id))
        return cursor.fetchone() is not None

    # === ТЕРМИНЫ ===

    def add_term(self, term: str, definition: str, category: str = None, 
                 example: str = None, added_by: int = None) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO terms (term, definition, category, example, added_by)
                VALUES (?, ?, ?, ?, ?)
            """, (term.lower(), definition, category, example, added_by))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_term(self, term: str) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM terms WHERE term = ?", (term.lower(),))
        row = cursor.fetchone()
        return dict(row) if row else None

    def search_terms(self, query: str) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM terms 
            WHERE term LIKE ? OR definition LIKE ?
            ORDER BY term ASC
        """, (f'%{query}%', f'%{query}%'))
        return [dict(row) for row in cursor.fetchall()]

    # === ПОЛЬЗОВАТЕЛИ ===

    def update_user(self, user_id: int, username: str = None, 
                    first_name: str = None, last_name: str = None):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO user_stats (user_id, username, first_name, last_name)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username = excluded.username,
                first_name = excluded.first_name,
                last_name = excluded.last_name,
                last_activity = CURRENT_TIMESTAMP
        """, (user_id, username, first_name, last_name))
        self.conn.commit()

    # === АДМИН ЛОГИ ===

    def log_admin_action(self, admin_id: int, action: str, details: str = None):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO admin_logs (admin_id, action, details) VALUES (?, ?, ?)
        """, (admin_id, action, details))
        self.conn.commit()

db = Database()
