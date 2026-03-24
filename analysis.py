import re
import random
from typing import Dict, List, Any

# Импортируем наши данные
from analysis_data import (
    TRAITS, _STRONG_PHRASES, _PREFIXES, 
    _IMPROVEMENT_ADVICE, _DAILY_CHALLENGES
)

# Попробуем использовать pymorphy2 для лемматизации
try:
    import pymorphy2
    morph = pymorphy2.MorphAnalyzer()
    _HAVE_MORPH = True
except ImportError:
    morph = None
    _HAVE_MORPH = False

# ─── Константы ──────────────────────────────────────────────────────────────
MAX_TEXT_LENGTH = 5000
_WORD_RE = re.compile(r"[А-Яа-яЁёA-Za-z0-9]+", flags=re.U)
_NEG_WORDS = {"не", "ни", "нет", "без", "никогда", "нехочу", "не хочу"}

# Лексикон тональности
_POS_PREFIXES = {"хорош", "отличн", "успех", "эффектив", "помог", "достиг", "смог", "справ"}
_NEG_PREFIXES = {"плох", "проблем", "трудн", "ошибк", "недостат", "неудач", "провал", "слаб"}

# ─── Утилиты ────────────────────────────────────────────────────────────────
def _tokenize(text: str) -> List[str]:
    return _WORD_RE.findall(text.lower())

def _lemmatize(tokens: List[str]) -> List[str]:
    if not _HAVE_MORPH: return tokens
    return [morph.parse(t)[0].normal_form for t in tokens]

def _sentences(text: str) -> List[str]:
    parts = re.split(r"[.!?]+", text)
    return [p.strip() for p in parts if p.strip()]

def _is_phrase_negated(text_lower: str, phrase: str) -> bool:
    idx = text_lower.find(phrase)
    if idx == -1: return False
    context = text_lower[max(0, idx - 40):idx]
    return any(re.search(rf"\b{neg}\b", context, re.U) for neg in _NEG_WORDS)

def _clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, value))

# ─── Основной анализ ────────────────────────────────────────────────────────
def analyze_text_with_meta(text: str, min_words: int = 8) -> Dict[str, Any]:
    text = text.strip()[:MAX_TEXT_LENGTH]
    if not text: return {"message": "Текст пустой."}

    tokens = _tokenize(text)
    if len(tokens) < min_words:
        return {"message": f"Добавьте больше текста (минимум {min_words} слов)."}

    lemmas = _lemmatize(tokens)
    total_words = len(lemmas)
    sentences = _sentences(text)
    lowered = text.lower()
    unique_words = len(set(lemmas))
    lexical_diversity = unique_words / total_words if total_words else 0

    raw: Dict[str, float] = {t: 0.0 for t in TRAITS}
    hits: Dict[str, int] = {t: 0 for t in TRAITS}

    for trait, phrases in _STRONG_PHRASES.items():
        for phrase in phrases:
            if phrase in lowered:
                if _is_phrase_negated(lowered, phrase): raw[trait] -= 12.0
                else:
                    raw[trait] += 15.0
                    hits[trait] += 1

    for token in lemmas:
        for trait, prefixes in _PREFIXES.items():
            if any(token.startswith(p) for p in prefixes):
                raw[trait] += 5.0
                hits[trait] += 1
                break

    sentiment_bonus = 0.0
    for sent in sentences:
        sent_tokens = _tokenize(sent)
        pos = sum(1 for t in sent_tokens if any(t.startswith(p) for p in _POS_PREFIXES))
        neg = sum(1 for t in sent_tokens if any(t.startswith(p) for p in _NEG_PREFIXES))
        sentiment_bonus += (pos - neg) * 3.0

    per_trait_sentiment = sentiment_bonus / len(TRAITS) if TRAITS else 0
    diversity_bonus = min(lexical_diversity * 12.0, 8.0)
    length_bonus = min(total_words / 50.0 * 7.0, 7.0)

    scores: Dict[str, int] = {}
    total_hits = sum(hits.values())

    for trait in TRAITS:
        base = 35.0 + (raw[trait] * 1.5) + (per_trait_sentiment * 1.5) + diversity_bonus + length_bonus
        if hits[trait] > 0:
            base += 20.0
            base = max(base, 65.0)
        if hits[trait] == 0 and total_hits > 0:
            base = max(base, 35.0)
        scores[trait] = int(_clamp(round(base), 0, 100))

    conf_text = min(total_words / 80.0, 0.5)
    conf_hits = min(total_hits / 12.0, 0.4)
    conf_diversity = min(lexical_diversity, 0.1)
    confidence = round(_clamp(conf_text + conf_hits + conf_diversity, 0.1, 1.0), 2)

    suggestions = []
    sorted_traits = sorted(scores.items(), key=lambda x: x[1])
    if total_words < 20: suggestions.append("Напишите более развёрнутый текст.")
    weak_traits = [t for t, s in sorted_traits[:2] if s < 50]
    for wt in weak_traits: suggestions.append(f"Раскройте тему «{wt}».")
    if not suggestions: suggestions.append("Отличный текст!")

    overall = round(sum(scores.values()) / len(scores), 1)
    meta = {
        "overall_score": overall, "confidence": confidence, "suggestions": suggestions,
        "raw": {"total_words": total_words, "lexical_diversity": round(lexical_diversity, 3)}
    }
    return {**scores, "_meta": meta}

