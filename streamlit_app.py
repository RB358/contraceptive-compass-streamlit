from pathlib import Path
import base64
import streamlit as st

from core.methods_data import METHODS, TELEHEALTH_OPTIONS
from core.schema import QUESTIONS, QUIZ_QUESTIONS, encode_answers
from core.quiz_logic import get_recommendations
from core.render_helpers import format_method_card_html, format_recommendation_text, format_telehealth_link

st.set_page_config(
    page_title="Find the contraceptive that fits you — in seven questions",
    layout="centered"
)
if "started" not in st.session_state:
    st.session_state.started = False

IMG_PATH = Path(__file__).resolve().parent / "Assets" / "iStock-contraceptives2.jpg"
hero_base64 = base64.b64encode(IMG_PATH.read_bytes()).decode()

st.markdown(f"""
<style>
.hero {{
    --hero-height: 440px;
    position: relative;
    width: 100%;
    height: var(--hero-height);
    border-radius: 24px;
    overflow: hidden;
    margin-bottom: 40px;

    background-image: url("data:image/jpeg;base64,{hero_base64}");
    background-size: cover;
    background-position: center 35%;
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

    padding: 35px 32px 32px 32px;
    color: white;
}}

.hero h1 {{
    font-size: 2.7rem;
    font-weight: 700;
    margin-bottom: 26px;
}}
</style>
""", unsafe_allow_html=True)

if not st.session_state.started:
    st.markdown(f"""
    <div class="hero hero-landing">
        <div class="hero-content">
            <h1>Find your contraceptive in seven questions</h1>
            <div style="margin-top: 40px;">
                <a href="?started=true" target="_self" style="
                    background-color: white !important;
                    color: #006d77 !important;
                    border-radius: 999px !important;
                    padding: 14px 38px !important;
                    font-size: 1.1rem !important;
                    font-weight: 700 !important;
                    text-decoration: none !important;
                    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25) !important;
                    display: inline-block !important;
                    border: none !important;
                    cursor: pointer !important;
                    line-height: 1.2 !important;
                    text-align: center !important;
                    min-width: 160px !important;
                ">Start</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.query_params.get("started") == "true":
        st.session_state.started = True
        st.query_params.clear()
        st.rerun()

if st.session_state.started:
    st.markdown(
        "<p style='color:#6b7280; font-size:0.95rem;'>"
        "Answer these questions for personalised insights"
        "</p>",
        unsafe_allow_html=True
    )

    age_group = st.selectbox(
        QUESTIONS["age_group"]["label"],
        QUESTIONS["age_group"]["options"]
    )

    smoking = st.selectbox(
        QUESTIONS["smoking"]["label"],
        QUESTIONS["smoking"]["options"]
    )

    bmi = st.selectbox(
        QUESTIONS["bmi"]["label"],
        QUESTIONS["bmi"]["options"]
    )

    periods = st.selectbox(
        QUESTIONS["periods"]["label"],
        QUESTIONS["periods"]["options"]
    )

    breastfeeding = st.selectbox(
        QUESTIONS["breastfeeding"]["label"],
        QUESTIONS["breastfeeding"]["options"]
    )

    conditions = st.multiselect(
        QUESTIONS["conditions"]["label"],
        QUESTIONS["conditions"]["options"]
    )

    priority = st.selectbox(
        QUESTIONS["priority"]["label"],
        QUESTIONS["priority"]["options"]
    )

st.markdown("""
<style>
    .main {
        background: #f0fafa;
        padding-bottom: 100px;
    }
    h1, h2, h3 {color: #006d77; font-family: 'Helvetica Neue', sans-serif;}
    .stButton>button {background: #83c5be; color: #006d77; border-radius: 12px; font-weight: bold;}
    .method-card {
        padding: 20px;
        border-radius: 16px;
        background: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 15px 0;
        text-align: center;
    }
    .main .block-container {
        max-width: 90% !important;
        padding-left: 5% !important;
        padding-right: 5% !important;
        padding-top: 2rem !important;
    }
    h1, h2, h3, h4, .stMarkdown, p, div {text-align: center !important;}
    
    .stButton 
    {
        text-align: center !important;
    }
    div.stButton {
        text-align: center !important;
    }
    .stButton > button {
        display: inline-block !important;
        margin: 20px auto !important;
        width: 90% !important;
        max-width: 400px !important;
    }
    .stSelectbox, .stMultiselect, .stSlider {
        margin: 0 auto !important;
        max-width: 400px !important;
    }
    img {
        display: block !important;
        margin: 0 auto !important;
        border-radius: 12px;
    }
    .method-card {margin: 20px auto !important; max-width: 400px !important;}
    details summary {text-align: center !important;}
    @media (min-width: 768px) {
        .main .block-container {max-width: 700px !important;}
    }
    .fixed-button-container {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 500px;
        z-index: 1000;
        pointer-events: none;
    }
    .fixed-button-inner {pointer-events: auto;}
    
</style>
""", unsafe_allow_html=True)

st.info("**Disclaimer:** None of your answers or data are stored by us. This is educational only • Always consult a healthcare provider • Not medical advice.")

st.title("Find the contraceptive that fits you - in seven questions.")
st.markdown("### Explore methods, learn effectiveness, and find what fits you")

for method in METHODS:
    with st.container():
        st.image(method["image"], width="stretch")
        st.markdown(format_method_card_html(method), unsafe_allow_html=True)

st.header("📊 Find Your Match")
st.markdown("Answer these questions for personalized insights")

q1 = st.selectbox(QUIZ_QUESTIONS["q1"]["label"], QUIZ_QUESTIONS["q1"]["options"], help=QUIZ_QUESTIONS["q1"]["help"])
q2 = st.selectbox(QUIZ_QUESTIONS["q2"]["label"], QUIZ_QUESTIONS["q2"]["options"], help=QUIZ_QUESTIONS["q2"]["help"])
q3 = st.selectbox(QUIZ_QUESTIONS["q3"]["label"], QUIZ_QUESTIONS["q3"]["options"], help=QUIZ_QUESTIONS["q3"]["help"])
q4 = st.selectbox(QUIZ_QUESTIONS["q4"]["label"], QUIZ_QUESTIONS["q4"]["options"], help=QUIZ_QUESTIONS["q4"]["help"])
q5 = st.selectbox(QUIZ_QUESTIONS["q5"]["label"], QUIZ_QUESTIONS["q5"]["options"], help=QUIZ_QUESTIONS["q5"]["help"])
q6 = st.multiselect(QUIZ_QUESTIONS["q6"]["label"], QUIZ_QUESTIONS["q6"]["options"], help=QUIZ_QUESTIONS["q6"]["help"])
q7 = st.selectbox(QUIZ_QUESTIONS["q7"]["label"], QUIZ_QUESTIONS["q7"]["options"], help=QUIZ_QUESTIONS["q7"]["help"])

if st.button("Your Personalized Recommendations"):
    answers = {"q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5, "q6": q6, "q7": q7}
    encoded = encode_answers(answers)
    results = get_recommendations(METHODS, encoded)

    st.success("### Your Personalized Recommendations")
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

st.markdown("<div class='fixed-button-container'><div class='fixed-button-inner'>", unsafe_allow_html=True)
with st.expander("📅 Book Doctor Now – Choose a Service", expanded=False):
    for service in TELEHEALTH_OPTIONS:
        st.markdown(format_telehealth_link(service))
st.markdown("</div></div>", unsafe_allow_html=True)

st.caption("Contraceptive Choices • Educational tool • December 2025")
