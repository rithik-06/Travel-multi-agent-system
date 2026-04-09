"""
Shared Groq client - one key, three models, three separate rate limit buckets
"""

from groq import Groq
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Each agent gets its own model = own rate limit bucket
MODELS = {
    "captain": "gemma2-9b-it",
    "atlas":   "llama-3.3-70b-versatile",
    "budget":  "mixtral-8x7b-32768"
}


def ask(agent_name: str, prompt: str) -> dict:
    """
    Single function all agents use.
    Returns parsed JSON dict always.
    """
    try:
        response = client.chat.completions.create(
            model=MODELS[agent_name],
            messages=[
                {
                    "role": "system",
                    "content": "You are a travel planning assistant. Always respond with valid JSON only. No markdown, no explanation, just raw JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2048
        )

        raw = response.choices[0].message.content.strip()

        # Strip markdown if model adds it anyway
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        
        return json.loads(raw.strip())

    except json.JSONDecodeError:
        return {"error": "JSON parse failed", "raw": raw}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    result = ask("atlas", 'Give me a JSON object with one trekking destination in Himachal Pradesh. Format: {"name": "...", "difficulty": "...", "best_season": "..."}')
    print(result)