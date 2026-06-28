import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import tempfile
import os

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from core.extraction.pdf_extractor import extract_text_from_pdf
from core.scoring.ats_scorer import calculate_ats_score
from core.analysis.recommendation import get_recommendation
from core.analysis.section_checker import check_sections
from reports.csv_export import create_dataframe
from reports.pdf_report import generate_pdf_report

st.set_page_config(
    page_title="Resume ATS Analyzer",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --bg:       #0c0c0f;
    --surface:  #131318;
    --surface2: #1a1a22;
    --border:   rgba(255,255,255,0.06);
    --border2:  rgba(255,255,255,0.1);
    --accent:   #7c6af7;
    --accent2:  #a89cf8;
    --text:     #e8e8f0;
    --sub:      #6b6b80;
    --dim:      #3a3a4a;
    --green:    #34d399;
    --amber:    #fbbf24;
    --red:      #f87171;
    --r:        10px;
}

.stApp {
    background: var(--bg);
    font-family: 'Inter', sans-serif;
    color: var(--text);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1100px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div { padding-top: 2rem !important; }
[data-testid="stSidebar"] .stRadio > label {
    display: none !important;
}
[data-testid="stSidebar"] .stRadio label {
    background: transparent !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 14px !important;
    color: var(--sub) !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    transition: all 0.15s !important;
    display: flex !important;
    align-items: center !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(124,106,247,0.08) !important;
    color: var(--text) !important;
}
[data-testid="stSidebar"] .stRadio label[data-checked="true"] {
    background: rgba(124,106,247,0.12) !important;
    color: var(--accent2) !important;
}

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    padding: 20px !important;
}
[data-testid="metric-container"] label {
    color: var(--sub) !important;
    font-size: 0.7rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: var(--text) !important;
    font-size: 1.6rem !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em;
}

/* ── Alerts ── */
.stAlert {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    color: var(--text) !important;
    font-size: 0.875rem !important;
}
div[data-baseweb="notification"] {
    border-radius: var(--r) !important;
}

/* ── Primary button ── */
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    border-radius: var(--r) !important;
    height: 44px !important;
    border: none !important;
    letter-spacing: 0.01em;
    transition: all 0.15s !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.4) !important;
}
.stButton > button:hover {
    background: var(--accent2) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(124,106,247,0.3) !important;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: var(--surface2) !important;
    color: var(--sub) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    height: 36px !important;
    font-size: 0.8rem !important;
}
[data-testid="stDownloadButton"] > button:hover {
    color: var(--text) !important;
    border-color: var(--accent) !important;
}

/* ── Text area ── */
.stTextArea > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
}
.stTextArea textarea {
    color: var(--text) !important;
    background: transparent !important;
    font-size: 0.875rem !important;
    font-family: 'Inter', sans-serif !important;
    line-height: 1.6 !important;
}
.stTextArea textarea::placeholder { color: var(--dim) !important; }
.stTextArea > div > div:focus-within {
    border-color: var(--accent) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploaderDropzone"] {
    background: var(--surface) !important;
    border: 1px dashed var(--border2) !important;
    border-radius: var(--r) !important;
    transition: border-color 0.15s !important;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: var(--accent) !important;
}

/* ── Expanders ── */
[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    margin-bottom: 8px !important;
}
[data-testid="stExpander"] summary {
    padding: 14px 18px !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    color: var(--text) !important;
}
[data-testid="stExpander"] summary:hover {
    background: rgba(255,255,255,0.02) !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: var(--r) !important;
    border: 1px solid var(--border) !important;
    overflow: hidden !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 24px 0 !important; }
h1, h2, h3, h4 { color: var(--text) !important; }

/* ───────────────────────────────────────
   CUSTOM LAYOUT COMPONENTS
─────────────────────────────────────── */

