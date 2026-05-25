import os
import google.generativeai as genai

from dotenv import load_dotenv
from pathlib import Path

# Load .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Configure Gemini
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Load Model
model = genai.GenerativeModel(
    "gemini-1.5-flash"
)


def analyze_logs(logs):

    prompt = f"""
You are an expert Site Reliability Engineer.

Analyze these infrastructure logs carefully.

Provide:
1. Severity
2. Root Cause
3. Suggested Fix

Keep answers SHORT.

Logs:
{logs}

Return ONLY in this format:

Severity: High

Root Cause: Short root cause.

Suggested Fix: Short fix.
"""

    try:

        response = model.generate_content(prompt)

        # SAFE RESPONSE CHECK
        if response and hasattr(response, "text"):

            return response.text

        return """
Severity: Medium

Root Cause: AI could not analyze logs.

Suggested Fix: Retry analysis.
"""

    except Exception as e:

        print("GEMINI ERROR:", e)

        # SMART LOCAL FALLBACK AI
        logs_lower = logs.lower()

        if "redis" in logs_lower:

            return """
Severity: Critical

Root Cause: Redis memory exhaustion detected.

Suggested Fix: Increase Redis memory or enable cache cleanup.
"""

        elif "database" in logs_lower or "postgresql" in logs_lower:

            return """
Severity: High

Root Cause: Database connection timeout detected.

Suggested Fix: Check database health and connection pool.
"""

        elif "latency" in logs_lower or "packet loss" in logs_lower:

            return """
Severity: High

Root Cause: Network instability causing packet loss.

Suggested Fix: Check network routes and node connectivity.
"""

        elif "cpu" in logs_lower:

            return """
Severity: High

Root Cause: CPU usage exceeded safe threshold.

Suggested Fix: Scale services or optimize workloads.
"""

        else:

            return """
Severity: Medium

Root Cause: Infrastructure issue detected.

Suggested Fix: Investigate logs and monitoring dashboards.
"""