def get_level(result_or_scores: Any) -> str:
    try:
        if isinstance(result_or_scores, dict):
            if "_meta" in result_or_scores: avg = float(result_or_scores["_meta"]["overall_score"])
            else:
                vals = [v for k, v in result_or_scores.items() if isinstance(v, (int, float))]
                avg = sum(vals) / max(1, len(vals)) if vals else 0.0
        else: avg = float(result_or_scores)
    except: return "Не удалось определить уровень"

    if avg >= 85: return "🏆 Выдающийся лидер"
    if avg >= 70: return "🔥 Уверенный новатор"
    if avg >= 55: return "📊 Командный игрок"
    if avg >= 40: return "📈 Перспективный участник"
    return "🌱 Начинающий исследователь"

def get_achievements(result_or_scores: Any) -> List[str]:
    try:
        if isinstance(result_or_scores, dict) and "_meta" in result_or_scores:
            scores = {k: v for k, v in result_or_scores.items() if k != "_meta" and isinstance(v, (int, float))}
        elif isinstance(result_or_scores, dict): scores = result_or_scores
        else: return []
    except: return []

    out = []
    for trait, v in scores.items():
        if v >= 85: out.append(f"🏆 {trait}: выдающийся уровень!")
        elif v >= 72: out.append(f"⭐ {trait}: сильная сторона.")
    return out if out else ["У вас огромный потенциал!"]

def get_improvement_plan(result_or_scores: Any) -> Dict[str, str]:
    if isinstance(result_or_scores, dict) and "_meta" in result_or_scores:
        scores = {k: v for k, v in result_or_scores.items() if k != "_meta" and isinstance(v, (int, float))}
    elif isinstance(result_or_scores, dict):
        scores = {k: v for k, v in result_or_scores.items() if isinstance(v, (int, float))}
    else: return {}

    plan = {}
    for trait, score in sorted(scores.items(), key=lambda x: x[1]):
        advice_map = _IMPROVEMENT_ADVICE.get(trait, {})
        if score < 40: plan[trait] = advice_map.get("low", "Работайте над этим.")
        elif score < 70: plan[trait] = advice_map.get("mid", "Совершенствуйтесь.")
        else: plan[trait] = advice_map.get("high", "Отличный уровень!")
    return plan

def get_daily_challenge(result_or_scores: Any) -> Dict[str, str]:
    if isinstance(result_or_scores, dict) and "_meta" in result_or_scores:
        scores = {k: v for k, v in result_or_scores.items() if k != "_meta" and isinstance(v, (int, float))}
    elif isinstance(result_or_scores, dict):
        scores = {k: v for k, v in result_or_scores.items() if isinstance(v, (int, float))}
    else: return {}

    sorted_traits = sorted(scores.items(), key=lambda x: x[1])
    challenges = {}
    for trait, _ in sorted_traits[:2]:
        options = _DAILY_CHALLENGES.get(trait, ["Работайте над этим навыком."])
        challenges[trait] = random.choice(options)
    return challenges
