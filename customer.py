import streamlit as st
import pandas as pd
from datetime import date
from database import (
    register_account, authenticate, get_account,
    deposit, withdraw, get_transactions
)
from pdf_report import (
    generate_registration_pdf, generate_transaction_pdf, generate_statement_pdf
)
from email_sender import (
    send_registration_email, send_deposit_email,
    send_withdrawal_email, send_statement_email
)


# ── helpers ────────────────────────────────────────────────────────────────────

def _email_status(ok, msg):
    if ok:
        st.success(f"📧 Email sent: {msg}")
    else:
        st.warning(f"📧 Email note: {msg}")


# ── Register ──────────────────────────────────────────────────────────────────

def register_page():
    st.markdown("""
        <div class='boc-header'>
            <h1>Bank of Chakshu</h1>
            <p>Open a New Account</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='auth-wrap'>", unsafe_allow_html=True)
    st.markdown("<div class='boc-card-title'>📋 Registration Form</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        full_name = st.text_input("Full Name *", placeholder="Chakshu Gupta")
        username  = st.text_input("Username *", placeholder="chakshu108")
        email     = st.text_input("Email Address *", placeholder="you@gmail.com")
        phone     = st.text_input("Phone Number *", placeholder="9876543210")
    with col2:
        dob             = st.date_input("Date of Birth *", value=date(2000, 1, 1),
                                        min_value=date(1920, 1, 1), max_value=date.today())
        address         = st.text_area("Address *", placeholder="123 Main St, City, State", height=90)
        initial_deposit = st.number_input("Initial Deposit (Rs.) *", min_value=0.0, step=500.0, value=1000.0)

    st.markdown("---")
    password  = st.text_input("Set Password *", type="password")
    password2 = st.text_input("Confirm Password *", type="password")

    if st.button("Register Account"):
        if not all([full_name, username, email, phone, address, password, password2]):
            st.error("Please fill in all required fields.")
        elif password != password2:
            st.error("Passwords do not match.")
        elif len(password) < 6:
            st.error("Password must be at least 6 characters.")
        else:
            ok, acnt_no, msg = register_account(
                full_name, username, email, str(phone),
                address, str(dob), initial_deposit, password
            )
            if ok:
                acc = get_account(acnt_no)
                st.success(f"✅ {msg}  Your Account Number: **{acnt_no}**")
                st.info("A welcome email with your account details has been sent to your email.")

                # Generate PDF & send email
                pdf_bytes = generate_registration_pdf(acc)
                email_ok, email_msg = send_registration_email(acc, pdf_bytes)
                _email_status(email_ok, email_msg)

                # Also offer PDF download
                st.download_button(
                    "⬇️ Download Welcome Letter (PDF)",
                    data=pdf_bytes,
                    file_name=f"BOC_Welcome_{acnt_no}.pdf",
                    mime="application/pdf"
                )
            else:
                st.error(f"❌ {msg}")

    st.markdown("</div>", unsafe_allow_html=True)


# ── Login ─────────────────────────────────────────────────────────────────────

def login_page():
    st.markdown("""
        <div class='boc-header'>
            <h1>Bank of Chakshu</h1>
            <p>Customer Portal &nbsp;·&nbsp; Secure Banking</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='auth-wrap'>", unsafe_allow_html=True)
    st.markdown("<div class='boc-card-title'>🏦 Customer Login</div>", unsafe_allow_html=True)

    identifier = st.text_input("Username or Account Number", placeholder="chakshu108  or  1000001")
    password   = st.text_input("Password", type="password")

    if st.button("Login"):
        if not identifier or not password:
            st.error("Please enter both credentials.")
        else:
            acc = authenticate(identifier.strip(), password)
            if acc:
                st.session_state["customer_logged_in"] = True
                st.session_state["cust_acnt_no"]       = acc["acnt_no"]
                st.session_state["cust_name"]          = acc["full_name"]
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")

    st.markdown("</div>", unsafe_allow_html=True)


# ── Dashboard ─────────────────────────────────────────────────────────────────

def customer_dashboard():
    acnt_no = st.session_state["cust_acnt_no"]

    # Sidebar
    with st.sidebar:
        acc = get_account(acnt_no)
        st.markdown(f"""
            <div style='padding:1rem 0 0.4rem;'>
                <div style='font-family:Playfair Display,serif;font-size:1.2rem;
                            color:#C9A84C;font-weight:700;'>Bank of Chakshu</div>
                <div style='font-size:0.7rem;color:#7a7a70;letter-spacing:0.1em;
                            text-transform:uppercase;'>Customer Portal</div>
            </div>
            <div style='padding:0.65rem 0.8rem;background:rgba(201,168,76,0.08);
                        border-radius:8px;margin:0.5rem 0 0.2rem;border:1px solid rgba(201,168,76,0.15);'>
                <div style='font-size:0.85rem;font-weight:600;'>{acc['full_name']}</div>
                <div style='font-size:0.72rem;color:#7a7a70;'>@{acc['username']} &nbsp;|&nbsp; A/C #{acnt_no}</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        page = st.radio("", ["🏠 My Account", "⬆️ Deposit", "⬇️ Withdraw", "📜 Statement"],
                        label_visibility="collapsed")
        st.markdown("---")
        if st.button("🚪 Logout"):
            st.session_state["customer_logged_in"] = False
            st.session_state["cust_acnt_no"]       = None
            st.rerun()

    if page == "🏠 My Account":
        _my_account(acc)
    elif page == "⬆️ Deposit":
        _deposit_page(acc)
    elif page == "⬇️ Withdraw":
        _withdraw_page(acc)
    elif page == "📜 Statement":
        _statement_page(acc)


# ── Sub-pages ─────────────────────────────────────────────────────────────────

def _my_account(acc):
    st.markdown(f"""
        <div class='boc-header'>
            <h1>Welcome Back</h1>
            <p>{acc['full_name']}</p>
        </div>
    """, unsafe_allow_html=True)

    txns = get_transactions(acc["acnt_no"])
    c1, c2, c3 = st.columns(3)
    c1.metric("Account Number",   f"#{acc['acnt_no']}")
    c2.metric("Available Balance", f"Rs.{acc['balance']:,.2f}")
    c3.metric("Total Transactions", len(txns))

    st.markdown("---")
    st.markdown("<div class='boc-card'><div class='boc-card-title'>Account Details</div>",
                unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Full Name:** {acc['full_name']}")
        st.markdown(f"**Username:** @{acc['username']}")
        st.markdown(f"**Email:** {acc['email']}")
        st.markdown(f"**Phone:** {acc['phone']}")
    with col2:
        st.markdown(f"**Date of Birth:** {acc['dob']}")
        st.markdown(f"**Address:** {acc['address']}")
        st.markdown(f"**Member Since:** {str(acc['created_at'])[:10]}")
        st.markdown(f"**Balance:** Rs.{acc['balance']:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)

    if txns:
        st.markdown("<div class='boc-card'><div class='boc-card-title'>Recent Activity</div>",
                    unsafe_allow_html=True)
        for t in txns[:4]:
            cls    = "badge-d" if t["txn_type"] == "DEPOSIT" else "badge-w"
            symbol = "+" if t["txn_type"] == "DEPOSIT" else "-"
            st.markdown(f"""
                <div style='display:flex;justify-content:space-between;align-items:center;
                            padding:0.5rem 0;border-bottom:1px solid rgba(201,168,76,0.08);'>
                    <div>
                        <span class='{cls}'>{t['txn_type']}</span>
                        <span style='color:#7a7a70;font-size:0.77rem;margin-left:0.5rem;'>
                            {t['timestamp']}
                        </span>
                    </div>
                    <div style='font-weight:600;'>{symbol}Rs.{t['amount']:,.0f}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


def _deposit_page(acc):
    # refresh account
    acc = get_account(acc["acnt_no"])
    st.markdown("### ⬆️ Deposit Money")
    st.markdown("<div class='boc-card'>", unsafe_allow_html=True)
    st.markdown(f"<div style='color:#7a7a70;font-size:0.85rem;margin-bottom:0.8rem;'>"
                f"Current Balance: <strong style='color:#C9A84C;'>Rs.{acc['balance']:,.2f}</strong></div>",
                unsafe_allow_html=True)

    amount = st.number_input("Amount to Deposit (Rs.)", min_value=0.0, step=500.0, value=1000.0)
    st.caption("Minimum deposit: Rs.1,000")

    if st.button("Confirm Deposit"):
        ok, result, timestamp = deposit(acc["acnt_no"], amount)
        if ok:
            new_balance = result
            st.success(f"✅ Rs.{amount:,.2f} deposited! New Balance: Rs.{new_balance:,.2f}")

            # PDF
            fresh_acc  = get_account(acc["acnt_no"])
            pdf_bytes  = generate_transaction_pdf(fresh_acc, "DEPOSIT", amount, new_balance, timestamp)
            email_ok, email_msg = send_deposit_email(fresh_acc, amount, new_balance, timestamp, pdf_bytes)
            _email_status(email_ok, email_msg)

            st.download_button(
                "⬇️ Download Deposit Receipt (PDF)",
                data=pdf_bytes,
                file_name=f"BOC_Deposit_{acc['acnt_no']}_{timestamp[:10]}.pdf",
                mime="application/pdf"
            )
            st.rerun()
        else:
            st.error(f"❌ {result}")

    st.markdown("</div>", unsafe_allow_html=True)


def _withdraw_page(acc):
    acc = get_account(acc["acnt_no"])
    st.markdown("### ⬇️ Withdraw Money")
    st.markdown("<div class='boc-card'>", unsafe_allow_html=True)
    st.markdown(f"<div style='color:#7a7a70;font-size:0.85rem;margin-bottom:0.8rem;'>"
                f"Current Balance: <strong style='color:#C9A84C;'>Rs.{acc['balance']:,.2f}</strong></div>",
                unsafe_allow_html=True)

    amount = st.number_input("Amount to Withdraw (Rs.)", min_value=0.0, step=500.0, value=1000.0)
    st.caption("Minimum withdrawal: Rs.1,000")

    if st.button("Confirm Withdrawal"):
        ok, result, timestamp = withdraw(acc["acnt_no"], amount)
        if ok:
            new_balance = result
            st.success(f"✅ Rs.{amount:,.2f} withdrawn! New Balance: Rs.{new_balance:,.2f}")

            fresh_acc  = get_account(acc["acnt_no"])
            pdf_bytes  = generate_transaction_pdf(fresh_acc, "WITHDRAWAL", amount, new_balance, timestamp)
            email_ok, email_msg = send_withdrawal_email(fresh_acc, amount, new_balance, timestamp, pdf_bytes)
            _email_status(email_ok, email_msg)

            st.download_button(
                "⬇️ Download Withdrawal Receipt (PDF)",
                data=pdf_bytes,
                file_name=f"BOC_Withdrawal_{acc['acnt_no']}_{timestamp[:10]}.pdf",
                mime="application/pdf"
            )
            st.rerun()
        else:
            st.error(f"❌ {result}")

    st.markdown("</div>", unsafe_allow_html=True)


def _statement_page(acc):
    acc  = get_account(acc["acnt_no"])
    txns = get_transactions(acc["acnt_no"])
    st.markdown("### 📜 Account Statement")

    if not txns:
        st.info("No transactions yet. Start with a deposit!")
        return

    df = pd.DataFrame(txns)[["timestamp", "txn_type", "amount", "balance_after"]]
    df.columns = ["Date & Time", "Type", "Amount (Rs.)", "Balance After (Rs.)"]
    df["Amount (Rs.)"]        = df["Amount (Rs.)"].apply(lambda x: f"{x:,.2f}")
    df["Balance After (Rs.)"] = df["Balance After (Rs.)"].apply(lambda x: f"{x:,.2f}")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        # Email statement
        if st.button("📧 Email Statement PDF"):
            pdf_bytes  = generate_statement_pdf(acc, txns)
            email_ok, email_msg = send_statement_email(acc, pdf_bytes)
            _email_status(email_ok, email_msg)

    with col2:
        # Download statement
        pdf_bytes = generate_statement_pdf(acc, txns)
        st.download_button(
            "⬇️ Download Statement (PDF)",
            data=pdf_bytes,
            file_name=f"BOC_Statement_{acc['acnt_no']}.pdf",
            mime="application/pdf"
        )
