import re
import random
from typing import Dict, List, Any

# Попробуем использовать pymorphy2 для лемматизации
try:
    import pymorphy2
    morph = pymorphy2.MorphAnalyzer()
    _HAVE_MORPH = True
except ImportError:
    morph = None
    _HAVE_MORPH = False

# ─── Константы ──────────────────────────────────────────────────────────────

MAX_TEXT_LENGTH = 5000  # Лимит ввода для защиты от переполнения

_WORD_RE = re.compile(r"[А-Яа-яЁёA-Za-z0-9]+", flags=re.U)
_NEG_WORDS = {"не", "ни", "нет", "без", "никогда", "нехочу", "не хочу"}

TRAITS = [
    "Дисциплина", "Уверенность", "Лидерство",
    "Креативность", "Эмпатия", "Адаптивность", "Коммуникация",
]

# Сильные фразы — дают большой вклад в оценку (вес ×15)
_STRONG_PHRASES: Dict[str, List[str]] = {
    "Дисциплина": [
        "соблюдаю сроки", "распределяю время", "выполняю по плану",
        "планирую задачи", "работаю системно", "следую графику",
    ],
    "Уверенность": [
        "уверен в себе", "готов принимать решения", "уверенно выступаю",
        "принимаю решения", "отстаиваю позицию", "беру ответственность",
    ],
    "Лидерство": [
        "организую команду", "координирую", "вёл проект", "руководил",
        "распределяю задачи", "мотивирую коллег",
    ],
    "Креативность": [
        "генерирую идеи", "нестандартные решения", "эксперимент",
        "новаторский", "придумываю подходы", "ищу новые способы",
    ],
    "Эмпатия": [
        "слушаю коллег", "понимаю собеседника", "поддерживаю коллег",
        "сопереживаю", "учитываю чувства", "помогаю другим",
    ],
    "Адаптивность": [
        "легко адаптируюсь", "быстро адаптируюсь", "приспосабливаюсь",
        "меняю подход", "гибко реагирую", "учусь на ходу",
    ],
    "Коммуникация": [
        "ясно формулирую", "письменно объясняю", "донести мысль",
        "объясняю свою позицию", "веду переговоры", "нахожу общий язык",
    ],
}

# Префиксы — дают средний вклад (вес ×5)
_PREFIXES: Dict[str, List[str]] = {
    "Дисциплина": ["план", "распис", "срок", "контрол", "соблюд", "систем", "порядок"],
    "Уверенность": ["уверен", "решител", "смел", "принимаю", "решаю", "ответствен"],
    "Лидерство": ["команд", "лидер", "руковод", "организ", "инициатив", "управл"],
    "Креативность": ["иде", "креатив", "нестандарт", "творч", "иннов", "выдум"],
    "Эмпатия": ["слуша", "понима", "сочувств", "поддерж", "сопережив", "забот"],
    "Адаптивность": ["адапт", "гибк", "приспособ", "адаптир", "измен", "перестра"],
    "Коммуникация": ["объясн", "донес", "общен", "презент", "ясн", "диалог"],
}

# Лексикон тональности
_POS_PREFIXES = {"хорош", "отличн", "успех", "эффектив", "помог", "достиг", "смог", "справ"}
_NEG_PREFIXES = {"плох", "проблем", "трудн", "ошибк", "недостат", "неудач", "провал", "слаб"}

# ─── Утилиты ────────────────────────────────────────────────────────────────


def _tokenize(text: str) -> List[str]:
    """Разбивает текст на слова."""
    return _WORD_RE.findall(text.lower())


def _lemmatize(tokens: List[str]) -> List[str]:
    """Лемматизация через pymorphy2 (если установлен)."""
    if not _HAVE_MORPH:
        return tokens
    return [morph.parse(t)[0].normal_form for t in tokens]


def _sentences(text: str) -> List[str]:
    """Разбиение на предложения."""
    parts = re.split(r"[.!?]+", text)
    return [p.strip() for p in parts if p.strip()]


def _is_phrase_negated(text_lower: str, phrase: str) -> bool:
    """Проверяет, есть ли отрицание в контексте фразы (40 символов до)."""
    idx = text_lower.find(phrase)
    if idx == -1:
        return False
    context = text_lower[max(0, idx - 40):idx]
    return any(re.search(rf"\b{neg}\b", context, re.U) for neg in _NEG_WORDS)


def _clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, value))


# ─── Основной анализ ────────────────────────────────────────────────────────


