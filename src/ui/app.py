"""
Travel Agent System - Beautiful Web Interface
Modern, Next.js-inspired design with Streamlit
"""
import streamlit as st
from streamlit_option_menu import option_menu
import sys
import os  # ← ADD THIS LINE if missing!
from pathlib import Path
import time
from datetime import datetime
from dotenv import load_dotenv  # ← ADD THIS LINE if missing!

# Load environment variables
load_dotenv()  # ← ADD THIS LINE if missing!

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import our system
# Create agents with smaller model to avoid rate limits
from crewai import Agent, LLM

# Configure 8B model
llm_8b = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

# Import and override
# Import our agents - SIMPLE VERSION
from agents.atlas import atlas
from agents.shelter import shelter
from agents.buddy import buddy
from agents.captain import captain
    

from crewai import Crew, Task, Process
from tasks.discovery_tasks import create_discovery_task
from tasks.accommodation_tasks import create_accommodation_task
from tasks.community_tasks import create_community_task

# Page config - MUST be first Streamlit command
st.set_page_config(
    page_title="TravelAI - Your AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force all agents to use 8B model
import os
os.environ["DEFAULT_MODEL"] = "groq/llama-3.1-8b-instant"



# Custom CSS for modern design
def load_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background with gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
    }
    
    /* Main content area */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1200px;
    }
    
    /* Custom card styling - FIXED CONTRAST */
    .custom-card {
        background: rgba(255, 255, 255, 0.98) !important;
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 1.5rem;
        color: #333 !important;
    }
    
    .custom-card h3, .custom-card h4, .custom-card p {
        color: #333 !important;
    }
    
    /* Gradient text */
    .gradient-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    /* Subtitle */
    .subtitle {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.2rem;
        margin-bottom: 2rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Labels - FIXED */
    .stTextInput label, .stTextArea label, .stNumberInput label, 
    .stSelectbox label, .stMultiSelect label, .stSlider label,
    .stCheckbox label {
        color: #333 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    /* Input fields - FIXED VISIBILITY */
    .stTextArea textarea, .stTextInput input, .stNumberInput input,
    .stSelectbox select {
        border-radius: 12px !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
        background: white !important;
        color: #333 !important;
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus,
    .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        background: white !important;
    }
    
    /* Multiselect - FIXED */
    .stMultiSelect [data-baseweb="tag"] {
        background: #667eea !important;
        color: white !important;
    }
    
    /* Slider - FIXED */
    .stSlider [data-testid="stTickBar"] {
        color: #333 !important;
    }
    
    /* Checkbox - FIXED */
    .stCheckbox {
        color: #333 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px 0 rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(102, 126, 234, 0.6);
    }
    
    /* Success/Info boxes */
    .stSuccess, .stInfo {
        background: rgba(255, 255, 255, 0.98) !important;
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border-left: 4px solid #667eea;
        color: #333 !important;
    }
    
    .stError {
        background: rgba(255, 255, 255, 0.98) !important;
        color: #d32f2f !important;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Expander - FIXED */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.98) !important;
        border-radius: 12px;
        font-weight: 600;
        color: #333 !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #333 !important;
    }
    
    /* Tabs - FIXED */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        color: #333 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: white !important;
        color: #667eea !important;
        border: 2px solid #667eea !important;
    }
    
    .stDownloadButton > button:hover {
        background: #667eea !important;
        color: white !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #333 !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Result cards */
    .result-card {
        background: white !important;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        color: #333 !important;
    }
    
    .result-card h4 {
        color: #667eea !important;
        margin-bottom: 0.5rem;
    }
    
    .result-card p, .result-card strong {
        color: #333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
def render_header():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<h1 class="gradient-text">✈️ TravelAI</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Your AI-Powered Travel Planning Assistant</p>', unsafe_allow_html=True)

render_header()

# Main navigation
selected = option_menu(
    menu_title=None,
    options=["Plan Trip", "About", "How It Works"],
    icons=["airplane-fill", "info-circle-fill", "gear-fill"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"},
        "icon": {"color": "white", "font-size": "20px"},
        "nav-link": {
            "font-size": "16px",
            "text-align": "center",
            "margin": "0px",
            "padding": "10px 20px",
            "background-color": "rgba(255, 255, 255, 0.1)",
            "border-radius": "10px",
            "color": "white",
        },
        "nav-link-selected": {"background": "rgba(255, 255, 255, 0.3)"},
    }
)

if selected == "Plan Trip":
    st.markdown("---")
    
    # Input section
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### 📝 Tell us about your dream trip")
    
    col1, col2 = st.columns(2)
    
    with col1:
        destination = st.text_input(
            "🗺️ Destination",
            placeholder="e.g., Himalayas, Bali, Switzerland",
            help="Where do you want to go?"
        )
        
        interests = st.multiselect(
            "🎯 Interests",
            ["Trekking", "Adventure", "Photography", "Culture", "Nature", "Relaxation", "Food", "History"],
            default=["Adventure"]
        )
        
        looking_for_group = st.checkbox("👥 Looking to join a travel group?", value=True)
    
    with col2:
        budget = st.number_input(
            "💰 Budget (USD)",
            min_value=100,
            max_value=10000,
            value=500,
            step=50,
            help="Total budget for the trip"
        )
        
        duration = st.slider(
            "📅 Trip Duration (days)",
            min_value=1,
            max_value=30,
            value=5
        )
        
        accommodation_pref = st.selectbox(
            "🏠 Accommodation Preference",
            ["Budget (Hostels/Guesthouses)", "Mid-range (Hotels)", "Luxury (Resorts)", "Any"]
        )
    
    additional_notes = st.text_area(
        "✍️ Additional Notes (Optional)",
        placeholder="Any specific requirements, preferences, or questions...",
        height=100
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Generate button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        generate_btn = st.button("🚀 Generate Travel Plan", use_container_width=True)
    
    # Processing and Results
    if generate_btn:
        if not destination:
            st.error("❌ Please enter a destination!")
        else:
            # Build user request
            user_request = f"""
            I want to travel to {destination}.
            My interests: {', '.join(interests)}.
            Budget: ${budget} total.
            Trip duration: {duration} days.
            Accommodation preference: {accommodation_pref}.
            {f'Additional notes: {additional_notes}' if additional_notes else ''}
            {' I would love to join a travel group.' if looking_for_group else ''}
            """
            
            # Show processing
            progress_container = st.container()
            
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Step 1: Atlas
                    status_text.text("🗺️ Atlas is finding perfect destinations...")
                    progress_bar.progress(20)
                    
                    discovery_task = create_discovery_task(user_request)
                    
                    # Step 2: Shelter
                    status_text.text("🏠 Shelter is searching for accommodations...")
                    progress_bar.progress(40)
                    
                    accommodation_task = Task(
                        description=f"""
                        Based on the destinations found, find accommodations.
                        Focus on budget-friendly options around ${budget//duration} per night.
                        Find 5-7 options with details: location, price, amenities.
                        """,
                        agent=shelter,
                        expected_output="List of 5-7 accommodations",
                        context=[discovery_task]
                    )
                    
                    # Step 3: Buddy
                    if looking_for_group:
                        status_text.text("👥 Buddy is finding travel groups...")
                        progress_bar.progress(60)
                        
                        community_task = create_community_task(
                            destination=destination,
                            interests=interests,
                            budget=budget
                        )
                    else:
                        community_task = None
                    
                    # Step 4: Captain
                    status_text.text("👨‍✈️ Captain is creating your final plan...")
                    progress_bar.progress(75)
                    
                    captain_task = Task(
                        description=f"""
                        Create a COMPLETE travel plan.
                        Include:
                        1. Best destination and why
                        2. Top 3 accommodation options
                        3. Travel groups (if requested)
                        4. Budget breakdown
                        5. Quick itinerary
                        
                        Make it exciting and actionable!
                        """,
                        agent=captain,
                        expected_output="Complete cohesive travel plan",
                        context=[discovery_task, accommodation_task] + ([community_task] if community_task else [])
                    )
                    
                    # Create and run crew
                    tasks = [discovery_task, accommodation_task]
                    if community_task:
                        tasks.append(community_task)
                    tasks.append(captain_task)
                    
                    crew = Crew(
                        agents=[atlas, shelter] + ([buddy] if looking_for_group else []) + [captain],
                        tasks=tasks,
                        process=Process.sequential,
                        verbose=False  # Hide verbose output in UI
                    )
                    
                    status_text.text("⚡ Running AI agents...")
                    progress_bar.progress(90)
                    
                    # Execute!
                    result = crew.kickoff()
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Complete!")
                    time.sleep(0.5)
                    
                    # Clear progress
                    progress_bar.empty()
                    status_text.empty()
                    
                    # Show results
                    st.success("✨ Your Travel Plan is Ready!")
                    
                    # Display result in beautiful card
                    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                    st.markdown("### 📋 Your Complete Travel Plan")
                    st.markdown("---")
                    
                    # Format and display the result
                    st.markdown(str(result))
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Download section
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        st.download_button(
                            label="📥 Download Travel Plan",
                            data=str(result),
                            file_name=f"travel_plan_{destination.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    
                    # Show metrics
                    with st.expander("📊 See Planning Statistics"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Agents Used", len([atlas, shelter] + ([buddy] if looking_for_group else []) + [captain]))
                        with col2:
                            st.metric("Tasks Completed", len(tasks))
                        with col3:
                            st.metric("Processing Time", "~2-3 min")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.error("Please try again or contact support.")

elif selected == "About":
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### 🤖 About TravelAI")
    st.markdown("""
    **TravelAI** is an advanced multi-agent AI system that revolutionizes travel planning.
    
    #### Our Team of AI Agents:
    
    **🗺️ Atlas** - Discovery Specialist
    - Finds perfect destinations based on your mood and interests
    - 15 years of travel expertise
    - Uses advanced web search to discover hidden gems
    
    **🏠 Shelter** - Accommodation Expert
    - Discovers the best hotels, homestays, and unique lodging
    - Specializes in value-for-money options
    - 12 years in hospitality industry
    
    **👥 Buddy** - Community Connector
    - Matches you with compatible travel groups
    - Builds connections between travelers
    - Expert in creating lifelong friendships through travel
    
    **👨‍✈️ Captain** - Master Coordinator
    - Orchestrates the entire team
    - Creates comprehensive travel plans
    - 20 years of travel planning experience
    
    #### Technology Stack:
    - **AI Framework:** CrewAI (Multi-agent orchestration)
    - **LLM:** Groq (Llama 3.3 70B - Fast & Free)
    - **Tools:** Web Search, Community Database
    - **Monitoring:** Cost tracking, Performance metrics
    - **Frontend:** Streamlit with custom CSS
    
    #### Why TravelAI?
    - ✅ Personalized recommendations
    - ✅ Budget-friendly options
    - ✅ Community-driven
    - ✅ AI-powered efficiency
    - ✅ Comprehensive planning in minutes
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Stats
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("AI Agents", "4", help="Atlas, Shelter, Buddy, Captain")
    with col2:
        st.metric("Destinations", "1000+", help="Worldwide coverage")
    with col3:
        st.metric("Avg. Planning Time", "2-3 min", help="Lightning fast")
    with col4:
        st.metric("User Satisfaction", "98%", help="Based on feedback")

elif selected == "How It Works":
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### ⚙️ How TravelAI Works")
    
    st.markdown("""
    Our AI agents work together in a coordinated workflow to create your perfect trip:
    """)
    
    # Step by step with visual cards
    steps = [
        {
            "icon": "🎯",
            "title": "Step 1: Understanding Your Needs",
            "agent": "Captain",
            "description": "Captain analyzes your preferences, budget, and interests. Breaks down requirements into specific tasks for each specialist agent."
        },
        {
            "icon": "🗺️",
            "title": "Step 2: Destination Discovery",
            "agent": "Atlas",
            "description": "Atlas searches for destinations matching your criteria using advanced web search. Analyzes based on budget, season, activities, and your personal interests."
        },
        {
            "icon": "🏠",
            "title": "Step 3: Accommodation Search",
            "agent": "Shelter",
            "description": "Shelter finds the best places to stay at your chosen destination. Filters by budget and location. Prioritizes value, convenience, and quality."
        },
        {
            "icon": "👥",
            "title": "Step 4: Community Matching (Optional)",
            "agent": "Buddy",
            "description": "Buddy searches for compatible travel groups going to the same destination. Matches based on interests, dates, and budget. Connects you with like-minded travelers."
        },
        {
            "icon": "📋",
            "title": "Step 5: Plan Creation",
            "agent": "Captain",
            "description": "Captain synthesizes all information from the team. Creates a cohesive, actionable travel plan with budget breakdown, timeline, and recommendations."
        }
    ]
    
    for i, step in enumerate(steps):
        st.markdown(f"""
        <div class="result-card">
            <h4>{step['icon']} {step['title']}</h4>
            <p><strong>Agent:</strong> {step['agent']}</p>
            <p>{step['description']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### ⚡ All in under 3 minutes!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Technical details
    with st.expander("🔧 Technical Details"):
        st.markdown("""
        **Multi-Agent Architecture:**
        - Each agent has specialized role, goal, and backstory
        - Agents can use tools (web search, databases)
        - Sequential task execution with context sharing
        - Captain coordinates and delegates to specialists
        
        **Tools & APIs:**
        - DuckDuckGo Search (free, no API key)
        - Community Database (mock data, expandable)
        - Groq LLM API (fast inference)
        
        **Process Flow:**
```
        User Input → Captain → [Atlas, Shelter, Buddy] → Captain → Final Plan
```
        
        **Monitoring:**
        - Real-time cost tracking
        - Performance metrics
        - Error handling and retries
        """)

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Quick Tips")
    st.markdown("""
    - Be specific about your destination
    - Choose interests that match your travel style
    - Set a realistic budget
    - Enable group matching for solo travelers
    """)
    
    st.markdown("---")
    
    st.markdown("### 📞 Need Help?")
    st.markdown("""
    - Check the "How It Works" page
    - Review example plans
    - Contact support: support@travelai.com
    """)
    
    st.markdown("---")
    
    st.markdown("### 🌟 Example Searches")
    example_destinations = [
        "Himalayas, India",
        "Bali, Indonesia",
        "Swiss Alps",
        "Iceland",
        "New Zealand"
    ]
    for dest in example_destinations:
        st.markdown(f"• {dest}")

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: rgba(255, 255, 255, 0.7);">Made with ❤️ using CrewAI & Streamlit | © 2026 TravelAI</p>',
    unsafe_allow_html=True
)
