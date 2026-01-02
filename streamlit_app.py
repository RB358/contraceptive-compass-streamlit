from pathlib import Path
import base64
import streamlit as st
import streamlit.components.v1 as components

from core.methods_data import METHODS, TELEHEALTH_OPTIONS
from core.schema import QUIZ_QUESTIONS, encode_answers
from core.quiz_logic import get_recommendations
from core.render_helpers import format_telehealth_link
from ui_components import start_cta

st.set_page_config(
    page_title="Find the contraceptive that fits you — in seven questions",
    layout="centered"
)

CSS_PATH = Path(__file__).resolve().parent / "styles.css"
if CSS_PATH.exists():
    st.markdown(f"<style>{CSS_PATH.read_text()}</style>", unsafe_allow_html=True)

BOOK_URL = "https://www.plannedparenthood.org/health-center"

if "started" not in st.session_state:
    st.session_state.started = False
if "q_idx" not in st.session_state:
    st.session_state.q_idx = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "show_results" not in st.session_state:
    st.session_state.show_results = False
if "selected_method_id" not in st.session_state:
    st.session_state.selected_method_id = None

QUESTION_IDS = list(QUIZ_QUESTIONS.keys())
NUM_QUESTIONS = len(QUESTION_IDS)

TIER_CONFIG = {
    "best": {
        "title": "Best match",
        "badge": "Best match",
        "icon": "✓",
        "class": "badge-best",
        "microcopy": "Tends to align with your answers. Review key details below."
    },
    "consider": {
        "title": "Worth considering",
        "badge": "Worth considering",
        "icon": "◯",
        "class": "badge-consider",
        "microcopy": "May suit you depending on preferences and tolerability."
    },
    "unlikely": {
        "title": "Less likely to be suitable",
        "badge": "Less likely",
        "icon": "—",
        "class": "badge-unlikely",
        "microcopy": "Based on your answers, this option is less likely to fit. Consider discussing with a clinician if interested."
    }
}

CATEGORY_MAP = {
    "recommended": "best",
    "caution": "consider",
    "contraindicated": "unlikely"
}

def get_method_id(method):
    return method["name"].lower().replace(" ", "_").replace("(", "").replace(")", "").replace(",", "")

IMG_PATH = Path(__file__).resolve().parent / "Assets" / "iStock-contraceptives2.jpg"
hero_base64 = base64.b64encode(IMG_PATH.read_bytes()).decode()

hero_margin = "12px" if st.session_state.started else "0"
start_btn_offset = -80 if st.session_state.started else -70