def analyze_text_with_meta(text: str, min_words: int = 8) -> Dict[str, Any]:
    """
    Анализ текста → оценка 7 личностных черт по шкале 0–100.

    Алгоритм:
      1. Сильные фразы   → +15 за совпадение, −12 за отрицание
      2. Совпадение префиксов → +5 за слово
      3. Тональность    → +3 за позитив, −3 за негатив (на предложение)
      4. Бонус за лексическое разнообразие  (до +8)
      5. Бонус за длину текста (до +7)
      6. Базовый порог: если тема затронута → минимум 20
      7. Итог clamped в [0, 100]
    """
    # Защита от переполнения
    text = text.strip()[:MAX_TEXT_LENGTH]
    if not text:
        return {"message": "Текст пустой."}

    tokens = _tokenize(text)
    if len(tokens) < min_words:
        return {"message": f"Добавьте больше текста (минимум {min_words} слов)."}

    lemmas = _lemmatize(tokens)
    total_words = len(lemmas)
    sentences = _sentences(text)
    lowered = text.lower()
    unique_words = len(set(lemmas))
    lexical_diversity = unique_words / total_words if total_words else 0

    # ── 1) Подсчёт по чертам ────────────────────────────────────────────
    raw: Dict[str, float] = {t: 0.0 for t in TRAITS}
    hits: Dict[str, int] = {t: 0 for t in TRAITS}  # общее кол-во совпадений

    # Сильные фразы
    for trait, phrases in _STRONG_PHRASES.items():
        for phrase in phrases:
            if phrase in lowered:
                if _is_phrase_negated(lowered, phrase):
                    raw[trait] -= 12.0
                else:
                    raw[trait] += 15.0
                    hits[trait] += 1

    # Префиксы
    for token in lemmas:
        for trait, prefixes in _PREFIXES.items():
            if any(token.startswith(p) for p in prefixes):
                raw[trait] += 5.0
                hits[trait] += 1
                break  # один токен — одна черта

    # ── 2) Тональность по предложениям ──────────────────────────────────
    sentiment_bonus = 0.0
    for sent in sentences:
        sent_tokens = _tokenize(sent)
        pos = sum(1 for t in sent_tokens if any(t.startswith(p) for p in _POS_PREFIXES))
        neg = sum(1 for t in sent_tokens if any(t.startswith(p) for p in _NEG_PREFIXES))
        sentiment_bonus += (pos - neg) * 3.0

    # Распределяем тональность равномерно по всем чертам
    per_trait_sentiment = sentiment_bonus / len(TRAITS) if TRAITS else 0

    # ── 3) Бонусы ───────────────────────────────────────────────────────
    diversity_bonus = min(lexical_diversity * 12.0, 8.0)   # до +8
    length_bonus = min(total_words / 50.0 * 7.0, 7.0)      # до +7

    # ── 4) Итоговая нормализация ────────────────────────────────────────
    scores: Dict[str, int] = {}
    total_hits = sum(hits.values())

    for trait in TRAITS:
        # Увеличим базовую оценку на 35, чтобы выдавать 60-90 за хороший текст
        base = 35.0 + raw[trait] + per_trait_sentiment + diversity_bonus + length_bonus

        # Если есть хоть одно совпадение — минимум 60
        if hits[trait] > 0:
            base = max(base, 60.0)

        # Без совпадений — базовый «нейтральный» уровень 35-45
        if hits[trait] == 0 and total_hits > 0:
            base = max(base, 35.0)

        scores[trait] = int(_clamp(round(base), 0, 100))

    # ── 5) Confidence (уверенность алгоритма) ───────────────────────────
    # Зависит от длины текста и количества совпадений
    conf_text = min(total_words / 80.0, 0.5)    # до 0.5 за длину
    conf_hits = min(total_hits / 12.0, 0.4)      # до 0.4 за совпадения
    conf_diversity = min(lexical_diversity, 0.1)  # до 0.1 за разнообразие
    confidence = round(_clamp(conf_text + conf_hits + conf_diversity, 0.1, 1.0), 2)

    # ── 6) Динамические рекомендации ────────────────────────────────────
    suggestions: List[str] = []
    sorted_traits = sorted(scores.items(), key=lambda x: x[1])

    if total_words < 20:
        suggestions.append("Напишите более развёрнутый текст для точного анализа.")

    weak_traits = [t for t, s in sorted_traits[:2] if s < 50]
    for wt in weak_traits:
        suggestions.append(f"Раскройте тему «{wt}» — приведите конкретные примеры.")

    if lexical_diversity < 0.5:
        suggestions.append("Используйте больше разнообразных слов и формулировок.")

    if not suggestions:
        suggestions.append("Отличный текст! Попробуйте описать ситуации детальнее для ещё большей точности.")

    # ── Результат ───────────────────────────────────────────────────────
    overall = round(sum(scores.values()) / len(scores), 1)

    meta = {
        "overall_score": overall,
        "confidence": confidence,
        "suggestions": suggestions,
        "raw": {
            "total_words": total_words,
            "unique_words": unique_words,
            "lexical_diversity": round(lexical_diversity, 3),
            "total_hits": total_hits,
        },
    }

    return {**scores, "_meta": meta}


