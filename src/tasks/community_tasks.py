"""
Tasks for Buddy - The Community Agent
Defines tasks for finding and matching travel groups
"""

from crewai import Task, Crew

# Import our agents
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.buddy import buddy

def create_community_task(destination: str, interests: list = None, budget: int = None) -> Task:
    """
    Create a task for Buddy to find matching travel groups
    
    Args:
        destination: Where the user wants to go (e.g., "Triund Trek")
        interests: List of interests (e.g., ["trekking", "photography"])
        budget: Budget per person (e.g., 500)
    
    Returns:
        A Task object for Buddy to execute
    """
    # Build a description of what the user is looking for
    interests_text = f" with interests in {', '.join(interests)}" if interests else ""
    budget_text = f" and a budget around ${budget}" if budget else ""
    
    task = Task(
        description=f"""
        The user wants to travel to {destination}{interests_text}{budget_text}.
        They are looking for travel groups or companions to join.
        
        Your job:
        1. Use the community database tool to search for groups going to {destination}
        2. If destination search doesn't find matches, search by interests: {interests or 'adventure, trekking'}
        3. For each matching group found, analyze:
           - How well the destination matches
           - If interests align
           - If budget is compatible
           - If dates are reasonable
        4. Present the top 3-5 best matches with:
           - Group name and size
           - Destination and dates
           - Why this group is a good match for the user
           - How to contact them
           - Any compatibility notes (budget difference, interest alignment, etc.)
        
        Be enthusiastic and encouraging! Help the user feel excited about joining a group.
        If no perfect matches exist, suggest the closest alternatives and explain why.
        """,
        agent=buddy,
        expected_output="A list of 3-5 matching travel groups with detailed compatibility analysis and contact information"
    )
    
    return task

if __name__ == "__main__":
    print("=" * 70)
    print("🎯 TESTING BUDDY WITH A REAL TASK")
    print("=" * 70)
    print()
    
    # Example: User wants to join a trekking group
    destination = "Triund Trek"
    interests = ["trekking", "photography", "camping"]
    budget = 400
    
    print(f"User wants to travel to: {destination}")
    print(f"Interests: {', '.join(interests)}")
    print(f"Budget: ${budget}")
    print()
    print("Creating task for Buddy...")
    print()
    
    # Create the task
    community_task = create_community_task(destination, interests, budget)
    
    # Create a crew with Buddy and the task
    crew = Crew(
        agents=[buddy],
        tasks=[community_task],
        verbose=True
    )
    
    print("Task created! Buddy will now:")
    print("1. Search community database for Triund Trek groups")
    print("2. Analyze compatibility with user's interests and budget")
    print("3. Present the best matching groups")
    print()
    print("=" * 70)
    print("🚀 BUDDY IS WORKING... (This may take 30-60 seconds)")
    print("=" * 70)
    print()
    
    # Execute the crew!
    result = crew.kickoff()
    
    print()
    print("=" * 70)
    print("✅ BUDDY COMPLETED THE TASK!")
    print("=" * 70)
    print()
    print(result)