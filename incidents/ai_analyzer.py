import os

from google.genai import Client
from dotenv import load_dotenv
from pathlib import Path

# Load .env file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Create Gemini client
client = Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_logs(logs):

    prompt = f"""
You are an expert Site Reliability Engineer.

Analyze these logs carefully.

Provide:
1. Severity
2. Root Cause
3. Suggested Fix

Logs:
{logs}

Return ONLY in this exact format:

Severity: <severity>

Root Cause: <root cause>

Suggested Fix: <fix>
"""

    try:

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        print("GEMINI ERROR:", str(e))

        return f"""
Severity: Medium

Root Cause: Gemini API failed.

Suggested Fix: Check API quota or configuration.
"""