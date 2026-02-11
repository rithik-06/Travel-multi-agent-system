

"""
Performance metrics tracking
"""

from datetime import datetime


class MetricsTracker:
    """Track performance metrics"""
    
    def __init__(self):
        self.metrics = {
            "session_start": datetime.now().isoformat(),
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
        }
    
    def track_request(self, agent_name: str, task: str, response_time: float, 
                     success: bool = True, error: str = None):
        """Track a request"""
        self.metrics["total_requests"] += 1
        if success:
            self.metrics["successful_requests"] += 1
        else:
            self.metrics["failed_requests"] += 1
    
    def print_summary(self):
        """Print metrics summary"""
        print("\n" + "="*60)
        print("📊 PERFORMANCE METRICS")
        print("="*60)
        print(f"Total Requests: {self.metrics['total_requests']}")
        print(f"Successful: {self.metrics['successful_requests']} ✅")
        print(f"Failed: {self.metrics['failed_requests']} ❌")
        
        if self.metrics['total_requests'] > 0:
            success_rate = (self.metrics['successful_requests'] / self.metrics['total_requests']) * 100
            print(f"Success Rate: {success_rate:.1f}%")
        
        print("="*60 + "\n")


def track_time(agent_name: str, task: str = ""):
    """Decorator for tracking time"""
    def decorator(func):
        return func
    return decorator


metrics_tracker = MetricsTracker()