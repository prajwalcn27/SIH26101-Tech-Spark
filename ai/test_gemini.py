import os
from dotenv import load_dotenv
from google import genai

# Load .env
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ GEMINI_API_KEY not found in .env")
    exit()

# Create Gemini client
client = genai.Client(api_key=api_key)


# Simple Gemini test
try:

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Explain what a Pivot Table is in one simple sentence."
    )

    print("✅ Gemini API connected successfully!")
    print()
    print("Gemini Response:")
    print(response.text)

except Exception as e:

    print("❌ Gemini API error:")
    print(e)