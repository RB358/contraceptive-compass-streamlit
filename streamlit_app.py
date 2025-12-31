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

BOOK_URL = "https://www.plannedparenthood.org/health-center"

if "started" not in st.session_state:
    st.session_state.started = False
if "scroll_to_quiz" not in st.session_state:
    st.session_state.scroll_to_quiz = False
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

hero_height = "clamp(140px, 25vh, 180px)" if st.session_state.started else "clamp(240px, 45vh, 440px)"
hero_margin = "12px" if st.session_state.started else "24px"
start_btn_offset = -80 if st.session_state.started else -140

st.markdown(f"""
<style>
:root {{
    --teal: #0F766E;
    --teal-600: #0B5F59;
    --coral: #D1495B;
    --coral-hover: #E06372;
    --ink: #0F172A;
    --surface: #FFFFFF;
    --warm-bg: #FFFBFA;
    --border: #E5E7EB;
}}

.stApp, .main {{
    background: var(--warm-bg) !important;
    color: var(--ink);
}}

section[data-testid="stVerticalBlock"] > div:first-child {{
    padding-top: 0;
}}

.stApp > section > .block-container {{
    padding-top: 1rem !important;
}}

.hero {{
    position: relative;
    width: 100%;
    height: {hero_height};
    border-radius: 24px;
    overflow: hidden;
    margin-bottom: {hero_margin};
    background-image: url("data:image/jpeg;base64,{hero_base64}");
    background-size: cover;
    background-position: center 35%;
    transition: height 0.3s ease, margin-bottom 0.3s ease;
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
    justify-content: center !important;
    align-items: center;
    text-align: center;
    padding: {"16px 20px" if st.session_state.started else "24px 28px"};
    color: white;
}}

.hero h1 {{
    font-size: {"1.4rem" if st.session_state.started else "clamp(1.6rem, 5vw, 2.7rem)"};
    font-weight: 700;
    margin-bottom: {"8px" if st.session_state.started else "16px"};
    transition: font-size 0.3s ease;
    line-height: 1.2;
}}

.start-cta-wrapper {{
    margin-top: {start_btn_offset}px !important;
}}

@media (max-height: 750px) {{
    .hero {{
        height: {"clamp(100px, 20vh, 140px)" if st.session_state.started else "clamp(180px, 35vh, 300px)"};
        margin-bottom: 12px;
        border-radius: 18px;
    }}
    .hero h1 {{
        font-size: {"1.2rem" if st.session_state.started else "clamp(1.4rem, 4vw, 2rem)"};
        margin-bottom: 8px;
    }}
    .hero-content {{
        padding: 16px 20px;
    }}
    .start-cta-wrapper {{
        margin-top: {-60 if st.session_state.started else -100}px !important;
    }}
    .main .block-container {{
        padding-top: 1rem !important;
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
    margin-bottom: 16px;
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
    st.markdown(f"""
    <div class="hero hero-landing">
        <div class="hero-content">
            <h1>Find your contraceptive in seven questions</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.started:
        start_cta()
        st.markdown(
            "<p style='text-align:center; font-size:0.85rem; color:rgba(15,23,42,0.65); margin:16px 0 0 0; padding:0 16px;'>This tool is educational only and does not replace medical advice.</p>",
            unsafe_allow_html=True
        )
    
    if st.query_params.get("start") == "1":
        st.session_state.started = True
        st.session_state.scroll_to_quiz = True
        st.query_params.clear()
        st.rerun()
    
    if st.session_state.started:
        st.markdown('<div id="started-note"></div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="accent-bg">
            <strong>Quiz started — your first question is below.</strong><br/>
            <span>7 questions • ~2 minutes • Educational only</span>
            <div class="chevron">▼</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.get("scroll_to_quiz", False):
            components.html("""
            <script>
                setTimeout(() => {
                    const quiz = window.parent.document.getElementById("quiz-start");
                    if (quiz) { quiz.scrollIntoView({behavior: "smooth", block: "start"}); }
                }, 900);
            </script>
            """, height=0)
            st.session_state.scroll_to_quiz = False


def render_quiz():
    st.markdown('<div id="quiz-start"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("↑ Back to top", key="back_to_top", use_container_width=True):
            components.html("""
            <script>
                window.parent.scrollTo({top: 0, behavior: "smooth"});
            </script>
            """, height=0)
    with col2:
        if st.button("🔄 Restart quiz", key="restart_quiz", use_container_width=True):
            st.session_state.started = False
            st.session_state.scroll_to_quiz = False
            st.session_state.q_idx = 0
            st.session_state.answers = {}
            st.session_state.show_results = False
            st.session_state.selected_method_id = None
            st.rerun()
    
    q_idx = st.session_state.q_idx
    q_id = QUESTION_IDS[q_idx]
    question = QUIZ_QUESTIONS[q_id]
    
    st.markdown(f'<p class="progress-text">Question {q_idx + 1} of {NUM_QUESTIONS}</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
    
    st.markdown(f"### {question['label']}")
    
    if question.get("help"):
        st.caption(question["help"])
    
    current_answer = st.session_state.answers.get(q_id)
    
    if question.get("multi"):
        default_val = current_answer if current_answer else []
        answer = st.multiselect(
            "Select all that apply:",
            question["options"],
            default=default_val,
            key=f"q_{q_id}",
            label_visibility="collapsed"
        )
    else:
        default_idx = 0
        if current_answer and current_answer in question["options"]:
            default_idx = question["options"].index(current_answer)
        answer = st.selectbox(
            "Choose one:",
            question["options"],
            index=default_idx,
            key=f"q_{q_id}",
            label_visibility="collapsed"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if q_idx > 0:
            if st.button("← Back", use_container_width=True):
                st.session_state.answers[q_id] = answer
                st.session_state.q_idx -= 1
                st.rerun()
    
    with col3:
        if q_idx < NUM_QUESTIONS - 1:
            if st.button("Next →", use_container_width=True):
                st.session_state.answers[q_id] = answer
                st.session_state.q_idx += 1
                st.rerun()
        else:
            if st.button("See Results", use_container_width=True):
                st.session_state.answers[q_id] = answer
                st.session_state.show_results = True
                st.session_state.selected_method_id = None
                st.rerun()


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
            st.session_state.scroll_to_quiz = False
            st.session_state.q_idx = 0
            st.session_state.answers = {}
            st.session_state.show_results = False
            st.session_state.selected_method_id = None
            st.rerun()


render_landing()

if st.session_state.started:
    if st.session_state.show_results:
        render_results()
    else:
        render_quiz()

