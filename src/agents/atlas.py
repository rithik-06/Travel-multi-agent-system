"""
Atlas - Location & Trek Discovery Agent
Model: llama-3.3-70b-versatile (own rate limit bucket)
Job: Given user request, find best matching destinations with real details
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.groq_client import ask


def run(user_request: str) -> dict:
    """
    Takes user's travel request, returns structured destination data.
    Makes exactly ONE Groq call.
    """

    prompt = f"""
You are Atlas, a travel discovery specialist for Indian destinations.

User wants: {user_request}

Find the best matching trek or travel destination and return ONLY this JSON:

{{
    "destination": "exact place name",
    "state": "state in India",
    "district": "nearest district/city",
    "difficulty": "Easy/Moderate/Hard",
    "duration_days": 5,
    "best_months": ["October", "November"],
    "max_altitude_meters": 4000,
    "nearest_railhead": "closest railway station",
    "nearest_airport": "closest airport",
    "distance_from_delhi_km": 500,
    "highlights": ["highlight 1", "highlight 2", "highlight 3"],
    "stay_options": [
        {{
            "name": "place name",
            "type": "Camping/Guesthouse/Hotel",
            "approx_cost_per_night_inr": 800
        }},
        {{
            "name": "place name", 
            "type": "Camping/Guesthouse/Hotel",
            "approx_cost_per_night_inr": 1500
        }}
    ],
    "permits_required": true,
    "permit_cost_inr": 200,
    "best_route": "Delhi -> Shimla -> Kaza -> destination"
}}

Be specific and accurate. Use real place names and real costs in INR.
"""

    result = ask("atlas", prompt)
    result["agent"] = "atlas"
    return result


if __name__ == "__main__":
    import json
    result = run("5 day trek in Spiti Valley, moderate difficulty")
    print(json.dumps(result, indent=2))