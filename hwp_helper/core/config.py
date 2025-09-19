"""Configuration management for HWP Helper."""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages application configuration and settings."""
    
    def __init__(self, config_file: str = "setting.yaml"):
        self.config_file = Path(config_file)
        self._settings: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from file."""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self._settings = yaml.safe_load(f) or {}
        else:
            self._settings = self._get_default_settings()
            self.save_config()
    
    def save_config(self) -> None:
        """Save current configuration to file."""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.safe_dump(self._settings, f, allow_unicode=True)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self._settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self._settings[key] = value
    
    def update(self, settings: Dict[str, Any]) -> None:
        """Update multiple configuration values."""
        self._settings.update(settings)
    
    @property
    def settings(self) -> Dict[str, Any]:
        """Get all settings."""
        return self._settings.copy()
    
    def _get_default_settings(self) -> Dict[str, Any]:
        """Get default configuration settings."""
        return {
            "app_width": 674,
            "tab": 0,
            "font_styles": {},
            "last_category": None,
            "window_always_on_top": False,
        }
