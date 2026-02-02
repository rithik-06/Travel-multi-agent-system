
"""
Test script for monitoring modules
Run this to verify logging, cost tracking, and metrics are working
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from monitoring import (
    setup_logger,
    log_agent_action,
    log_api_call,
    cost_tracker,
    metrics_tracker
)

def test_monitoring():
    """Test all monitoring functionality"""
    print("🧪 Testing Travel Agent System Monitoring...\n")
    
    # Test 1: Logger
    print("1️⃣ Testing Logger...")
    logger = setup_logger("test")
    logger.info("✅ Logger initialized successfully")
    log_agent_action("TestAgent", "Running tests", {"module": "monitoring"})
    log_api_call("Groq", "chat/completions", tokens_used=150, cost=0.0001)
    print("✅ Logger test passed\n")
    
    # Test 2: Cost Tracker
    print("2️⃣ Testing Cost Tracker...")
    cost_tracker.track_usage(1000, "llama-3.1-70b-versatile", "DiscoveryAgent", "Test search")
    cost_tracker.track_usage(500, "llama-3.1-70b-versatile", "AccommodationAgent", "Test hotels")
    cost_tracker.print_summary()
    print("✅ Cost tracker test passed\n")
    
    # Test 3: Metrics Tracker
    print("3️⃣ Testing Metrics Tracker...")
    metrics_tracker.track_request("DiscoveryAgent", "Test search", 2.3, success=True)
    metrics_tracker.track_request("AccommodationAgent", "Test hotels", 1.8, success=True)
    metrics_tracker.track_request("TestAgent", "Test failure", 0.5, success=False, error="Simulated error")
    metrics_tracker.print_summary()
    print("✅ Metrics tracker test passed\n")
    
    # Test 4: Save data
    print("4️⃣ Testing Data Persistence...")
    cost_tracker.save_session()
    metrics_tracker.save_metrics()
    print("✅ Data persistence test passed\n")
    
    print("=" * 60)
    print("🎉 ALL TESTS PASSED!")
    print("=" * 60)
    print("\nMonitoring system is ready to use!")
    print("Check the 'logs/' directory for output files.")

if __name__ == "__main__":
    test_monitoring()