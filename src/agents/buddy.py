"""
Buddy - The Community Agent
Uses Llama 3.2 3B for lightweight matching
"""

from crewai import Agent, LLM
import os
from dotenv import load_dotenv
import sys
from pathlib import Path

# Setup paths
sys.path.insert(0, str(Path(__file__).parent.parent))
load_dotenv()

# Import tools
from tools.community_db import community_db_tool
from tools.web_search import web_search_tool

# Configure LLM - Using Llama 3.2 3B (lightweight!)
buddy_llm = LLM(
    model="huggingface/meta-llama/Meta-Llama-3-8B-Instruct",
    api_key=os.getenv("HUGGINGFACE_API_KEY")
)

# Create Buddy Agent
buddy = Agent(
    role="Travel Community Connector",
    goal="Match travelers with compatible groups",
    backstory="""Community manager connecting travelers. Match by destination, interests, 
    budget, dates. Use community database first. Be friendly and concise.""",
    tools=[community_db_tool, web_search_tool],
    llm=buddy_llm,
    verbose=True,
    allow_delegation=False
)


if __name__ == "__main__":
    print("=" * 60)
    print("👥 BUDDY - Community Agent")
    print("=" * 60)
    print(f"Role: {buddy.role}")
    print(f"Model: llama-3.2-3b-preview")
    print(f"Tools: {len(buddy.tools)}")
    print("=" * 60)