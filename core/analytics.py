import streamlit as st
import streamlit.components.v1 as components

def inject_google_analytics():
    if st.session_state.get("_ga_loaded"):
        return
    st.session_state["_ga_loaded"] = True

    components.html(
        """
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-S3RTFPRMLX"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());

          gtag('config', 'G-S3RTFPRMLX', {
            'anonymize_ip': true,
            'allow_google_signals': false,
            'allow_ad_personalization_signals': false
          });
        </script>
        """,
        height=0,
    )
