"""Configuration management for the affiliate link tool."""

import os
import yaml
from typing import Dict, Any
from pathlib import Path


class Config:
    """Configuration manager with YAML and environment variable support."""
    
    def __init__(self, config_file: str = None):
        """
        Initialize configuration.
        
        Args:
            config_file: Path to YAML config file. If None, uses default.
        """
        self.config: Dict[str, Any] = self._load_config(config_file)
    
    def _load_config(self, config_file: str = None) -> Dict[str, Any]:
        """
        Load configuration from YAML file and environment variables.
        
        Args:
            config_file: Path to config file
            
        Returns:
            Configuration dictionary
        """
        # Start with defaults
        config = {
            "affiliate": {"id": "12345"},
            "llm": {"model": "mock", "type": "mock"},
            "output": {"suffix": "_linked"}
        }
        
        # Try to load from config file
        if config_file and Path(config_file).exists():
            with open(config_file, 'r') as f:
                file_config = yaml.safe_load(f)
                if file_config:
                    config = self._deep_merge(config, file_config)
        elif not config_file:
            # Try default config location
            default_config_path = Path(__file__).parent.parent / "config" / "default_config.yaml"
            if default_config_path.exists():
                with open(default_config_path, 'r') as f:
                    file_config = yaml.safe_load(f)
                    if file_config:
                        config = self._deep_merge(config, file_config)
        
        # Override with environment variables
        if os.getenv("AFFILIATE_ID"):
            config["affiliate"]["id"] = os.getenv("AFFILIATE_ID")
        if os.getenv("LLM_MODEL"):
            config["llm"]["model"] = os.getenv("LLM_MODEL")
        
        return config
    
    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """
        Deep merge override dictionary into base dictionary.
        
        Args:
            base: Base configuration dictionary
            override: Override configuration dictionary
            
        Returns:
            Merged dictionary
        """
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'affiliate.id')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default
    
    def to_dict(self) -> Dict[str, Any]:
        """Get full configuration as dictionary."""
        return self.config