/* Sidebar wordmark */
.wordmark {
    padding: 0 16px 28px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 20px;
}
.wordmark-dot {
    display: inline-block;
    width: 8px; height: 8px;
    background: var(--accent);
    border-radius: 50%;
    margin-right: 8px;
    vertical-align: middle;
}
.wordmark-title {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text);
    letter-spacing: -0.01em;
}
.wordmark-sub {
    font-size: 0.7rem;
    color: var(--sub);
    margin-top: 2px;
    padding-left: 16px;
}

/* Page header */
.page-header { margin-bottom: 28px; }
.page-header h1 {
    font-size: 1.6rem;
    font-weight: 600;
    color: var(--text) !important;
    letter-spacing: -0.025em;
    margin-bottom: 4px;
}
.page-header p {
    font-size: 0.875rem;
    color: var(--sub);
    line-height: 1.5;
}

/* Stats row */
.stats-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    border-radius: var(--r);
    overflow: hidden;
    margin-bottom: 24px;
}
.stat-cell {
    background: var(--surface);
    padding: 16px 20px;
}
.stat-cell-label {
    font-size: 0.68rem;
    font-weight: 500;
    color: var(--sub);
    letter-spacing: 0.07em;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.stat-cell-value {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text);
    letter-spacing: -0.01em;
}
.stat-cell-value.accent { color: var(--accent2); }

/* Feature pills */
.feature-row {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 28px;
}
.feature-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 0.78rem;
    font-weight: 500;
    color: var(--sub);
}
.feature-pill .dot {
    width: 5px; height: 5px;
    border-radius: 50%;
    background: var(--accent);
    flex-shrink: 0;
}

/* Input section labels */
.input-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--sub);
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 8px;
}

/* Section title */
.section-title {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--sub);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin: 28px 0 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
}

/* Candidate card */
.c-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r);
    padding: 18px 20px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 18px;
    transition: border-color 0.15s;
}
.c-card:hover { border-color: var(--border2); }

.rank-num {
    width: 28px;
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--dim);
    text-align: center;
    flex-shrink: 0;
}
.rank-num.top { color: var(--accent2); }

.c-info { flex: 1; min-width: 0; }
.c-name {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 3px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.c-file { font-size: 0.72rem; color: var(--sub); }

/* Score badge */
.score-badge {
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    min-width: 52px;
    text-align: right;
    flex-shrink: 0;
}
.score-badge.high   { color: var(--green); }
.score-badge.medium { color: var(--amber); }
.score-badge.low    { color: var(--red); }

/* Status label */
.status-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    padding: 3px 10px;
    border-radius: 4px;
    flex-shrink: 0;
}
.sl-high   { background: rgba(52,211,153,0.1); color: var(--green); }
.sl-medium { background: rgba(251,191,36,0.1);  color: var(--amber); }
.sl-low    { background: rgba(248,113,113,0.1); color: var(--red); }

/* Mini bars */
.bars-col { min-width: 180px; flex: 1.2; }
.bar-row { margin-bottom: 5px; }
.bar-meta {
    display: flex;
    justify-content: space-between;
    font-size: 0.65rem;
    color: var(--sub);
    margin-bottom: 3px;
}
.bar-meta span:last-child { font-weight: 600; color: var(--sub); }
.bar-track {
    height: 3px;
    background: var(--surface2);
    border-radius: 2px;
    overflow: hidden;
}
.bar-fill {
    height: 100%;
    border-radius: 2px;
    background: var(--accent);
    opacity: 0.75;
}
.bar-fill.green  { background: var(--green); }
.bar-fill.amber  { background: var(--amber); }
.bar-fill.purple { background: var(--accent); }

/* Skill chips */
.chip {
    display: inline-block;
    border-radius: 5px;
    padding: 3px 9px;
    font-size: 0.72rem;
    font-weight: 500;
    margin: 2px 2px 2px 0;
}
.chip-ok  { background: rgba(52,211,153,0.08); color: var(--green); border: 1px solid rgba(52,211,153,0.15); }
.chip-no  { background: rgba(248,113,113,0.08); color: var(--red);   border: 1px solid rgba(248,113,113,0.15); }

