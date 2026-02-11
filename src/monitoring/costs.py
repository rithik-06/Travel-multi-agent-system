

"""
Cost tracking for API usage
"""

import json
from datetime import datetime
from pathlib import Path

COSTS_DIR = Path(__file__).parent.parent.parent / "logs"
COSTS_FILE = COSTS_DIR / "usage_costs.json"

COST_PER_MILLION_TOKENS = {
    "llama-3.3-70b-versatile": 0.59,
    "llama-3.1-8b-instant": 0.05,
}


class CostTracker:
    """Track API costs"""
    
    def __init__(self):
        self.session_costs = {
            "total_tokens": 0,
            "total_cost_usd": 0.0,
            "api_calls": 0,
            "timestamp": datetime.now().isoformat()
        }
    
    def track_usage(self, tokens_used: int, model: str = "llama-3.3-70b-versatile", 
                   agent_name: str = None, task: str = None):
        """Track token usage"""
        cost_per_token = COST_PER_MILLION_TOKENS.get(model, 0.5) / 1_000_000
        cost = tokens_used * cost_per_token
        
        self.session_costs["total_tokens"] += tokens_used
        self.session_costs["total_cost_usd"] += cost
        self.session_costs["api_calls"] += 1
        
        return cost
    
    def print_summary(self):
        """Print cost summary"""
        print("\n" + "="*60)
        print("💰 COST SUMMARY")
        print("="*60)
        print(f"Total Tokens: {self.session_costs['total_tokens']:,}")
        print(f"Total Cost: ${self.session_costs['total_cost_usd']:.4f}")
        print(f"API Calls: {self.session_costs['api_calls']}")
        print("="*60 + "\n")


cost_tracker = CostTracker()