"""
Travel search tool - uses Gemini Flash (free, no rate limit issues)
"""

from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def web_search(query: str) -> str:
    """
    Search for travel information using Gemini.
    Returns detailed results as a string that agents can reason over.
    """
    try:
        prompt = f"""
You are a travel research assistant with deep knowledge of Indian travel destinations.
Answer this search query with detailed, accurate, and practical information:

Query: {query}

Provide:
- Specific place names and locations
- Real practical details (distances, costs, timings, seasons)
- Helpful tips a traveler would actually need

Be specific and factual. No vague answers.
"""
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt
        )
        return response.text.strip()

    except Exception as e:
        return f"Search failed: {str(e)}"


if __name__ == "__main__":
    result = web_search("best trekking spots in Himachal Pradesh")
    print(result)