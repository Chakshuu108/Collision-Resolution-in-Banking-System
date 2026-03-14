import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# ── Brand colours ──────────────────────────────────────────────────────────────
GOLD        = colors.HexColor("#C9A84C")
GOLD_LIGHT  = colors.HexColor("#F5E6C0")
DARK        = colors.HexColor("#0D0D0D")
DARK_MID    = colors.HexColor("#2A2A2A")
WHITE       = colors.white
GREY_LIGHT  = colors.HexColor("#F7F5F0")
GREY_TEXT   = colors.HexColor("#555550")
SUCCESS     = colors.HexColor("#2E7D55")
DANGER      = colors.HexColor("#B03A3A")


def _styles():
    base = getSampleStyleSheet()
    custom = {}

    custom["bank_title"] = ParagraphStyle(
        "bank_title", fontSize=22, textColor=GOLD,
        fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=2
    )
    custom["bank_tagline"] = ParagraphStyle(
        "bank_tagline", fontSize=8, textColor=GREY_TEXT,
        fontName="Helvetica", alignment=TA_CENTER, spaceAfter=0,
        letterSpacing=2
    )
    custom["section_head"] = ParagraphStyle(
        "section_head", fontSize=10, textColor=DARK,
        fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=4
    )
    custom["body"] = ParagraphStyle(
        "body", fontSize=9, textColor=DARK,
        fontName="Helvetica", spaceAfter=3, leading=14
    )
    custom["small_grey"] = ParagraphStyle(
        "small_grey", fontSize=7.5, textColor=GREY_TEXT,
        fontName="Helvetica", spaceAfter=2
    )
    custom["amount_big"] = ParagraphStyle(
        "amount_big", fontSize=18, textColor=GOLD,
        fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=2
    )
    custom["footer"] = ParagraphStyle(
        "footer", fontSize=7, textColor=GREY_TEXT,
        fontName="Helvetica", alignment=TA_CENTER
    )
    return custom


def _header_block(story, s, action_label):
    """Bank of Chakshu letterhead."""
    story.append(Paragraph("Bank of Chakshu", s["bank_title"]))
    story.append(Paragraph("COLLISION-RESOLUTION BANKING SYSTEM", s["bank_tagline"]))
    story.append(Spacer(1, 4 * mm))
    story.append(HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=4))

    now = datetime.now().strftime("%d %B %Y, %I:%M %p")
    # Report type banner
    banner_data = [[
        Paragraph(f"<b>{action_label}</b>", ParagraphStyle("b", fontSize=11, textColor=WHITE,
                  fontName="Helvetica-Bold", alignment=TA_CENTER)),
        Paragraph(f"<b>Date &amp; Time:</b> {now}", ParagraphStyle("b2", fontSize=8.5,
                  textColor=WHITE, fontName="Helvetica", alignment=TA_RIGHT))
    ]]
    banner = Table(banner_data, colWidths=["55%", "45%"])
    banner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK),
        ("PADDING",    (0, 0), (-1, -1), 8),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(banner)
    story.append(Spacer(1, 5 * mm))


def _account_info_table(story, s, acc):
    story.append(Paragraph("Account Holder Details", s["section_head"]))
    data = [
        ["Full Name",    acc.get("full_name", "—"),   "Account No.",  str(acc.get("acnt_no", "—"))],
        ["Username",     acc.get("username", "—"),     "Email",        acc.get("email", "—")],
        ["Phone",        acc.get("phone", "—"),        "Date of Birth",acc.get("dob", "—")],
        ["Address",      acc.get("address", "—"),      "Member Since", str(acc.get("created_at", "—"))[:10]],
    ]
    tbl = Table(data, colWidths=[30*mm, 60*mm, 35*mm, 60*mm])
    tbl.setStyle(TableStyle([
        ("FONTNAME",    (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME",    (2, 0), (2, -1), "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, -1), 8.5),
        ("TEXTCOLOR",   (0, 0), (0, -1), GOLD),
        ("TEXTCOLOR",   (2, 0), (2, -1), GOLD),
        ("BACKGROUND",  (0, 0), (-1, -1), GREY_LIGHT),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [GREY_LIGHT, WHITE]),
        ("GRID",        (0, 0), (-1, -1), 0.4, colors.HexColor("#DDDDCC")),
        ("PADDING",     (0, 0), (-1, -1), 5),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 5 * mm))


def _footer(story, s):
    story.append(Spacer(1, 8 * mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD, spaceAfter=4))
    story.append(Paragraph(
        "This is a system-generated report from Bank of Chakshu. "
        "No signature is required. For queries, contact support@bankofchakshu.in",
        s["footer"]
    ))
    story.append(Paragraph(
        f"Generated on {datetime.now().strftime('%d-%m-%Y at %H:%M:%S')} | "
        "Bank of Chakshu — Collision-Resolution Banking System",
        s["footer"]
    ))


# ── Public API ─────────────────────────────────────────────────────────────────

