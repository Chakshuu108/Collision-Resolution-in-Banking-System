import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime


# ── Config — reads from Streamlit Cloud Secrets ───────────────────────────────
# In Streamlit Cloud dashboard → App Settings → Secrets, add:
#
#   [email]
#   sender  = "yourgmail@gmail.com"
#   app_pwd = "xxxx xxxx xxxx xxxx"
#
# That's it. No local file needed.

def _get_config():
    try:
        import streamlit as st

        # Try nested [email] section first
        try:
            sender  = st.secrets["email"]["sender"]
            app_pwd = st.secrets["email"]["app_pwd"]
            if sender and app_pwd:
                return sender.strip(), app_pwd.strip()
        except (KeyError, TypeError):
            pass

        # Try flat root-level keys
        try:
            sender  = st.secrets["sender"]
            app_pwd = st.secrets["app_pwd"]
            if sender and app_pwd:
                return sender.strip(), app_pwd.strip()
        except (KeyError, TypeError):
            pass

        return None, None

    except Exception:
        return None, None


def debug_secrets():
    try:
        import streamlit as st
        keys = list(st.secrets.keys())
        nested = {}
        for k in keys:
            try:
                nested[k] = list(st.secrets[k].keys())
            except Exception:
                nested[k] = "flat"
        return f"Secret keys found: {nested}"
    except Exception as e:
        return f"Could not read secrets: {e}"


