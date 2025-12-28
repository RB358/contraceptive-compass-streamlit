QUESTIONS = {
    "age_group": {
        "label": "What is your age group?",
        "options": ["Under 20", "20–29", "30–39", "40+"],
        "help": "Age affects which methods are most suitable."
    },
    "smoking": {
        "label": "Do you smoke?",
        "options": ["No", "Yes"],
        "help": "Smoking affects safety of some hormonal methods."
    },
    "bmi": {
        "label": "What is your approximate BMI?",
        "options": ["<30", "30+"],
        "help": "Bodyweight can affect effectiveness of some methods."
    },
    "periods": {
        "label": "Do you experience heavy or painful periods?",
        "options": ["No significant issues", "Moderate", "Severe"],
        "help": "Some methods can help manage menstrual symptoms."
    },
    "breastfeeding": {
        "label": "Are you currently breastfeeding?",
        "options": ["No", "Yes"],
        "help": "Some methods are safer while breastfeeding."
    },
    "conditions": {
        "label": "Do you have any of these conditions?",
        "options": [
            "Migraine with aura",
            "High blood pressure",
            "History of blood clots",
            "None of the above"
        ],
        "multi": True,
        "help": "Certain conditions make some methods unsafe."
    },
    "priority": {
        "label": "What matters most to you?",
        "options": [
            "Highest effectiveness",
            "Avoiding weight gain",
            "Clearer skin",
            "Lowest cost",
            "Hormone-free"
        ],
        "help": "This helps us prioritize recommendations."
    }
}

QUIZ_QUESTIONS = {
    "q1": {
        "label": "1. What is your age group?",
        "options": ["Under 20", "20-34", "35-44", "45+"],
        "help": "Age affects which methods are most suitable."
    },
    "q2": {
        "label": "2. Do you smoke?",
        "options": ["No", "<15 cigarettes/day", ">15 cigarettes/day"],
        "help": "Smoking affects safety of some hormonal methods."
    },
    "q3": {
        "label": "3. What is your approximate BMI?",
        "options": ["<30", "30 or higher"],
        "help": "Bodyweight can affect effectiveness of some methods."
    },
    "q4": {
        "label": "4. Do you experience heavy or painful periods?",
        "options": ["No significant issues", "Heavy bleeding", "Painful periods", "Both heavy and painful"],
        "help": "Some methods can help manage menstrual symptoms."
    },
    "q5": {
        "label": "5. Are you currently breastfeeding?",
        "options": ["No", "Yes"],
        "help": "Some methods are safer while breastfeeding."
    },
    "q6": {
        "label": "6. Do you have any of these conditions?",
        "options": ["None of these", "History of blood clots (VTE)", "Migraine with aura", "High blood pressure"],
        "multi": True,
        "help": "Certain conditions make some methods unsafe."
    },
    "q7": {
        "label": "7. What matters most to you?",
        "options": ["Highest effectiveness", "Avoiding hormones", "Managing periods", "Low maintenance (set and forget)", "Quick return to fertility"],
        "help": "This helps us prioritize recommendations."
    }
}


def encode_answers(answers: dict) -> dict:
    return {
        "has_smoke_heavy": answers.get("q2", "No") != "No",
        "has_clot": "History of blood clots (VTE)" in answers.get("q6", []),
        "has_migraine": "Migraine with aura" in answers.get("q6", []),
        "has_bp": "High blood pressure" in answers.get("q6", []),
        "is_breastfeeding": answers.get("q5", "No") == "Yes",
        "bmi_high": answers.get("q3", "<30") == "30 or higher",
        "heavy_painful": answers.get("q4", "No significant issues") in ["Heavy bleeding", "Painful periods", "Both heavy and painful"],
        "priority": answers.get("q7", "Highest effectiveness")
    }
