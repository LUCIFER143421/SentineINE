from datetime import datetime

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_filename():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"SentinelNE_Report_{ts}.md"

def format_for_download(report_text, risk_level):
    timestamp = get_timestamp()
    header = f"""# SENTINELNE INTELLIGENCE BRIEF
Generated: {timestamp}
Risk Level: {risk_level}
System: SentinelNE AI Analysis v1.0

---

"""
    footer = """

---
AI-generated report for informational purposes only.
Verify with ground truth before mission execution.
"""
    return header + report_text + footer

def get_risk_color(risk_level):
    colors = {
        "LOW":      "#00FF88",
        "MEDIUM":   "#FFD700",
        "HIGH":     "#FF6B35",
        "CRITICAL": "#FF0000",
        "UNKNOWN":  "#888888",
    }
    return colors.get(risk_level.upper(), "#888888")

def get_risk_emoji(risk_level):
    emojis = {
        "LOW":      "🟢",
        "MEDIUM":   "🟡",
        "HIGH":     "🟠",
        "CRITICAL": "🔴",
        "UNKNOWN":  "⚪",
    }
    return emojis.get(risk_level.upper(), "⚪")
