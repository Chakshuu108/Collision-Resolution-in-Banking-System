STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --gold:       #C9A84C;
    --gold-dim:   rgba(201,168,76,0.12);
    --dark:       #0C0C0C;
    --dark-2:     #141414;
    --dark-3:     #1C1C1C;
    --text:       #EAEAE2;
    --muted:      #7a7a70;
    --success:    #4aad72;
    --danger:     #cf4f4f;
    --border:     rgba(201,168,76,0.15);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--dark) !important;
    color: var(--text) !important;
}
.stApp { background: var(--dark) !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; max-width: 960px !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: var(--gold); border-radius: 2px; }

/* sidebar */
[data-testid="stSidebar"] {
    background: var(--dark-2) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* inputs */
input, textarea {
    background-color: var(--dark-3) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 7px !important;
}
input:focus { border-color: var(--gold) !important; box-shadow: 0 0 0 2px rgba(201,168,76,0.12) !important; }
[data-testid="stNumberInput"] input { background-color: var(--dark-3) !important; color: var(--text) !important; }
[data-baseweb="select"] > div { background-color: var(--dark-3) !important; border: 1px solid var(--border) !important; }

/* buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--gold) 0%, #a87c28 100%) !important;
    color: #0C0C0C !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.83rem !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 7px !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.18s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 18px rgba(201,168,76,0.25) !important;
}

/* metrics */
[data-testid="stMetric"] {
    background: var(--dark-3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 0.73rem !important; text-transform: uppercase !important; letter-spacing: 0.09em !important; }
[data-testid="stMetricValue"] { color: var(--gold) !important; font-family: 'Playfair Display', serif !important; font-size: 1.5rem !important; }

/* dataframe */
[data-testid="stDataFrame"] { border: 1px solid var(--border) !important; border-radius: 10px !important; overflow: hidden !important; }

hr { border-color: var(--border) !important; margin: 1.2rem 0 !important; }

/* tabs */
.stTabs [data-baseweb="tab-list"] { background: var(--dark-2) !important; border-radius: 8px !important; padding: 4px !important; border: 1px solid var(--border) !important; }
.stTabs [data-baseweb="tab"] { color: var(--muted) !important; font-size: 0.83rem !important; border-radius: 6px !important; }
.stTabs [aria-selected="true"] { background: var(--gold-dim) !important; color: var(--gold) !important; }

/* cards */
.boc-card { background: var(--dark-3); border: 1px solid var(--border); border-radius: 12px; padding: 1.4rem 1.6rem; margin-bottom: 1rem; }
.boc-card-title { font-family: 'Playfair Display', serif; font-size: 1.05rem; color: var(--gold); margin-bottom: 0.7rem; }

/* page header */
.boc-header { text-align: center; padding: 1.5rem 0 1rem; }
.boc-header h1 { font-family: 'Playfair Display', serif !important; font-size: 2.5rem !important; font-weight: 900 !important; color: var(--gold) !important; letter-spacing: 0.04em !important; margin: 0 !important; }
.boc-header p { color: var(--muted); font-size: 0.78rem; letter-spacing: 0.16em; text-transform: uppercase; margin-top: 0.3rem; }

/* login / register box */
.auth-wrap { max-width: 480px; margin: 1rem auto; background: var(--dark-3); border: 1px solid var(--border); border-radius: 16px; padding: 2.2rem 2rem; }

/* badges */
.badge-d { display:inline-block; background:rgba(74,173,114,0.15); color:var(--success); border:1px solid rgba(74,173,114,0.3); border-radius:5px; padding:2px 10px; font-size:0.74rem; font-weight:600; }
.badge-w { display:inline-block; background:rgba(207,79,79,0.15); color:var(--danger); border:1px solid rgba(207,79,79,0.3); border-radius:5px; padding:2px 10px; font-size:0.74rem; font-weight:600; }

.stSuccess { background:rgba(74,173,114,0.10) !important; border:1px solid rgba(74,173,114,0.25) !important; border-radius:8px !important; }
.stError   { background:rgba(207,79,79,0.10) !important; border:1px solid rgba(207,79,79,0.25) !important; border-radius:8px !important; }
.stWarning { background:rgba(201,168,76,0.10) !important; border:1px solid rgba(201,168,76,0.25) !important; border-radius:8px !important; }
.stInfo    { background:rgba(201,168,76,0.07) !important; border:1px solid rgba(201,168,76,0.18) !important; border-radius:8px !important; }
</style>
"""
