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
        preview = str(text_preview).strip()
        display_preview = (preview[:197] + "...") if len(preview) > 200 else preview
        data = {
            "user_id": user_id,
            "text_preview": display_preview,
            "full_analysis": json.dumps(full_analysis, ensure_ascii=False),
            "score": float(score),
            "created_at": datetime.now().isoformat()
        }
        sb.table("history").insert(data).execute()
        return True
    except Exception as e:
        import logging
        logging.error(f"Error saving to Supabase: {str(e)}")
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
    if not sb: return 0
    
    try:
        res = sb.table("history").delete().eq("user_id", user_id).execute()
        return len(res.data) if hasattr(res, 'data') and res.data else 0
    except Exception:
        return 0

def get_stats(user_id: int) -> dict:
    """Высчитывает средние баллы по всем анализам пользователя."""
    scores = get_user_scores(user_id)
    if not scores:
        return {"total_analyses": 0}
        
    stats = {"total_analyses": len(scores)}
    all_traits = {}
    
    for row in scores:
        analysis = row.get("full_analysis", {})
        if isinstance(analysis, dict):
            for trait, val in analysis.items():
                if trait != "_meta" and isinstance(val, (int, float)):
                    if trait not in all_traits: 
                        all_traits[trait] = []
                    all_traits[trait].append(float(val))
                    
    for trait, vals in all_traits.items():
        stats[trait] = sum(vals) / len(vals)
        
    return stats
