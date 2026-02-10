"""
Main Travel Agent System
Coordinates all agents to create complete travel plans
"""

from crewai import Crew, Task, Process
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

# Import all our agents
from agents.atlas import atlas
from agents.shelter import shelter
from agents.buddy import buddy
from agents.captain import captain

# Import task creators
from tasks.discovery_tasks import create_discovery_task
from tasks.accommodation_tasks import create_accommodation_task
from tasks.community_tasks import create_community_task

# Import monitoring
from monitoring import metrics_tracker, cost_tracker


def create_travel_plan(user_request: str):
    """
    Create a complete travel plan using all agents
    
    Args:
        user_request: What the user wants
    
    Returns:
        All tasks for the crew
    """
    print("=" * 80)
    print("🌍 TRAVEL AGENT SYSTEM - COMPLETE PLANNING")
    print("=" * 80)
    print(f"\n📝 User Request: {user_request}\n")
    
    # Create tasks
    print("Creating tasks for the team...\n")
    
    # Task 1: Atlas finds destinations
    discovery_task = create_discovery_task(user_request)
    
    # Task 2: Shelter finds accommodations
    accommodation_task = Task(
        description=f"""
        Based on the destinations found by Atlas, find accommodations.
        
        Look at the destinations that Atlas recommended and for the TOP destination:
        1. Find 5-7 accommodation options
        2. Focus on budget-friendly options under $30/night
        3. Prioritize homestays and guesthouses
        4. Include key details: location, price, amenities, contact
        
        Make sure accommodations are convenient for the activities mentioned.
        """,
        agent=shelter,
        expected_output="List of 5-7 accommodation options",
        context=[discovery_task]
    )
    
    # Task 3: Buddy finds travel groups
    community_task = Task(
        description=f"""
        Based on: {user_request}
        
        Search for travel groups:
        1. Use community database
        2. Look for groups going to similar destinations
        3. Match based on interests
        4. Find 2-3 best matches
        """,
        agent=buddy,
        expected_output="List of 2-3 matching travel groups",
    )
    
    # Task 4: Captain synthesizes
    captain_task = Task(
        description=f"""
        Create a COMPLETE travel plan.
        
        You have destinations, accommodations, and travel groups.
        
        Create a plan with:
        1. Best destination and why
        2. Best accommodation with details
        3. Travel group option (if good match)
        4. Total budget estimate
        5. Best time to go
        6. Quick itinerary
        
        Make it exciting and actionable!
        """,
        agent=captain,
        expected_output="Complete cohesive travel plan",
        context=[discovery_task, accommodation_task, community_task]
    )
    
    return discovery_task, accommodation_task, community_task, captain_task


def run_travel_system(user_request: str):
    """Run the complete system"""
    
    # Create tasks
    tasks = create_travel_plan(user_request)
    
    # Create crew
    print("🚀 Assembling the crew...\n")
    
    crew = Crew(
        agents=[atlas, shelter, buddy, captain],
        tasks=list(tasks),
        process=Process.sequential,
        verbose=True
    )
    
    print("=" * 80)
    print("🎬 STARTING TRAVEL PLANNING")
    print("=" * 80)
    print("\nOrder:")
    print("1️⃣  Atlas → destinations")
    print("2️⃣  Shelter → accommodations")
    print("3️⃣  Buddy → groups")
    print("4️⃣  Captain → final plan")
    print("\n" + "=" * 80)
    print("⏳ This will take 2-3 minutes...\n")
    
    # Execute!
    result = crew.kickoff()
    
    # Results
    print("\n" + "=" * 80)
    print("✅ COMPLETE TRAVEL PLAN READY!")
    print("=" * 80)
    print()
    print(result)
    
    # Monitoring
    print("\n" + "=" * 80)
    metrics_tracker.print_summary()
    cost_tracker.print_summary()
    
    return result


if __name__ == "__main__":
    user_request = """
    I want to go trekking in the Himalayas. I love adventure and photography.
    My budget is $500 total. I'd love to join a group if possible.
    """
    
    result = run_travel_system(user_request)