def generate_transaction_pdf(acc, txn_type, amount, new_balance, timestamp):
    """
    Returns PDF bytes for a single transaction (deposit or withdrawal).
    acc: dict from database.get_account()
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=15*mm, bottomMargin=15*mm
    )
    s = _styles()
    story = []

    label = "DEPOSIT RECEIPT" if txn_type == "DEPOSIT" else "WITHDRAWAL RECEIPT"
    _header_block(story, s, label)
    _account_info_table(story, s, acc)

    # ── Transaction summary ──
    story.append(Paragraph("Transaction Summary", s["section_head"]))

    colour = SUCCESS if txn_type == "DEPOSIT" else DANGER
    symbol = "+" if txn_type == "DEPOSIT" else "-"

    summary_data = [
        ["Transaction Type", txn_type],
        ["Amount",           f"{symbol} Rs. {amount:,.2f}"],
        ["Balance After",    f"Rs. {new_balance:,.2f}"],
        ["Transaction Time", timestamp],
    ]
    stbl = Table(summary_data, colWidths=[60*mm, 120*mm])
    stbl.setStyle(TableStyle([
        ("FONTNAME",    (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, -1), 9),
        ("TEXTCOLOR",   (0, 0), (0, -1), GOLD),
        ("BACKGROUND",  (0, 0), (-1, -1), GREY_LIGHT),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [GREY_LIGHT, WHITE]),
        ("GRID",        (0, 0), (-1, -1), 0.4, colors.HexColor("#DDDDCC")),
        ("PADDING",     (0, 0), (-1, -1), 6),
        ("TEXTCOLOR",   (1, 1), (1, 1), colour),
        ("FONTNAME",    (1, 1), (1, 1), "Helvetica-Bold"),
    ]))
    story.append(stbl)

    # big amount display
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(f"{symbol} Rs. {amount:,.2f}", s["amount_big"]))
    story.append(Paragraph(
        f"New Balance: <b>Rs. {new_balance:,.2f}</b>",
        ParagraphStyle("nb", fontSize=10, textColor=DARK, fontName="Helvetica",
                       alignment=TA_CENTER, spaceAfter=4)
    ))

    _footer(story, s)
    doc.build(story)
    buf.seek(0)
    return buf.read()


def generate_statement_pdf(acc, transactions):
    """
    Returns PDF bytes for full account statement.
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=15*mm, bottomMargin=15*mm
    )
    s = _styles()
    story = []

    _header_block(story, s, "ACCOUNT STATEMENT")
    _account_info_table(story, s, acc)

    # current balance box
    bal_data = [[
        Paragraph("Current Balance", ParagraphStyle("cl", fontSize=9, textColor=WHITE,
                  fontName="Helvetica-Bold", alignment=TA_CENTER)),
        Paragraph(f"Rs. {acc['balance']:,.2f}", ParagraphStyle("cv", fontSize=15,
                  textColor=GOLD, fontName="Helvetica-Bold", alignment=TA_CENTER)),
    ]]
    bal_tbl = Table(bal_data, colWidths=["40%", "60%"])
    bal_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK),
        ("PADDING",    (0, 0), (-1, -1), 8),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(bal_tbl)
    story.append(Spacer(1, 5*mm))

    # transactions table
    story.append(Paragraph("Transaction History", s["section_head"]))
    if not transactions:
        story.append(Paragraph("No transactions found.", s["body"]))
    else:
        header = [["#", "Date & Time", "Type", "Amount (Rs.)", "Balance After (Rs.)"]]
        rows = []
        for i, t in enumerate(transactions, 1):
            symbol = "+" if t["txn_type"] == "DEPOSIT" else "-"
            rows.append([
                str(i),
                t["timestamp"],
                t["txn_type"],
                f"{symbol} {t['amount']:,.2f}",
                f"{t['balance_after']:,.2f}",
            ])
        tbl = Table(header + rows, colWidths=[10*mm, 45*mm, 28*mm, 45*mm, 45*mm])
        style_cmds = [
            ("BACKGROUND",  (0, 0), (-1, 0), DARK),
            ("TEXTCOLOR",   (0, 0), (-1, 0), GOLD),
            ("FONTNAME",    (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",    (0, 0), (-1, -1), 8),
            ("GRID",        (0, 0), (-1, -1), 0.3, colors.HexColor("#DDDDCC")),
            ("PADDING",     (0, 0), (-1, -1), 5),
            ("ALIGN",       (3, 1), (4, -1), "RIGHT"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, GREY_LIGHT]),
        ]
        # colour amount column
        for i, t in enumerate(transactions, 1):
            colour = SUCCESS if t["txn_type"] == "DEPOSIT" else DANGER
            style_cmds.append(("TEXTCOLOR", (3, i), (3, i), colour))
        tbl.setStyle(TableStyle(style_cmds))
        story.append(tbl)

    _footer(story, s)
    doc.build(story)
    buf.seek(0)
    return buf.read()


def generate_registration_pdf(acc):
    """Welcome letter sent after registration."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=15*mm, bottomMargin=15*mm
    )
    s = _styles()
    story = []

    _header_block(story, s, "WELCOME — ACCOUNT OPENED")
    story.append(Paragraph(
        f"Dear <b>{acc['full_name']}</b>,",
        s["body"]
    ))
    story.append(Paragraph(
        "Congratulations! Your account with <b>Bank of Chakshu</b> has been successfully created. "
        "Below are your account details. Please keep this document safe.",
        s["body"]
    ))
    story.append(Spacer(1, 4*mm))
    _account_info_table(story, s, acc)

    # account number highlight
    acno_data = [[
        Paragraph("Your Account Number", ParagraphStyle("al", fontSize=9, textColor=WHITE,
                  fontName="Helvetica-Bold", alignment=TA_CENTER)),
        Paragraph(str(acc["acnt_no"]), ParagraphStyle("av", fontSize=18,
                  textColor=GOLD, fontName="Helvetica-Bold", alignment=TA_CENTER)),
    ]]
    acno_tbl = Table(acno_data, colWidths=["45%", "55%"])
    acno_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK),
        ("PADDING",    (0, 0), (-1, -1), 10),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(acno_tbl)
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph(
        f"Opening Balance: <b>Rs. {acc['balance']:,.2f}</b>",
        ParagraphStyle("ob", fontSize=10, textColor=DARK, fontName="Helvetica", spaceAfter=4)
    ))
    story.append(Paragraph(
        "You can now log in using your username or account number and password.",
        s["body"]
    ))

    _footer(story, s)
    doc.build(story)
    buf.seek(0)
    return buf.read()
