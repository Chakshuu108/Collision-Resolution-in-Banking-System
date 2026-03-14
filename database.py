import sqlite3
from datetime import datetime

DB_PATH = "bank_of_chakshu.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            acnt_no         INTEGER UNIQUE NOT NULL,
            full_name       TEXT NOT NULL,
            username        TEXT UNIQUE NOT NULL,
            email           TEXT UNIQUE NOT NULL,
            phone           TEXT NOT NULL,
            address         TEXT NOT NULL,
            dob             TEXT NOT NULL,
            balance         REAL NOT NULL DEFAULT 0.0,
            password        TEXT NOT NULL,
            created_at      TEXT DEFAULT (datetime('now','localtime'))
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            acnt_no         INTEGER NOT NULL,
            txn_type        TEXT NOT NULL,
            amount          REAL NOT NULL,
            balance_after   REAL NOT NULL,
            timestamp       TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (acnt_no) REFERENCES accounts(acnt_no)
        )
    """)

    conn.commit()
    conn.close()


# ── helpers ────────────────────────────────────────────────────────────────────

def _next_account_number():
    """Auto-generate unique 7-digit account number."""
    conn = get_connection()
    row = conn.execute("SELECT MAX(acnt_no) FROM accounts").fetchone()[0]
    conn.close()
    return (row + 1) if row else 1000001


# ── CRUD ───────────────────────────────────────────────────────────────────────

def register_account(full_name, username, email, phone, address, dob, initial_deposit, password):
    if initial_deposit < 0:
        initial_deposit = 0.0
    acnt_no = _next_account_number()
    conn = get_connection()
    try:
        conn.execute("""
            INSERT INTO accounts
                (acnt_no, full_name, username, email, phone, address, dob, balance, password)
            VALUES (?,?,?,?,?,?,?,?,?)
        """, (acnt_no, full_name, username, email, phone, address, dob, initial_deposit, password))
        conn.commit()
        return True, acnt_no, "Account registered successfully."
    except sqlite3.IntegrityError as e:
        msg = str(e)
        if "username" in msg:
            return False, None, "Username already taken."
        if "email" in msg:
            return False, None, "Email already registered."
        return False, None, "Registration failed. Try again."
    finally:
        conn.close()


def authenticate(username_or_acnt, password):
    """Login via username OR account number."""
    conn = get_connection()
    # try username first, then account number
    row = conn.execute(
        "SELECT * FROM accounts WHERE (username=? OR CAST(acnt_no AS TEXT)=?) AND password=?",
        (username_or_acnt, username_or_acnt, password)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def get_account(acnt_no):
    conn = get_connection()
    row = conn.execute("SELECT * FROM accounts WHERE acnt_no=?", (acnt_no,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_accounts():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM accounts ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def deposit(acnt_no, amount):
    if amount < 1000:
        return False, "Deposit must be at least Rs.1,000.", None
    conn = get_connection()
    acc = conn.execute("SELECT balance FROM accounts WHERE acnt_no=?", (acnt_no,)).fetchone()
    if not acc:
        conn.close()
        return False, "Account not found.", None
    new_bal = acc["balance"] + amount
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("UPDATE accounts SET balance=? WHERE acnt_no=?", (new_bal, acnt_no))
    conn.execute(
        "INSERT INTO transactions (acnt_no, txn_type, amount, balance_after, timestamp) VALUES (?,?,?,?,?)",
        (acnt_no, "DEPOSIT", amount, new_bal, now)
    )
    conn.commit()
    conn.close()
    return True, new_bal, now


def withdraw(acnt_no, amount):
    if amount < 1000:
        return False, "Withdrawal must be at least Rs.1,000.", None
    conn = get_connection()
    acc = conn.execute("SELECT balance FROM accounts WHERE acnt_no=?", (acnt_no,)).fetchone()
    if not acc:
        conn.close()
        return False, "Account not found.", None
    if amount > acc["balance"]:
        conn.close()
        return False, "Insufficient balance.", None
    new_bal = acc["balance"] - amount
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("UPDATE accounts SET balance=? WHERE acnt_no=?", (new_bal, acnt_no))
    conn.execute(
        "INSERT INTO transactions (acnt_no, txn_type, amount, balance_after, timestamp) VALUES (?,?,?,?,?)",
        (acnt_no, "WITHDRAWAL", amount, new_bal, now)
    )
    conn.commit()
    conn.close()
    return True, new_bal, now


def delete_account_db(acnt_no):
    conn = get_connection()
    cur = conn.execute("DELETE FROM accounts WHERE acnt_no=?", (acnt_no,))
    conn.commit()
    conn.close()
    return cur.rowcount > 0


def get_transactions(acnt_no):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM transactions WHERE acnt_no=? ORDER BY timestamp DESC", (acnt_no,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_transactions():
    conn = get_connection()
    rows = conn.execute("""
        SELECT t.*, a.full_name, a.username
        FROM transactions t
        JOIN accounts a ON t.acnt_no = a.acnt_no
        ORDER BY t.timestamp DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_stats():
    conn = get_connection()
    total_accounts    = conn.execute("SELECT COUNT(*) FROM accounts").fetchone()[0]
    total_balance     = conn.execute("SELECT COALESCE(SUM(balance),0) FROM accounts").fetchone()[0]
    total_deposits    = conn.execute("SELECT COALESCE(SUM(amount),0) FROM transactions WHERE txn_type='DEPOSIT'").fetchone()[0]
    total_withdrawals = conn.execute("SELECT COALESCE(SUM(amount),0) FROM transactions WHERE txn_type='WITHDRAWAL'").fetchone()[0]
    conn.close()
    return {
        "total_accounts": total_accounts,
        "total_balance": total_balance,
        "total_deposits": total_deposits,
        "total_withdrawals": total_withdrawals,
    }
