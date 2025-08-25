# app/components/cards.py
import streamlit as st

def render_info_card(title: str, value: str):
    """Renders a simple card with a title and a value."""
    st.markdown(
        f"""
        <div style="
            border: 1px solid #4f515e;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
        ">
            <h5 style="margin: 0; color: #a1a3ab;">{title}</h5>
            <p style="margin: 5px 0 0 0; font-size: 1.1em;">{value if value else 'Not Found'}</p>
        </div>
        """,
        unsafe_allow_html=True
    )