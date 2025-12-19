# streamlit_app.py - Updated: Colored borders around full method tiles, no separate tier plaques
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Contraceptive Compass", page_icon="🧭", layout="wide")

# Teal palette + tier border colors
st.markdown("""
<style>
    .main {background: #f0fafa;}
    h1, h2, h3 {color: #008080; font-family: 'Helvetica Neue', sans-serif;}
    .stButton>button {background: #008080; color: white; border-radius: 20px;}
    .method-tile {
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        cursor: pointer;
        background: white;
        border: 8px solid;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .gold-border {border-color: #cd7f32;}   /* Tier 1 - Cool gold */
    .silver-border {border-color: #c0c0c0;} /* Tier 2 - Silver */
    .bronze-border {border-color: #8b4513;} /* Tier 3 - Bronze */
    .floating-button {position: fixed; bottom: 20px; right: 20px; z-index: 1000;}
</style>
""", unsafe_allow_html=True)

# Methods data (tier_class for borders)
methods = [
    {"name": "Implant", "effectiveness": ">99%", "tier_class": "gold-border", "mechanism": "Progestin prevents ovulation", "pros": ["Long-lasting (3-5 yrs)", "Reversible", "Low maintenance"], "cons": ["Irregular bleeding", "Insertion procedure"], "side_effects": "Spotting, weight gain possible", "sti": False, "contraindications": ["Breast cancer", "Liver disease"]},
    {"name": "Hormonal IUD", "effectiveness": ">99%", "tier_class": "gold-border", "mechanism": "Progestin thickens mucus & thins lining", "pros": ["5-8 yrs protection", "Lighter periods"], "cons": ["Insertion cramping"], "side_effects": "Spotting initially", "sti": False, "contraindications": ["Current pelvic infection"]},
    {"name": "Copper IUD", "effectiveness": ">99%", "tier_class": "gold-border", "mechanism": "Copper toxic to sperm", "pros": ["10+ yrs, hormone-free", "Emergency contraception"], "cons": ["Heavier periods"], "side_effects": "Cramps, heavier flow", "sti": False, "contraindications": ["Copper allergy"]},
    {"name": "Sterilization", "effectiveness": ">99%", "tier_class": "gold-border", "mechanism": "Permanent block of tubes/vas", "pros": ["Permanent"], "cons": ["Surgical, not easily reversible"], "side_effects": "Surgical risks", "sti": False, "contraindications": ["Desire future fertility"]},
    {"name": "Injection (Depo)", "effectiveness": "94%", "tier_class": "silver-border", "mechanism": "Progestin shot every 3 months", "pros": ["No daily routine"], "cons": ["Bone density loss (reversible)"], "side_effects": "Weight gain, delayed fertility return", "sti": False, "contraindications": ["Breast cancer"]},
    {"name": "Pill/Patch/Ring", "effectiveness": "91%", "tier_class": "silver-border", "mechanism": "Hormones prevent ovulation", "pros": ["Regulates periods", "Reversible"], "cons": ["Daily/weekly/monthly adherence"], "side_effects": "Nausea, mood changes", "sti": False, "contraindications": ["Smoking >35", "History of clots", "Migraine with aura"]},
    {"name": "Condom (Male/Female)", "effectiveness": "82%", "tier_class": "bronze-border", "mechanism": "Barrier", "pros": ["STI protection", "No hormones"], "cons": ["User-dependent"], "side_effects": "Allergy possible", "sti": True, "contraindications": []},
    {"name": "Diaphragm/Cervical Cap", "effectiveness": "88%", "tier_class": "bronze-border", "mechanism": "Barrier with spermicide", "pros": ["Reusable"], "cons": ["Insertion required"], "side_effects": "UTI risk", "sti": False, "contraindications": []},
    {"name": "Fertility Awareness", "effectiveness": "76%", "tier_class": "bronze-border", "mechanism": "Track cycle", "pros": ["Hormone-free"], "cons": ["High user effort"], "side_effects": "None", "sti": False, "contraindications": ["Irregular cycles"]},
    {"name": "Withdrawal", "effectiveness": "78%", "tier_class": "bronze-border", "mechanism": "Pull out", "pros": ["Free"], "cons": ["Pre-ejaculate risk"], "side_effects": "None", "sti": False, "contraindications": []},
]

# Persistent Book Doctor Now button
st.markdown("""
<div class="floating-button">
    <a href="https://nurx.com" target="_blank">
        <button style="background:#008080; color:white; padding:15px 30px; font-size:18px; border:none; border-radius:50px;">
            📅 Book Doctor Now
        </button>
    </a>
</div>
""", unsafe_allow_html=True)

st.title("Contraceptive Compass")

# Effectiveness tiles with full bordered tiles
st.header("Contraceptive Methods by Effectiveness")
cols = st.columns(4)
for i, method in enumerate(methods):
    with cols[i % 4]:
        # Clickable button for the method name + effectiveness
        if st.button(f"**{method['name']}**\n{method['effectiveness']}", key=f"method_btn_{i}", use_container_width=True):
            st.session_state.selected = method
        # The bordered tile (no separate tier plaque)
        st.markdown(f'<div class="method-tile {method["tier_class"]}"></div>', unsafe_allow_html=True)

# Details expander
if "selected" in st.session_state:
    m = st.session_state.selected
    with st.expander(f"🔍 {m['name']} ({m['effectiveness']})", expanded=True):
        st.write(f"**Mechanism:** {m['mechanism']}")
        st.write("**Pros:** " + ", ".join(m['pros']))
        st.write("**Cons:** " + ", ".join(m['cons']))
        st.write("**Common Side Effects:** {m['side_effects']}")
        st.write("**STI Protection:** " + ("Yes" if m['sti'] else "No"))
        if st.button("Close details"):
            del st.session_state.selected
            st.rerun()

# (Questionnaire, recommendations, table, etc. remain unchanged below)

st.info("This is educational only • Always consult a healthcare provider • Not medical advice • No data is stored on this site.")

st.caption("Contraceptive Compass • Built with ❤️ for informed choices • December 2025")
