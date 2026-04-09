"""
Budget Agent
Model: mixtral-8x7b-32768 (own rate limit bucket)
Job: Takes Atlas output, calculates complete cost breakdown per person
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.groq_client import ask


def run(atlas_result: dict, num_people: int, budget_per_person_inr: int) -> dict:
    """
    Takes Atlas destination data + trip details.
    Returns complete cost breakdown.
    Makes exactly ONE Groq call.
    """

    prompt = f"""
You are Budget, a travel cost planning specialist for Indian trips.

Destination data from Atlas agent:
- Place: {atlas_result.get('destination')}, {atlas_result.get('state')}
- Duration: {atlas_result.get('duration_days')} days
- Difficulty: {atlas_result.get('difficulty')}
- Nearest railhead: {atlas_result.get('nearest_railhead')}
- Nearest airport: {atlas_result.get('nearest_airport')}
- Distance from Delhi: {atlas_result.get('distance_from_delhi_km')} km
- Stay options: {atlas_result.get('stay_options')}
- Permits required: {atlas_result.get('permits_required')}
- Permit cost: {atlas_result.get('permit_cost_inr')} INR

Trip details:
- Number of people: {num_people}
- Budget per person: {budget_per_person_inr} INR
- Duration: {atlas_result.get('duration_days')} days

Calculate a realistic cost breakdown and return ONLY this JSON:

{{
    "destination": "{atlas_result.get('destination')}",
    "num_people": {num_people},
    "duration_days": {atlas_result.get('duration_days')},
    "budget_per_person_inr": {budget_per_person_inr},
    "cost_breakdown_per_person": {{
        "transport_to_base_inr": 2500,
        "local_transport_inr": 800,
        "accommodation_inr": 4000,
        "food_inr": 2000,
        "permits_inr": 200,
        "gear_rental_inr": 500,
        "guide_porter_inr": 1000,
        "miscellaneous_inr": 500
    }},
    "total_per_person_inr": 11500,
    "total_group_inr": 23000,
    "within_budget": true,
    "budget_remaining_per_person_inr": 3500,
    "transport_options": [
        {{
            "mode": "Bus",
            "route": "Delhi -> Manali",
            "cost_inr": 800,
            "duration_hours": 14
        }},
        {{
            "mode": "Train + Bus",
            "route": "Delhi -> Chandigarh -> Manali",
            "cost_inr": 600,
            "duration_hours": 16
        }}
    ],
    "money_saving_tips": [
        "tip 1",
        "tip 2",
        "tip 3"
    ],
    "budget_warning": null
}}

Use real INR costs. If total exceeds budget, set within_budget to false and add a warning in budget_warning.
"""

    result = ask("budget", prompt)
    result["agent"] = "budget"
    return result


if __name__ == "__main__":
    import json

    # Test with Atlas output
    mock_atlas = {
        "destination": "Hampta Pass",
        "state": "Himachal Pradesh",
        "duration_days": 5,
        "difficulty": "Moderate",
        "nearest_railhead": "Chandigarh Junction",
        "nearest_airport": "Bhuntar Airport",
        "distance_from_delhi_km": 520,
        "stay_options": [
            {"name": "Chika Campsite", "type": "Camping", "approx_cost_per_night_inr": 1000}
        ],
        "permits_required": False,
        "permit_cost_inr": 0
    }

    result = run(mock_atlas, num_people=2, budget_per_person_inr=15000)
    print(json.dumps(result, indent=2))