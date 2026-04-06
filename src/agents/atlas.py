"""
Atlas - Discovery Agent (Groq Optimized)
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
atlas_llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3,      # More focused
    max_tokens=800        # Limit output
)

atlas = Agent(
    role="Discovery Agent",
    goal="Find 3 destinations fast",
    backstory="Expert. Find destinations. Be brief.",  # Ultra short!
    tools=[TOOL],
    llm=atlas_llm,
    verbose=False,  # Less logging = fewer tokens!
    allow_delegation=False
)