# ============================================================
#  SentinelNE — Main Application
#  AI-Powered Border Intelligence & Terrain Analysis Tool
#  Built for Hack4Brahma Hackathon
# ============================================================

import streamlit as st
import time
from PIL import Image

# Local modules
from gemini_analyzer import analyze
from image_processor import process_image
from report_formatter import (
    format_for_download,
    get_filename,
    get_risk_color,
    get_risk_emoji
)

# ── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="SentinelNE — Intelligence Analysis",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS Theme ─────────────────────────────────────────────────
st.markdown("""
<style>
    /* Background */
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }

    /* Buttons */
    .stButton > button {
        background-color: #238636;
        color: white;
        border: 1px solid #2ea043;
        border-radius: 6px;
        font-weight: bold;
        width: 100%;
        padding: 10px;
    }

    .stButton > button:hover {
        background-color: #2ea043;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        border: 2px dashed #30363d;
        border-radius: 8px;
        background-color: #161b22;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 🛰️ SentinelNE")
    st.markdown("**Northeast India Intelligence Tool**")
    st.divider()

    st.markdown("### 📌 About")
    st.info(
        "SentinelNE uses Google Gemini AI to analyze "
        "terrain images and situation reports, generating "
        "military-grade intelligence briefs instantly."
    )

    st.markdown("### 🚦 Risk Levels")
    st.markdown("""
    🟢 **LOW** — Standard protocols  
    🟡 **MEDIUM** — Enhanced vigilance  
    🟠 **HIGH** — Extra resources needed  
    🔴 **CRITICAL** — Immediate escalation
    """)

    st.markdown("### 💡 Tips")
    st.markdown("""
    - Use satellite/aerial images
    - Add situation context for deeper analysis
    - Sample images in `sample_images/` folder
    - Works with Google Maps screenshots!
    """)

    st.divider()
    st.caption("Built for Hack4Brahma 🏆")
    st.caption("Powered by Gemini AI 🤖")

# ── Main Header ───────────────────────────────────────────────
st.markdown("""
<div style="
    text-align: center;
    padding: 30px;
    background: linear-gradient(135deg, #0d1117, #161b22);
    border: 1px solid #30363d;
    border-radius: 12px;
    margin-bottom: 30px;
">
    <h1 style="color: #58a6ff; font-size: 2.5em; margin: 0;">
        🛰️ SENTINELNE
    </h1>
    <p style="color: #8b949e; margin-top: 10px; letter-spacing: 2px;">
        AI-POWERED BORDER INTELLIGENCE & TERRAIN ANALYSIS SYSTEM
    </p>
    <p style="color: #3fb950; font-size: 0.85em; margin-top: 5px;">
        NORTHEAST INDIA FIELD OPERATIONS SUPPORT TOOL
    </p>
</div>
""", unsafe_allow_html=True)

# ── Two Column Layout ─────────────────────────────────────────
col1, col2 = st.columns([1, 1], gap="large")

# ═══════════════════════════════════════════════════
# LEFT COLUMN — INPUTS
# ═══════════════════════════════════════════════════
with col1:
    st.markdown("## 📡 Input Intelligence Data")

    # ── Image Upload ──────────────────────────────────────────
    st.markdown("#### 🖼️ Terrain / Satellite Image")
    uploaded_file = st.file_uploader(
        "Upload Image",
        type=["jpg", "jpeg", "png", "webp"],
        help="Upload satellite imagery, aerial photos, or terrain images",
        label_visibility="collapsed"
    )

    pil_image = None

    if uploaded_file is not None:
        try:
            pil_image, original_size, resized_size = process_image(uploaded_file)
            st.image(
                pil_image,
                caption=f"📍 {uploaded_file.name}",
                use_column_width=True
            )
            st.success(
                f"✅ Image loaded: {original_size[0]}×{original_size[1]}px"
            )
        except Exception as e:
            st.error(f"❌ Image processing failed: {e}")
    else:
        st.markdown("""
        <div style="
            border: 2px dashed #30363d;
            border-radius: 8px;
            padding: 40px;
            text-align: center;
            color: #8b949e;
            background-color: #161b22;
        ">
            <div style="font-size: 2.5em">🛰️</div>
            <div style="margin-top: 10px;">No image uploaded yet</div>
            <div style="font-size: 0.8em; margin-top: 5px; color: #6e7681;">
                Use sample images from sample_images/ folder
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Situation Report Input ────────────────────────────────
    st.markdown("#### 📝 Field Situation Report *(Optional)*")
    situation_text = st.text_area(
        "Situation Report",
        placeholder=(
            "Example:\n"
            "Location: Tawang, Arunachal Pradesh\n"
            "Time: Night patrol 0200 hrs\n"
            "Weather: Heavy fog, -5°C\n"
            "Activity: Motion sensors triggered in sector 4\n"
            "Last patrol: 12 hours ago"
        ),
        height=200,
        label_visibility="collapsed"
    )

    # ── Input Status ──────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    if uploaded_file and situation_text.strip():
        st.success("✅ Image + Situation Report ready!")
    elif uploaded_file:
        st.success("✅ Image ready! (No situation report — that's OK)")
    elif situation_text.strip():
        st.success("✅ Situation report ready! (No image — that's OK)")
    else:
        st.warning("⚠️ Please provide an image and/or situation report")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Analyze Button ────────────────────────────────────────
    is_ready = uploaded_file is not None or situation_text.strip() != ""
    analyze_btn = st.button(
        "🔍 GENERATE INTELLIGENCE BRIEF",
        disabled=not is_ready,
        use_container_width=True,
        type="primary"
    )

    st.caption(
        "📁 Sample satellite images in `sample_images/` folder for testing"
    )

# ═══════════════════════════════════════════════════
# RIGHT COLUMN — OUTPUT
# ═══════════════════════════════════════════════════
with col2:
    st.markdown("## 📋 Intelligence Brief")

    # Session state for report
    if "report_data" not in st.session_state:
        st.session_state.report_data = None

    # ── Run Analysis When Button Clicked ─────────────────────
    if analyze_btn:
        with st.spinner("🛰️ SentinelNE analyzing terrain data..."):
            time.sleep(0.5)
            result = analyze(
                pil_image=pil_image,
                situation_text=situation_text
            )
            st.session_state.report_data = result

    # ── Display Report ────────────────────────────────────────
    if st.session_state.report_data:
        result = st.session_state.report_data

        if result["success"]:
            risk_level  = result["risk_level"]
            report_text = result["report"]
            risk_emoji  = get_risk_emoji(risk_level)
            risk_color  = get_risk_color(risk_level)

            # ── Risk Level Display ────────────────────────────
            st.markdown(f"""
            <div style="
                text-align: center;
                padding: 20px;
                background-color: #161b22;
                border: 2px solid {risk_color};
                border-radius: 10px;
                margin-bottom: 20px;
            ">
                <div style="color: #8b949e; font-size: 0.85em;
                            letter-spacing: 2px; margin-bottom: 8px;">
                    OVERALL RISK ASSESSMENT
                </div>
                <div style="color: {risk_color}; font-size: 2em;
                            font-weight: bold; letter-spacing: 4px;">
                    {risk_emoji} {risk_level}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Quick Stats ───────────────────────────────────
            sc1, sc2, sc3 = st.columns(3)
            sc1.metric("Analysis", "✅ Done")
            sc2.metric("Risk Level", f"{risk_emoji} {risk_level}")
            sc3.metric("Powered By", "Gemini AI")

            st.divider()

            # ── Full Report ───────────────────────────────────
            st.markdown("### 📄 Full Intelligence Brief")
            st.markdown(report_text)

            st.divider()

            # ── Download Button ───────────────────────────────
            download_content = format_for_download(report_text, risk_level)
            download_filename = get_filename()

            st.download_button(
                label="📥 Download Intelligence Brief (.md)",
                data=download_content,
                file_name=download_filename,
                mime="text/markdown",
                use_container_width=True
            )

            st.caption(
                "⚠️ AI-generated report — always verify with "
                "ground truth before mission execution."
            )

        else:
            # ── Error State ───────────────────────────────────
            st.error("❌ Analysis Failed!")
            st.error(result["error"])

            with st.expander("🔧 How to Fix"):
                st.markdown("""
                **Common Solutions:**
                1. Check your `GEMINI_API_KEY` in `.env` file
                2. Make sure internet is connected
                3. Try a smaller image (under 5MB)
                4. Try rephrasing situation report
                5. Wait 60 seconds if rate limited
                """)

    else:
        # ── Empty State ───────────────────────────────────────
        st.markdown("""
        <div style="
            border: 1px solid #30363d;
            border-radius: 10px;
            padding: 60px 20px;
            text-align: center;
            background-color: #161b22;
            min-height: 400px;
        ">
            <div style="font-size: 4em;">🛰️</div>
            <h3 style="color: #58a6ff; margin-top: 15px;">
                Awaiting Intelligence Data
            </h3>
            <p style="color: #8b949e; max-width: 300px; margin: 0 auto;">
                Upload a terrain image and/or provide a situation
                report on the left panel, then click
                <strong>GENERATE INTELLIGENCE BRIEF</strong>
            </p>
            <div style="margin-top: 30px; color: #3fb950; font-size: 0.8em;">
                ── SYSTEM READY ──
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="text-align: center; color: #6e7681; font-size: 0.85em;">
    🛰️ SentinelNE v1.0 &nbsp;|&nbsp;
    Built for <strong>Hack4Brahma 🏆</strong> &nbsp;|&nbsp;
    Powered by <strong>Google Gemini AI</strong> &nbsp;|&nbsp;
    Dedicated to the Guardians of Northeast India 🇮🇳
</div>
""", unsafe_allow_html=True)