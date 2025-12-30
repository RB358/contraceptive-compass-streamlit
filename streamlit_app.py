from pathlib import Path
import base64
import streamlit as st
import streamlit.components.v1 as components

from core.methods_data import METHODS, TELEHEALTH_OPTIONS
from core.schema import QUIZ_QUESTIONS, encode_answers
from core.quiz_logic import get_recommendations
from core.render_helpers import format_recommendation_text, format_telehealth_link
from ui_components import start_cta

st.set_page_config(
    page_title="Find the contraceptive that fits you — in seven questions",
    layout="centered"
)

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

QUESTION_IDS = list(QUIZ_QUESTIONS.keys())
NUM_QUESTIONS = len(QUESTION_IDS)

IMG_PATH = Path(__file__).resolve().parent / "Assets" / "iStock-contraceptives2.jpg"
hero_base64 = base64.b64encode(IMG_PATH.read_bytes()).decode()

hero_height = 180 if st.session_state.started else 440
hero_margin = 16 if st.session_state.started else 40
start_btn_offset = -80 if st.session_state.started else -170

st.markdown(f"""
<style>
.hero {{
    position: relative;
    width: 100%;
    height: {hero_height}px;
    border-radius: 24px;
    overflow: hidden;
    margin-bottom: {hero_margin}px;
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
    justify-content: flex-start !important;
    align-items: center;
    text-align: center;
    padding: {"20px 24px" if st.session_state.started else "35px 32px 32px 32px"};
    color: white;
}}

.hero h1 {{
    font-size: {"1.6rem" if st.session_state.started else "2.7rem"};
    font-weight: 700;
    margin-bottom: {"10px" if st.session_state.started else "26px"};
    transition: font-size 0.3s ease;
}}

.start-cta-wrapper {{
    margin-top: {start_btn_offset}px !important;
}}

.main {{
    background: #f0fafa;
    padding-bottom: 100px;
}}

h1, h2, h3 {{color: #006d77; font-family: 'Helvetica Neue', sans-serif;}}

.stButton>button {{
    background: #83c5be;
    color: #006d77;
    border-radius: 12px;
    font-weight: bold;
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
    color: #6b7280;
    font-size: 0.9rem;
    margin-bottom: 16px;
}}

.quiz-container {{
    background: white;
    padding: 24px;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    margin: 20px auto;
    max-width: 500px;
}}

.quiz-started-callout {{
    background: linear-gradient(135deg, #006d77 0%, #00939e 100%);
    color: white;
    padding: 16px 24px;
    border-radius: 12px;
    text-align: center;
    margin: 0 auto 24px auto;
    max-width: 400px;
    box-shadow: 0 4px 12px rgba(0,109,119,0.3);
}}

.quiz-started-callout h4 {{
    color: white !important;
    margin: 0 0 8px 0;
    font-size: 1.1rem;
}}

.quiz-started-callout p {{
    margin: 0;
    font-size: 0.85rem;
    opacity: 0.9;
}}

.quiz-started-callout .chevron {{
    font-size: 1.5rem;
    margin-top: 8px;
    animation: bounce 1.5s infinite;
}}

@keyframes bounce {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(6px); }}
}}

.quiz-controls {{
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-bottom: 16px;
}}

.quiz-control-btn {{
    background: #e5e7eb;
    color: #374151;
    border: none;
    padding: 6px 14px;
    border-radius: 8px;
    font-size: 0.8rem;
    cursor: pointer;
    text-decoration: none !important;
}}

.quiz-control-btn:hover {{
    background: #d1d5db;
}}
</style>
""", unsafe_allow_html=True)


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
    
    if st.query_params.get("start") == "1":
        st.session_state.started = True
        st.session_state.scroll_to_quiz = True
        st.query_params.clear()
        st.rerun()
    
    if st.session_state.started:
        st.markdown("""
        <div class="quiz-started-callout">
            <h4>Quiz started</h4>
            <p>7 questions • ~2 minutes • Educational only</p>
            <div class="chevron">▼</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("**Disclaimer:** None of your answers or data are stored by us. This is educational only • Always consult a healthcare provider • Not medical advice.")


def render_quiz():
    st.markdown('<div id="quiz-start"></div>', unsafe_allow_html=True)
    
    if st.session_state.scroll_to_quiz:
        components.html("""
        <script>
            const el = window.parent.document.getElementById("quiz-start");
            if (el) { el.scrollIntoView({behavior: "smooth", block: "start"}); }
        </script>
        """, height=0)
        st.session_state.scroll_to_quiz = False
    
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
            st.rerun()
    
    q_idx = st.session_state.q_idx
    q_id = QUESTION_IDS[q_idx]
    question = QUIZ_QUESTIONS[q_id]
    
    st.markdown(f'<p class="progress-text">Question {q_idx + 1} of {NUM_QUESTIONS}</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
    
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
                st.rerun()


def render_results():
    st.markdown("---")
    st.markdown("### Your Personalized Recommendations")
    
    encoded = encode_answers(st.session_state.answers)
    results = get_recommendations(METHODS, encoded)
    
    if results["recommended"]:
        st.markdown("**🟢 Recommended for you:**")
        for m in results["recommended"]:
            st.markdown(format_recommendation_text(m))
    
    if results["caution"]:
        st.markdown("**🟡 Use with caution:**")
        for m in results["caution"]:
            st.markdown(format_recommendation_text(m, include_failure=False))
    
    if results["contraindicated"]:
        st.markdown("**🔴 Avoid (contraindicated):**")
        for m in results["contraindicated"]:
            st.markdown(format_recommendation_text(m, include_failure=False))
    
    st.markdown("---")
    
    with st.expander("📅 Book Doctor Now – Choose a Service", expanded=False):
        for service in TELEHEALTH_OPTIONS:
            st.markdown(format_telehealth_link(service))
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Start Over", use_container_width=True):
            st.session_state.started = False
            st.session_state.scroll_to_quiz = False
            st.session_state.q_idx = 0
            st.session_state.answers = {}
            st.session_state.show_results = False
            st.rerun()


render_landing()

if st.session_state.started:
    if st.session_state.show_results:
        render_results()
    else:
        render_quiz()

st.caption("Contraceptive Choices • Educational tool • December 2025")
