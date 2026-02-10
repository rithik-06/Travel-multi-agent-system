"""
Monitoring module for Travel Agent System
Provides logging, cost tracking, and performance metrics
"""

from .logger import (
    setup_logger,
    log_agent_action,
    log_api_call,
    log_error,
    default_logger
)

from .costs import (
    CostTracker,
    cost_tracker,
    COST_PER_MILLION_TOKENS
)

from .metrics import (
    MetricsTracker,
    metrics_tracker,
    track_time
)

__all__ = [
    # Logger
    'setup_logger',
    'log_agent_action',
    'log_api_call',
    'log_error',
    'default_logger',
    
    # Costs
    'CostTracker',
    'cost_tracker',
    'COST_PER_MILLION_TOKENS',
    
    # Metrics
    'MetricsTracker',
    'metrics_tracker',
    'track_time',
]