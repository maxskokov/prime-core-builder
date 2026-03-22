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
        base = raw[trait] + per_trait_sentiment + diversity_bonus + length_bonus

        # Если есть хоть одно совпадение — минимум 20
        if hits[trait] > 0:
            base = max(base, 20.0)

        # Без совпадений — базовый «нейтральный» уровень 15-25
        # (текст написан, но черта не упомянута)
        if hits[trait] == 0 and total_hits > 0:
            base = max(base, 15.0)

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
        return "🏆 Сильный / Экспертный"
    if avg >= 70:
        return "🔥 Продвинутый"
    if avg >= 55:
        return "📊 Средний"
    if avg >= 40:
        return "📈 Ниже среднего"
    return "🌱 Начальный"


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
            out.append(f"🏆 {trait}: проявляется на высоком уровне!")
        elif v >= 72:
            out.append(f"⭐ {trait}: сильная сторона.")

    if not out:
        out.append("Явных сильных сторон пока не выявлено — есть точки роста.")
    return out


# ─── План развития ──────────────────────────────────────────────────────────

_IMPROVEMENT_ADVICE: Dict[str, Dict[str, str]] = {
    "Дисциплина": {
        "low": "Начните с составления простого списка задач на день. Выделяйте 3 приоритетные задачи каждое утро.",
        "mid": "Попробуйте методику тайм-блокинга: разбейте день на 25-минутные блоки (помодоро).",
        "high": "Вы уже дисциплинированы — помогите коллегам выстроить процессы.",
    },
    "Уверенность": {
        "low": "Фиксируйте свои успехи ежедневно — даже маленькие. Ведите «дневник побед».",
        "mid": "Практикуйте публичные выступления: начните с 2 минут перед 3 людьми.",
        "high": "Делитесь уверенностью — менторьте тех, кто сомневается в себе.",
    },
    "Лидерство": {
        "low": "Возьмите на себя организацию одного маленького проекта или встречи.",
        "mid": "Делегируйте: доверяйте задачи другим и давайте конструктивную обратную связь.",
        "high": "Развивайте стратегическое мышление — планируйте на горизонте 6-12 месяцев.",
    },
    "Креативность": {
        "low": "Попробуйте «мозговой штурм»: 10 идей за 5 минут, не фильтруя.",
        "mid": "Изучайте смежные области — свежие идеи рождаются на стыке дисциплин.",
        "high": "Создайте среду для инноваций в вашей команде: регулярные креатив-сессии.",
    },
    "Эмпатия": {
        "low": "Практикуйте активное слушание: не перебивайте, задавайте уточняющие вопросы.",
        "mid": "Старайтесь понять мотивацию собеседника, прежде чем давать советы.",
        "high": "Помогайте разрешать конфликты в команде — вы чувствуете настроение людей.",
    },
    "Адаптивность": {
        "low": "Каждую неделю пробуйте что-то новое: маршрут, инструмент, подход к задаче.",
        "mid": "При изменениях фокусируйтесь на возможностях, а не на потерях.",
        "high": "Помогайте другим адаптироваться — станьте «проводником» изменений.",
    },
    "Коммуникация": {
        "low": "Тренируйтесь формулировать мысль в 2–3 предложения: ясность > многословность.",
        "mid": "Практикуйте разные форматы: письменно, устно, визуально (схемы, диаграммы).",
        "high": "Проводите мини-тренинги по коммуникации для коллег.",
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
        "Составьте список из 5 задач на завтра и расставьте приоритеты.",
        "Проведите 25-минутный «помодоро» без отвлечений.",
        "Запишите вечером 3 выполненных дела за день.",
    ],
    "Уверенность": [
        "Выскажите своё мнение первым на следующей встрече.",
        "Запишите 3 вещи, в которых вы хороши.",
        "Скажите «нет» одной неважной просьбе сегодня.",
    ],
    "Лидерство": [
        "Предложите план действий коллеге, который просит совета.",
        "Возьмите организацию одной рабочей задачи на себя.",
        "Дайте конструктивный фидбэк одному человеку.",
    ],
    "Креативность": [
        "Придумайте 5 нестандартных применений обычного предмета.",
        "Запишите 3 идеи для улучшения вашего рабочего процесса.",
        "Посмотрите TED-лекцию на незнакомую тему.",
    ],
    "Эмпатия": [
        "Задайте коллеге вопрос «как ты?» и внимательно выслушайте.",
        "Поблагодарите кого-то за конкретную помощь.",
        "Попробуйте посмотреть на спорную ситуацию глазами оппонента.",
    ],
    "Адаптивность": [
        "Измените один привычный маршрут или процессу сегодня.",
        "Изучите одну новую функцию инструмента, которым пользуетесь каждый день.",
        "Спросите у коллеги, как он решает задачу, которую вы делаете по-другому.",
    ],
    "Коммуникация": [
        "Объясните сложную идею кому-то простым языком за 1 минуту.",
        "Напишите короткое сообщение с чёткой структурой: проблема → решение → просьба.",
        "Задайте 3 открытых вопроса в следующем разговоре.",
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
