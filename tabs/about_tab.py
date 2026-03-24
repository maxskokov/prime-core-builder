import streamlit as st
import streamlit.components.v1 as components

def show_about_tab():
    # ── ПРЕМИУМ ДИЗАЙН "BENTO GLASS" 3.0 ──
    # Используем st.components.v1.html для полной изоляции кода и плавности 60 FPS.
    # Больше никаких ошибок с выводом "сырого" кода!
    
    html_code = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&family=Montserrat:wght@900&display=swap" rel="stylesheet">
        <style>
            :root {
                --cyan: #00d1ff;
                --purple: #a200ff;
                --bg: #050505;
            }
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                background-color: transparent;
                color: #fff;
                font-family: 'Inter', sans-serif;
                overflow-x: hidden;
            }

            /* Контейнеры секций */
            section {
                height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                padding: 20px;
                position: relative;
            }

            /* Эффект свечения на фоне */
            .glow-bg {
                position: absolute;
                width: 40vw;
                height: 40vw;
                background: radial-gradient(circle, rgba(0, 209, 255, 0.1) 0%, transparent 70%);
                filter: blur(80px);
                z-index: -1;
                pointer-events: none;
            }

            /* Текстовые стили */
            .title {
                font-family: 'Montserrat', sans-serif;
                font-size: 4rem;
                font-weight: 900;
                margin-bottom: 2rem;
                letter-spacing: -2px;
                line-height: 1;
                background: linear-gradient(90deg, #fff, #bbb);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .accent-cyan { background: linear-gradient(90deg, var(--cyan), #0072ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
            .accent-purple { background: linear-gradient(90deg, var(--purple), #ff00d1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

            .description {
                font-size: 1.5rem;
                color: #aaa;
                line-height: 1.6;
                font-weight: 300;
            }

            /* Премиум карточка (Bento/Glass) */
            .glass-card {
                background: rgba(20, 25, 35, 0.7);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 40px;
                padding: 60px;
                max-width: 900px;
                width: 90%;
                box-shadow: 0 50px 100px -20px rgba(0,0,0,0.6);
                transition: transform 0.6s cubic-bezier(0.23, 1, 0.32, 1), opacity 0.6s ease;
                opacity: 0.2;
                transform: scale(0.9);
            }

            /* Простая JS анимация появления (вместо view-timeline для совместимости) */
            .glass-card.visible { opacity: 1; transform: scale(1); }

            .scroll-hint {
                margin-top: 50px;
                font-size: 0.8rem;
                letter-spacing: 4px;
                color: var(--cyan);
                animation: pulse 2s infinite;
            }
            @keyframes pulse { 0%, 100% { opacity: 0.3; transform: translateY(0); } 50% { opacity: 1; transform: translateY(10px); } }
        </style>
    </head>
    <body onscroll="handleScroll()">

        <section>
            <div class="glow-bg" style="top: 10%; left: 20%;"></div>
            <h1 class="title" style="font-size: 5.5rem;">Prime Core <br><span class="accent-cyan">BUILDER</span></h1>
            <p class="description" style="max-width: 600px;">Ваш персональный архитектор личности на базе ИИ.</p>
            <div class="scroll-hint">ЛИСТАЙ ВНИЗ ▼</div>
        </section>

        <section>
            <div class="glass-card" id="card1">
                <h2 class="title accent-cyan">Глубокий Анализ.</h2>
                <p class="description">Мы не просто считаем слова. Наша нейросеть понимает <b>контекст</b>, <b>эмоции</b> и <b>скрытые таланты</b>. Мы видим то, что пропускают обычные тесты.</p>
            </div>
        </section>

        <section>
            <div class="glow-bg" style="bottom: 10%; right: 20%; background: radial-gradient(circle, rgba(162, 0, 255, 0.1) 0%, transparent 70%);"></div>
            <div class="glass-card" id="card2">
                <h2 class="title accent-purple">7 Измерений.</h2>
                <p class="description">Ваш потенциал разложен на <b>7 векторов развития</b>. От лидерства до креативности — создайте четкую карту своих сильных сторон.</p>
            </div>
        </section>

        <section>
            <div class="glass-card" id="card3">
                <h2 class="title" style="background: linear-gradient(90deg, #fceabb, #f8b500); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">План Победы.</h2>
                <p class="description">Система дает <b>персональные задания</b> на каждый день, помогая вам расти там, где это нужнее всего в данный момент.</p>
            </div>
        </section>

        <script>
            function handleScroll() {
                const cards = document.querySelectorAll('.glass-card');
                cards.forEach(card => {
                    const rect = card.getBoundingClientRect();
                    if (rect.top < window.innerHeight * 0.75) {
                        card.classList.add('visible');
                    }
                });
            }
            window.addEventListener('scroll', handleScroll);
            handleScroll(); // Initial check
        </script>
    </body>
    </html>
    """
    
    # Высота для скролла
    components.html(html_code, height=2500, scrolling=False)
