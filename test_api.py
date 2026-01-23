#!/usr/bin/env python3
import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file from project root
env_path = Path(__file__).parent / ".env"
print(f"Loading .env from: {env_path}")
print(f".env exists: {env_path.exists()}")

load_dotenv(dotenv_path=env_path, override=True)

# Get API keys
api_key = os.getenv("GEMINI_API_KEY", "")
print(f"\nAPI Key loaded: {api_key[:50] if api_key else 'NOT FOUND'}...")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found!")
    exit(1)

# Get first key
keys = [k.strip() for k in api_key.split(",") if k.strip()]
print(f"Number of keys: {len(keys)}")
print(f"First key: {keys[0][:30]}...")

# Test the first key
test_key = keys[0]
print(f"\n--- Testing key ---")
try:
    genai.configure(api_key=test_key)
    print("✅ API configured successfully")
    
    model = genai.GenerativeModel("gemini-2.5-flash")
    print("✅ Model created successfully")
    
    response = model.generate_content("Hello, who are you?")
    print(f"✅ Response received: {response.text[:100]}...")
    
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