st.markdown(f"""
<style>
:root {{
    --teal: #0F766E;
    --teal-600: #0B5F59;
    --coral: #D1495B;
    --coral-hover: #E06372;
    --ink: #211816;
    --surface: #FFFFFF;
    --warm-bg: #FFFBFA;
    --border: #E5E7EB;
    --mint: #74B89A;
    --mint-bg: rgba(116,184,154,0.10);
    --mint-bg-hover: rgba(116,184,154,0.14);
    --mint-border: rgba(116,184,154,0.55);
    --mint-border-strong: rgba(116,184,154,0.95);
}}

.stApp, .main {{
    background: var(--warm-bg) !important;
    color: var(--ink);
}}

header[data-testid="stHeader"] {{
    display: none !important;
}}

.cc-landing {{
    display: grid;
    grid-template-rows: 1fr auto;
    height: 100vh;
    height: 100dvh;
    overflow: hidden;
    box-sizing: border-box;
    padding-bottom: 72px;
}}

.cc-landing-bottom {{
    padding: 0 16px 8px 16px;
}}

.cc-landing-active .stApp {{
    height: 100vh !important;
    height: 100dvh !important;
    overflow: hidden !important;
}}

.cc-landing-active section.main {{
    overflow: hidden !important;
}}

.cc-landing-active section.main > div {{
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}}

.hero {{
    position: relative;
    width: 100%;
    height: 100%;
    min-height: 0;
    border-radius: 20px;
    overflow: hidden;
    background-image: url("data:image/jpeg;base64,{hero_base64}");
    background-size: cover;
    background-position: center 35%;
}}

.hero-landing {{
    margin-bottom: 0;
}}

.hero-started {{
    height: clamp(120px, 20vh, 160px);
    margin-bottom: 12px;
}}

.hero::after {{
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    background: linear-gradient(
        rgba(0, 0, 0, 0.20),
        rgba(0, 0, 0, 0.35)
    );
}}

.hero-content {{
    position: relative;
    z-index: 2;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 24px 28px;
    color: white;
}}

.hero h1 {{
    font-size: clamp(1.5rem, 5vw, 2.7rem);
    font-weight: 700;
    margin-bottom: 0;
    line-height: 1.2;
}}

.hero-landing .hero-content {{
    justify-content: center;
}}

.start-cta-wrapper {{
    margin-top: -50px !important;
    text-align: center;
}}

.landing-disclaimer {{
    text-align: center;
    font-size: 0.8rem;
    color: rgba(15,23,42,0.65);
    padding: 6px 0 0 0;
    margin: 0;
    line-height: 1.4;
}}

@media (max-height: 600px) {{
    .landing-disclaimer {{
        font-size: 0.7rem;
        padding: 4px 0 0 0;
    }}
    .cc-landing {{
        padding-bottom: 64px;
    }}
}}

h1, h2, h3 {{
    color: var(--teal);
    font-family: 'Helvetica Neue', sans-serif;
}}

.stButton > button {{
    background: var(--teal) !important;
    border: 1px solid var(--teal) !important;
    color: white !important;
    border-radius: 999px;
    padding: 10px 18px;
    font-weight: bold;
}}

.stButton > button:hover {{
    background: var(--teal-600) !important;
    border-color: var(--teal-600) !important;
}}

.cc-quiz button[data-testid="baseButton-secondary"],
.cc-quiz .stButton > button {{
    background: var(--mint-bg) !important;
    border: 1px solid var(--mint-border) !important;
    color: var(--ink) !important;
    border-radius: 12px !important;
    padding: 14px 16px !important;
    font-weight: 500 !important;
    text-align: left !important;
    transition: all 0.15s ease !important;
}}

.cc-quiz button[data-testid="baseButton-secondary"]:hover,
.cc-quiz .stButton > button:hover {{
    border-color: var(--mint-border-strong) !important;
    background: var(--mint-bg-hover) !important;
}}

.main .block-container {{
    max-width: 90% !important;
    padding-left: 5% !important;
    padding-right: 5% !important;
    padding-top: 2rem !important;
}}

h1, h2, h3, h4, .stMarkdown, p, div {{text-align: center !important;}}

.stButton {{text-align: center !important;}}

div.stButton {{text-align: center !important;}}

.stButton > button {{
    display: inline-block !important;
    margin: 10px auto !important;
}}

.stSelectbox, .stMultiselect {{
    margin: 0 auto !important;
    max-width: 400px !important;
}}

@media (min-width: 768px) {{
    .main .block-container {{max-width: 700px !important;}}
}}

.progress-text {{
    color: var(--coral);
    font-size: 0.95rem;
    font-weight: 600;
    margin: 0 0 4px 0 !important;
}}

div[data-testid="stProgress"] {{
    margin-bottom: 8px !important;
}}

.quiz-container {{
    max-width: 480px;
    width: 100%;
    margin: 0 auto;
    padding: 0 16px;
}}

.quiz-question {{
    font-size: 1.35rem !important;
    font-weight: 700 !important;
    line-height: 1.35 !important;
    color: var(--ink) !important;
    margin: 16px 0 8px 0 !important;
    text-align: center !important;
}}

.quiz-help {{
    font-size: 0.9rem;
    color: rgba(15, 23, 42, 0.65);
    margin: 0 0 20px 0 !important;
    text-align: center !important;
}}

.cc-tile {{
    display: block;
    width: 100%;
    padding: 16px 20px;
    margin: 8px 0;
    background: var(--surface);
    border: 2px solid var(--border);
    border-radius: 16px;
    font-size: 1rem;
    font-weight: 500;
    color: var(--ink);
    text-align: left !important;
    cursor: pointer;
    transition: all 0.15s ease;
}}

.cc-tile:hover {{
    border-color: var(--teal);
    background: rgba(15, 118, 110, 0.04);
}}

.cc-tile--selected {{
    border-color: var(--teal) !important;
    border-width: 2.5px !important;
    background: rgba(15, 118, 110, 0.08) !important;
}}

.cc-tile--selected::before {{
    content: "✓ ";
    color: var(--teal);
    font-weight: 700;
}}

.restart-link {{
    font-size: 0.85rem;
    color: rgba(15, 23, 42, 0.5);
    text-align: right !important;
    margin: 4px 0 16px 0 !important;
}}

.restart-link:hover {{
    color: var(--coral);
}}

.quiz-nav {{
    margin-top: 24px;
}}

.quiz-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
    margin: 20px auto;
    max-width: 500px;
}}

.accent {{
    color: var(--coral);
}}

.accent-bg {{
    background: rgba(209, 73, 91, 0.10);
    border: 1px solid rgba(209, 73, 91, 0.25);
    border-radius: 14px;
    padding: 16px 20px;
    text-align: center;
    margin: 0 auto 24px auto;
    max-width: 400px;
}}

.accent-bg strong {{
    color: var(--coral);
    font-size: 1rem;
}}

.accent-bg span {{
    color: var(--ink);
    font-size: 0.85rem;
    opacity: 0.8;
}}

.accent-bg .chevron {{
    color: var(--coral);
    font-size: 1.3rem;
    display: block;
    margin-top: 8px;
    animation: bounce 1.5s infinite;
}}

@keyframes bounce {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(6px); }}
}}

.category-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 16px;
    margin: 12px 0;
}}

.category-title {{
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--ink);
    margin: 0 0 4px 0;
    text-align: left !important;
}}

.category-sub {{
    margin: 0 0 12px 0;
    color: rgba(15, 23, 42, 0.75);
    font-size: 0.95rem;
    text-align: left !important;
}}

.badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    border-radius: 999px;
    padding: 7px 12px;
    font-size: 0.8rem;
    font-weight: 650;
    border: 1px solid var(--border);
    background: rgba(255,255,255,0.8);
}}

.badge-best {{
    border-color: rgba(15, 118, 110, 0.35);
    color: var(--teal);
    background: rgba(15, 118, 110, 0.08);
}}

.badge-consider {{
    border-color: rgba(51, 65, 85, 0.35);
    color: rgba(51, 65, 85, 0.95);
    background: rgba(51, 65, 85, 0.08);
}}

.badge-unlikely {{
    border-color: rgba(209, 73, 91, 0.35);
    color: var(--coral);
    background: rgba(209, 73, 91, 0.08);
}}

.rec-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    padding: 10px 12px;
    border-radius: 14px;
    border: 1px solid rgba(229, 231, 235, 0.9);
    background: rgba(255,255,255,0.75);
    margin: 8px 0;
}}

.rec-name {{
    font-weight: 650;
    color: var(--ink);
    text-align: left !important;
}}

.rec-meta {{
    font-size: 0.88rem;
    color: rgba(15, 23, 42, 0.7);
    text-align: left !important;
}}

.details-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 20px;
    margin-top: 16px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
}}

.details-card h4 {{
    color: var(--teal);
    margin-bottom: 12px;
}}

.section-h {{
    margin: 12px 0 6px 0;
    font-weight: 700;
    color: var(--ink);
    text-align: left !important;
}}

.pros-list, .cons-list {{
    text-align: left !important;
    padding-left: 20px;
    margin: 0;
}}

.pros-list li {{
    color: var(--ink);
    margin: 4px 0;
}}

.pros-list li::marker {{
    color: var(--teal);
}}

.cons-list li {{
    color: var(--ink);
    margin: 4px 0;
}}

.cons-list li::marker {{
    color: var(--coral);
}}

.floating-cta {{
    position: fixed;
    right: 18px;
    bottom: 18px;
    z-index: 9999;
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 14px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid rgba(209, 73, 91, 0.35);
    box-shadow: 0 10px 28px rgba(15, 23, 42, 0.12);
    text-decoration: none;
    color: var(--ink);
    font-weight: 700;
}}

.floating-cta:hover {{
    border-color: rgba(209, 73, 91, 0.55);
    box-shadow: 0 12px 32px rgba(15, 23, 42, 0.16);
}}

.floating-cta .dot {{
    width: 10px;
    height: 10px;
    border-radius: 999px;
    background: var(--coral);
    flex: 0 0 auto;
}}

.floating-cta .sub {{
    font-weight: 600;
    color: rgba(15, 23, 42, 0.70);
    font-size: 0.85rem;
    margin-left: 6px;
}}

@media (max-width: 640px) {{
    .floating-cta {{
        right: 12px;
        left: 12px;
        bottom: 12px;
        justify-content: center;
    }}
}}

.details-cta {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    margin-top: 10px;
    padding: 12px 14px;
    border-radius: 999px;
    background: var(--teal);
    border: 1px solid var(--teal);
    color: white !important;
    text-decoration: none;
    font-weight: 750;
    width: 100%;
}}

.details-cta:hover {{
    background: var(--teal-600);
    border-color: var(--teal-600);
}}

.details-cta.unlikely {{
    background: var(--coral);
    border-color: var(--coral);
}}

.details-cta.unlikely:hover {{
    background: var(--coral-hover);
    border-color: var(--coral-hover);
}}

.inline-link {{
    color: var(--coral) !important;
    text-decoration: none;
    font-weight: 700;
}}

.inline-link:hover {{
    text-decoration: underline;
}}

.end-cta-section {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 24px;
    margin: 20px 0;
    text-align: center;
}}

.end-cta-section h4 {{
    color: var(--ink);
    margin: 0 0 8px 0;
}}

.end-cta-section p {{
    color: rgba(15, 23, 42, 0.75);
    margin: 0 0 16px 0;
    font-size: 0.95rem;
}}
</style>
""", unsafe_allow_html=True)

