"""
TravelAI - Next-Gen Travel Planning System
Beautiful AI-powered travel planner with multi-agent coordination
"""

import streamlit as st
from streamlit_option_menu import option_menu
import sys
import os
from pathlib import Path
import time
from datetime import datetime
from dotenv import load_dotenv
import re

# Disable telemetry
os.environ["CREWAI_TELEMETRY_ENABLED"] = "false"
os.environ["OTEL_SDK_DISABLED"] = "true"

# Load environment
load_dotenv()

# Add to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import components
from agents.atlas import atlas
from agents.shelter import shelter
from agents.buddy import buddy
from agents.captain import captain
from crewai import Crew, Task, Process
from tasks.discovery_tasks import create_discovery_task
from tasks.accommodation_tasks import create_accommodation_task
from tasks.community_tasks import create_community_task

# Cache utilities
try:
    from utils.cache import get_cached_result, save_to_cache, clear_old_cache
    CACHE_AVAILABLE = True
    clear_old_cache()
except:
    CACHE_AVAILABLE = False

# Page config
st.set_page_config(
    page_title="TravelAI - Smart Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Stunning CSS
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Animated gradient background */
    .stApp {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main .block-container {
        padding: 1.5rem 2rem;
        max-width: 1400px;
    }
    
    /* Glass cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin: 1rem 0;
    }
    
    /* Hero section */
    .hero {
        text-align: center;
        padding: 2rem 0;
    }
    
    .hero h1 {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        text-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .hero p {
        font-size: 1.5rem;
        color: white;
        margin-top: 0.5rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        font-weight: 300;
    }
    
    /* Labels and inputs */
    label {
        color: #2d3436 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    .stTextInput input, .stNumberInput input, .stSelectbox select, .stTextArea textarea {
        border-radius: 12px !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        background: white !important;
        color: #2d3436 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus,
    .stSelectbox select:focus, .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15) !important;
        transform: translateY(-2px);
    }
    
    /* Multiselect */
    .stMultiSelect span[data-baseweb="tag"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border-radius: 20px !important;
        font-weight: 500;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 1rem 2.5rem !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.4) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: white !important;
        color: #667eea !important;
        border: 3px solid #667eea !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
    }
    
    .stDownloadButton > button:hover {
        background: #667eea !important;
        color: white !important;
    }
    
    /* Messages */
    .stSuccess {
        background: linear-gradient(135deg, #00b894, #00cec9) !important;
        color: white !important;
        border-radius: 15px !important;
        border: none !important;
        font-weight: 500;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #74b9ff, #0984e3) !important;
        color: white !important;
        border-radius: 15px !important;
        border: none !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #ffeaa7, #fdcb6e) !important;
        color: #2d3436 !important;
        border-radius: 15px !important;
        border: none !important;
        font-weight: 500;
    }
    
    .stError {
        background: linear-gradient(135deg, #ff7675, #d63031) !important;
        color: white !important;
        border-radius: 15px !important;
        border: none !important;
        font-weight: 500;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb) !important;
        border-radius: 10px;
        height: 15px !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        color: #2d3436 !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(102, 126, 234, 0.95), rgba(118, 75, 162, 0.95));
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Hide branding */
    #MainMenu, footer {visibility: hidden;}
    
    /* Result card */
    .result-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.3rem;
    }
    
    .badge-success {
        background: linear-gradient(135deg, #00b894, #00cec9);
        color: white;
    }
    
    .badge-info {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        color: white;
    }
    
    .badge-warning {
        background: linear-gradient(135deg, #ffeaa7, #fdcb6e);
        color: #2d3436;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .glass-card {
        animation: fadeInUp 0.6s ease;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# Header
st.markdown("""
<div class="hero">
    <h1>✈️ TravelAI</h1>
    <p>Your AI-Powered Travel Planning Assistant</p>
</div>
""", unsafe_allow_html=True)

# Navigation
selected = option_menu(
    menu_title=None,
    options=["🚀 Plan Trip", "ℹ️ About", "⚙️ How It Works"],
    icons=["rocket-takeoff", "info-circle", "gear"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0", "background": "transparent"},
        "icon": {"color": "white", "font-size": "20px"},
        "nav-link": {
            "font-size": "16px",
            "text-align": "center",
            "margin": "0 10px",
            "padding": "12px 30px",
            "background": "rgba(255, 255, 255, 0.2)",
            "border-radius": "15px",
            "color": "white",
            "font-weight": "600",
            "border": "2px solid rgba(255, 255, 255, 0.3)",
            "transition": "all 0.3s ease",
        },
        "nav-link-selected": {
            "background": "linear-gradient(135deg, #667eea, #764ba2)",
            "border": "2px solid rgba(255, 255, 255, 0.5)",
            "box-shadow": "0 5px 20px rgba(0, 0, 0, 0.3)",
            "transform": "translateY(-2px)",
        },
    }
)

st.markdown("<br>", unsafe_allow_html=True)

# Main Content
if selected == "🚀 Plan Trip":
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🌍 Design Your Perfect Adventure")
    st.markdown("Tell us your dream destination and let our AI agents craft your personalized travel plan!")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Form
    col1, col2, col3 = st.columns(3)
    
    with col1:
        destination = st.text_input(
            "🗺️ Destination",
            placeholder="Himalayas, Bali, Paris...",
            help="Where do you want to explore?"
        )
        
        budget = st.number_input(
            "💰 Budget (USD)",
            min_value=100,
            max_value=50000,
            value=500,
            step=100
        )
    
    with col2:
        interests = st.multiselect(
            "🎯 Your Interests",
            ["🥾 Trekking", "🎢 Adventure", "📸 Photography", "🏛️ Culture", 
             "🌲 Nature", "🧘 Wellness", "🍜 Food", "🏖️ Beach"],
            default=["🎢 Adventure"]
        )
        
        duration = st.slider(
            "📅 Duration (days)",
            1, 30, 5
        )
    
    with col3:
        accommodation = st.selectbox(
            "🏠 Accommodation",
            ["💵 Budget", "🏨 Standard", "⭐ Luxury", "🎯 Any"]
        )
        
        looking_for_group = st.checkbox("👥 Join travel group?", value=False)
    
    with st.expander("✍️ Additional Notes (Optional)"):
        notes = st.text_area(
            "Special requests",
            placeholder="Dietary restrictions, accessibility needs, etc.",
            height=80,
            label_visibility="collapsed"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Generate button
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🚀 GENERATE PLAN", use_container_width=True):
            
            if not destination:
                st.error("❌ Please enter a destination!")
            else:
                # Build request
                user_request = f"""
                Destination: {destination}
                Interests: {', '.join(interests)}
                Budget: ${budget}
                Duration: {duration} days
                Accommodation: {accommodation}
                {f'Notes: {notes}' if notes else ''}
                {' Looking for group.' if looking_for_group else ''}
                """
                
                # Check cache
                cache_hit = False
                result = None
                
                if CACHE_AVAILABLE:
                    cache_result = get_cached_result(user_request)
                    if cache_result["found"]:
                        cache_hit = True
                        st.success(f"⚡ Found recent plan ({cache_result['age_hours']}h old)! Instant result!")
                        result = cache_result["result"]
                
                if not cache_hit:
                    # Progress
                    status = st.empty()
                    progress = st.empty()
                    
                    try:
                        # Tasks
                        status.info("🗺️ Atlas discovering destinations...")
                        progress.progress(25)
                        
                        discovery_task = create_discovery_task(user_request)
                        
                        status.info("🏠 Shelter finding accommodations...")
                        progress.progress(50)
                        
                        accommodation_task = Task(
                            description=f"Find 5 accommodations. Budget: ${budget//duration}/night. Type: {accommodation}.",
                            agent=shelter,
                            expected_output="5 options",
                            context=[discovery_task]
                        )
                        
                        tasks = [discovery_task, accommodation_task]
                        agents_list = [atlas, shelter]
                        
                        if looking_for_group:
                            status.info("👥 Buddy matching groups...")
                            progress.progress(65)
                            community_task = create_community_task(
                                destination=destination,
                                interests=[i.replace('🥾 ','').replace('🎢 ','').replace('📸 ','').replace('🏛️ ','').replace('🌲 ','').replace('🧘 ','').replace('🍜 ','').replace('🏖️ ','') for i in interests],
                                budget=budget
                            )
                            tasks.append(community_task)
                            agents_list.append(buddy)
                        
                        status.info("👨‍✈️ Captain creating plan...")
                        progress.progress(80)
                        
                        captain_task = Task(
                            description="Create concise plan: destination, top 3 hotels, budget, 3-day itinerary. Under 500 words.",
                            agent=captain,
                            expected_output="Complete plan",
                            context=tasks
                        )
                        
                        tasks.append(captain_task)
                        agents_list.append(captain)
                        
                        crew = Crew(
                            agents=agents_list,
                            tasks=tasks,
                            process=Process.sequential,
                            verbose=False
                        )
                        
                        status.info("⚡ AI agents working...")
                        progress.progress(90)
                        
                        # Execute with retry
                        max_retries = 5
                        for attempt in range(max_retries):
                            try:
                                result = crew.kickoff()
                                if CACHE_AVAILABLE:
                                    save_to_cache(user_request, result)
                                break
                            except Exception as e:
                                if "rate_limit" in str(e).lower() and attempt < max_retries - 1:
                                    wait_time = 20
                                    status.warning(f"⏳ Rate limit. Waiting {wait_time}s... ({attempt+1}/{max_retries})")
                                    time.sleep(wait_time)
                                else:
                                    raise e
                        
                        progress.progress(100)
                        status.success("✅ Plan complete!")
                        time.sleep(1)
                        status.empty()
                        progress.empty()
                        
                    except Exception as e:
                        status.empty()
                        progress.empty()
                        st.error(f"❌ {str(e)}")
                        st.info("💡 Wait a moment and try again!")
                        st.stop()
                
                # Display result
                if result:
                    st.balloons()
                    
                    st.markdown('<div class="glass-card result-card">', unsafe_allow_html=True)
                    st.success("✨ Your Personalized Travel Plan is Ready!")
                    st.markdown("---")
                    st.markdown(str(result))
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Actions
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.download_button(
                            "📥 Download",
                            str(result),
                            f"TravelPlan_{destination.replace(' ','')}_{datetime.now().strftime('%Y%m%d')}.txt",
                            use_container_width=True
                        )
                    with col2:
                        if st.button("🔄 New Plan", use_container_width=True):
                            st.rerun()
                    with col3:
                        st.button("📤 Share", use_container_width=True, disabled=True)
                    
                    # Stats
                    with st.expander("📊 Planning Stats"):
                        c1, c2, c3, c4 = st.columns(4)
                        c1.metric("Agents", len(agents_list) if not cache_hit else 0)
                        c2.metric("Tasks", len(tasks) if not cache_hit else 0)
                        c3.metric("Time", "Instant" if cache_hit else "~2 min")
                        c4.metric("Status", "Cached" if cache_hit else "Fresh")

elif selected == "ℹ️ About":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🤖 Meet Our AI Team")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **🗺️ Atlas** - Discovery Agent
        - 15 years travel expertise
        - Finds hidden gems worldwide
        - Matches destinations to your mood
        
        **🏠 Shelter** - Accommodation Expert
        - 12 years hospitality experience
        - Value-for-money specialist
        - Unique lodging options
        """)
    
    with col2:
        st.markdown("""
        **👥 Buddy** - Community Connector
        - Traveler matchmaking expert
        - Builds meaningful connections
        - Compatible group finder
        
        **👨‍✈️ Captain** - Orchestrator
        - 20 years planning experience
        - Team coordinator
        - Creates cohesive plans
        """)
    
    st.markdown("---")
    st.markdown("### 💻 Tech Stack")
    
    st.markdown("""
    <div style='display: flex; gap: 1rem; flex-wrap: wrap;'>
        <span class='badge badge-info'>CrewAI</span>
        <span class='badge badge-info'>Groq API</span>
        <span class='badge badge-info'>Llama 3.1</span>
        <span class='badge badge-success'>Streamlit</span>
        <span class='badge badge-success'>Python</span>
        <span class='badge badge-warning'>Smart Caching</span>
        <span class='badge badge-warning'>MLOps</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("AI Agents", "4")
    col2.metric("Destinations", "1000+")
    col3.metric("Avg Speed", "2-3 min")
    cache_count = 0
    if CACHE_AVAILABLE:
        cache_dir = Path(__file__).parent.parent.parent / "cache"
        if cache_dir.exists():
            cache_count = len(list(cache_dir.glob("*.json")))
    col4.metric("Cached Plans", cache_count)
    st.markdown('</div>', unsafe_allow_html=True)

else:  # How It Works
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### ⚙️ How TravelAI Works")
    
    steps = [
        ("🎯", "Smart Cache Check", "Instant results if similar plan exists"),
        ("🗺️", "Destination Discovery", "Atlas finds perfect matches"),
        ("🏠", "Accommodation Search", "Shelter finds best stays"),
        ("👥", "Group Matching", "Buddy connects travelers"),
        ("📋", "Plan Creation", "Captain synthesizes everything")
    ]
    
    for icon, title, desc in steps:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(102,126,234,0.1), rgba(118,75,162,0.1)); 
                    border-left: 4px solid #667eea; border-radius: 12px; padding: 1.5rem; margin: 1rem 0;'>
            <h4 style='color: #667eea; margin: 0;'>{icon} {title}</h4>
            <p style='margin: 0.5rem 0 0; color: #2d3436;'>{desc}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### ⚡ Complete in under 3 minutes!")
    st.markdown('</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 💡 Tips")
    st.info("• Be specific about destination\n• Choose matching interests\n• Set realistic budget\n• Enable groups if solo")
    
    st.markdown("### 🌟 Examples")
    for ex in ["Himalayas", "Bali", "Swiss Alps", "Iceland"]:
        st.markdown(f"• {ex}")
    
    st.markdown("### ⚡ Status")
    st.success("✅ All systems ready")
    if CACHE_AVAILABLE:
        st.info("💾 Cache active")

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    '<p style="text-align: center; color: white; font-weight: 500; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">'
    'Made with ❤️ by Rithik | TravelAI © 2026'
    '</p>',
    unsafe_allow_html=True
)