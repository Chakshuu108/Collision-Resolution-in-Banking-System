import streamlit as st
from database import init_db
from styles import STYLE
from admin import admin_login, admin_dashboard
from customer import register_page, login_page, customer_dashboard

st.set_page_config(
    page_title="Bank of Chakshu",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()
st.markdown(STYLE, unsafe_allow_html=True)

# ── Session defaults ───────────────────────────────────────────────────────────
for key, val in {
    "admin_logged_in":    False,
    "customer_logged_in": False,
    "cust_acnt_no":       None,
    "cust_name":          None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── Routing ────────────────────────────────────────────────────────────────────

if st.session_state["admin_logged_in"]:
    admin_dashboard()

elif st.session_state["customer_logged_in"]:
    customer_dashboard()

else:
    # Landing — choose portal
    st.markdown("""
        <div style='text-align:center;padding:2rem 0 0.8rem;'>
            <div style='font-family:Playfair Display,serif;font-size:3rem;font-weight:900;
                        color:#C9A84C;letter-spacing:0.04em;line-height:1.1;'>
                Bank of Chakshu
            </div>
            <div style='font-size:0.76rem;color:#7a7a70;letter-spacing:0.18em;
                        text-transform:uppercase;margin-top:0.4rem;'>
                Collision-Resolution Banking System
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Portal selector
    _, mid, _ = st.columns([2, 3, 2])
    with mid:
        portal = st.selectbox(
            "", ["🏦 Customer Portal", "🔐 Admin Portal"],
            label_visibility="collapsed"
        )

    if "Admin" in portal:
        admin_login()
    else:
        # Customer: Login / Register tabs
        _, mid2, _ = st.columns([1, 4, 1])
        with mid2:
            tab_login, tab_register = st.tabs(["🔑 Login", "📋 Register"])
            with tab_login:
                login_page()
            with tab_register:
                register_page()
