"""
Community database tool for finding matching travel groups
Uses mock data (in real app, this would be a real database)
"""

from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


# Mock data for travelers looking for groups
MOCK_TRAVELERS = [
    {
        "id": "user_001",
        "name": "Adventure Squad",
        "destination": "Triund Trek",
        "dates": "2026-03-15 to 2026-03-18",
        "group_size": 4,
        "looking_for": 2,
        "interests": ["trekking", "photography", "camping"],
        "budget_per_person": 400,
        "contact": "adventuresquad@example.com"
    },
    {
        "id": "user_002",
        "name": "Mountain Wanderers",
        "destination": "Valley of Flowers",
        "dates": "2026-04-10 to 2026-04-15",
        "group_size": 3,
        "looking_for": 3,
        "interests": ["trekking", "nature", "photography"],
        "budget_per_person": 600,
        "contact": "wanderers@example.com"
    },
    {
        "id": "user_003",
        "name": "Himalayan Explorers",
        "destination": "Har Ki Dun Trek",
        "dates": "2026-03-20 to 2026-03-25",
        "group_size": 5,
        "looking_for": 1,
        "interests": ["trekking", "adventure", "culture"],
        "budget_per_person": 500,
        "contact": "explorers@example.com"
    },
    {
        "id": "user_004",
        "name": "Trek Buddies",
        "destination": "Kedarkantha Trek",
        "dates": "2026-02-20 to 2026-02-25",
        "group_size": 2,
        "looking_for": 4,
        "interests": ["trekking", "snow", "adventure"],
        "budget_per_person": 450,
        "contact": "buddies@example.com"
    },
    {
        "id": "user_005",
        "name": "Solo to Group",
        "destination": "Triund Trek",
        "dates": "2026-03-12 to 2026-03-15",
        "group_size": 1,
        "looking_for": 5,
        "interests": ["trekking", "making friends", "budget travel"],
        "budget_per_person": 300,
        "contact": "solo@example.com"
    },
    {
        "id": "user_006",
        "name": "Weekend Warriors",
        "destination": "Manali Adventure",
        "dates": "2026-03-08 to 2026-03-10",
        "group_size": 3,
        "looking_for": 3,
        "interests": ["adventure", "paragliding", "rafting"],
        "budget_per_person": 350,
        "contact": "warriors@example.com"
    }
]


class CommunitySearchInput(BaseModel):
    """Input for community database search"""
    query: str = Field(..., description="Search query - destination name, interest, or travel type")


class CommunityDatabaseTool(BaseTool):
    name: str = "Community Database"
    description: str = "Search for travel groups and companions. Use this to find groups going to similar destinations or with similar interests. Input should be a destination name or travel interest."
    args_schema: Type[BaseModel] = CommunitySearchInput
    
    def _run(self, query: str) -> str:
        """
        Search the community database for matching travel groups
        
        Args:
            query: Search query (destination, interest, or general search)
        
        Returns:
            Matching travel groups with details
        """
        try:
            query_lower = query.lower()
            matches = []
            
            # Search through all travelers
            for traveler in MOCK_TRAVELERS:
                # Check if query matches destination
                if query_lower in traveler['destination'].lower():
                    matches.append(traveler)
                    continue
                
                # Check if query matches any interest
                if any(query_lower in interest.lower() for interest in traveler['interests']):
                    matches.append(traveler)
                    continue
            
            # Remove duplicates (if any)
            seen_ids = set()
            unique_matches = []
            for match in matches:
                if match['id'] not in seen_ids:
                    seen_ids.add(match['id'])
                    unique_matches.append(match)
            
            if not unique_matches:
                return f"No matching travel groups found for '{query}'.\n\nTip: Try searching by destination name (e.g., 'Triund') or interest (e.g., 'trekking')."
            
            # Format results
            formatted_results = f"Found {len(unique_matches)} matching travel group(s) for '{query}':\n\n"
            
            for i, traveler in enumerate(unique_matches, 1):
                formatted_results += f"{i}. {traveler['name']}\n"
                formatted_results += f"   📍 Destination: {traveler['destination']}\n"
                formatted_results += f"   📅 Dates: {traveler['dates']}\n"
                formatted_results += f"   👥 Current group size: {traveler['group_size']} people\n"
                formatted_results += f"   ➕ Looking for: {traveler['looking_for']} more member(s)\n"
                formatted_results += f"   🎯 Interests: {', '.join(traveler['interests'])}\n"
                formatted_results += f"   💰 Budget per person: ${traveler['budget_per_person']}\n"
                formatted_results += f"   📧 Contact: {traveler['contact']}\n\n"
            
            return formatted_results
            
        except Exception as e:
            return f"Search failed: {str(e)}"


# Create instance
community_db_tool = CommunityDatabaseTool()


if __name__ == "__main__":
    # Test the tool
    print("Testing community database tool...\n")
    
    print("Test 1: Search by destination")
    result = community_db_tool._run("Triund")
    print(result)
    
    print("\n" + "="*60 + "\n")
    
    print("Test 2: Search by interest")
    result = community_db_tool._run("photography")
    print(result)