"""
Shelter - Accommodation Agent (Groq Optimized)
"""

from crewai import Agent, LLM
import os
from dotenv import load_dotenv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
load_dotenv()

try:
    from tools.tavily_search import tavily_search_tool
    TOOL = tavily_search_tool
except:
    from tools.web_search import web_search_tool
    TOOL = web_search_tool

# Optimized Groq setup
shelter_llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3,
    max_tokens=800
)

shelter = Agent(
    role="Accommodation Agent",
    goal="Find 5 hotels fast",
    backstory="Expert. Find hotels. Be brief.",
    tools=[TOOL],
    llm=shelter_llm,
    verbose=False,
    allow_delegation=False
)