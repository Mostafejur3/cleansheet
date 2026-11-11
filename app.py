import io
import html
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

from src.data_quality import (
    analyze_dataframe,
    clean_dataframe,
    dataframe_to_csv_bytes,
    format_bytes,
)

# ==========================================================
# CONFIG & SEO METADATA
# ==========================================================
# Note: Streamlit does not natively support full SEO. 
# We inject meta tags via st.html for better indexing.

st.set_page_config(
    page_title="CleanSheet — Smart CSV Data Cleaner",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================================
# DESIGN SYSTEM (Glossy, Professional, Fast)
# ==========================================================
st.html("""
<head>
    <!-- Google Analytics (GA4) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-WQK7KTCMK8"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-WQK7KTCMK8');
    </script>

    <!-- SEO Meta Tags -->
    <meta name="description" content="CleanSheet is a lightweight data-quality app to inspect and clean messy CSV files without writing code.">
    <meta name="keywords" content="CSV cleaner, data cleaning, data quality, smart data studio">
    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,600&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --blue: #2563EB;
            --blue-light: #EFF6FF;
            --ink: #0F172A;
            --muted: #475569;
            --line: #E2E8F0;
            --canvas: #F8FAFC;
            --green: #059669;
        }
        html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; color: var(--ink); }
        h1, h2, h3, h4, h5, h6, .logo-name { font-family: 'Inter', sans-serif !important; font-weight: 800 !important; }
        .stApp { background: var(--canvas); }
        
        section[data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
        header, footer, #MainMenu { visibility: hidden; }
        .block-container { max-width: 1200px; padding: 1.5rem 2rem 3rem !important; }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .fade-in { animation: fadeIn 0.6s ease-out forwards; }

        /* Header & Logo */
        .top-header { display: flex; align-items: center; justify-content: space-between; padding: 5px 0 15px; border-bottom: 2px solid var(--line); margin-bottom: 15px; }
        .logo-wrap { display: flex; align-items: center; gap: 12px; cursor: pointer; text-decoration: none; }
        .logo-icon { height: 42px; width: 42px; display: flex; align-items: center; justify-content: center; border-radius: 12px; font-size: 22px; color: white; background: linear-gradient(135deg, #3B82F6, #2563EB); box-shadow: 0 4px 12px rgba(37,99,235,0.2); }
        .logo-name { font-size: 24px; font-weight: 800; line-height: 1.1; color: var(--ink); }
        .logo-tagline { font-size: 11px; color: var(--muted); font-weight: 700; letter-spacing: 1px; }
        .header-right { display: flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 600; color: var(--muted); }
        .live-dot { height: 8px; width: 8px; border-radius: 50%; background: var(--green); }

        /* AD SPACE */
        .ad-space { background: #F1F5F9; border: 1px dashed #CBD5E1; border-radius: 8px; padding: 15px; text-align: center; margin-bottom: 20px; color: #94A3B8; font-size: 13px; font-weight: 600; }

        /* Professional Hero */
        .hero-section { padding: 10px 0 20px; animation: fadeIn 0.8s ease-out forwards; }
        .hero-eyebrow { color: var(--blue); font-size: 14px; font-weight: 800; letter-spacing: 1.5px; margin-bottom: 12px; text-transform: uppercase; display: flex; align-items: center; gap: 6px; }
        .hero-title { font-family: 'Playfair Display', serif !important; font-size: 52px; font-weight: 700; line-height: 1.1; margin-bottom: 18px; color: var(--ink); }
        .hero-title span { color: var(--blue); font-style: italic; }
        .hero-description { color: var(--muted); font-size: 17px; line-height: 1.6; font-weight: 500; margin-bottom: 15px; max-width: 95%; }

        /* Glossy Cards */
        div[data-testid="stVerticalBlockBorderWrapper"] { background: linear-gradient(145deg, #ffffff, #f8fafc); border: 1px solid #E2E8F0; border-top: 3px solid #CBD5E1; border-radius: 14px; box-shadow: 0 4px 20px rgba(0,0,0,0.03), inset 0 1px 0 rgba(255,255,255,1); transition: all 0.3s ease; }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover { box-shadow: 0 8px 30px rgba(37,99,235,0.08); border-top-color: var(--blue); }

        /* Uploader */
        div[data-testid="stFileUploader"] { background: white; border: 2px dashed #CBD5E1; border-radius: 12px; padding: 15px; transition: border-color 0.2s ease; }
        div[data-testid="stFileUploader"]:hover { border-color: var(--blue); }

        /* Workflow */
        .workflow-heading { margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; }
        .workflow-title { font-size: 22px; font-weight: 800; }
        .workflow-subtitle { font-size: 14px; color: var(--muted); font-weight: 500; }
        .workflow-counter { background: white; border: 1px solid var(--line); padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 800; color: var(--blue); }

        /* Step Buttons */
        div[data-testid="stHorizontalBlock"] button { min-height: 60px; border-radius: 10px; font-size: 20px; font-weight: 800; border: 2px solid var(--line); background: white; color: #94A3B8; transition: all 0.2s ease; }
        div[data-testid="stHorizontalBlock"] button:hover { border-color: var(--blue); color: var(--blue); }
        div[data-testid="stHorizontalBlock"] button[kind="primary"] { background: var(--blue); color: white; border: 2px solid var(--blue); box-shadow: 0 4px 12px rgba(37,99,235,0.3); }
        .step-label { text-align: center; font-size: 15px; font-weight: 800; color: #1E293B; margin-top: 6px; }
        .step-number { font-size: 12px; font-weight: 700; color: #94A3B8; text-align: center; }

        /* Section Headers */
        .section-title { font-size: 20px; font-weight: 800; margin-bottom: 4px; }
        .section-desc { font-size: 14px; font-weight: 500; color: var(--muted); margin-bottom: 12px; }
        .section-tag { display: inline-block; padding: 4px 10px; border-radius: 8px; background: var(--blue-light); color: var(--blue); font-size: 12px; font-weight: 800; margin-bottom: 8px; }

        /* Metrics */
        div[data-testid="stMetric"] { background: #F8FAFC; border: 1px solid var(--line); padding: 12px; border-radius: 10px; }
        div[data-testid="stMetricLabel"] p { font-size: 13px !important; font-weight: 700; color: var(--muted) !important; }
        div[data-testid="stMetricValue"] { font-size: 26px !important; font-weight: 800 !important; }

        /* Buttons */
        .stButton button { border-radius: 8px; font-size: 15px; font-weight: 700; min-height: 40px; transition: transform 0.2s ease, box-shadow 0.2s ease !important; }
        .stButton button:hover { transform: scale(1.02) translateY(-1px) !important; box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important; }
        .stButton button[kind="primary"] { background: linear-gradient(135deg, #3B82F6, #2563EB) !important; color: #FFFFFF !important; border: none !important; }
        .stButton button[kind="primary"]:hover, .stButton button[kind="primary"]:active, .stButton button[kind="primary"]:focus { color: #FFFFFF !important; background: linear-gradient(135deg, #2563EB, #1D4ED8) !important; }
        .stDownloadButton button { width: 100%; min-height: 40px; border-radius: 8px; background: var(--green); color: white; font-weight: 800; }
        .stDownloadButton button:hover { transform: scale(1.01); }

        /* Inputs & Tabs */
        .stSelectbox div[data-baseweb="select"], .stTextInput input { border-radius: 8px; }
        .stCheckbox label p { font-size: 15px; font-weight: 600; }
        .stTabs [data-baseweb="tab"] { font-weight: 700; font-size: 15px; }

        /* Dataframe */
        div[data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 8px; }

        /* Footer */
        .app-footer { text-align: center; padding: 20px 0 10px; color: #94A3B8; font-size: 13px; font-weight: 600; }
    </style>
    
    <!-- Logo Click Reload Script -->
    <script>
    document.addEventListener("DOMContentLoaded", function() {
        const logo = document.querySelector('.logo-wrap');
        if(logo) { logo.addEventListener('click', function() { window.location.reload(); }); }
    });
    </script>
</head>
""")

# ==========================================================
# SESSION STATE
# ==========================================================
defaults = {"active_step": 0, "cleaned_df": None, "clean_report": None, "dataset_signature": None}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==========================================================
# HELPERS
# ==========================================================
STEPS = [("UPLOAD", "Upload Data"), ("EXPLORE", "Explore Data"), ("CLEAN", "Smart Cleaning"), ("VALIDATE", "Validation"), ("EXPORT", "Export")]

def section_header(title, description, tag=None):
    tag_html = f'<div><span class="section-tag">{html.escape(tag)}</span></div>' if tag else ""
    st.html(f"""
    <div style="margin-bottom:10px;">
        {tag_html}
        <div class="section-title">{html.escape(title)}</div>
        <div class="section-desc">{html.escape(description)}</div>
    </div>
    """)

def parse_csv(file):
    raw = file.getvalue()
    for encoding in ["utf-8-sig", "utf-8", "latin-1"]:
        try:
            return pd.read_csv(io.BytesIO(raw), encoding=encoding, sep=None, engine="python")
        except (UnicodeDecodeError, pd.errors.ParserError, pd.errors.EmptyDataError):
            continue
    raise ValueError("Unable to read this CSV file. Please check the format.")

def quality_color(score):
    if score >= 90: return "#059669"
    if score >= 70: return "#D97706"
    return "#DC2626"

# ==========================================================
# HEADER
# ==========================================================
st.html("""
<div class="top-header">
    <div class="logo-wrap" title="Reload Page">
        <div class="logo-icon">✦</div>
        <div>
            <div class="logo-name">CleanSheet</div>
            <div class="logo-tagline">INTELLIGENT DATA STUDIO</div>
        </div>
    </div>
    <div class="header-right">
        <span class="live-dot"></span>
        <span>Secure Workspace</span>
    </div>
</div>
""")

# ==========================================================
# AD SPACE
# ==========================================================
st.html('<div class="ad-space"></div>')

# ==========================================================
# HERO + UPLOAD
# ==========================================================
hero_left, hero_right = st.columns([1.2, 1], gap="large")

with hero_left:
    st.html("""
    <div class="hero-section">
        <div class="hero-eyebrow">✦ Next Generation Data Studio</div>
        <div class="hero-title">
            Make your data<br>
            <span>beautifully clean.</span>
        </div>
        <div class="hero-description">
            Transform messy datasets into reliable, analysis-ready data in seconds. 
            Discover hidden issues, clean your records, and download your perfect dataset.
        </div>
    </div>
    """)

with hero_right:
    with st.container(border=True):
        st.html("""
        <div style="text-align:center; padding:5px 0 10px;">
            <div style="width:50px;height:50px;margin:auto;border-radius:12px; background:#EFF6FF;display:flex;align-items:center;justify-content:center;font-size:24px; color:#2563EB;">☁️</div>
            <div style="font-size:16px; font-weight:800; margin-top:8px;">Upload your dataset</div>
            <div style="font-size:13px; font-weight:500; color:#64748B;">Drag and drop your CSV file</div>
        </div>
        """)
        uploaded = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")

# ==========================================================
# LOAD DATA
# ==========================================================
df, filename = None, None
if uploaded is not None:
    try:
        df = parse_csv(uploaded)
        filename = uploaded.name
    except Exception as exc:
        st.error(f"File reading error: {exc}")
        st.stop()

if df is not None:
    if df.empty or len(df.columns) == 0:
        st.error("The uploaded dataset is empty or invalid.")
        st.stop()
    signature = (filename, len(df), len(df.columns), hash(df.to_csv(index=False).encode("utf-8")))
    if signature != st.session_state.dataset_signature:
        st.session_state.dataset_signature = signature
        st.session_state.cleaned_df = None
        st.session_state.clean_report = None
        st.session_state.active_step = 1
    report = analyze_dataframe(df)
else:
    report = None

# ==========================================================
# FILE STATUS
# ==========================================================
if df is not None:
    st.html(f"""
    <div style="background:white; border:1px solid #E2E8F0; border-radius:10px; padding:10px 14px; display:flex; align-items:center; gap:12px; margin-top: 15px; margin-bottom: 15px;">
        <div style="background:#EFF6FF; width:32px;height:32px;border-radius:8px; display:flex;align-items:center;justify-content:center;font-size:16px;">📄</div>
        <div style="flex:1;">
            <div style="font-size:14px; font-weight:800; color:#0F172A;">{html.escape(filename)}</div>
            <div style="font-size:12px; font-weight:500; color:#64748B;">{len(df):,} rows · {len(df.columns):,} cols · {format_bytes(len(uploaded.getvalue()))}</div>
        </div>
        <div style="color:#059669; background:#ECFDF5; padding:4px 10px; border-radius:12px; font-size:12px; font-weight:800;">✓ READY</div>
    </div>
    """)

# ==========================================================
# WORKFLOW MAP
# ==========================================================
completed_steps = set()
if df is not None: completed_steps.update([0, 1])
if st.session_state.cleaned_df is not None: completed_steps.update([2, 3, 4])
current_step = st.session_state.active_step

st.html(f"""
<div class="workflow-heading">
    <div>
        <div class="workflow-title">Your Workspace</div>
        <div class="workflow-subtitle">Follow the process from raw data to clean results.</div>
    </div>
    <div class="workflow-counter">{len(completed_steps)} / 5 STEPS READY</div>
</div>
""")

cols = st.columns(5, gap="small")
for i, (short_name, label) in enumerate(STEPS):
    with cols[i]:
        kind = "primary" if i == current_step else "secondary"
        number = f"{i+1:02d}" if i not in completed_steps or i == current_step else "✓"
        disabled = (i > 0 and df is None) or (i >= 3 and st.session_state.cleaned_df is None)
        if st.button(number, key=f"workflow_{i}", type=kind, disabled=disabled, use_container_width=True):
            st.session_state.active_step = i
            st.rerun()
        label_color = "#2563EB" if i == current_step else "#334155"
        st.html(f"""<div class="step-label" style="color:{label_color};">{label}</div><div class="step-number">STEP {i+1:02d}</div>""")

st.html("<div style='margin-bottom: 15px;'></div>")

# ==========================================================
# WORKSPACE CONTENT
# ==========================================================
step = st.session_state.active_step
cleaned = st.session_state.cleaned_df
clean_report = st.session_state.clean_report

if step == 0:
    with st.container(border=True):
        section_header("Start your data journey", "Upload your CSV above to begin the data processing workflow.", "STEP 01")
        if df is None:
            a, b, c = st.columns(3)
            a.metric("SUPPORTED FORMAT", "CSV")
            b.metric("WORKFLOW", "5 Steps")
            c.metric("PROCESSING", "In-session")
            st.info("Once your dataset is uploaded, CleanSheet will automatically inspect its structure.")
        else:
            a, b, c, d = st.columns(4)
            a.metric("TOTAL ROWS", f"{len(df):,}")
            b.metric("COLUMNS", f"{len(df.columns):,}")
            c.metric("MISSING CELLS", f"{report['missing_cells']:,}")
            d.metric("DUPLICATES", f"{report['duplicate_rows']:,}")
            st.success("Your dataset has been successfully uploaded.")
            if st.button("Continue to data exploration →", type="primary"):
                st.session_state.active_step = 1
                st.rerun()

elif step == 1:
    if df is None: st.warning("Please upload a CSV dataset first.")
    else:
        with st.container(border=True):
            section_header("Explore your dataset", "Inspect records, discover missing values and understand columns.", "STEP 02")
            a, b, c, d = st.columns(4)
            a.metric("TOTAL RECORDS", f"{len(df):,}")
            b.metric("TOTAL COLUMNS", f"{len(df.columns):,}")
            c.metric("MISSING CELLS", f"{report['missing_cells']:,}")
            d.metric("DUPLICATE ROWS", f"{report['duplicate_rows']:,}")
            tab1, tab2, tab3 = st.tabs(["Data Preview", "Column Profile", "Missing Values"])
            with tab1:
                search = st.text_input("Search records", placeholder="Search values...", label_visibility="collapsed")
                visible = df.copy()
                if search.strip():
                    query = search.strip().lower()
                    mask = visible.astype(str).apply(lambda col: col.str.lower().str.contains(query, regex=False, na=False)).any(axis=1)
                    visible = visible[mask]
                st.dataframe(visible, use_container_width=True, height=350, hide_index=True)
            with tab2:
                profile = pd.DataFrame({"Column": df.columns, "Data type": df.dtypes.astype(str).values, "Non-null": df.notna().sum().values, "Missing": df.isna().sum().values, "Unique": df.nunique().values})
                st.dataframe(profile, use_container_width=True, hide_index=True)
            with tab3:
                missing = report["missing_by_column"]
                missing = missing[missing > 0].sort_values(ascending=False)
                if not missing.empty:
                    chart = missing.rename("Missing").rename_axis("Column").reset_index()
                    fig = px.bar(chart, x="Column", y="Missing", color_discrete_sequence=["#2563EB"], template="plotly_white")
                    fig.update_layout(height=300, margin=dict(l=5, r=5, t=10, b=5), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig, use_container_width=True)
                else: st.success("No missing values found.")
            if st.button("Continue to smart cleaning →", type="primary"):
                st.session_state.active_step = 2
                st.rerun()

elif step == 2:
    if df is None: st.warning("Upload your dataset first.")
    else:
        with st.container(border=True):
            section_header("Smart cleaning studio", "Configure how CleanSheet should process your data.", "STEP 03")
            left, right = st.columns([1.2, .8], gap="large")
            with left:
                st.markdown("**Missing value treatment**")
                numeric_strategy = st.selectbox("Numeric columns", ["Median", "Mean", "Zero", "Drop rows"])
                text_strategy = st.selectbox("Text columns", ["Most frequent value", "Fill with 'Unknown'", "Drop rows"])
                st.markdown("---")
                st.markdown("**Additional cleaning operations**")
                trim_text = st.checkbox("Trim extra spaces", value=True)
                remove_duplicates = st.checkbox("Remove duplicate rows", value=True)
                
                # EXECUTE BUTTON - Auto Redirects to Step 3 (Validation)
                if st.button("✦ Execute cleaning", type="primary", use_container_width=True, key="execute_clean_btn"):
                    try:
                        with st.spinner("Processing..."):
                            new_df, new_report = clean_dataframe(df, numeric_strategy=numeric_strategy, text_strategy=text_strategy, trim_text=trim_text, remove_duplicates=remove_duplicates)
                            st.session_state.cleaned_df = new_df
                            st.session_state.clean_report = new_report
                            st.session_state.active_step = 3 # <--- AUTO REDIRECT
                        st.rerun()
                    except Exception as exc: st.error(f"Cleaning error: {exc}")
            with right:
                section_header("Detected issues", "Issues identified during initial inspection.")
                st.metric("Missing cells", f"{report['missing_cells']:,}")
                st.metric("Duplicate records", f"{report['duplicate_rows']:,}")
                st.metric("Current quality score", f"{report['quality_score']}/100")

# STEP 4 — VALIDATION (With Success Banner at top)
elif step == 3:
    if df is None or cleaned is None: st.warning("Complete the cleaning step before validation.")
    else:
        # Success Banner at Top
        st.html("""
        <div style="background:#ECFDF5; border:1px solid #10B981; border-radius:12px; padding:15px; margin-bottom:20px; display:flex; align-items:center; gap:10px;">
            <div style="font-size:24px;">✅</div>
            <div>
                <div style="font-size:16px; font-weight:800; color:#065F46;">Cleaning completed successfully!</div>
                <div style="font-size:14px; font-weight:500; color:#047857;">Your cleaned dataset is ready for validation.</div>
            </div>
        </div>
        """)

        final_report = analyze_dataframe(cleaned)
        with st.container(border=True):
            section_header("Quality validation", "Compare the original dataset with your cleaned version.", "STEP 04")
            before, after = st.columns(2)
            with before:
                st.markdown("**Original dataset**")
                score = report["quality_score"]
                st.html(f"""<div style="font-size:42px;font-weight:800;font-family:Manrope;color:{quality_color(score)};">{score}<span style="font-size:14px;color:#94A3B8;"> / 100</span></div>""")
                st.progress(score / 100)
            with after:
                st.markdown("**Cleaned dataset**")
                score = final_report["quality_score"]
                st.html(f"""<div style="font-size:42px;font-weight:800;font-family:Manrope;color:{quality_color(score)};">{score}<span style="font-size:14px;color:#94A3B8;"> / 100</span></div>""")
                st.progress(score / 100)
            st.markdown("---")
            comparison = pd.DataFrame({"Metric": ["Total rows", "Missing cells", "Duplicate rows", "Quality score"], "Original": [len(df), report["missing_cells"], report["duplicate_rows"], report["quality_score"]], "Cleaned": [len(cleaned), final_report["missing_cells"], final_report["duplicate_rows"], final_report["quality_score"]]})
            st.dataframe(comparison, use_container_width=True, hide_index=True)
            if st.button("Approve & continue to export →", type="primary"):
                st.session_state.active_step = 4
                st.rerun()

# STEP 5 — EXPORT (Full Data Preview)
elif step == 4:
    if df is None or cleaned is None: st.warning("Please complete the cleaning process first.")
    else:
        final_report = analyze_dataframe(cleaned)
        with st.container(border=True):
            section_header("Your data is ready", "Review your final output and download your cleaned dataset.", "STEP 05 · FINAL")
            a, b, c = st.columns(3)
            a.metric("FINAL RECORDS", f"{len(cleaned):,}")
            b.metric("TOTAL COLUMNS", f"{len(cleaned.columns):,}")
            c.metric("QUALITY SCORE", f"{final_report['quality_score']}/100")
            st.markdown("---")
            
            # FULL DATASET PREVIEW HERE
            st.markdown("**Full Cleaned Dataset Preview**")
            st.dataframe(cleaned, use_container_width=True, height=400, hide_index=True)
            
            csv_data = dataframe_to_csv_bytes(cleaned)
            st.html(f"""
            <div style="display:flex; align-items:center; gap:12px; padding:12px; background:#F0FDF4; border:1px solid #D1FAE5; border-radius:10px; margin-top:15px; margin-bottom:15px;">
                <div style="font-size:20px;">📄</div>
                <div style="flex:1;">
                    <div style="font-size:14px; font-weight:800; color:#065F46;">{html.escape(Path(filename).stem)}_cleaned.csv</div>
                    <div style="font-size:12px; font-weight:500; color:#047857;">CSV · {format_bytes(len(csv_data))}</div>
                </div>
                <span style="font-size:12px; font-weight:800; color:#059669;">READY</span>
            </div>
            """)
            st.download_button("↓ Download your cleaned dataset", data=csv_data, file_name=f"{Path(filename).stem}_cleaned.csv", mime="text/csv", use_container_width=True)

# ==========================================================
# DEMO DATASETS
# ==========================================================
st.html("<div style='margin-top: 40px;'></div>")
st.html("<div style='text-align:center; font-size:16px; font-weight:700; color:#334155; margin-bottom:10px;'>Don't have a file? Try our messy demo dataset to test the cleaning power:</div>")

demo_data = {
    "customer_id": [str(1000 + (i % 60)) for i in range(85)],
    "name": [f"  User {i%50}  " if i%3==0 else f"User {i%50}" for i in range(85)],
    "email": [f"user{i%50}@test.com" if i%4!=0 else "" for i in range(85)],
    "age": [str(i%40 + 18) if i%5!=0 else "" for i in range(85)],
    "city": [f"City {i%10}" if i%7!=0 else "   " for i in range(85)],
    "signup_date": [f"2023-{(i%12)+1:02d}-{(i%28)+1:02d}" if i%6!=0 else "" for i in range(85)],
    "total_spent": [f"{round((i*13.5)%500 + 20, 2)}" if i%5!=0 else "" for i in range(85)],
    "status": [["active", "inactive", "ACTIVE", " Inactive "][i%4] for i in range(85)]
}
demo_df = pd.DataFrame(demo_data)
demo_csv_str = demo_df.to_csv(index=False)

st.download_button(
    label="⬇️ Download Messy Demo Data (85 rows)",
    data=demo_csv_str,
    file_name="messy_demo_data.csv",
    mime="text/csv",
    use_container_width=False 
)
# ==========================================================
# AD SPACE
# ==========================================================
st.html('<div class="ad-space"></div>')
# ==========================================================
# FOOTER
# ==========================================================
st.html("""
<div class="app-footer">
    ✦ CLEANSHEET DATA STUDIO · CLEAN DATA. CLEAR DECISIONS.
</div>
""")
