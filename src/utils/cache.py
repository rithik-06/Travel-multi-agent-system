"""
Smart caching system to reduce API calls
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

# Cache settings
CACHE_DIR = Path(__file__).parent.parent.parent / "cache"
CACHE_DIR.mkdir(exist_ok=True)
CACHE_DURATION_DAYS = 7  # Cache results for 1 week


def normalize_request(user_request: str) -> str:
    """Normalize user request for consistent caching"""
    # Convert to lowercase, remove extra spaces
    normalized = user_request.lower().strip()
    # Remove numbers (budget/dates change but similar requests)
    import re
    normalized = re.sub(r'\d+', 'X', normalized)
    return normalized


def get_cache_key(user_request: str) -> str:
    """Generate cache key from user request"""
    normalized = normalize_request(user_request)
    return hashlib.md5(normalized.encode()).hexdigest()[:16]


def get_cached_result(user_request: str) -> dict:
    """
    Try to get cached result
    
    Returns:
        dict with 'found' (bool) and 'result' (str if found)
    """
    cache_key = get_cache_key(user_request)
    cache_file = CACHE_DIR / f"{cache_key}.json"
    
    if not cache_file.exists():
        return {"found": False}
    
    try:
        with open(cache_file, 'r') as f:
            cached_data = json.load(f)
        
        # Check if cache is still fresh
        cached_time = datetime.fromisoformat(cached_data['timestamp'])
        age = datetime.now() - cached_time
        
        if age > timedelta(days=CACHE_DURATION_DAYS):
            # Cache expired
            cache_file.unlink()  # Delete old cache
            return {"found": False}
        
        return {
            "found": True,
            "result": cached_data['result'],
            "cached_at": cached_data['timestamp'],
            "age_hours": int(age.total_seconds() / 3600)
        }
    
    except Exception as e:
        print(f"Cache read error: {e}")
        return {"found": False}


def save_to_cache(user_request: str, result: str):
    """Save result to cache"""
    cache_key = get_cache_key(user_request)
    cache_file = CACHE_DIR / f"{cache_key}.json"
    
    try:
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'request': user_request[:500],  # Store first 500 chars
            'result': str(result)
        }
        
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)
        
        print(f"✅ Cached result: {cache_key}")
    except Exception as e:
        print(f"Cache write error: {e}")


def clear_old_cache():
    """Clear cache files older than CACHE_DURATION_DAYS"""
    cleared = 0
    for cache_file in CACHE_DIR.glob("*.json"):
        try:
            with open(cache_file, 'r') as f:
                cached_data = json.load(f)
            
            cached_time = datetime.fromisoformat(cached_data['timestamp'])
            age = datetime.now() - cached_time
            
            if age > timedelta(days=CACHE_DURATION_DAYS):
                cache_file.unlink()
                cleared += 1
        except:
            pass
    
    if cleared > 0:
        print(f"🧹 Cleared {cleared} old cache files")


if __name__ == "__main__":
    # Test caching
    test_request = "I want to go trekking in Himalayas, budget $500"
    
    # Save test
    save_to_cache(test_request, "Test travel plan result")
    
    # Retrieve test
    cached = get_cached_result(test_request)
    print("Cache test:", cached)
    
    # Clear old
    clear_old_cache()