# ─── Уровень ────────────────────────────────────────────────────────────────


def get_level(result_or_scores: Any) -> str:
    """Уровень на основе среднего балла."""
    try:
        if isinstance(result_or_scores, dict):
            if "_meta" in result_or_scores:
                avg = float(result_or_scores["_meta"]["overall_score"])
            else:
                vals = [v for k, v in result_or_scores.items() if isinstance(v, (int, float))]
                avg = sum(vals) / max(1, len(vals)) if vals else 0.0
        else:
            avg = float(result_or_scores)
    except Exception:
        return "Не удалось определить уровень"

    if avg >= 85:
        return "🏆 Выдающийся лидер / Эксперт"
    if avg >= 70:
        return "🔥 Уверенный новатор / Продвинутый"
    if avg >= 55:
        return "📊 Командный игрок / Средний"
    if avg >= 40:
        return "📈 Перспективный участник / Ниже среднего"
    return "🌱 Начинающий исследователь"


# ─── Достижения ─────────────────────────────────────────────────────────────


def get_achievements(result_or_scores: Any) -> List[str]:
    """Достижения по чертам."""
    try:
        if isinstance(result_or_scores, dict) and "_meta" in result_or_scores:
            scores = {k: v for k, v in result_or_scores.items()
                      if k != "_meta" and isinstance(v, (int, float))}
        elif isinstance(result_or_scores, dict):
            scores = result_or_scores
        else:
            return []
    except Exception:
        return []

    out: List[str] = []
    for trait, v in scores.items():
        if v >= 85:
            out.append(f"🏆 {trait}: проявляется на выдающемся уровне!")
        elif v >= 72:
            out.append(f"⭐ {trait}: ваша сильная сторона.")

    if not out:
        out.append("У вас огромный потенциал для развития всех качеств!")
    return out


# ─── План развития ──────────────────────────────────────────────────────────

_IMPROVEMENT_ADVICE: Dict[str, Dict[str, str]] = {
    "Дисциплина": {
        "low": "Начните с правила 5 минут: делайте сложную задачу хотя бы 5 минут в день. Это формирует привычку.",
        "mid": "Попробуйте методику «Помодоро» для учебы или работы: 25 минут фокуса, 5 минут отдыха.",
        "high": "Вы отлично планируете время! Помогите организовать работу в команде или учебной группе.",
    },
    "Уверенность": {
        "low": "Рядом с рабочим столом повесьте список из 3 ваших главных успехов. Напоминайте себе о них.",
        "mid": "Берите инициативу в небольших делах: например, первым ответьте на сложный вопрос в группе.",
        "high": "Ваша уверенность заряжает других. Выступайте наставником для тех, кто сомневается в себе.",
    },
    "Лидерство": {
        "low": "Предложите взять на себя ответственность за небольшую часть школьного проекта или рабочей задачи.",
        "mid": "Учитесь слушать команду: настоящий лидер не только отдает команды, но и собирает идеи.",
        "high": "Развивайте стратегическое видение: куда ваш проект или команда должна прийти через полгода?",
    },
    "Креативность": {
        "low": "Попробуйте решать привычные задачи по-новому. Идите другим маршрутом, используйте новые форматы заметок.",
        "mid": "Практикуйте брейншторминг: записывайте 10 безумных идей для любого текущего проекта.",
        "high": "Вы генератор идей! Создавайте среду, где люди не боятся делиться даже самыми странными мыслями.",
    },
    "Эмпатия": {
        "low": "Тренируйте активное слушание: старайтесь понять эмоци собеседника до того, как давать советы.",
        "mid": "Спрашивайте однокурсников или коллег: «Как я могу тебя поддержать в этой задаче?»",
        "high": "Вы отлично чувствуете людей. Используйте этот навык для мирного разрешения конфликтов в коллективе.",
    },
    "Адаптивность": {
        "low": "Внедряйте мелкие изменения: попробуйте новый софт для учебы/работы или измените порядок утренних дел.",
        "mid": "При неожиданных изменениях спрашивайте себя: «Какие новые возможности мне это открывает?»",
        "high": "Вы гибки и легко перестраиваетесь. Помогайте другим не паниковать при внезапных сменах планов.",
    },
    "Коммуникация": {
        "low": "Учитесь формулировать мысль в 2 предложениях. Это полезно и для короткого эссе, и для резюме.",
        "mid": "Перед важным диалогом или презентацией заранее прописывайте 3 ключевые мысли, которые хотите донести.",
        "high": "Ваши навыки общения на высоте! Попробуйте вести дискуссионные группы или мастер-классы.",
    },
}


