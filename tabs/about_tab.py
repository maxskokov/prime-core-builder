import streamlit as st

def show_about_tab():
    # ── ПРЕМИУМ ЛЕНДИНГ "ULTIMATE CORE" 5.0 ──
    # Этот вариант — полноценная презентация для жюри. 
    # Дизайн мирового уровня: Bento Grid, Cyber-Shield, Parallax.
    
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&family=Montserrat:wght@900&display=swap');

.stApp { overflow-x: hidden; scroll-behavior: smooth; }

/* ОБЩИЕ СТИЛИ СЕКЦИЙ */
.presentation-section {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    position: relative;
    padding: 60px 20px;
    view-timeline-name: --view;
    view-timeline-axis: block;
}

/* ФОНОВЫЕ ЭФФЕКТЫ */
.cyber-grid {
    position: absolute;
    width: 200%;
    height: 200%;
    background-image: linear-gradient(rgba(0, 209, 255, 0.05) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(0, 209, 255, 0.05) 1px, transparent 1px);
    background-size: 50px 50px;
    transform: perspective(500px) rotateX(60deg);
    top: -50%;
    z-index: -2;
    animation: grid-move 20s linear infinite;
}
@keyframes grid-move { from { background-position: 0 0; } to { background-position: 0 1000px; } }

.glow-orb {
    position: absolute;
    width: 40vw;
    height: 40vw;
    background: radial-gradient(circle, rgba(0, 209, 255, 0.15) 0%, transparent 70%);
    filter: blur(100px);
    z-index: -1;
    pointer-events: none;
}

/* ЗАГОЛОВКИ */
.hero-title {
    font-family: 'Montserrat', sans-serif;
    font-size: clamp(3rem, 10vw, 6rem);
    font-weight: 1000;
    line-height: 0.9;
    letter-spacing: -5px;
    margin-bottom: 20px;
    background: linear-gradient(135deg, #fff, #555);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.accent { background: linear-gradient(135deg, #00d1ff, #a200ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

/* BENTO GRID */
.bento-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 25px;
    max-width: 1200px;
    width: 100%;
    margin-top: 50px;
}

.bento-card {
    background: rgba(15, 20, 30, 0.5);
    backdrop-filter: blur(30px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 40px;
    padding: 40px;
    text-align: left;
    transition: all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
    
    animation: reveal-bento both;
    animation-timeline: --view;
    animation-range: entry 10% cover 40%;
}

@keyframes reveal-bento {
    0% { opacity: 0; transform: translateY(100px) scale(0.9); }
    100% { opacity: 1; transform: translateY(0) scale(1); }
}

.bento-card:hover { 
    border-color: #00d1ff; 
    box-shadow: 0 30px 60px -20px rgba(0, 209, 255, 0.3); 
    transform: translateY(-10px);
}

/* КИБЕРБЕЗОПАСНОСТЬ: АНИМАЦИЯ ЩИТА */
.shield-icon {
    width: 80px;
    height: 80px;
    margin-bottom: 25px;
    background: url('https://img.icons8.com/isometric/100/shield.png') no-repeat center/contain;
    filter: drop-shadow(0 0 10px #00d1ff);
    animation: shield-pulse 3s infinite;
}
@keyframes shield-pulse { 0%, 100% { transform: scale(1); filter: brightness(1); } 50% { transform: scale(1.1); filter: brightness(1.5) drop-shadow(0 0 20px #00d1ff); } }

/* ТЕКСТ */
.bento-h { font-size: 2rem; font-weight: 900; color: #fff; margin-bottom: 15px; }
.bento-p { font-size: 1.1rem; color: #9ca3af; line-height: 1.5; font-weight: 300; }

.scroll-indicator {
    margin-top: 60px;
    font-size: 0.9rem;
    letter-spacing: 5px;
    color: #444;
    animation: arrow-down 2s infinite;
}
@keyframes arrow-down { 0% {transform:translateY(0); color:#444;} 50% {transform:translateY(15px); color:#00d1ff;} 100% {transform:translateY(0); color:#444;} }
</style>

<!-- СЕКЦИЯ 1: ХЕРО -->
<div class="presentation-section">
    <div class="cyber-grid"></div>
    <div class="glow-orb" style="top:20%; left:30%;"></div>
    <h1 class="hero-title">Prime Core <br><span class="accent">ARCHITECT</span></h1>
    <p style="font-size: 1.8rem; color: #6b7280; max-width: 800px; font-weight: 300;">Ваш персональный путеводитель в мир потенциала и безопасности.</p>
    <div class="scroll-indicator">ПРЕЗЕНТАЦИЯ ▼</div>
</div>

<!-- СЕКЦИЯ 2: КИБЕРБЕЗОПАСНОСТЬ (УДИВЛЯЕМ ЖЮРИ) -->
<div class="presentation-section" style="background: radial-gradient(circle at center, #0a1120 0%, #050505 100%);">
    <div class="glow-orb" style="right:10%; top:20%; background: radial-gradient(circle, rgba(162, 0, 255, 0.1) 0%, transparent 70%);"></div>
    <div class="shield-icon"></div>
    <h2 class="hero-title" style="font-size: 4rem;">Приватность — <br><span class="accent">Наш Приоритет.</span></h2>
    
    <div class="bento-container">
        <div class="bento-card">
            <h3 class="bento-h">Анонимизация данных</h3>
            <p class="bento-p">Все анализируемые тексты проходят через фильтр анонимности. Мы не храним ваши личные данные — только чистую аналитику смыслов.</p>
        </div>
        <div class="bento-card">
            <h3 class="bento-h">AES-256 Шифрование</h3>
            <p class="bento-p">Передача результатов анализа в облако защищена промышленными стандартами шифрования. Ваши мысли остаются только вашими.</p>
        </div>
    </div>
</div>

<!-- СЕКЦИЯ 3: ЯДРО ИИ (ТЕХНОЛОГИЧНОСТЬ) -->
<div class="presentation-section">
    <h2 class="hero-title" style="font-size: 4rem;">Интеллект <br><span class="accent">Нового Поколения.</span></h2>
    
    <div class="bento-container">
        <div class="bento-card" style="grid-column: span 2;">
            <h3 class="bento-h">Семантический NLP-Движок</h3>
            <p class="bento-p">Мы используем продвинутые алгоритмы обработки естественного языка (NLP) для выявления скрытых паттернов поведения, лидерских качеств и креативного потенциала.</p>
        </div>
        <div class="bento-card">
            <h3 class="bento-h">Мгновенный отклик</h3>
            <p class="bento-p">Анализ текста объемом в тысячи слов занимает менее 1 секунды. Технологии Streamlit обеспечивают максимальную плавность работы.</p>
        </div>
    </div>
</div>

<!-- СЕКЦИЯ 4: ФИНАЛ -->
<div class="presentation-section">
    <h2 class="hero-title">Готовы к <br><span class="accent">Будущему?</span></h2>
    <div style="margin-top: 40px; font-size: 1.5rem; color: #4b5563;">Prime Core: Builder v2.0 • 2024</div>
</div>
""", unsafe_allow_html=True)
