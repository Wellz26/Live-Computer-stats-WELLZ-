"""
Wellz Configuration Manager - Load, save, and manage configuration
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# Try to import tomllib (Python 3.11+) or tomli
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None


# Default configuration values
DEFAULT_CONFIG: Dict[str, Any] = {
    "general": {
        "refresh_rate": 1.0,
        "history_size": 120,
        "layout": "default",
    },
    "display": {
        "show_cpu": True,
        "show_memory": True,
        "show_network": True,
        "show_disk": True,
        "show_gpu": True,
        "show_processes": True,
        "graph_style": "braille",
        "show_graphs": True,
        "graph_height": 5,
        "show_per_core": True,
        "max_cores": 8,
        "max_disks": 4,
        "max_interfaces": 2,
    },
    "theme": {
        "name": "default",
        "custom": {},
    },
    "processes": {
        "sort_by": "cpu",
        "sort_descending": True,
        "tree_view": False,
        "max_processes": 20,
        "update_interval": 2,
    },
    "keybindings": {
        "vim_mode": True,
    },
    "advanced": {
        "mouse_enabled": True,
        "show_fps": False,
        "unicode_borders": True,
        "network_unit": "auto",
        "temp_unit": "celsius",
    },
}


class ConfigManager:
    """Manages Wellz configuration loading and saving"""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize config manager.

        Args:
            config_path: Optional custom config file path
        """
        self.config_path = Path(config_path) if config_path else self._get_default_path()
        self.config: Dict[str, Any] = self._deep_copy(DEFAULT_CONFIG)
        self._load()

    @staticmethod
    def _get_default_path() -> Path:
        """Get default config file path based on OS"""
        if sys.platform == "win32":
            base = Path(os.environ.get("APPDATA", Path.home()))
            return base / "wellz" / "config.toml"
        else:
            # XDG spec for Linux/macOS
            xdg_config = os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")
            return Path(xdg_config) / "wellz" / "config.toml"

    @staticmethod
    def _deep_copy(d: Dict[str, Any]) -> Dict[str, Any]:
        """Deep copy a dictionary"""
        result = {}
        for k, v in d.items():
            if isinstance(v, dict):
                result[k] = ConfigManager._deep_copy(v)
            elif isinstance(v, list):
                result[k] = v.copy()
            else:
                result[k] = v
        return result

    def _load(self) -> None:
        """Load configuration from file"""
        if not self.config_path.exists():
            return

        if tomllib is None:
            # Can't parse TOML without library
            return

        try:
            with open(self.config_path, "rb") as f:
                user_config = tomllib.load(f)
            self._merge_config(user_config)
        except Exception as e:
            # Silently use defaults if config is invalid
            pass

    def _merge_config(self, user_config: Dict[str, Any]) -> None:
        """Merge user config into default config"""
        for section, values in user_config.items():
            if section in self.config and isinstance(values, dict):
                for key, value in values.items():
                    if key in self.config[section]:
                        self.config[section][key] = value
            elif section in self.config:
                self.config[section] = values

    def save(self) -> bool:
        """
        Save current configuration to file.

        Returns:
            True if saved successfully
        """
        try:
            # Create directory if needed
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

            # Generate TOML content
            content = self._to_toml()

            with open(self.config_path, "w") as f:
                f.write(content)
            return True
        except Exception as e:
            return False

    def _to_toml(self) -> str:
        """Convert config to TOML string"""
        lines = ["# Wellz Configuration File", ""]

        for section, values in self.config.items():
            lines.append(f"[{section}]")
            if isinstance(values, dict):
                for key, value in values.items():
                    if isinstance(value, dict):
                        # Nested table
                        lines.append(f"[{section}.{key}]")
                        for k, v in value.items():
                            lines.append(f"{k} = {self._format_value(v)}")
                    else:
                        lines.append(f"{key} = {self._format_value(value)}")
            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def _format_value(value: Any) -> str:
        """Format a value for TOML"""
        if isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, list):
            items = ", ".join(ConfigManager._format_value(v) for v in value)
            return f"[{items}]"
        else:
            return f'"{value}"'

    def create_default_config(self) -> bool:
        """
        Create default config file if it doesn't exist.

        Returns:
            True if created or already exists
        """
        if self.config_path.exists():
            return True

        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

            # Copy the default.toml template
            template_path = Path(__file__).parent / "default.toml"
            if template_path.exists():
                with open(template_path, "r") as src:
                    content = src.read()
                with open(self.config_path, "w") as dst:
                    dst.write(content)
            else:
                # Generate from defaults
                self.save()
            return True
        except Exception:
            return False

    # ========================================================================
    # Accessor methods for common settings
    # ========================================================================

    @property
    def refresh_rate(self) -> float:
        """Get refresh rate in seconds"""
        rate = self.config["general"]["refresh_rate"]
        return max(0.5, min(10.0, float(rate)))

    @refresh_rate.setter
    def refresh_rate(self, value: float) -> None:
        self.config["general"]["refresh_rate"] = max(0.5, min(10.0, value))

    @property
    def history_size(self) -> int:
        """Get history buffer size"""
        return int(self.config["general"]["history_size"])

    @property
    def theme_name(self) -> str:
        """Get current theme name"""
        return self.config["theme"]["name"]

    @theme_name.setter
    def theme_name(self, value: str) -> None:
        self.config["theme"]["name"] = value

    @property
    def graph_style(self) -> str:
        """Get graph rendering style"""
        return self.config["display"]["graph_style"]

    @property
    def show_graphs(self) -> bool:
        """Whether to show graphs"""
        return self.config["display"]["show_graphs"]

    @property
    def graph_height(self) -> int:
        """Get graph height in lines"""
        return int(self.config["display"]["graph_height"])

    @property
    def show_cpu(self) -> bool:
        return self.config["display"]["show_cpu"]

    @property
    def show_memory(self) -> bool:
        return self.config["display"]["show_memory"]

    @property
    def show_network(self) -> bool:
        return self.config["display"]["show_network"]

    @property
    def show_disk(self) -> bool:
        return self.config["display"]["show_disk"]

    @property
    def show_gpu(self) -> bool:
        return self.config["display"]["show_gpu"]

    @property
    def show_processes(self) -> bool:
        return self.config["display"]["show_processes"]

    @property
    def process_sort_by(self) -> str:
        return self.config["processes"]["sort_by"]

    @process_sort_by.setter
    def process_sort_by(self, value: str) -> None:
        if value in ["cpu", "memory", "pid", "name"]:
            self.config["processes"]["sort_by"] = value

    @property
    def process_sort_descending(self) -> bool:
        return self.config["processes"]["sort_descending"]

    @property
    def process_tree_view(self) -> bool:
        return self.config["processes"]["tree_view"]

    @process_tree_view.setter
    def process_tree_view(self, value: bool) -> None:
        self.config["processes"]["tree_view"] = value

    @property
    def max_processes(self) -> int:
        return int(self.config["processes"]["max_processes"])

    @property
    def vim_mode(self) -> bool:
        return self.config["keybindings"]["vim_mode"]

    @property
    def unicode_borders(self) -> bool:
        return self.config["advanced"]["unicode_borders"]

    @property
    def temp_unit(self) -> str:
        return self.config["advanced"]["temp_unit"]

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get a config value by section and key"""
        try:
            return self.config[section][key]
        except KeyError:
            return default

    def set(self, section: str, key: str, value: Any) -> None:
        """Set a config value"""
        if section in self.config:
            self.config[section][key] = value

    def toggle(self, section: str, key: str) -> bool:
        """Toggle a boolean config value, returns new value"""
        if section in self.config and key in self.config[section]:
            current = self.config[section][key]
            if isinstance(current, bool):
                self.config[section][key] = not current
                return self.config[section][key]
        return False


# Global config instance
_config_instance: Optional[ConfigManager] = None


def get_config(config_path: Optional[str] = None) -> ConfigManager:
    """
    Get the global config manager instance.

    Args:
        config_path: Optional custom config path (only used on first call)

    Returns:
        ConfigManager instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigManager(config_path)
    return _config_instance


def reset_config() -> None:
    """Reset the global config instance (for testing)"""
    global _config_instance
    _config_instance = None