/* Section items */
.sec-item {
    font-size: 0.8rem;
    color: var(--sub);
    padding: 3px 0;
}
.sec-item.ok  { color: var(--green); }
.sec-item.bad { color: var(--red); }

/* Footer */
.footer {
    text-align: center;
    font-size: 0.7rem;
    color: var(--dim);
    padding-top: 32px;
    border-top: 1px solid var(--border);
    margin-top: 48px;
    letter-spacing: 0.04em;
}

/* About card */
.about-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r);
    padding: 28px 32px;
    max-width: 680px;
}
.about-card h2 {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text) !important;
    margin-bottom: 6px;
    letter-spacing: -0.01em;
}
.about-card .tagline {
    font-size: 0.82rem;
    color: var(--sub);
    margin-bottom: 22px;
    line-height: 1.5;
}
.about-section-title {
    font-size: 0.65rem;
    font-weight: 600;
    color: var(--accent2);
    text-transform: uppercase;
    letter-spacing: 0.09em;
    margin-bottom: 10px;
}
.about-list {
    list-style: none;
    padding: 0;
    margin-bottom: 20px;
}
.about-list li {
    font-size: 0.82rem;
    color: var(--sub);
    padding: 4px 0;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 8px;
}
.about-list li::before {
    content: '';
    display: inline-block;
    width: 4px; height: 4px;
    border-radius: 50%;
    background: var(--accent);
    flex-shrink: 0;
}
.tech-badge {
    display: inline-block;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 5px;
    padding: 4px 10px;
    font-size: 0.74rem;
    font-weight: 500;
    color: var(--sub);
    margin: 3px 3px 3px 0;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div class="wordmark">
  <div>
    <span class="wordmark-dot"></span>
    <span class="wordmark-title">ATS Analyzer</span>
  </div>
  <div class="wordmark-sub">Resume Intelligence</div>
</div>
""", unsafe_allow_html=True)

    page = st.radio(
        "nav",
        ["Home", "Analytics", "About"],
        label_visibility="collapsed"
    )

    st.markdown("""
<div style="position:absolute;bottom:28px;left:0;right:0;padding:0 16px;">
  <div style="font-size:0.68rem;color:#3a3a4a;line-height:1.8;">
    Built with Python · Streamlit<br>Scikit-Learn · NLP
  </div>
</div>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════
# HOME
# ═════════════════════════════════════════
if page == "Home":

    st.markdown("""
<div class="page-header">
  <h1>Resume Screener</h1>
  <p>Match candidates to job descriptions using NLP — scored, ranked, and ready to download.</p>
</div>

<div class="feature-row">
  <span class="feature-pill"><span class="dot"></span>AI Scoring</span>
  <span class="feature-pill"><span class="dot"></span>Skill Extraction</span>
  <span class="feature-pill"><span class="dot"></span>Candidate Ranking</span>
  <span class="feature-pill"><span class="dot"></span>PDF Reports</span>
  <span class="feature-pill"><span class="dot"></span>CSV Export</span>
</div>

<div class="stats-strip">
  <div class="stat-cell">
    <div class="stat-cell-label">Speed</div>
    <div class="stat-cell-value accent">&lt; 5s</div>
  </div>
  <div class="stat-cell">
    <div class="stat-cell-label">Format</div>
    <div class="stat-cell-value">PDF</div>
  </div>
  <div class="stat-cell">
    <div class="stat-cell-label">Accuracy</div>
    <div class="stat-cell-value accent">High</div>
  </div>
  <div class="stat-cell">
    <div class="stat-cell-label">Analytics</div>
    <div class="stat-cell-value">Real-time</div>
  </div>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown('<div class="input-label">Job Description</div>', unsafe_allow_html=True)
        job_description = st.text_area(
            "jd", height=220,
            placeholder="Paste the job description here...",
            label_visibility="collapsed"
        )

    with col2:
        st.markdown('<div class="input-label">Resume Files</div>', unsafe_allow_html=True)
        uploaded_files = st.file_uploader(
            "up", type=["pdf"],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )
        if uploaded_files:
            st.success(f"{len(uploaded_files)} file(s) ready to analyze.")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if st.button("Analyze Resumes", use_container_width=True):

        if not job_description:
            st.warning("Paste a job description to continue.")
        elif not uploaded_files:
            st.warning("Upload at least one resume PDF.")
        else:
            results = []
            with st.spinner("Analyzing..."):
                for uf in uploaded_files:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(uf.getbuffer())
                        tmp_path = tmp.name

                    resume_text = extract_text_from_pdf(tmp_path)
                    analysis    = calculate_ats_score(resume_text, job_description)
                    present_s, missing_s = check_sections(resume_text)
                    analysis["present_sections"] = present_s
                    analysis["missing_sections"]  = missing_s
                    rec, emoji = get_recommendation(analysis["ats_score"])
                    analysis["candidate"]      = uf.name
                    analysis["recommendation"] = rec
                    analysis["emoji"]          = emoji
                    results.append(analysis)

            results = sorted(results, key=lambda x: x["ats_score"], reverse=True)
            st.session_state["results"] = results

            st.success("Analysis complete.")

            df = create_dataframe(results)
            st.download_button(
                "Download CSV",
                data=df.to_csv(index=False),
                file_name="ats_results.csv",
                mime="text/csv"
            )

            st.markdown('<div class="section-title">Candidate Rankings</div>',
                        unsafe_allow_html=True)

            for idx, c in enumerate(results):
                score     = c["ats_score"]
                name      = c["candidate"]
                disp_name = name.replace(".pdf","").replace("_"," ")
                skill_pct = c.get("skill_score", 0)
                sim_pct   = c.get("similarity_score", 0)
                sec_pct   = c.get("section_score", 0)

                rank_cls = "top" if idx < 3 else ""

                if score >= 75:
                    score_cls, status_cls, status_txt = "high", "sl-high", "Strong"
                elif score >= 50:
                    score_cls, status_cls, status_txt = "medium", "sl-medium", "Moderate"
                else:
                    score_cls, status_cls, status_txt = "low", "sl-low", "Weak"

                bar_cls = "green" if score >= 75 else ("amber" if score >= 50 else "purple")

                rank_label = ["01","02","03"][idx] if idx < 3 else f"{idx+1:02d}"

                st.markdown(f"""
<div class="c-card">
  <div class="rank-num {rank_cls}">{rank_label}</div>
  <div class="c-info">
    <div class="c-name">{disp_name}</div>
    <div class="c-file">{name}</div>
  </div>
  <div class="bars-col">
    <div class="bar-row">
      <div class="bar-meta"><span>Skills</span><span>{skill_pct}%</span></div>
      <div class="bar-track"><div class="bar-fill {bar_cls}" style="width:{skill_pct}%"></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-meta"><span>Similarity</span><span>{sim_pct}%</span></div>
      <div class="bar-track"><div class="bar-fill {bar_cls}" style="width:{sim_pct}%"></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-meta"><span>Sections</span><span>{sec_pct}%</span></div>
      <div class="bar-track"><div class="bar-fill {bar_cls}" style="width:{sec_pct}%"></div></div>
    </div>
  </div>
  <div class="score-badge {score_cls}">{score}%</div>
  <div class="status-label {status_cls}">{status_txt}</div>
</div>
""", unsafe_allow_html=True)

                with st.expander(f"Details — {disp_name}"):
                    # Gauge
                    if score >= 75:
                        gauge_color = "#34d399"
                    elif score >= 50:
                        gauge_color = "#fbbf24"
                    else:
                        gauge_color = "#f87171"

                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=score,
                        number={"font": {"color": gauge_color, "size": 32},
                                "suffix": "%"},
                        title={"text": "ATS Score",
                               "font": {"color": "#6b6b80", "size": 12}},
                        gauge={
                            "axis": {
                                "range": [0, 100],
                                "tickcolor": "#3a3a4a",
                                "tickfont": {"color": "#3a3a4a", "size": 9},
                            },
                            "bar": {"color": gauge_color, "thickness": 0.55},
                            "bgcolor": "#131318",
                            "borderwidth": 0,
                            "steps": [
                                {"range": [0,   100], "color": "#1a1a22"},
                            ],
                        }
                    ))
                    fig.update_layout(
                        height=200,
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font_color="#e8e8f0",
                        margin=dict(l=16, r=16, t=40, b=8)
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    ca, cb = st.columns(2, gap="medium")

                    with ca:
                        st.markdown('<div class="input-label" style="margin-bottom:8px">Matched Skills</div>',
                                    unsafe_allow_html=True)
                        if c.get("matched_skills"):
                            chips = "".join(
                                f'<span class="chip chip-ok">{s}</span>'
                                for s in c["matched_skills"]
                            )
                            st.markdown(chips, unsafe_allow_html=True)
                        else:
                            st.markdown('<span style="color:#3a3a4a;font-size:0.8rem">None found</span>',
                                        unsafe_allow_html=True)

                        st.markdown('<div class="input-label" style="margin:16px 0 8px">Sections Present</div>',
                                    unsafe_allow_html=True)
                        for sec in c.get("present_sections", []):
                            st.markdown(f'<div class="sec-item ok">+ {sec.title()}</div>',
                                        unsafe_allow_html=True)

                    with cb:
                        st.markdown('<div class="input-label" style="margin-bottom:8px">Missing Skills</div>',
                                    unsafe_allow_html=True)
                        if c.get("missing_skills"):
                            chips = "".join(
                                f'<span class="chip chip-no">{s}</span>'
                                for s in c["missing_skills"]
                            )
                            st.markdown(chips, unsafe_allow_html=True)
                        else:
                            st.markdown('<span style="color:#3a3a4a;font-size:0.8rem">None</span>',
                                        unsafe_allow_html=True)

                        st.markdown('<div class="input-label" style="margin:16px 0 8px">Sections Missing</div>',
                                    unsafe_allow_html=True)
                        for sec in c.get("missing_sections", []):
                            st.markdown(f'<div class="sec-item bad">– {sec.title()}</div>',
                                        unsafe_allow_html=True)

                    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                    os.makedirs("output", exist_ok=True)
                    rpt_path = f"output/report_{idx}.pdf"
                    generate_pdf_report(c, rpt_path)
                    with open(rpt_path, "rb") as f:
                        st.download_button(
                            "Download PDF Report",
                            data=f,
                            file_name=f"{name}_report.pdf",
                            mime="application/pdf"
                        )

    st.markdown('<div class="footer">Resume ATS Analyzer · 2024</div>',
                unsafe_allow_html=True)


# ═════════════════════════════════════════
# ANALYTICS
# ═════════════════════════════════════════
elif page == "Analytics":

    st.markdown("""
<div class="page-header">
  <h1>Analytics</h1>
  <p>Candidate breakdown and score distribution.</p>
</div>
""", unsafe_allow_html=True)

    if "results" not in st.session_state:
        st.warning("Run an analysis on the Home page first.")
    else:
        results = st.session_state["results"]
        total   = len(results)
        avg     = round(sum(c["ats_score"] for c in results) / total, 1)
        top     = results[0]

        m1, m2, m3 = st.columns(3, gap="medium")
        m1.metric("Candidates",    total)
        m2.metric("Avg ATS Score", f"{avg}%")
        m3.metric("Top Candidate", top["candidate"].replace(".pdf","").replace("_"," "))

        st.markdown('<div class="section-title">Score Comparison</div>',
                    unsafe_allow_html=True)

        chart_df = pd.DataFrame({
            "Candidate": [c["candidate"].replace(".pdf","").replace("_"," ")
                          for c in results],
            "ATS Score": [c["ats_score"] for c in results],
        })

        def bar_color(s):
            if s >= 75: return "#34d399"
            if s >= 50: return "#fbbf24"
            return "#f87171"

        colors = [bar_color(s) for s in chart_df["ATS Score"]]

        fig = go.Figure(go.Bar(
            x=chart_df["Candidate"],
            y=chart_df["ATS Score"],
            text=chart_df["ATS Score"].astype(str) + "%",
            textposition="outside",
            marker_color=colors,
            marker_line_width=0,
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#6b6b80",
            font_family="Inter, sans-serif",
            xaxis=dict(
                title=None,
                gridcolor="rgba(255,255,255,0.03)",
                tickfont=dict(color="#6b6b80", size=11),
                linecolor="rgba(255,255,255,0.06)",
            ),
            yaxis=dict(
                title=None,
                gridcolor="rgba(255,255,255,0.04)",
                tickfont=dict(color="#6b6b80", size=11),
                range=[0, 115],
                ticksuffix="%",
            ),
            margin=dict(l=0, r=0, t=28, b=0),
            bargap=0.4,
        )
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2, gap="medium")

        with c1:
            st.markdown('<div class="section-title">Distribution</div>',
                        unsafe_allow_html=True)

            strong   = sum(c["recommendation"] == "Strong Candidate"   for c in results)
            moderate = sum(c["recommendation"] == "Moderate Candidate" for c in results)
            weak     = sum(c["recommendation"] == "Weak Candidate"     for c in results)

            pie_df = pd.DataFrame({
                "Category": ["Strong", "Moderate", "Weak"],
                "Count":    [strong, moderate, weak],
            })
            fig_pie = go.Figure(go.Pie(
                labels=pie_df["Category"],
                values=pie_df["Count"],
                hole=0.6,
                marker=dict(
                    colors=["#34d399","#fbbf24","#f87171"],
                    line=dict(color="#0c0c0f", width=2),
                ),
                textfont=dict(color="#e8e8f0", size=12),
                hoverinfo="label+percent",
            ))
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#6b6b80",
                font_family="Inter, sans-serif",
                legend=dict(font=dict(color="#6b6b80", size=11)),
                margin=dict(l=0, r=0, t=10, b=0),
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with c2:
            st.markdown('<div class="section-title">Leaderboard</div>',
                        unsafe_allow_html=True)

            lb = pd.DataFrame({
                "Rank":       [f"{i+1:02d}" for i in range(len(results))],
                "Candidate":  [c["candidate"].replace(".pdf","").replace("_"," ")
                               for c in results],
                "Score":      [f"{c['ats_score']}%" for c in results],
                "Result":     [c["recommendation"].replace(" Candidate","")
                               for c in results],
            })
            st.dataframe(lb, use_container_width=True, hide_index=True)

        st.markdown('<div class="footer">Resume ATS Analyzer · 2024</div>',
                    unsafe_allow_html=True)


# ═════════════════════════════════════════
# ABOUT
# ═════════════════════════════════════════
elif page == "About":

    st.markdown("""
<div class="page-header">
  <h1>About</h1>
  <p>How it works and what it's built with.</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="about-card">
  <h2>Resume ATS Analyzer</h2>
  <div class="tagline">
    An intelligent resume screening tool that scores, ranks,
    and analyses candidates against a job description using NLP and machine learning.
  </div>

  <div class="about-section-title">Features</div>
  <ul class="about-list">
    <li>Resume parsing from PDF</li>
    <li>ATS score calculation</li>
    <li>Keyword &amp; skill extraction</li>
    <li>Candidate ranking</li>
    <li>Missing skill detection</li>
    <li>Section completeness analysis</li>
    <li>CSV export &amp; PDF report generation</li>
    <li>Analytics dashboard</li>
  </ul>

  <div class="about-section-title">Stack</div>
  <div>
    <span class="tech-badge">Python</span>
    <span class="tech-badge">Streamlit</span>
    <span class="tech-badge">Scikit-Learn</span>
    <span class="tech-badge">NLTK</span>
    <span class="tech-badge">PyPDF2</span>
    <span class="tech-badge">Plotly</span>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="footer">Resume ATS Analyzer · 2024</div>',
                unsafe_allow_html=True)