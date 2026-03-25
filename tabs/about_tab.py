import streamlit as st

def show_about_tab():
    # ── ПЕРЕРАБОТАННАЯ ВКЛАДКА "О НЕЙРОСЕТИ" ──
    # Простой текст, плавные смены, никаких лишних слов.
    
    st.markdown("""
<style>
/* Чистый темный фон */
.stApp { background-color: #050505; }

/* Скрываем стандартные элементы */
#MainMenu, footer, header { visibility: hidden; }

/* Контейнеры секций */
.about-section {
    min-height: 80vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 2rem;
    position: relative;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.about-title {
    font-family: 'Montserrat', sans-serif;
    font-size: clamp(2.5rem, 8vw, 4.5rem);
    font-weight: 900;
    line-height: 1.1;
    background: linear-gradient(90deg, #00d1ff, #a200ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 30px;
}

.about-p {
    font-family: 'Inter', sans-serif;
    font-size: 1.5rem;
    color: #b9cacb;
    max-width: 750px;
    line-height: 1.6;
    font-weight: 300;
}

.tech-detail {
    margin-top: 40px;
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: 0.3em;
    font-size: 0.9rem;
    color: #4b5563;
    text-transform: uppercase;
}

.highlight {
    color: #00d1ff;
    font-weight: 600;
}

/* Анимация плавного появления */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(40px); }
    to { opacity: 1; transform: translateY(0); }
}

.about-section {
    animation: fadeInUp 1.2s ease-out both;
}

</style>

<!-- Секция 1: Главная -->
<div class="about-section">
    <div class="about-title">Простота и <br>Аналитика.</div>
    <p class="about-p">
        Prime Core Builder — это персональный помощник, который анализирует ваш текст и помогает увидеть объективную картину ваших сильных сторон.
    </p>
    <div class="tech-detail">MODERN AI ARCHITECTURE</div>
</div>

<!-- Секция 2: Безопасность -->
<div class="about-section">
    <div class="about-title">Надежная <br>Защита.</div>
    <p class="about-p">
        Безопасность — наш приоритет. Все пароли пользователей шифруются методом <span class="highlight">2FJFJS</span>. Мы гарантируем полную приватность ваших данных.
    </p>
    <div class="tech-detail">PROPRIETARY ENCRYPTION</div>
</div>

<!-- Секция 3: Анализ -->
<div class="about-section">
    <div class="about-title">Точный <br>Результат.</div>
    <p class="about-p">
        Нейросеть выявляет в тексте скрытые паттерны <span class="highlight">лидерства</span>, <span class="highlight">дисциплины</span> и <span class="highlight">эмпатии</span>. Объективный взгляд на ваши таланты без искажений.
    </p>
    <div class="tech-detail">CORE TRAIT ANALYZER</div>
</div>

<!-- Секция 4: Инфраструктура -->
<div class="about-section">
    <div class="about-title">Облачная <br>Синхронизация.</div>
    <p class="about-p">
        Благодаря системе <span class="highlight">Supabase</span> ваши результаты мгновенно сохраняются и доступны с любого устройства — будь то смартфон или компьютер.
    </p>
    <div class="tech-detail">HYBRID CLOUD STORAGE</div>
</div>

<div style="height: 10vh; text-align: center; color: #1f2937; padding: 20px;">
    PRIME CORE BUILDER (C) 2026
</div>
""", unsafe_allow_html=True)
