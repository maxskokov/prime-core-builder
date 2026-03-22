import streamlit as st
from supabase import create_client, Client
from datetime import datetime
import json

# ─── Инициализация Supabase ────────────────────────────────────────────────

def _get_supabase() -> Client | None:
    """Подключается к облачной базе Supabase."""
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception:
        return None

# ─── Управление Историей ───────────────────────────────────────────────────

def save_score(user_id: int, text_preview: str, full_analysis: dict, score: float):
    """Сохраняет результат анализа в облачную базу Supabase."""
    sb = _get_supabase()
    if not sb: return False
    
    try:
        # Убеждаемся, что text_preview это строка
        preview = str(text_preview)
        data = {
            "user_id": user_id,
            "text_preview": preview[:200] + ("..." if len(preview) > 200 else ""),
            "full_analysis": json.dumps(full_analysis, ensure_ascii=False),
            "score": float(score),
            "created_at": datetime.now().isoformat()
        }
        sb.table("history").insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Ошибка сохранения в облако: {str(e)}")
        return False

def get_user_scores(user_id: int):
    """Получает все записи истории для конкретного пользователя."""
    sb = _get_supabase()
    if not sb: return []
    
    try:
        res = sb.table("history").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        
        scores = []
        for row in res.data:
            scores.append({
                "id": row["id"],
                "text_preview": row["text_preview"],
                "full_analysis": json.loads(row["full_analysis"]) if isinstance(row["full_analysis"], str) else row["full_analysis"],
                "score": row["score"],
                "created_at": row["created_at"]
            })
        return scores
    except Exception:
        return []

def delete_user_history(user_id: int):
    """Полностью очищает историю пользователя в облаке."""
    sb = _get_supabase()
    if not sb: return False
    
    try:
        sb.table("history").delete().eq("user_id", user_id).execute()
        return True
    except Exception:
        return False

# ─── Алиасы для обратной совместимости ──────────────────────────────────────

def load_history(user_id: int):
    return get_user_scores(user_id)

def delete_history(user_id: int):
    return delete_user_history(user_id)
