"""Logging utilities for the voice agent system."""
import logging
from typing import Optional


def setup_logger(
    name: str, 
    level: int = logging.INFO,
    format_string: Optional[str] = None
) -> logging.Logger:
    """Set up a logger with the specified configuration."""
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configure logging
    logging.basicConfig(
        level=level,
        format=format_string,
        handlers=[logging.StreamHandler()]
    )
    
    logger = logging.getLogger(name)
    return logger


# Create a default logger for the voice agent
logger = setup_logger('voice_agent')