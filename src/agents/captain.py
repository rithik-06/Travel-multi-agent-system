"""
Captain - Orchestrator (Groq Optimized)
"""

from crewai import Agent, LLM
import os
from dotenv import load_dotenv

load_dotenv()

# Use 70B for Captain (better quality, higher limit)
captain_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3,
    max_tokens=1000
)

captain = Agent(
    role="Coordinator",
    goal="Create plan",
    backstory="Synthesize. Max 400 words.",
    tools=[],
    llm=captain_llm,
    verbose=False,
    allow_delegation=False
)