if not st.session_state.started or st.session_state.show_results:
    st.markdown(
        f'''
        <a class="floating-cta" href="{BOOK_URL}" target="_blank" rel="noopener noreferrer">
            <span class="dot"></span>
            <span>Talk to a clinician<span class="sub">Book a telehealth visit</span></span>
        </a>
        ''',
        unsafe_allow_html=True
    )


def render_landing():
    """Render landing page with hero and Start button."""
    st.markdown(f'''
    <style>
    .stApp {{ height: 100dvh !important; overflow: hidden !important; }}
    section.main {{ overflow: hidden !important; height: 100dvh !important; }}
    div[data-testid="stMainBlockContainer"] {{ 
        padding: 0 !important;
        height: 100dvh !important;
        overflow: hidden !important;
    }}
    .landing-grid {{
        display: grid;
        grid-template-rows: 1fr auto;
        height: 100dvh;
        width: 100%;
        padding: 12px 5% 0 5%;
        box-sizing: border-box;
        gap: 16px;
        overflow: hidden;
    }}
    .landing-hero-cell {{
        min-height: 0;
        overflow: hidden;
    }}
    .landing-hero {{
        height: 100%;
        width: 100%;
        border-radius: 20px;
        overflow: hidden;
        background-image: url("data:image/jpeg;base64,{hero_base64}");
        background-size: cover;
        background-position: center 35%;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    .landing-hero::after {{
        content: "";
        position: absolute;
        inset: 0;
        pointer-events: none;
        background: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.35));
        border-radius: 20px;
    }}
    .landing-hero h1 {{
        position: relative;
        z-index: 2;
        color: white;
        font-size: clamp(1.5rem, 5vw, 2.7rem);
        font-weight: 700;
        line-height: 1.2;
        text-align: center;
        padding: 240px 24px 0 24px;
        margin: 0;
    }}
    .landing-footer {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 12px;
        padding-bottom: 80px;
    }}
    .landing-start-btn {{
        background: white;
        color: #0F172A;
        border: none;
        border-radius: 999px;
        padding: 14px 48px;
        font-size: 1.1rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
    }}
    .landing-start-btn:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.2);
    }}
    .landing-disclaimer {{
        text-align: center;
        font-size: 0.8rem;
        color: rgba(15,23,42,0.65);
        margin: 0;
        line-height: 1.4;
    }}
    @media (max-height: 600px) {{
        .landing-disclaimer {{ font-size: 0.7rem; }}
        .landing-footer {{ padding-bottom: 70px; }}
    }}
    </style>
    <div class="landing-grid">
        <div class="landing-hero-cell">
            <div class="landing-hero">
                <h1>Find your contraceptive<br>in seven questions</h1>
            </div>
        </div>
        <div class="landing-footer">
            <a href="?start=1" style="text-decoration: none;">
                <button class="landing-start-btn">Start</button>
            </a>
            <p class="landing-disclaimer">None of your data is stored. This is an educational tool only, not medical advice. Always consult a healthcare provider.</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    if st.query_params.get("start") == "1":
        st.query_params.clear()
        if not st.session_state.started:
            st.session_state.started = True
            st.session_state.q_idx = 0
            st.rerun()


def render_single_select_tiles(question_key, options):
    """Render single-select tiles. Returns selected option or None."""
    state_key = f"tile_{question_key}"
    if state_key not in st.session_state:
        current = st.session_state.answers.get(question_key)
        st.session_state[state_key] = current
    
    selected = st.session_state[state_key]
    
    for i, option in enumerate(options):
        is_selected = (selected == option)
        btn_key = f"tile_{question_key}_{i}"
        
        prefix = "✓ " if is_selected else ""
        display_text = f"{prefix}{option}"
        
        if is_selected:
            st.markdown(f"""
            <style>
            button[data-testid="stBaseButton-secondary"][key="{btn_key}"],
            div[data-testid="stVerticalBlock"] div:nth-child({i + 1}) .stButton > button {{
                border: 2.5px solid var(--mint-border-strong) !important;
                background: var(--mint-bg) !important;
            }}
            </style>
            """, unsafe_allow_html=True)
        
        if st.button(display_text, key=btn_key, use_container_width=True):
            st.session_state[state_key] = option
            st.rerun()
    
    return selected


def render_multi_select_tiles(question_key, options):
    """Render multi-select tiles. Returns list of selected options."""
    state_key = f"tile_{question_key}"
    if state_key not in st.session_state:
        current = st.session_state.answers.get(question_key, [])
        st.session_state[state_key] = list(current) if current else []
    
    selected_list = st.session_state[state_key]
    
    for i, option in enumerate(options):
        is_selected = option in selected_list
        btn_key = f"tile_{question_key}_{i}"
        
        prefix = "✓ " if is_selected else ""
        display_text = f"{prefix}{option}"
        
        if is_selected:
            st.markdown(f"""
            <style>
            div[data-testid="stVerticalBlock"] div:nth-child({i + 1}) .stButton > button {{
                border: 2.5px solid var(--mint-border-strong) !important;
                background: var(--mint-bg) !important;
            }}
            </style>
            """, unsafe_allow_html=True)
        
        if st.button(display_text, key=btn_key, use_container_width=True):
            if is_selected:
                st.session_state[state_key] = [o for o in selected_list if o != option]
            else:
                st.session_state[state_key] = selected_list + [option]
            st.rerun()
    
    return st.session_state[state_key]


def render_quiz():
    st.markdown("""
    <style>
    [data-testid="stHeader"], header {
        display: none !important;
        height: 0 !important;
    }
    [data-testid="stAppViewContainer"] {
        padding-top: 8px !important;
    }
    div[data-testid="stMainBlockContainer"] {
        padding-top: 0 !important;
    }
    .block-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    .cc-quiz-header {
        padding-top: 2px;
    }
    .cc-quiz-header .progress-text {
        margin: 0 0 4px 0 !important;
    }
    /* Mint tile styles for quiz answer buttons */
    button[data-testid="baseButton-secondary"],
    .stButton > button {
        background: rgba(116,184,154,0.10) !important;
        border: 1px solid rgba(116,184,154,0.55) !important;
        color: #211816 !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        font-weight: 500 !important;
        text-align: left !important;
        transition: all 0.15s ease !important;
    }
    button[data-testid="baseButton-secondary"]:hover,
    .stButton > button:hover {
        border-color: rgba(116,184,154,0.95) !important;
        background: rgba(116,184,154,0.14) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="cc-quiz">', unsafe_allow_html=True)
    
    q_idx = st.session_state.q_idx
    q_id = QUESTION_IDS[q_idx]
    question = QUIZ_QUESTIONS[q_id]
    
    step = q_idx + 1
    progress_fraction = step / NUM_QUESTIONS
    
    st.markdown(f'<div class="cc-quiz-header"><p class="progress-text">Question {step} of {NUM_QUESTIONS}</p></div>', unsafe_allow_html=True)
    st.progress(progress_fraction)
    
    st.markdown(f'<p class="quiz-question">{question["label"]}</p>', unsafe_allow_html=True)
    
    if question.get("help"):
        st.markdown(f'<p class="quiz-help">{question["help"]}</p>', unsafe_allow_html=True)
    
    is_multi = question.get("multi", False)
    
    if is_multi:
        answer = render_multi_select_tiles(q_id, question["options"])
        is_valid = len(answer) >= 1
    else:
        answer = render_single_select_tiles(q_id, question["options"])
        is_valid = answer is not None
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if q_idx > 0:
            if st.button("← Back", use_container_width=True):
                st.session_state.answers[q_id] = answer
                prev_q_id = QUESTION_IDS[q_idx - 1]
                tile_key = f"tile_{prev_q_id}"
                if tile_key in st.session_state:
                    del st.session_state[tile_key]
                st.session_state.q_idx -= 1
                st.rerun()
    
    with col3:
        if q_idx < NUM_QUESTIONS - 1:
            if st.button("Next →", use_container_width=True, disabled=not is_valid):
                if is_valid:
                    st.session_state.answers[q_id] = answer
                    st.session_state.q_idx += 1
                    st.rerun()
        else:
            if st.button("See Results", use_container_width=True, disabled=not is_valid):
                if is_valid:
                    st.session_state.answers[q_id] = answer
                    st.session_state.show_results = True
                    st.session_state.selected_method_id = None
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_category(tier_key, methods):
    if not methods:
        return
    
    tier = TIER_CONFIG[tier_key]
    
    st.markdown(f"""
    <div class="category-card">
        <p class="category-title">{tier['icon']} {tier['title']}</p>
        <p class="category-sub">{tier['microcopy']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    for method in methods:
        method_id = get_method_id(method)
        is_expanded = st.session_state.selected_method_id == method_id
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"""
            <div style="text-align: left !important;">
                <span class="rec-name">{method['name']}</span><br/>
                <span class="badge {tier['class']}">{tier['icon']} {tier['badge']}</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            label = "Hide" if is_expanded else "View"
            if st.button(label, key=f"view_{method_id}", use_container_width=True):
                if is_expanded:
                    st.session_state.selected_method_id = None
                else:
                    st.session_state.selected_method_id = method_id
                st.rerun()
        
        if is_expanded:
            st.markdown('<div class="details-card">', unsafe_allow_html=True)
            
            st.markdown(
                f"<div style='display:flex; justify-content:space-between; align-items:center; gap:12px;'>"
                f"<div style='font-weight:800; font-size:1.05rem; color:var(--ink); text-align:left !important;'>{method['name']}</div>"
                f"<div class='badge {tier['class']}'>{tier['icon']} {tier['badge']}</div>"
                f"</div>",
                unsafe_allow_html=True
            )
            
            if method.get("image"):
                try:
                    st.image(method["image"], use_container_width=True)
                except:
                    st.caption("Image unavailable")
            
            st.markdown("<div class='section-h'>Pros</div>", unsafe_allow_html=True)
            if method.get("pros"):
                st.markdown("<ul class='pros-list'>" + "".join([f"<li>{p}</li>" for p in method["pros"]]) + "</ul>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='rec-meta'>Pros coming soon.</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='section-h'>Cons</div>", unsafe_allow_html=True)
            if method.get("cons"):
                st.markdown("<ul class='cons-list'>" + "".join([f"<li>{c}</li>" for c in method["cons"]]) + "</ul>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='rec-meta'>Cons coming soon.</div>", unsafe_allow_html=True)
            
            effectiveness = method.get("typical", "")
            if effectiveness:
                st.markdown("<div class='section-h'>Typical effectiveness</div>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: left !important;'>{effectiveness} failure rate with typical use</p>", unsafe_allow_html=True)
            
            cta_class = "details-cta unlikely" if tier_key == "unlikely" else "details-cta"
            helper = (
                "Based on your answers, this option is less likely to fit. A clinician can help you review safer alternatives."
                if tier_key == "unlikely"
                else "If you'd like, you can book a telehealth visit to talk through your options."
            )
            
            st.markdown(f"<div class='rec-meta' style='margin-top:14px;'>{helper}</div>", unsafe_allow_html=True)
            st.markdown(
                f"<a class='{cta_class}' href='{BOOK_URL}' target='_blank' rel='noopener noreferrer'>Book a telehealth visit →</a>",
                unsafe_allow_html=True
            )
            
            col_a, col_b = st.columns([1, 1])
            with col_a:
                if st.button("Close details", key=f"close_{method_id}", use_container_width=True):
                    st.session_state.selected_method_id = None
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)


def render_results():
    st.markdown(f'<p class="progress-text">Complete</p>', unsafe_allow_html=True)
    st.progress(1.0)
    
    st.markdown("---")
    st.markdown("### Your Personalized Recommendations")
    
    encoded = encode_answers(st.session_state.answers)
    results = get_recommendations(METHODS, encoded)
    
    render_category("best", results["recommended"])
    render_category("consider", results["caution"])
    render_category("unlikely", results["contraindicated"])
    
    st.markdown("---")
    
    st.markdown(f"""
    <div class="end-cta-section">
        <h4>Want personalized medical advice?</h4>
        <p>Book a telehealth visit to discuss your options and medical eligibility.</p>
        <a class="details-cta" href="{BOOK_URL}" target="_blank" rel="noopener noreferrer">Book a telehealth visit →</a>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Start Over", use_container_width=True):
            st.session_state.started = False
            st.session_state.q_idx = 0
            st.session_state.answers = {}
            st.session_state.show_results = False
            st.session_state.selected_method_id = None
            st.rerun()


if not st.session_state.started:
    render_landing()
elif st.session_state.show_results:
    render_results()
else:
    render_quiz()

