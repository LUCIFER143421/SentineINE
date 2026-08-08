import os
import io
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_ID = os.getenv("GEMINI_MODEL_ID", "gemini-2.5-flash")


def get_max_output_tokens():
    try:
        return int(os.getenv("GEMINI_MAX_OUTPUT_TOKENS", "2048"))
    except ValueError:
        return 2048


def get_client():
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY not found in .env file!")
    return genai.Client(api_key=API_KEY)


def get_retry_delay_seconds(error_text):
    for marker in ("retry_delay {", "retryDelay"):
        if marker in error_text:
            digits = "".join(ch for ch in error_text.split(marker, 1)[1][:20] if ch.isdigit())
            if digits:
                return int(digits)
    return None


def build_quota_error(error_text):
    retry_delay = get_retry_delay_seconds(error_text)
    wait_hint = (
        f" Gemini asked to retry after about {retry_delay} seconds."
        if retry_delay
        else " Wait a minute, then try once."
    )
    return (
        "Gemini API quota/rate limit reached for this API key or project."
        f"{wait_hint} If this happens on the first image, check the API key's "
        "active quota in Google AI Studio, confirm the selected model is "
        "available for your plan, or set GEMINI_MODEL_ID to a model with "
        f"available free quota. Details: {error_text}"
    )


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
        if "CRITICAL" in section:
            return "CRITICAL"
        if "HIGH" in section:
            return "HIGH"
        if "MEDIUM" in section:
            return "MEDIUM"
        if "LOW" in section:
            return "LOW"
    if "CRITICAL" in text_upper:
        return "CRITICAL"
    if "HIGH" in text_upper:
        return "HIGH"
    if "MEDIUM" in text_upper:
        return "MEDIUM"
    if "LOW" in text_upper:
        return "LOW"
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
        client = get_client()
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.4,
                max_output_tokens=get_max_output_tokens(),
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
        error_lower = error_msg.lower()
        if "api_key" in error_lower or "invalid" in error_lower:
            friendly = "Invalid API Key - check your .env file!"
        elif (
            "429" in error_msg
            or "resource_exhausted" in error_lower
            or "quota" in error_lower
            or "rate limit" in error_lower
        ):
            friendly = build_quota_error(error_msg)
        elif "blocked" in error_lower or "safety" in error_lower:
            friendly = "Safety filter triggered - rephrase situation report!"
        elif "404" in error_msg or "not found" in error_lower:
            friendly = "Model not found - check MODEL_ID"
        else:
            friendly = f"Error: {error_msg}"
        return {
            "success": False,
            "report": "",
            "risk_level": "UNKNOWN",
            "error": friendly
        }
