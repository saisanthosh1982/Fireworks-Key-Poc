import os
import json
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("FIREWORKS_API_KEY"),
    base_url="https://api.fireworks.ai/inference/v1"
)

PARSE_MODEL = "accounts/saisanthosh0902-hqwt/deployedModels/llama-v3p1-8b-instruct-p3ra4v10"


PROMPT = """
You are a KYC parsing agent.

Extract ONLY the following fields from the provided document text and return valid JSON:

{
  "full_name": string or null,
  "dob": "YYYY-MM-DD" or null,
  "expiry_date": "YYYY-MM-DD" or null,
  "document_number": string or null,
  "sex": string or null,
  "nationality": string or null,
  "address": string or null,
  "document_type": "Passport" or "Driver License" or null
}

Rules:
- Return ONLY the JSON.
- No markdown, no text before or after.
- If unsure about a field, return null.
"""


def parse_fields(raw_text: str) -> str:
    
    messages = [
        {
            "role": "user",
            "content": f"{PROMPT}\n\nDocument Content:\n{raw_text}"
        }
    ]

    # --- Retry logic (prevents the loop freezing) ---
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=PARSE_MODEL,
                messages=messages,
                temperature=0
            )
            content = response.choices[0].message.content.strip()

            # Remove markdown formatting if present
            content = content.replace("```json", "").replace("```", "").strip()

            # Validate JSON
            json.loads(content)  # will throw if invalid

            return content
        
        except Exception as e:
            print(f"⚠️ Parse failed (attempt {attempt+1}) → {e}")
            time.sleep(2)

    return json.dumps({"error": "Failed to parse output after retries"})
