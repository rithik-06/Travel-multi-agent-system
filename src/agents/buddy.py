from crewai import Agent, LLM
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our custom tools
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.community_db import community_db_tool
from tools.web_search import web_search_tool