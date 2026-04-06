import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def ask_gemini(prompt: str) -> dict:
    """
    Send a prompt to Gemini Flash and get back structured JSON.
    This is the single function all agents will use.
    """
    try:
        response = model.generate_content(
            f"{prompt}\n\nRespond ONLY with valid JSON. No explanation, no markdown, no code blocks. Just the raw JSON object.",
        )
        
        raw = response.text.strip()
        
        # Clean up if Gemini wraps in markdown anyway
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        
        return json.loads(raw.strip())
    
    except json.JSONDecodeError as e:
        return {"error": f"JSON parse failed: {str(e)}", "raw": response.text}
    except Exception as e:
        return {"error": str(e)}


def ask_gemini_text(prompt: str) -> str:
    """
    For when you just need plain text back, not JSON.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"