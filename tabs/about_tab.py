import streamlit as st

def show_about_tab():
    # ── ДИЗАЙН-СИСТЕМА STITCH: "OBSIDIAN PULSE" ──
    # Чистый, элитный дизайн без лишних дат и версий.
    # Используем асимметричную сетку Bento и тональные переходы.
    
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
padding: 80px 20px;
position: relative;
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
font-size: clamp(3.5rem, 8vw, 7rem);
font-weight: 900;
line-height: 0.85;
letter-spacing: -0.04em;
color: #e5e2e3;
margin-bottom: 24px;
}
.obsidian-label {
font-family: 'Space Grotesk', sans-serif;
text-transform: uppercase;
letter-spacing: 0.3em;
font-size: 0.75rem;
color: #00f0ff;
margin-bottom: 16px;
font-weight: 500;
}
.obsidian-p {
font-family: 'Inter', sans-serif;
font-size: 1.25rem;
color: #b9cacb;
max-width: 650px;
line-height: 1.6;
font-weight: 300;
}
.bento-layout {
display: grid;
grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
gap: 20px;
max-width: 1200px;
width: 100%;
margin-top: 60px;
}
.bento-box {
background: rgba(28, 27, 28, 0.4);
backdrop-filter: blur(40px);
border: 1px solid rgba(255, 255, 255, 0.05);
border-radius: 32px;
padding: 48px;
text-align: left;
transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
animation: reveal-obsidian both;
animation-timeline: --obsidian;
animation-range: entry 15% cover 45%;
}
.bento-box:hover {
background: rgba(35, 34, 35, 0.6);
border-color: rgba(0, 240, 255, 0.2);
transform: translateY(-8px);
}
@keyframes reveal-obsidian {
0% { opacity: 0; transform: translateY(60px) scale(0.96); }
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
width: 64px; height: 64px;
background: url('https://img.icons8.com/wired/64/00f0ff/shield--v1.png') no-repeat center/contain;
margin-bottom: 32px;
filter: drop-shadow(0 0 8px rgba(0, 240, 255, 0.3));
}
</style>
<div class="obsidian-section">
<div class="pulse-orb" style="top: -10%; left: 20%;"></div>
<div class="obsidian-label">Advanced Intelligence</div>
<h1 class="obsidian-h1">Engineering <br>The Future.</h1>
<p class="obsidian-p">Prime Core Builder — это симбиоз нейронауки и искусственного интеллекта, созданный для раскрытия вашего истинного потенциала.</p>
</div>
<div class="obsidian-section">
<div class="obsidian-label">System Architecture</div>
<div class="bento-layout">
<div class="bento-box glow-edge" style="grid-column: span 2;">
<h3 class="obsidian-h1" style="font-size: 2.5rem; margin-bottom: 16px;">NLP Engine</h3>
<p class="obsidian-p">Семантический анализ в реальном времени. Мы понимаем не только слова, но и тональность, контекст и глубинные психологические паттерны вашего текста.</p>
</div>
<div class="bento-box">
<h3 class="obsidian-h1" style="font-size: 2.5rem; margin-bottom: 16px;">Efficiency</h3>
<p class="obsidian-p">Выполнение сложнейших алгоритмов за миллисекунды. Скорость, которая не заставляет ждать.</p>
</div>
</div>
</div>
<div class="obsidian-section" style="background-color: #0e0e0f;">
<div class="pulse-orb" style="bottom: 10%; right: 10%; background: radial-gradient(circle, rgba(157, 5, 255, 0.05) 0%, transparent 70%);"></div>
<div class="shield-pulse"></div>
<div class="obsidian-label">Data Integrity</div>
<h1 class="obsidian-h1" style="font-size: 4.5rem;">Enterprise-Grade <br>Security.</h1>
<div class="bento-layout">
<div class="bento-box">
<h2 class="obsidian-h1" style="font-size: 2rem;">AES-256 Protocol</h2>
<p class="obsidian-p">Ваши данные зашифрованы по стандартам профессионального уровня. Приватность — это не опция, а фундамент нашей системы.</p>
</div>
<div class="bento-box">
<h2 class="obsidian-h1" style="font-size: 2rem;">Anon Privacy</h2>
<p class="obsidian-p">Полная анонимизация входящих потоков. Мы анализируем смыслы, не собирая персональные данные пользователей.</p>
</div>
</div>
</div>
<div class="obsidian-section">
<h1 class="obsidian-h1" style="font-size: 3rem; color: #4b5563;">Prime Core Architecture</h1>
<div style="margin-top: 32px; font-family: 'Space Grotesk', sans-serif; color: #313031; letter-spacing: 0.5em;">INTELLIGENCE WITHOUT COMPROMISE</div>
</div>
""", unsafe_allow_html=True)
