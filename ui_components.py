import streamlit as st

def start_cta():
    st.markdown(
        """
        <style>
        .start-cta-wrapper {
            display: flex;
            justify-content: center;
            margin-top: 32px;
            margin-bottom: 48px;
        }

        .start-cta-button {
            background-color: #ffffff;
            color: #111827; /* near-black, high contrast */
            font-size: 1.1rem;
            font-weight: 600;
            padding: 14px 44px;
            border-radius: 999px; /* capsule */
            border: 1px solid rgba(0, 0, 0, 0.08);
            text-decoration: none;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
            transition: all 0.2s ease;
        }

        .start-cta-button:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 28px rgba(0, 0, 0, 0.12);
        }

        .start-cta-button:active {
            transform: translateY(0);
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.10);
        }
        </style>

        <div class="start-cta-wrapper">
            <a href="?start=1" class="start-cta-button">Start</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
