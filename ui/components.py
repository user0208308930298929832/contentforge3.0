
import streamlit as st

def header(logo_path: str, app_name: str, credits: int):
    c1, c2, c3 = st.columns([0.62, 0.2, 0.18])
    with c1:
        st.markdown(f"<div style='display:flex;gap:10px;align-items:center'><img src='app://assets/logo.svg' height='28'/>"
                    f"<div style='font-weight:600;font-size:18px'> {app_name}</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div style='text-align:right'>Créditos: <b>{credits}</b></div>", unsafe_allow_html=True)

def section_title(title: str, kicker: str=""):
    st.markdown(f"### {title}")
    if kicker:
        st.caption(kicker)

def card(html: str):
    st.markdown(f"<div style='background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:14px'>{html}</div>", unsafe_allow_html=True)
