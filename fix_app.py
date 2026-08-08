# Fixes app.py and tests correct model ID

# ── STEP 1: Find working model ────────────────────────────
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

print("Testing models...")
print("─" * 40)

models_to_try = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-latest",
    "gemini-2.0-flash",
    "gemini-2.0-flash-001",
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
]

working_model = None

for model_id in models_to_try:
    try:
        response = client.models.generate_content(
            model=model_id,
            contents="Say OK"
        )
        print(f"✅ WORKS: {model_id}")
        working_model = model_id
        break
    except Exception as e:
        print(f"❌ FAILED: {model_id} → {str(e)[:50]}")

print("─" * 40)

if not working_model:
    print("❌ No model worked! Check API key!")
else:
    print(f"\n🎯 Best working model: {working_model}")

    # ── STEP 2: Update gemini_analyzer.py with working model ──
    with open('gemini_analyzer.py', 'r', encoding='utf-8') as f:
        content = f.read()

    for m in models_to_try:
        content = content.replace(f'MODEL_ID = "{m}"', f'MODEL_ID = "{working_model}"')

    with open('gemini_analyzer.py', 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ gemini_analyzer.py updated with: {working_model}")

    # ── STEP 3: Fix app.py use_column_width issue ─────────────
    with open('app.py', 'r', encoding='utf-8') as f:
        app_content = f.read()

    app_content = app_content.replace(
        'use_column_width=True',
        'use_container_width=True'
    )

    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(app_content)

    print("✅ app.py fixed: use_column_width → use_container_width")

    print("\n🎉 ALL FIXED! Run: streamlit run app.py")