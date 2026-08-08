# 🛰️ SentinelNE — AI-Powered Border Intelligence & Terrain Analysis

> Built for **Hack4Brahma Hackathon** | Powered by **Google Gemini AI**

SentinelNE is an AI-powered intelligence analysis tool designed for
Northeast India field operations. Upload satellite/terrain images and
provide situation reports to generate instant military-grade intelligence
briefs — in seconds.

---

## 🚀 Features

- 🖼️ **Multimodal Analysis** — Upload satellite/terrain images
- 📝 **Situation Report Input** — Add field context for deeper analysis
- 🤖 **Gemini AI Brain** — Google's most capable free multimodal model
- 🚨 **Risk Level Assessment** — Color-coded LOW/MEDIUM/HIGH/CRITICAL
- 📋 **Structured Intel Brief** — 7-section military-grade report
- 📥 **Download Report** — Export as Markdown file
- 🖥️ **Works on Any PC** — Just pip install and run

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core language |
| Streamlit | Web UI |
| Gemini 2.0 Flash | AI analysis engine |
| Pillow | Image processing |
| python-dotenv | API key management |

---

## ⚡ Quick Setup (5 Minutes)

### Step 1 — Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/SentinelNE.git
cd SentinelNE
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Get your FREE Gemini API Key
1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Click **"Get API Key"**
3. Create a new key — completely FREE, no credit card!

### Step 4 — Setup API Key
```bash
# Copy the example env file
cp .env.example .env

# Open .env and paste your key
GEMINI_API_KEY=paste_your_key_here

# Optional: use another Gemini model if your key has quota there
GEMINI_MODEL_ID=gemini-2.0-flash
```

### Step 5 — Run!
```bash
streamlit run app.py
```

Opens automatically at **http://localhost:8501** ✅

---

## 🔧 Troubleshooting Rate Limits

If the app says the Gemini API quota/rate limit was reached on the first
image, it usually means the API key or Google Cloud project has no available
quota for the configured model, not that the image upload itself failed.

Try these fixes:

1. Open Google AI Studio and check the active quota for your API key/project.
2. Wait for the retry delay shown in the error details, then submit once.
3. Use a model that has available quota for your account by setting
   `GEMINI_MODEL_ID` in `.env`.
4. Keep image files small; the app already resizes images before sending them.

---

## 🧪 Testing

Sample satellite/terrain images are included in the
`sample_image/` folder — use them to test instantly!

---

## 📁 Project Structure

```
SentinelNE/
├── app.py                 ← Main Streamlit application
├── gemini_analyzer.py     ← Gemini API integration
├── image_processor.py     ← Image optimization
├── report_formatter.py    ← Report formatting utilities
├── requirements.txt       ← Dependencies
├── .env.example           ← API key template
├── .gitignore
├── README.md
└── sample_image/          ← Test images for judges
    ├── Screenshot 2026-08-08 103958.png
    ├── Screenshot 2026-08-08 104042.png
    └── ...
```

---

## ⚠️ Disclaimer

This tool is built for hackathon demonstration purposes.
AI-generated reports should always be verified with
ground truth before any real-world mission execution.

---

## 🏆 Built for Hack4Brahma
*Dedicated to the brave soldiers and paramilitary forces
guarding Northeast India 🇮🇳*