def _build_html_body(action_label, acc, extra_rows: list[tuple]) -> str:
    """Branded HTML email body."""
    now = datetime.now().strftime("%d %B %Y, %I:%M %p")
    rows_html = "".join(
        f"""<tr>
              <td style="padding:7px 12px;background:#f7f5f0;color:#888880;
                         font-size:13px;font-weight:600;width:40%;">{k}</td>
              <td style="padding:7px 12px;font-size:13px;">{v}</td>
            </tr>"""
        for k, v in extra_rows
    )
    return f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="margin:0;padding:0;background:#f0ede6;font-family:'DM Sans',Arial,sans-serif;">
      <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
          <td align="center" style="padding:30px 15px;">
            <table width="600" cellpadding="0" cellspacing="0"
                   style="background:#ffffff;border-radius:12px;overflow:hidden;
                          box-shadow:0 4px 24px rgba(0,0,0,0.10);">

              <!-- Header -->
              <tr>
                <td style="background:#0D0D0D;padding:28px 32px;text-align:center;">
                  <div style="font-size:26px;font-weight:900;color:#C9A84C;
                              letter-spacing:1px;font-family:Georgia,serif;">
                    Bank of Chakshu
                  </div>
                  <div style="font-size:10px;color:#7a7a70;letter-spacing:3px;
                              text-transform:uppercase;margin-top:4px;">
                    Collision-Resolution Banking System
                  </div>
                </td>
              </tr>

              <!-- Action banner -->
              <tr>
                <td style="background:#C9A84C;padding:14px 32px;text-align:center;">
                  <span style="font-size:13px;font-weight:700;color:#0D0D0D;
                               letter-spacing:2px;text-transform:uppercase;">
                    {action_label}
                  </span>
                  <span style="float:right;font-size:11px;color:#0D0D0D;opacity:0.7;">
                    {now}
                  </span>
                </td>
              </tr>

              <!-- Greeting -->
              <tr>
                <td style="padding:24px 32px 8px;">
                  <p style="margin:0;font-size:15px;color:#1a1a1a;">
                    Dear <strong>{acc.get('full_name','Customer')}</strong>,
                  </p>
                  <p style="margin:8px 0 0;font-size:13px;color:#555550;line-height:1.6;">
                    This is an automated notification from <strong>Bank of Chakshu</strong>
                    regarding your account activity. A detailed PDF report is attached below.
                  </p>
                </td>
              </tr>

              <!-- Details table -->
              <tr>
                <td style="padding:12px 32px;">
                  <table width="100%" cellpadding="0" cellspacing="0"
                         style="border:1px solid #e8e5de;border-radius:8px;overflow:hidden;">
                    <tr>
                      <td colspan="2"
                          style="background:#0D0D0D;padding:10px 12px;color:#C9A84C;
                                 font-size:11px;font-weight:700;letter-spacing:1.5px;
                                 text-transform:uppercase;">
                        Account Information
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:7px 12px;background:#f7f5f0;color:#888880;
                                 font-size:13px;font-weight:600;width:40%;">Account No.</td>
                      <td style="padding:7px 12px;font-size:13px;">{acc.get('acnt_no','—')}</td>
                    </tr>
                    <tr>
                      <td style="padding:7px 12px;color:#888880;font-size:13px;font-weight:600;">Username</td>
                      <td style="padding:7px 12px;font-size:13px;">{acc.get('username','—')}</td>
                    </tr>
                    {rows_html}
                  </table>
                </td>
              </tr>

              <!-- Footer -->
              <tr>
                <td style="padding:20px 32px 28px;border-top:1px solid #e8e5de;margin-top:8px;">
                  <p style="margin:0;font-size:11px;color:#aaa89a;line-height:1.6;">
                    This is a system-generated email. Please do not reply to this message.<br>
                    For support, contact <a href="mailto:support@bankofchakshu.in"
                    style="color:#C9A84C;">support@bankofchakshu.in</a>
                  </p>
                  <p style="margin:8px 0 0;font-size:10px;color:#ccccbb;">
                    &copy; {datetime.now().year} Bank of Chakshu. All rights reserved.
                  </p>
                </td>
              </tr>

            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """


def send_email(to_email: str, subject: str, action_label: str,
               acc: dict, extra_rows: list[tuple], pdf_bytes: bytes,
               pdf_filename: str = "report.pdf") -> tuple[bool, str]:
    """
    Send a branded HTML email with PDF attachment via Gmail SMTP.
    Returns (success: bool, message: str)
    """
    sender, app_pwd = _get_config()
    if not sender or not app_pwd:
        return False, ("Email credentials not set. In Streamlit Cloud go to: "
               "App Settings → Secrets → add [email] sender and app_pwd")

    try:
        msg = MIMEMultipart("mixed")
        msg["From"]    = f"Bank of Chakshu <{sender}>"
        msg["To"]      = to_email
        msg["Subject"] = subject

        # HTML body
        html_part = MIMEText(_build_html_body(action_label, acc, extra_rows), "html")
        msg.attach(html_part)

        # PDF attachment
        if pdf_bytes:
            pdf_part = MIMEApplication(pdf_bytes, _subtype="pdf")
            pdf_part.add_header(
                "Content-Disposition", "attachment", filename=pdf_filename
            )
            msg.attach(pdf_part)

        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx) as server:
            server.login(sender, app_pwd)
            server.sendmail(sender, to_email, msg.as_string())

        return True, "Email sent successfully."

    except smtplib.SMTPAuthenticationError:
        return False, "Gmail authentication failed. Check your App Password in secrets.toml."
    except smtplib.SMTPException as e:
        return False, f"SMTP error: {e}"
    except Exception as e:
        return False, f"Failed to send email: {e}"


# ── Convenience wrappers ───────────────────────────────────────────────────────

def send_registration_email(acc, pdf_bytes):
    subject = f"Welcome to Bank of Chakshu — A/C #{acc['acnt_no']}"
    extra = [
        ("Email",          acc.get("email", "—")),
        ("Phone",          acc.get("phone", "—")),
        ("Opening Balance",f"Rs. {acc.get('balance', 0):,.2f}"),
        ("Date of Birth",  acc.get("dob", "—")),
        ("Address",        acc.get("address", "—")),
        ("Registered On",  str(acc.get("created_at", "—"))[:16]),
    ]
    return send_email(
        acc["email"], subject,
        "ACCOUNT REGISTRATION SUCCESSFUL",
        acc, extra, pdf_bytes,
        pdf_filename=f"BOC_Welcome_{acc['acnt_no']}.pdf"
    )


def send_deposit_email(acc, amount, new_balance, timestamp, pdf_bytes):
    subject = f"Deposit Confirmed — Rs.{amount:,.0f} — A/C #{acc['acnt_no']}"
    extra = [
        ("Transaction Type", "DEPOSIT"),
        ("Amount Deposited", f"Rs. {amount:,.2f}"),
        ("Balance After",    f"Rs. {new_balance:,.2f}"),
        ("Transaction Time", timestamp),
    ]
    return send_email(
        acc["email"], subject,
        "DEPOSIT SUCCESSFUL",
        acc, extra, pdf_bytes,
        pdf_filename=f"BOC_Deposit_{acc['acnt_no']}_{timestamp[:10]}.pdf"
    )


def send_withdrawal_email(acc, amount, new_balance, timestamp, pdf_bytes):
    subject = f"Withdrawal Confirmed — Rs.{amount:,.0f} — A/C #{acc['acnt_no']}"
    extra = [
        ("Transaction Type",  "WITHDRAWAL"),
        ("Amount Withdrawn",  f"Rs. {amount:,.2f}"),
        ("Balance After",     f"Rs. {new_balance:,.2f}"),
        ("Transaction Time",  timestamp),
    ]
    return send_email(
        acc["email"], subject,
        "WITHDRAWAL SUCCESSFUL",
        acc, extra, pdf_bytes,
        pdf_filename=f"BOC_Withdrawal_{acc['acnt_no']}_{timestamp[:10]}.pdf"
    )


def send_statement_email(acc, pdf_bytes):
    subject = f"Account Statement — Bank of Chakshu — A/C #{acc['acnt_no']}"
    extra = [
        ("Current Balance", f"Rs. {acc.get('balance', 0):,.2f}"),
        ("Requested On",    datetime.now().strftime("%d %B %Y, %I:%M %p")),
    ]
    return send_email(
        acc["email"], subject,
        "ACCOUNT STATEMENT",
        acc, extra, pdf_bytes,
        pdf_filename=f"BOC_Statement_{acc['acnt_no']}.pdf"
    )
