import streamlit as st

st.set_page_config(page_title="Contraceptive Choices", layout="centered")

# Single merged CSS for teal theme, centering, and fixed button
st.markdown("""
<style>
    .main {
        background: #f0fafa;
        padding-bottom: 100px;  /* Space for fixed button */
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
    /* Centering for mobile/desktop */
    .main .block-container {
        max-width: 90% !important;
        padding-left: 5% !important;
        padding-right: 5% !important;
        padding-top: 2rem !important;
    }
    h1, h2, h3, h4, .stMarkdown, p, div {text-align: center !important;}
        /* Center ALL buttons (including "Get Recommendations") */
    .stButton {
        text-align: center !important;

            /* Center the entire button container and button */
    div.stButton {
        text-align: center !important;
    }
    .stButton > button {
        display: inline-block !important;
        margin: 20px auto !important;
        width: 90% !important;
        max-width: 400px !important;
    }
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
    /* Fixed button */
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

# Disclaimer
st.info("**Disclaimer:** None of your answers or data are stored by us. This is educational only • Always consult a healthcare provider • Not medical advice.")

# Methods data
methods = [
    {"name": "Oral Contraceptive Pill", "image": "http://media.self.com/photos/5e986f441911a00008b4275d/master/pass/birthcontrol_pills.jpg", "perfect": "<1%", "typical": "7%", "pros": ["Regulates periods", "Reduces acne", "Daily control"], "cons": ["Daily pill", "No STI protection", "Side effects possible"]},
    {"name": "Male Condom", "image": "https://post.healthline.com/wp-content/uploads/2022/02/male-condoms-1296x1000-body-1296x1004.png", "perfect": "2%", "typical": "13%", "pros": ["STI protection", "No hormones", "Widely available"], "cons": ["User-dependent", "Can break"]},
    {"name": "Contraceptive Implant", "image": "https://blog.thelowdown.com/wp-content/uploads/2020/10/implant-side-effects.png", "perfect": "<1%", "typical": "<1%", "pros": ["3-5 years protection", "Highly effective", "Reversible"], "cons": ["Insertion procedure", "Irregular bleeding"]},
    {"name": "Hormonal IUD (e.g., Mirena)", "image": "https://www.plannedparenthood.org/uploads/filer_public_thumbnails/filer_public/6b/ed/6bedc931-35c4-4f5a-bc65-e3839ae6b6de/hormonal-and-copper-iud-illustration.gif__1200x1200_q65_subsampling-2.jpg", "perfect": "<1%", "typical": "<1%", "pros": ["5-8 years", "Lighter periods", "Low maintenance"], "cons": ["Insertion cramping"]},
    {"name": "Copper IUD (ParaGard)", "image": "https://www.mayoclinic.org/-/media/kcms/gbs/patient-consumer/images/2013/08/26/10/19/my00997_im04275_mcdc7_paragard_photothu_jpg.jpg", "perfect": "<1%", "typical": "<1%", "pros": ["10+ years", "Hormone-free", "Emergency option"], "cons": ["Heavier periods"]},
    {"name": "Depo-Provera Injection", "image": "https://www.verywellhealth.com/thmb/zML8U8nV3QmdRdO_eC1l1QI5Sqs=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/depo-56a1c4193df78cf7726dc0e9.jpg", "perfect": "<1%", "typical": "4%", "pros": ["Every 3 months", "No daily routine"], "cons": ["Delayed fertility return", "Bone density concerns"]},
    {"name": "Contraceptive Patch", "image": "https://www.nhsinform.scot/wp-content/uploads/2024/02/contraceptive-patch-1.jpg", "perfect": "<1%", "typical": "7%", "pros": ["Weekly change", "Regulates periods"], "cons": ["Visible", "Skin irritation possible"]},
    {"name": "Vaginal Ring (NuvaRing)", "image": "https://www.obgynecologistnyc.com/wp-content/uploads/2016/09/Nuvaring-Birth-Control-Vaginal-Ring.jpg", "perfect": "<1%", "typical": "7%", "pros": ["Monthly", "Low dose hormones"], "cons": ["Insertion required"]},
    {"name": "Female Condom", "image": "https://www.cdc.gov/condom-use/media/images/Femalecondom5hires.png", "perfect": "5%", "typical": "21%", "pros": ["STI protection", "User control"], "cons": ["Higher failure rate"]},
    {"name": "Diaphragm", "image": "https://ixbapi.healthwise.net/Resource/14.7/en-us/media/medical/hw/aco3583_368x240.jpg", "perfect": "6%", "typical": "17%", "pros": ["Reusable", "Hormone-free"], "cons": ["Insertion each time", "Spermicide needed"]},
    {"name": "Fertility Awareness", "image": "https://images.squarespace-cdn.com/content/v1/5ce5fdaed49c8900017d5630/1604508343420-GX1XCK067VKE20TZ1FWY/Cycle+13+marked.png", "perfect": "1-9%", "typical": "24%", "pros": ["No hormones", "Free"], "cons": ["High effort", "Irregular cycles reduce reliability"]},
]

st.title("Contraceptive Choices")
st.markdown("### Explore methods, learn effectiveness, and find what fits you")

# Methods cards
for method in methods:
    with st.container():
        st.image(method["image"], use_column_width=True)
        st.markdown(f"<div class='method-card'><h3>{method['name']}</h3>"
                    f"<p><strong>Perfect use:</strong> {method['perfect']} failure<br>"
                    f"<strong>Typical use:</strong> {method['typical']} failure</p>"
                    f"<p><strong>Pros:</strong> {', '.join(method['pros'])}</p>"
                    f"<p><strong>Cons:</strong> {', '.join(method['cons'])}</p></div>", unsafe_allow_html=True)

# Quiz
st.header("📊 Find Your Match")
st.markdown("Answer these questions for personalized insights")
q1 = st.selectbox("1. What is your age group?", ["Under 20", "20-34", "35-44", "45+"], help="Age affects which methods are most suitable.")
q2 = st.selectbox("2. Do you smoke?", ["No", "<15 cigarettes/day", ">15 cigarettes/day"], help="Smoking affects safety of some hormonal methods.")
q3 = st.selectbox("3. What is your approximate BMI?", ["<30", "30 or higher"], help="Bodyweight can affect effectiveness of some methods.")
q4 = st.selectbox("4. Do you experience heavy or painful periods?", ["No significant issues", "Heavy bleeding", "Painful periods", "Both heavy and painful"], help="Some methods can help manage menstrual symptoms")
q5 = st.selectbox("5. Are you currently breastfeeding?", ["No", "Yes"], help="Some methods are safer while breastfeeding.")
q6 = st.multiselect("6. Do you have any of these conditions?", ["None of these", "History of blood clots (VTE)", "Migraine with aura", "High blood pressure"], help="Certain conditions make some methods unsafe.")
q7 = st.selectbox("7. What matters most to you?", ["Highest effectiveness", "Avoiding hormones", "Managing periods", "Low maintenance (set and forget)", "Quick return to fertility"], help="This helps us prioritize recommendations.")

if st.button("Get Recommendations"):
    contraindicated = []
    caution = []
    recommended = []

    has_smoke_heavy = q2 != "No"
    has_clot = "History of blood clots (VTE)" in q6
    has_migraine = "Migraine with aura" in q6
    has_bp = "High blood pressure" in q6
    breastfeeding = q5 == "Yes"
    bmi_high = q3 == "30 or higher"
    heavy_painful = q4 in ["Heavy bleeding", "Painful periods", "Both heavy and painful"]
    priority = q7

    for m in methods:
        name = m["name"]
        red = False

        # Contraindications for combined hormonal (Pill, Patch, Ring)
        if "Pill" in name or "Patch" in name or "Ring" in name:
            if has_smoke_heavy or has_clot or has_migraine or has_bp:
                red = True

        # Contraindications for progestin-only long-acting (Implant, Hormonal IUD, Depo)
        if "Implant" in name or "Hormonal IUD" in name or "Depo" in name:
            if has_clot:
                red = True

        # Caution for breastfeeding + hormonal
        if breastfeeding and ("hormonal" in name.lower() or "Pill" in name or "Patch" in name or "Ring" in name or "Implant" in name or "Hormonal IUD" in name or "Depo" in name):
            caution.append(m)
            if red:
                contraindicated.append(m)
            continue

        if red:
            contraindicated.append(m)
        elif priority == "Highest effectiveness" and m["typical"] == "<1%":
            recommended.append(m)
        elif priority == "Avoiding hormones" and ("Copper IUD" in name or "Condom" in name or "Diaphragm" in name or "Fertility Awareness" in name):
            recommended.append(m)
        elif priority == "Managing periods" and "Lighter periods" in m["pros"]:
            recommended.append(m)
        elif priority == "Low maintenance (set and forget)" and ("years" in " ".join(m["pros"]) or "3 months" in " ".join(m["pros"])):
            recommended.append(m)
        elif priority == "Quick return to fertility" and "Condom" in name or "Diaphragm" in name or "Fertility Awareness" in name:
            recommended.append(m)
        else:
            if m not in recommended and m not in contraindicated:
                caution.append(m)

    st.success("### Your Personalized Insights")
    if recommended:
        st.markdown("**🟢 Recommended for you:**")
        for m in recommended:
            st.markdown(f"- {m['name']} ({m['typical']} typical failure)")
    if caution:
        st.markdown("**🟡 Use with caution:**")
        for m in caution:
            st.markdown(f"- {m['name']}")
    if contraindicated:
        st.markdown("**🔴 Avoid (contraindicated):**")
        for m in contraindicated:
            st.markdown(f"- {m['name']}")

# Telehealth options (secure)
telehealth_options = [
    {"name": "Nurx", "url": "https://www.nurx.com/birth-control/"},
    {"name": "Pandia Health", "url": "https://www.pandiahealth.com"},
    {"name": "Twentyeight Health", "url": "https://www.twentyeighthealth.com/birth-control"},
    {"name": "Planned Parenthood Health Centers", "url": "https://www.plannedparenthood.org/health-center"},
    {"name": "Lemonaid Health", "url": "https://www.lemonaidhealth.com/"},
    {"name": "Sesame Care", "url": "https://sesamecare.com/medication/birth-control"},
    {"name": "PRJKT RUBY", "url": "https://prjktruby.com"},
    {"name": "GoodRx Care", "url": "https://www.goodrx.com/care"},
]

# Fixed Book Doctor button
st.markdown("<div class='fixed-button-container'><div class='fixed-button-inner'>", unsafe_allow_html=True)
with st.expander("📅 Book Doctor Now – Choose a Service", expanded=False):
    for service in telehealth_options:
        st.markdown(f"[{service['name']} →]({service['url']})")
st.markdown("</div></div>", unsafe_allow_html=True)

st.caption("Contraceptive Choices • Educational tool • December 2025")
