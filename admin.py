import streamlit as st
import pandas as pd
from database import (
    get_all_accounts, get_all_transactions, get_stats,
    delete_account_db, get_account
)

ADMIN_USERNAME = "chakshugupta108"
ADMIN_PASSWORD = "BANKOFCHAKSHU"


def admin_login():
    st.markdown("""
        <div class='boc-header'>
            <h1>Bank of Chakshu</h1>
            <p>Admin Portal &nbsp;·&nbsp; Restricted Access</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='auth-wrap'>", unsafe_allow_html=True)
    st.markdown("<div class='boc-card-title'>🔐 Administrator Login</div>", unsafe_allow_html=True)

    username = st.text_input("Admin Username")
    password = st.text_input("Admin Password", type="password")

    if st.button("Login as Admin"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state["admin_logged_in"] = True
            st.rerun()
        else:
            st.error("Invalid credentials. Access denied.")

    st.markdown("</div>", unsafe_allow_html=True)


def admin_dashboard():
    with st.sidebar:
        st.markdown("""
            <div style='padding:1rem 0 0.4rem;'>
                <div style='font-family:Playfair Display,serif;font-size:1.2rem;
                            color:#C9A84C;font-weight:700;'>Bank of Chakshu</div>
                <div style='font-size:0.7rem;color:#7a7a70;letter-spacing:0.1em;
                            text-transform:uppercase;'>Admin Panel</div>
            </div>
            <div style='padding:0.55rem 0.8rem;background:rgba(201,168,76,0.08);
                        border-radius:8px;margin:0.4rem 0;border:1px solid rgba(201,168,76,0.15);'>
                <div style='font-size:0.82rem;font-weight:600;'>chakshugupta108</div>
                <div style='font-size:0.7rem;color:#7a7a70;'>Administrator</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        page = st.radio("", [
            "📊 Dashboard", "👥 All Accounts",
            "📋 All Transactions", "🗑️ Delete Account"
        ], label_visibility="collapsed")
        st.markdown("---")
        if st.button("🚪 Logout"):
            st.session_state["admin_logged_in"] = False
            st.rerun()

    if page == "📊 Dashboard":
        _dashboard()
    elif page == "👥 All Accounts":
        _all_accounts()
    elif page == "📋 All Transactions":
        _all_transactions()
    elif page == "🗑️ Delete Account":
        _delete_account()


def _dashboard():
    st.markdown("<div class='boc-header'><h1>Bank of Chakshu</h1><p>Admin Dashboard</p></div>",
                unsafe_allow_html=True)

    stats = get_stats()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Accounts",   stats["total_accounts"])
    c2.metric("Total Balance",    f"Rs.{stats['total_balance']:,.0f}")
    c3.metric("Total Deposited",  f"Rs.{stats['total_deposits']:,.0f}")
    c4.metric("Total Withdrawn",  f"Rs.{stats['total_withdrawals']:,.0f}")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='boc-card'><div class='boc-card-title'>Recent Accounts</div>",
                    unsafe_allow_html=True)
        accounts = get_all_accounts()[:6]
        for a in accounts:
            st.markdown(f"""
                <div style='display:flex;justify-content:space-between;align-items:center;
                            padding:0.45rem 0;border-bottom:1px solid rgba(201,168,76,0.08);'>
                    <div>
                        <div style='font-size:0.9rem;font-weight:500;'>{a['full_name']}</div>
                        <div style='font-size:0.73rem;color:#7a7a70;'>@{a['username']} · #{a['acnt_no']}</div>
                    </div>
                    <div style='color:#C9A84C;font-weight:600;font-size:0.88rem;'>
                        Rs.{a['balance']:,.0f}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='boc-card'><div class='boc-card-title'>Recent Transactions</div>",
                    unsafe_allow_html=True)
        txns = get_all_transactions()[:6]
        for t in txns:
            cls    = "badge-d" if t["txn_type"] == "DEPOSIT" else "badge-w"
            symbol = "+" if t["txn_type"] == "DEPOSIT" else "-"
            st.markdown(f"""
                <div style='display:flex;justify-content:space-between;align-items:center;
                            padding:0.45rem 0;border-bottom:1px solid rgba(201,168,76,0.08);'>
                    <div>
                        <div style='font-size:0.85rem;font-weight:500;'>{t['full_name']}</div>
                        <span class='{cls}'>{t['txn_type']}</span>
                    </div>
                    <div style='font-size:0.88rem;font-weight:600;'>
                        {symbol}Rs.{t['amount']:,.0f}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


def _all_accounts():
    st.markdown("### 👥 All Customer Accounts")
    accounts = get_all_accounts()
    if not accounts:
        st.info("No accounts found.")
        return
    df = pd.DataFrame(accounts)[[
        "acnt_no","full_name","username","email","phone","dob","address","balance","created_at"
    ]]
    df.columns = ["A/C No.","Full Name","Username","Email","Phone","DOB","Address","Balance (Rs.)","Joined"]
    df["Balance (Rs.)"] = df["Balance (Rs.)"].apply(lambda x: f"{x:,.2f}")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown(f"<div style='color:#7a7a70;font-size:0.8rem;'>Total: {len(accounts)} accounts</div>",
                unsafe_allow_html=True)


def _all_transactions():
    st.markdown("### 📋 All Transactions")
    txns = get_all_transactions()
    if not txns:
        st.info("No transactions yet.")
        return
    df = pd.DataFrame(txns)[["timestamp","acnt_no","full_name","txn_type","amount","balance_after"]]
    df.columns = ["Timestamp","A/C No.","Name","Type","Amount (Rs.)","Balance After (Rs.)"]
    df["Amount (Rs.)"]        = df["Amount (Rs.)"].apply(lambda x: f"{x:,.2f}")
    df["Balance After (Rs.)"] = df["Balance After (Rs.)"].apply(lambda x: f"{x:,.2f}")
    st.dataframe(df, use_container_width=True, hide_index=True)


def _delete_account():
    st.markdown("### 🗑️ Delete Account")
    st.markdown("<div class='boc-card'>", unsafe_allow_html=True)

    acnt_no = st.number_input("Enter 7-Digit Account Number", min_value=1000000, max_value=9999999,
                               step=1, value=1000001)
    acc = get_account(int(acnt_no))
    if acc:
        st.markdown(f"""
            <div style='padding:0.8rem;background:rgba(201,168,76,0.07);border-radius:8px;margin:0.6rem 0;'>
                <div style='font-weight:600;'>{acc['full_name']} &nbsp;(@{acc['username']})</div>
                <div style='color:#7a7a70;font-size:0.82rem;'>
                    {acc['email']} &nbsp;|&nbsp; Rs.{acc['balance']:,.2f}
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.warning("⚠️ This permanently deletes the account and all its data.")
        if st.button("Confirm Delete"):
            if delete_account_db(int(acnt_no)):
                st.success("Account deleted successfully.")
            else:
                st.error("Failed to delete.")
    else:
        st.info("Enter a valid account number above to preview.")

    st.markdown("</div>", unsafe_allow_html=True)
