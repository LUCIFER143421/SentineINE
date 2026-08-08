# This script rewrites all broken files with correct encoding

# ── FILE 1: image_processor.py ────────────────────────────
image_processor_code = '''from PIL import Image
import io

MAX_SIZE = (1024, 1024)
QUALITY = 85

def process_image(uploaded_file):
    try:
        image = Image.open(uploaded_file)
        if image.mode != "RGB":
            image = image.convert("RGB")
        original_size = image.size
        image.thumbnail(MAX_SIZE, Image.LANCZOS)
        resized_size = image.size
        print(f"Image processed: {original_size} to {resized_size}")
        return image, original_size, resized_size
    except Exception as e:
        raise ValueError(f"Failed to process image: {str(e)}")

def image_to_bytes(pil_image):
    buffer = io.BytesIO()
    pil_image.save(buffer, format="JPEG", quality=QUALITY)
    buffer.seek(0)
    return buffer.read()
'''

# ── FILE 2: report_formatter.py ───────────────────────────
report_formatter_code = '''from datetime import datetime

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
'''

# ── FILE 3: gemini_analyzer.py ────────────────────────────
gemini_analyzer_code = '''import os
import io
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file!")

client = genai.Client(api_key=API_KEY)
MODEL_ID = "gemini-2.5-flash"

def pil_to_bytes(pil_image):
    buffer = io.BytesIO()
    pil_image.save(buffer, format="JPEG", quality=85)
    buffer.seek(0)
    return buffer.read()

def build_prompt(situation_text=""):
    base = """
You are SentinelNE, an expert military terrain analyst specializing
in Northeast India operations. Analyze the provided image and/or
situation report and generate a structured intelligence brief.

Use EXACTLY this format:

## SENTINELNE INTELLIGENCE BRIEF

### 1. TERRAIN ANALYSIS
- Terrain Type:
- Estimated Elevation:
- Vegetation Density:
- Water Bodies:
- Seasonal Conditions:

### 2. PATROL DIFFICULTY SCORE
- Score: X / 10
- Difficulty Level: Easy / Moderate / Hard / Extreme
- Key Factors: (3 reasons)
- Recommended Squad Size:

### 3. ANOMALY DETECTION REPORT
- Anomaly 1:
- Anomaly 2:
- Anomaly 3:

### 4. STRATEGIC RECOMMENDATIONS
1.
2.
3.
4.
5.

### 5. RESOURCE REQUIREMENTS
- Personnel:
- Equipment:
- Vehicles:
- Medical:
- Communication:

### 6. RISK ASSESSMENT
- Overall Risk Level: LOW / MEDIUM / HIGH / CRITICAL
- Primary Risk Factor:
- Secondary Risk Factor:
- Recommended Action:

### 7. ANALYST NOTES

---
Report by SentinelNE AI System
"""
    if situation_text and situation_text.strip():
        base += f"""
### FIELD SITUATION REPORT:
{situation_text.strip()}
"""
    return base

def extract_risk_level(text):
    text_upper = text.upper()
    if "OVERALL RISK LEVEL:" in text_upper:
        section = text_upper.split("OVERALL RISK LEVEL:")[1][:60]
        if "CRITICAL" in section: return "CRITICAL"
        if "HIGH"     in section: return "HIGH"
        if "MEDIUM"   in section: return "MEDIUM"
        if "LOW"      in section: return "LOW"
    if "CRITICAL" in text_upper: return "CRITICAL"
    if "HIGH"     in text_upper: return "HIGH"
    if "MEDIUM"   in text_upper: return "MEDIUM"
    if "LOW"      in text_upper: return "LOW"
    return "UNKNOWN"

def analyze(pil_image=None, situation_text=""):
    if pil_image is None and not situation_text.strip():
        return {
            "success": False,
            "report": "",
            "risk_level": "UNKNOWN",
            "error": "Please provide an image or situation report!"
        }
    try:
        prompt = build_prompt(situation_text)
        contents = []
        if pil_image is not None:
            image_bytes = pil_to_bytes(pil_image)
            image_part = types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/jpeg"
            )
            contents.append(image_part)
        contents.append(prompt)
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.4,
                max_output_tokens=4096,
            )
        )
        report_text = response.text
        risk_level = extract_risk_level(report_text)
        return {
            "success": True,
            "report": report_text,
            "risk_level": risk_level,
            "error": ""
        }
    except Exception as e:
        error_msg = str(e)
        if "api_key" in error_msg.lower() or "invalid" in error_msg.lower():
            friendly = "Invalid API Key - check your .env file!"
        elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
            friendly = "Rate limit hit - wait 60 seconds!"
        elif "blocked" in error_msg.lower() or "safety" in error_msg.lower():
            friendly = "Safety filter triggered - rephrase situation report!"
        elif "404" in error_msg or "not found" in error_msg.lower():
            friendly = "Model not found - check MODEL_ID"
        else:
            friendly = f"Error: {error_msg}"
        return {
            "success": False,
            "report": "",
            "risk_level": "UNKNOWN",
            "error": friendly
        }
'''

# ── WRITE ALL FILES ───────────────────────────────────────
files = {
    'image_processor.py': image_processor_code,
    'report_formatter.py': report_formatter_code,
    'gemini_analyzer.py': gemini_analyzer_code,
}

for filename, code in files.items():
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(code.lstrip('\n'))
    print(f"✅ {filename} written successfully!")

print("\n🎉 ALL FILES FIXED! Now run: streamlit run app.py")