"""
Configuration loader for C.L.A.I.R.E
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any


def load_config() -> Dict[str, Any]:
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent.parent.parent / "config.yaml"
    
    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}\n"
            "Please copy config.example.yaml to config.yaml"
        )
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # Load environment variables if present
    if 'ai' in config:
        if os.getenv('OPENAI_API_KEY'):
            config['ai']['openai_api_key'] = os.getenv('OPENAI_API_KEY')
        if os.getenv('ANTHROPIC_API_KEY'):
            config['ai']['anthropic_api_key'] = os.getenv('ANTHROPIC_API_KEY')
    
    return config


def get_config_value(config: Dict, path: str, default=None):
    """
    Get nested configuration value using dot notation
    Example: get_config_value(config, 'ai.provider', 'openai')
    """
    keys = path.split('.')
    value = config
    
    try:
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return default
