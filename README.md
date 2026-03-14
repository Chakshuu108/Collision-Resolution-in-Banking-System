# 🏦 Bank of Chakshu — Streamlit Banking System

Full-stack banking app with registration, login, PDF receipts, and Gmail email notifications.

---

## Project Structure

```
banking_system/
├── app.py              ← Entry point — run this
├── database.py         ← SQLite database (all CRUD operations)
├── customer.py         ← Register, Login, Deposit, Withdraw, Statement
├── admin.py            ← Admin dashboard
├── pdf_report.py       ← PDF generator (reportlab) — receipts & statements
├── email_sender.py     ← Gmail SMTP email notifications
├── styles.py           ← Dark gold CSS theme
├── requirements.txt
├── .streamlit/
│   └── secrets.toml    ← ⚠️  EDIT THIS with your Gmail credentials
└── bank_of_chakshu.db  ← Auto-created SQLite database on first run
```

---

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure Gmail (see below)
# Edit .streamlit/secrets.toml

# 3. Run
streamlit run app.py
```

App opens at **http://localhost:8501**

---

## Gmail Email Setup (Required for email features)

Edit `.streamlit/secrets.toml`:

```toml
[email]
sender  = "yourgmail@gmail.com"
app_pwd = "xxxx xxxx xxxx xxxx"
```

### How to get your Gmail App Password:
1. Go to **myaccount.google.com → Security**
2. Enable **2-Step Verification**
3. Go to **Security → App Passwords**
4. Select **Mail** + **Other (custom name)** → "Bank of Chakshu"
5. Copy the 16-character password → paste into `secrets.toml`

> Without this setup, the app still works — emails just won't send, and a warning appears.

---

## Login Credentials

### Admin
| Field    | Value             |
|----------|-------------------|
| Username | `chakshugupta108` |
| Password | `BANKOFCHAKSHU`   |

### Customer
- Register a new account via the **Register** tab
- Login with your **Username** or **Account Number** + password

---

## Features

### Customer Portal
| Feature | Description |
|---|---|
| Register | Full form: Name, Username, Email, Phone, DOB, Address, Initial Deposit, Password |
| Login | Via username OR account number |
| My Account | Balance, full profile, recent activity |
| Deposit | Min Rs.1,000 → PDF receipt emailed + downloadable |
| Withdraw | Min Rs.1,000, balance checked → PDF receipt emailed + downloadable |
| Statement | Full transaction history → PDF emailed + downloadable |

### Admin Portal
| Feature | Description |
|---|---|
| Dashboard | Live stats, recent accounts & transactions |
| All Accounts | Complete customer database |
| All Transactions | Full transaction log |
| Delete Account | Preview + permanent delete |

### Email Notifications
Every action triggers a **branded HTML email** with a **PDF attachment**:
- ✅ Registration → Welcome letter with account details
- ✅ Deposit → Deposit receipt with amount & new balance
- ✅ Withdrawal → Withdrawal receipt with amount & new balance
- ✅ Statement request → Full PDF statement

---

## Business Rules (from C++ original)
- Account numbers: auto-assigned 7-digit (1000001, 1000002 …)
- Minimum deposit: **Rs.1,000**
- Minimum withdrawal: **Rs.1,000**
- Cannot withdraw more than available balance
