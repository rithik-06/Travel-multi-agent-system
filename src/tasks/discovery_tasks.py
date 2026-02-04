"""
Tasks for Atlas - The Discovery Agent
Defines what work Atlas needs to do
"""

from crewai import Task

# Import our agents
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.atlas import atlas


def create_discovery_task(user_preferences: str) -> Task:
    """
    Create a task for Atlas to find destinations
    
    Args:
        user_preferences: What the user is looking for
        Example: "I want to go trekking in mountains, budget $500"
    
    Returns:
        A Task object for Atlas to execute
    """
    task = Task(
        description=f"""
        Based on these user preferences: {user_preferences}
        
        Your job:
        1. Understand what type of experience the user wants (adventure, relaxation, culture, etc.)
        2. Use the web search tool to find 3-5 perfect destinations
        3. For each destination, provide:
           - Name and location
           - Why it matches their mood/interests
           - Best time to visit
           - Estimated budget
           - What makes it special
        
        Be specific and enthusiastic! Help them get excited about the trip.
        """,
        agent=atlas,
        expected_output="A list of 3-5 recommended destinations with detailed information for each"
    )
    
    return task


if __name__ == "__main__":
    print("=" * 70)
    print("🎯 TESTING ATLAS WITH A REAL TASK")
    print("=" * 70)
    print()
    
    # Example user request
    user_request = "I want to go trekking in the Himalayas, I love adventure and have a budget of $500"
    
    print(f"User Request: {user_request}")
    print()
    print("Creating task for Atlas...")
    print()
    
    # Create the task
    discovery_task = create_discovery_task(user_request)
    
    print("Task created! Atlas will now:")
    print("1. Read the user preferences")
    print("2. Search the web for destinations")
    print("3. Analyze and recommend the best options")
    print()
    print("=" * 70)
    print("🚀 ATLAS IS WORKING... (This may take 30-60 seconds)")
    print("=" * 70)
    print()
    
    # Execute the task!
    result = discovery_task.execute()
    
    print()
    print("=" * 70)
    print("✅ ATLAS COMPLETED THE TASK!")
    print("=" * 70)
    print()
    print(result)