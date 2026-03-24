import streamlit as st

def show_about_tab():
    # ── ПРЕМИУМ ДИЗАЙН С АНИМАЦИЕЙ СКРОЛЛА ──────────────────────────────────
    # Этот модуль отвечает за вкладку "О нейросети"
    
    st.markdown("""
    <style>
    /* Динамический скролл-ревил */
    @keyframes reveal {
        from { opacity: 0; transform: translateY(40px) scale(0.95); filter: blur(10px); }
        to { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
    }
    @keyframes fade-out {
        from { opacity: 1; transform: scale(1); filter: blur(0); }
        to { opacity: 0; transform: scale(0.9) translateY(-40px); filter: blur(10px); }
    }

    .scroll-block-container {
        height: 100vh;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
        view-timeline-name: --block-reveal;
        view-timeline-axis: block;
    }

    .glass-card {
        max-width: 800px;
        width: 90%;
        padding: 4rem;
        background: rgba(13, 14, 22, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 40px;
        text-align: center;
        position: sticky;
        top: 25vh;
        animation: reveal both, fade-out both;
        animation-timeline: --block-reveal;
        animation-range: entry 10% cover 40%, exit 60% exit 90%;
        box-shadow: 0 50px 100px -20px rgba(0,0,0,0.5);
    }

    .card-title { font-size: 3rem; font-weight: 700; margin-bottom: 1.5rem; letter-spacing: -0.02em; }
    .card-text { font-size: 1.3rem; color: #b0b0c0; line-height: 1.6; }
    
    .g-blue   { background: linear-gradient(90deg, #00C6FF, #0072FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .g-purple { background: linear-gradient(90deg, #9D50BB, #6E48AA); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .g-green  { background: linear-gradient(90deg, #11998E, #38EF7D); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>

    <div style="height: 60vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
        <h1 style="font-size: 4rem; font-weight: 800; letter-spacing: -0.05em; margin-bottom: 1rem;">Prime Core <span style='color:#00C6FF'>v2.0</span></h1>
        <p style="color: #889; font-size: 1.4rem; max-width: 600px;">Пролистайте вниз, чтобы увидеть магию анализа в действии.</p>
    </div>

    <!-- Блок 1 -->
    <div class="scroll-block-container">
        <div class="glass-card">
            <h2 class="card-title g-blue">Нейро-ядро.</h2>
            <p class="card-text">Наш алгоритм выполняет глубокий семантический разбор, анализируя вес фраз и скрытые паттерны вашего стиля. Каждое слово имеет значение.</p>
        </div>
    </div>

    <!-- Блок 2 -->
    <div class="scroll-block-container">
        <div class="glass-card">
            <h2 class="card-title g-purple">7 Измерений.</h2>
            <p class="card-text">Мы раскладываем вашу личность на 7 векторов: от дисциплины до эмпатии. Хаос слов превращается в четкую математическую модель личности.</p>
        </div>
    </div>

    <!-- Блок 3 -->
    <div class="scroll-block-container">
        <div class="glass-card">
            <h2 class="card-title g-green">Вектор Роста.</h2>
            <p class="card-text">Система генерирует персональный план развития и ежедневные челленджи, которые адаптируются под ваш текущий уровень успеха.</p>
        </div>
    </div>

    <div style="height: 20vh;"></div>
    """, unsafe_allow_html=True)
