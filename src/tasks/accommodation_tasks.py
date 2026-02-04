"""
Tasks for Shelter - The Accommodation Agent
Defines accommodation finding tasks
"""

from crewai import Task, Crew

# Import our agents
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.shelter import shelter


def create_accommodation_task(destination: str, budget: str, preferences: str = "") -> Task:
    """
    Create a task for Shelter to find accommodations
    
    Args:
        destination: Where to find accommodation (e.g., "Manali, India")
        budget: Budget range (e.g., "$20-30 per night")
        preferences: Any special preferences (e.g., "close to trekking routes")
    
    Returns:
        A Task object for Shelter to execute
    """
    pref_text = f" Preferences: {preferences}" if preferences else ""
    
    task = Task(
        description=f"""
        Find the best accommodations in {destination} within budget of {budget}.{pref_text}
        
        Your job:
        1. Use web search to find hotels, homestays, guesthouses in {destination}
        2. Focus on options within the budget range of {budget}
        3. For each accommodation (find 5-7 options), provide:
           - Name and type (hotel/homestay/guesthouse)
           - Location within {destination}
           - Price range per night
           - Key amenities (WiFi, breakfast, parking, etc.)
           - Why it's a good choice
           - Booking contact or website
        
        Prioritize value for money, good reviews, and convenient locations.
        """,
        agent=shelter,
        expected_output="A list of 5-7 accommodation recommendations with full details"
    )
    
    return task


if __name__ == "__main__":
    print("=" * 70)
    print("🎯 TESTING SHELTER WITH A REAL TASK")
    print("=" * 70)
    print()
    
    # Example accommodation request
    destination = "Manali, Himachal Pradesh"
    budget = "$20-30 per night"
    preferences = "close to trekking routes, homestays preferred"
    
    print(f"Destination: {destination}")
    print(f"Budget: {budget}")
    print(f"Preferences: {preferences}")
    print()
    print("Creating task for Shelter...")
    print()
    
    # Create the task
    accommodation_task = create_accommodation_task(destination, budget, preferences)
    
    # Create a crew with Shelter and the task
    crew = Crew(
        agents=[shelter],
        tasks=[accommodation_task],
        verbose=True
    )
    
    print("Task created! Shelter will now:")
    print("1. Search for accommodations in Manali")
    print("2. Filter by budget ($20-30/night)")
    print("3. Find homestays near trekking routes")
    print()
    print("=" * 70)
    print("🚀 SHELTER IS WORKING... (This may take 30-60 seconds)")
    print("=" * 70)
    print()
    
    # Execute the crew!
    result = crew.kickoff()
    
    print()
    print("=" * 70)
    print("✅ SHELTER COMPLETED THE TASK!")
    print("=" * 70)
    print()
    print(result)