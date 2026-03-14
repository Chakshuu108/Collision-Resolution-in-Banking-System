# 🏦 Bank of Chakshu — Streamlit Banking System

---

## Project Structure

```
banking_system/
├── app.py              ← Entry point
├── database.py         ← SQLite (all CRUD)
├── customer.py         ← Register, Login, Deposit, Withdraw, Statement
├── admin.py            ← Admin dashboard
├── pdf_report.py       ← PDF receipts & statements (reportlab)
├── email_sender.py     ← Gmail SMTP notifications
├── styles.py           ← Dark gold CSS theme
└── requirements.txt
```

---

## Deploy on Streamlit Cloud

1. Push this folder to a **GitHub repo**
2. Go to **share.streamlit.io** → New app → select repo → set `app.py` as entry
3. Click **Deploy**
4. In the app → **Settings → Secrets**, paste:

```toml
[email]
sender  = "yourgmail@gmail.com"
app_pwd = "xxxx xxxx xxxx xxxx"
```

### How to get your Gmail App Password
1. Google Account → Security → enable **2-Step Verification**
2. Security → **App Passwords** → Mail → Other → name it "Bank of Chakshu"
3. Copy the 16-char password → paste as `app_pwd`

No local secrets file needed for Streamlit Cloud.

---

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

For local email, create `.streamlit/secrets.toml` with the same `[email]` block above.

---

## Credentials

**Admin** — Username: `chakshugupta108` | Password: `BANKOFCHAKSHU`

**Customer** — Register first, then login with username or account number.

---

## What Happens on Every Action

| Action | Email sent | PDF attached |
|---|---|---|
| Register | Welcome letter | Account details letter |
| Deposit | Deposit confirmation | Receipt with amount & balance |
| Withdraw | Withdrawal confirmation | Receipt with amount & balance |
| Statement | Statement email | Full transaction history PDF |
