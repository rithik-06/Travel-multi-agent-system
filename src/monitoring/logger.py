"""
Logging configuration for the Travel Agent System
"""

import logging
from datetime import datetime
from pathlib import Path

# Create logs directory
LOGS_DIR = Path(__file__).parent.parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Log file
LOG_FILE = LOGS_DIR / f"travel_agent_{datetime.now().strftime('%Y%m%d')}.log"


def setup_logger(name: str = "travel_agent", level: str = "INFO"):
    """Setup a logger"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))
    
    if logger.handlers:
        return logger
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    
    # File handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


def log_agent_action(agent_name: str, action: str, details: dict = None):
    """Log agent actions"""
    logger = setup_logger()
    details_str = f" | Details: {details}" if details else ""
    logger.info(f"[AGENT: {agent_name}] {action}{details_str}")


def log_api_call(api_name: str, endpoint: str, tokens_used: int = None, cost: float = None):
    """Log API calls"""
    logger = setup_logger()
    metrics = []
    if tokens_used:
        metrics.append(f"Tokens: {tokens_used}")
    if cost:
        metrics.append(f"Cost: ${cost:.4f}")
    
    metrics_str = " | ".join(metrics) if metrics else ""
    logger.info(f"[API: {api_name}] {endpoint} {metrics_str}")


def log_error(component: str, error: Exception, context: dict = None):
    """Log errors"""
    logger = setup_logger()
    context_str = f" | Context: {context}" if context else ""
    logger.error(f"[ERROR: {component}] {str(error)}{context_str}", exc_info=True)


default_logger = setup_logger()