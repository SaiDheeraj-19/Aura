"""
Script to verify which Gemini models are available and functional for the user.
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print(f"Checking API Key: {api_key[:5]}...{api_key[-5:] if api_key else 'None'}")

# Models to test
candidates = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-001",
    "gemini-1.5-flash-002",
    "gemini-1.5-pro",
    "gemini-2.0-flash-exp",
    "gemini-pro"
]

print("\n--- MODEL DIAGNOSTICS ---\n")

available_models = []
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)
            print(f"FOUND: {m.name}")
except Exception as e:
    print(f"Listing failed: {e}")

print("\n--- FUNCTIONAL TESTING ---\n")

functional_model = None

for model_name in candidates:
    print(f"Testing {model_name}...", end=" ")
    full_name = f"models/{model_name}" if not model_name.startswith("models/") else model_name
    
    # Check if in list first (optimization)
    if full_name not in available_models and model_name not in available_models:
        print("❌ Not in list")
        continue

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello")
        if response and response.text:
            print("✅ SUCCESS")
            functional_model = model_name
            break
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")

if functional_model:
    print(f"\nRecommended Model: {functional_model}")
else:
    print("\n⚠️ NO FUNCTIONAL MODEL FOUND. CHECK API KEY OR QUOTA.")
