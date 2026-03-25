import streamlit as st

def show_about_tab():
    # ── OBSIDIAN PULSE 7.0: ГЕОМЕТРИЯ И РУССКИЙ ЯЗЫК ──
    # Исправляем выравнивание карточек и переводим интерфейс.
    
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&family=Space+Grotesk:wght@300;400;500;700&display=swap');
.stApp { background-color: #0e0e0f; overflow-x: hidden; }
.obsidian-section {
min-height: 100vh;
display: flex;
flex-direction: column;
justify-content: center;
align-items: center;
padding: 100px 30px;
position: relative;
text-align: center;
view-timeline-name: --obsidian;
view-timeline-axis: block;
}
.pulse-orb {
position: absolute;
width: 50vw;
height: 50vw;
background: radial-gradient(circle, rgba(0, 240, 255, 0.07) 0%, transparent 70%);
filter: blur(120px);
z-index: -1;
pointer-events: none;
}
.obsidian-h1 {
font-family: 'Inter', sans-serif;
font-size: clamp(3rem, 7vw, 6rem);
font-weight: 900;
line-height: 0.9;
letter-spacing: -0.04em;
color: #e5e2e3;
margin-bottom: 24px;
margin-left: auto;
margin-right: auto;
}
.obsidian-label {
font-family: 'Space Grotesk', sans-serif;
text-transform: uppercase;
letter-spacing: 0.4em;
font-size: 0.8rem;
color: #00f0ff;
margin-bottom: 24px;
font-weight: 500;
}
.obsidian-p {
font-family: 'Inter', sans-serif;
font-size: 1.25rem;
color: #b9cacb;
max-width: 750px;
line-height: 1.6;
font-weight: 300;
margin-left: auto;
margin-right: auto;
}
.bento-layout {
display: grid;
grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
gap: 30px;
max-width: 1100px;
width: 100%;
margin-top: 60px;
margin-left: auto;
margin-right: auto;
}
.bento-box {
background: rgba(28, 27, 28, 0.4);
backdrop-filter: blur(40px);
border: 1px solid rgba(255, 255, 255, 0.05);
border-radius: 40px;
padding: 50px;
text-align: left;
transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
animation: reveal-obsidian both;
animation-timeline: --obsidian;
animation-range: entry 10% cover 40%;
display: flex;
flex-direction: column;
justify-content: space-between;
}
.bento-box:hover {
background: rgba(35, 34, 35, 0.6);
border-color: rgba(0, 240, 255, 0.2);
transform: translateY(-10px);
}
@keyframes reveal-obsidian {
0% { opacity: 0; transform: translateY(80px) scale(0.95); }
100% { opacity: 1; transform: translateY(0) scale(1); }
}
.glow-edge { position: relative; overflow: hidden; }
.glow-edge::after {
content: "";
position: absolute;
top: 0; left: 0; right: 0; height: 1px;
background: linear-gradient(90deg, transparent, rgba(0, 240, 255, 0.4), transparent);
}
.shield-pulse {
width: 60px; height: 60px;
background: url('https://img.icons8.com/wired/64/00f0ff/shield--v1.png') no-repeat center/contain;
margin-bottom: 24px;
filter: drop-shadow(0 0 10px rgba(0, 240, 255, 0.4));
animation: pulse-shield 3s infinite;
}
@keyframes pulse-shield { 0%, 100% {opacity: 1;} 50% {opacity: 0.6;} }
</style>
<div class="obsidian-section">
<div class="pulse-orb" style="top: -10%; left: 20%;"></div>
<div class="lottie-container" style="width: 300px; height: 300px; margin-bottom: 20px;">
    <iframe src="https://lottie.host/embed/84c3b7f1-2856-4b8c-85a0-044439c719e5/f1vB67z87H.json" style="border: none; width: 100%; height: 100%;"></iframe>
</div>
<div class="obsidian-label">Интеллект Будущего</div>
<h1 class="obsidian-h1">Prime Core <br>Builder.</h1>
<p class="obsidian-p">Симбиоз нейросетевого анализа и психометрики, созданный для раскрытия вашего истинного потенциала через текст.</p>
</div>
<div class="obsidian-section">
<div class="obsidian-label">Архитектура Системы</div>
<div class="bento-layout">
<div class="bento-box glow-edge" style="grid-column: span 2;">
<div>
<h3 class="obsidian-h1" style="font-size: 2.5rem; text-align: left; margin-bottom: 16px;">Ядро NLP</h3>
<p class="obsidian-p" style="text-align: left; margin: 0;">Семантический анализ в реальном времени. Мы понимаем не только слова, но и тональность, контекст и глубинные психологические паттерны вашего текста.</p>
</div>
</div>
<div class="bento-box">
<div>
<h3 class="obsidian-h1" style="font-size: 2.5rem; text-align: left; margin-bottom: 16px;">Скорость</h3>
<p class="obsidian-p" style="text-align: left; margin: 0;">Выполнение сложнейших алгоритмов за миллисекунды. Технологии, которые не заставляют ждать.</p>
</div>
</div>
</div>
</div>
<div class="obsidian-section" style="background-color: #0e0e0f;">
<div class="pulse-orb" style="bottom: 10%; right: 10%; background: radial-gradient(circle, rgba(157, 5, 255, 0.05) 0%, transparent 70%);"></div>
<div class="shield-pulse" style="margin-left: auto; margin-right: auto;"></div>
<div class="obsidian-label">Безопасность Данных</div>
<h1 class="obsidian-h1" style="font-size: 4rem;">Промышленная <br>Защита.</h1>
<div class="bento-layout">
<div class="bento-box">
<div>
<h2 class="obsidian-h1" style="font-size: 2rem; text-align: left;">Протокол AES</h2>
<p class="obsidian-p" style="text-align: left; margin: 0;">Ваши данные зашифрованы по стандартам высшего уровня. Приватность — это не опция, а фундамент нашей системы.</p>
</div>
</div>
<div class="bento-box">
<div>
<h2 class="obsidian-h1" style="font-size: 2rem; text-align: left;">Анонимность</h2>
<p class="obsidian-p" style="text-align: left; margin: 0;">Полная анонимизация входящих потоков. Мы анализируем смыслы, никогда не собирая ваши персональные данные.</p>
</div>
</div>
</div>
</div>
<div class="obsidian-section">
<h1 class="obsidian-h1" style="font-size: 3rem; color: #4b5563;">Prime Core Architect</h1>
<div style="margin-top: 32px; font-family: 'Space Grotesk', sans-serif; color: #313031; letter-spacing: 0.5em;">ИНТЕЛЛЕКТ БЕЗ КОМПРОМИССОВ</div>
</div>
""", unsafe_allow_html=True)
