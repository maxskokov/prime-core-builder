import sqlite3
import pandas as pd
from datetime import datetime

DB_PATH = "scores.db"

TRAITS = [
    "Дисциплина", "Уверенность", "Лидерство",
    "Креативность", "Эмпатия", "Адаптивность", "Коммуникация",
]


def _get_conn():
    """Подключение к БД."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """Создаёт таблицу scores, если не существует."""
    conn = _get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            Дисциплина INTEGER DEFAULT 0,
            Уверенность INTEGER DEFAULT 0,
            Лидерство INTEGER DEFAULT 0,
            Креативность INTEGER DEFAULT 0,
            Эмпатия INTEGER DEFAULT 0,
            Адаптивность INTEGER DEFAULT 0,
            Коммуникация INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


def save_scores(user_id: int, scores: dict):
    """
    Сохраняет результаты анализа для пользователя.
    Фильтрует ключ _meta перед записью.
    Использует параметризованные запросы (защита от SQL-инъекций).
    """
    conn = _get_conn()
    timestamp = datetime.now().isoformat()

    values = [user_id, timestamp]
    for trait in TRAITS:
        values.append(int(scores.get(trait, 0)))

    conn.execute(
        """INSERT INTO scores
           (user_id, timestamp, Дисциплина, Уверенность, Лидерство,
            Креативность, Эмпатия, Адаптивность, Коммуникация)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        values,
    )
    conn.commit()
    conn.close()


def load_history(user_id: int) -> pd.DataFrame:
    """Загружает историю анализов для конкретного пользователя."""
    conn = _get_conn()
    df = pd.read_sql_query(
        "SELECT * FROM scores WHERE user_id = ? ORDER BY timestamp DESC",
        conn,
        params=(user_id,),
    )
    conn.close()

    if not df.empty and "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    return df


def clear_history(user_id: int) -> int:
    """
    Удаляет всю историю пользователя.
    Возвращает количество удалённых записей.
    """
    conn = _get_conn()
    cursor = conn.execute(
        "DELETE FROM scores WHERE user_id = ?",
        (user_id,),
    )
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted


def get_stats(user_id: int) -> dict:
    """Средние оценки пользователя по всем анализам."""
    conn = _get_conn()
    row = conn.execute(
        """SELECT
             AVG(Дисциплина), AVG(Уверенность), AVG(Лидерство),
             AVG(Креативность), AVG(Эмпатия), AVG(Адаптивность),
             AVG(Коммуникация), COUNT(*)
           FROM scores WHERE user_id = ?""",
        (user_id,),
    ).fetchone()
    conn.close()

    if row is None or row[-1] == 0:
        return {}

    stats = {}
    for i, trait in enumerate(TRAITS):
        stats[trait] = round(row[i] or 0, 1)
    stats["total_analyses"] = row[-1]
    return stats


# Инициализация при импорте
init_db()
