import streamlit as st

def start_cta():
    st.markdown(
        """
        <style>
        .start-cta-wrapper {
            display: flex;
            justify-content: center;
            margin-top: -170px;
            margin-bottom: 80px;
            position: relative;
            z-index: 10;
        }

        .start-cta-button {
            background-color: #ffffff !important;
            color: #111827 !important;
            font-size: 1.1rem;
            font-weight: 600;
            padding: 14px 44px;
            border-radius: 999px;
            border: 1px solid rgba(0, 0, 0, 0.08);
            text-decoration: none !important;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
            transition: all 0.2s ease;
        }

        .start-cta-button:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 28px rgba(0, 0, 0, 0.18);
            color: #111827 !important;
            text-decoration: none !important;
        }

        .start-cta-button:active {
            transform: translateY(0);
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.10);
        }

        .start-cta-button:visited {
            color: #111827 !important;
        }
        </style>

        <div class="start-cta-wrapper">
            <a href="?start=1" class="start-cta-button">Start</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
