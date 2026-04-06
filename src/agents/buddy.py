"""
Buddy - Community Agent (Groq Optimized)
"""

from crewai import Agent, LLM
import os
from dotenv import load_dotenv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
load_dotenv()

from tools.community_db import community_db_tool

# Optimized Groq setup
buddy_llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3,
    max_tokens=600  # Buddy needs less
)

buddy = Agent(
    role="Community Agent",
    goal="Match travelers",
    backstory="Match travelers. Be brief.",
    tools=[community_db_tool],  # Only use DB, no web search!
    llm=buddy_llm,
    verbose=False,
    allow_delegation=False
)