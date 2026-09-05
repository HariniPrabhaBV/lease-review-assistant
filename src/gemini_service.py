import os
from google import genai

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_summary(report):
    prompt = f"""
You are a legal review assistant.

Based on the following lease review findings, create a plain-English summary.

Keep it to 3-4 bullet points.

Findings:
{report}

Do not approve or reject the agreement.
Mention that a human reviewer should review it.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text 