def get_improvement_plan(result_or_scores: Any) -> Dict[str, str]:
    """
    Генерирует персональный план развития.
    Для каждой черты — совет в зависимости от уровня.
    """
    if isinstance(result_or_scores, dict) and "_meta" in result_or_scores:
        scores = {k: v for k, v in result_or_scores.items()
                  if k != "_meta" and isinstance(v, (int, float))}
    elif isinstance(result_or_scores, dict):
        scores = {k: v for k, v in result_or_scores.items()
                  if isinstance(v, (int, float))}
    else:
        return {}

    plan: Dict[str, str] = {}
    # Сортируем: сначала слабые черты
    for trait, score in sorted(scores.items(), key=lambda x: x[1]):
        advice_map = _IMPROVEMENT_ADVICE.get(trait, {})
        if score < 40:
            plan[trait] = advice_map.get("low", "Работайте над этим навыком.")
        elif score < 70:
            plan[trait] = advice_map.get("mid", "Продолжайте совершенствоваться.")
        else:
            plan[trait] = advice_map.get("high", "Отличный уровень — поддерживайте!")

    return plan


# ─── Ежедневное задание ─────────────────────────────────────────────────────

_DAILY_CHALLENGES: Dict[str, List[str]] = {
    "Дисциплина": [
        "Составьте расписание на завтра и строго выполните первые 3 пункта.",
        "Заведите будильник на 10 минут раньше обычного и сделайте небольшую разминку.",
        "Уберите телефон на 1 час во время важной учебы или работы.",
    ],
    "Уверенность": [
        "Сделайте комплимент себе вслух перед зеркалом.",
        "Сегодня на занятиях или собрании задайте 1 вопрос спикеру.",
        "Выразите своё мнение по обсуждаемой теме, даже если оно отличается от большинства.",
    ],
    "Лидерство": [
        "Организуйте небольшую группу для совместного решения задачи.",
        "Помогите однокласснику или коллеге разобраться с тем, что вы уже хорошо знаете.",
        "Возьмите на себя ответственность за финальную проверку совместного документа.",
    ],
    "Креативность": [
        "Нарисуйте майнд-мап (карту мыслей) для вашего текущего проекта или выходного дня.",
        "Свяжите два несвязанных понятия. Например: как «космос» поможет улучшить «оценки/отчеты»?",
        "Напишите короткий рассказ из 5 предложений, где все слова начинаются на одну букву.",
    ],
    "Эмпатия": [
        "Искренне поинтересуйтесь у близкого или коллеги, как прошло его утро.",
        "Предложите помощь члену команды без его просьбы.",
        "Внимательно выслушайте человека, не перебивая минимум 3 минуты.",
    ],
    "Адаптивность": [
        "Выучите 5 новых терминов по вашей специализации или 1 новую формулу.",
        "Выполните привычную рутину совершенно по-другому.",
        "Прочитайте статью на тему, которой никогда раньше не интересовались.",
    ],
    "Коммуникация": [
        "Объясните сложное правило или задачу своими словами так, чтобы понял человек не из темы.",
        "Напишите структурированное сообщение: приветствие, суть в одном пункте, призыв к действию.",
        "Сделайте 3 искренних комплимента разным людям в течение дня.",
    ],
}


def get_daily_challenge(result_or_scores: Any) -> Dict[str, str]:
    """
    Выбирает ежедневное задание для 2 самых слабых черт.
    """
    if isinstance(result_or_scores, dict) and "_meta" in result_or_scores:
        scores = {k: v for k, v in result_or_scores.items()
                  if k != "_meta" and isinstance(v, (int, float))}
    elif isinstance(result_or_scores, dict):
        scores = {k: v for k, v in result_or_scores.items()
                  if isinstance(v, (int, float))}
    else:
        return {}

    sorted_traits = sorted(scores.items(), key=lambda x: x[1])
    challenges: Dict[str, str] = {}

    for trait, _ in sorted_traits[:2]:
        options = _DAILY_CHALLENGES.get(trait, ["Поработайте над этим навыком."])
        challenges[trait] = random.choice(options)

    return challenges
