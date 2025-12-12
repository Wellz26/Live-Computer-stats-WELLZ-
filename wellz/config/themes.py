"""
Wellz Themes - Color schemes for the dashboard
"""

from typing import Dict, List, Any


# ANSI escape code helpers
def fg(r: int, g: int, b: int) -> str:
    """Create foreground color from RGB"""
    return f"\033[38;2;{r};{g};{b}m"


def bg(r: int, g: int, b: int) -> str:
    """Create background color from RGB"""
    return f"\033[48;2;{r};{g};{b}m"


# Standard ANSI colors
ANSI = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "italic": "\033[3m",
    "underline": "\033[4m",
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "bright_black": "\033[90m",
    "bright_red": "\033[91m",
    "bright_green": "\033[92m",
    "bright_yellow": "\033[93m",
    "bright_blue": "\033[94m",
    "bright_magenta": "\033[95m",
    "bright_cyan": "\033[96m",
    "bright_white": "\033[97m",
}


# ============================================================================
# THEME DEFINITIONS
# ============================================================================

THEMES: Dict[str, Dict[str, str]] = {
    # Default theme - blue/cyan (current wellz style)
    "default": {
        "name": "Default",
        "title": ANSI["bright_cyan"],
        "border": ANSI["bright_black"],
        "label": ANSI["bright_white"],
        "value": ANSI["white"],
        "low": ANSI["bright_green"],       # 0-49% usage
        "mid": ANSI["bright_yellow"],      # 50-79% usage
        "high": ANSI["bright_red"],        # 80-100% usage
        "accent": ANSI["bright_magenta"],
        "cpu": ANSI["bright_green"],
        "gpu": ANSI["bright_yellow"],
        "mem": ANSI["bright_blue"],
        "disk": ANSI["bright_magenta"],
        "net": ANSI["bright_cyan"],
        "process": ANSI["bright_white"],
        "selected": ANSI["bright_cyan"],
        "graph_fill": ANSI["bright_cyan"],
        "graph_empty": ANSI["bright_black"],
        "header": ANSI["bright_cyan"] + ANSI["bold"],
        "footer": ANSI["bright_black"],
    },

    # Dracula theme - purple/pink/cyan
    "dracula": {
        "name": "Dracula",
        "title": fg(189, 147, 249),         # Purple
        "border": fg(68, 71, 90),           # Comment gray
        "label": fg(248, 248, 242),         # Foreground
        "value": fg(248, 248, 242),
        "low": fg(80, 250, 123),            # Green
        "mid": fg(255, 184, 108),           # Orange
        "high": fg(255, 85, 85),            # Red
        "accent": fg(255, 121, 198),        # Pink
        "cpu": fg(80, 250, 123),
        "gpu": fg(241, 250, 140),           # Yellow
        "mem": fg(139, 233, 253),           # Cyan
        "disk": fg(255, 121, 198),
        "net": fg(139, 233, 253),
        "process": fg(248, 248, 242),
        "selected": fg(189, 147, 249),
        "graph_fill": fg(189, 147, 249),
        "graph_empty": fg(68, 71, 90),
        "header": fg(189, 147, 249) + ANSI["bold"],
        "footer": fg(98, 114, 164),
    },

    # Nord theme - frost blue colors
    "nord": {
        "name": "Nord",
        "title": fg(136, 192, 208),         # Frost
        "border": fg(76, 86, 106),          # Polar Night 3
        "label": fg(236, 239, 244),         # Snow Storm
        "value": fg(229, 233, 240),
        "low": fg(163, 190, 140),           # Aurora Green
        "mid": fg(235, 203, 139),           # Aurora Yellow
        "high": fg(191, 97, 106),           # Aurora Red
        "accent": fg(180, 142, 173),        # Aurora Purple
        "cpu": fg(163, 190, 140),
        "gpu": fg(235, 203, 139),
        "mem": fg(129, 161, 193),           # Frost 2
        "disk": fg(180, 142, 173),
        "net": fg(136, 192, 208),
        "process": fg(229, 233, 240),
        "selected": fg(136, 192, 208),
        "graph_fill": fg(136, 192, 208),
        "graph_empty": fg(76, 86, 106),
        "header": fg(136, 192, 208) + ANSI["bold"],
        "footer": fg(76, 86, 106),
    },

    # Gruvbox theme - warm retro colors
    "gruvbox": {
        "name": "Gruvbox",
        "title": fg(254, 128, 25),          # Orange
        "border": fg(102, 92, 84),          # Gray
        "label": fg(235, 219, 178),         # Light
        "value": fg(213, 196, 161),
        "low": fg(184, 187, 38),            # Green
        "mid": fg(250, 189, 47),            # Yellow
        "high": fg(251, 73, 52),            # Red
        "accent": fg(211, 134, 155),        # Purple
        "cpu": fg(184, 187, 38),
        "gpu": fg(250, 189, 47),
        "mem": fg(131, 165, 152),           # Aqua
        "disk": fg(211, 134, 155),
        "net": fg(254, 128, 25),
        "process": fg(235, 219, 178),
        "selected": fg(254, 128, 25),
        "graph_fill": fg(254, 128, 25),
        "graph_empty": fg(102, 92, 84),
        "header": fg(254, 128, 25) + ANSI["bold"],
        "footer": fg(146, 131, 116),
    },

    # Monokai theme - classic syntax highlight colors
    "monokai": {
        "name": "Monokai",
        "title": fg(102, 217, 239),         # Cyan
        "border": fg(117, 113, 94),         # Comment
        "label": fg(248, 248, 242),         # Foreground
        "value": fg(248, 248, 242),
        "low": fg(166, 226, 46),            # Green
        "mid": fg(230, 219, 116),           # Yellow
        "high": fg(249, 38, 114),           # Pink/Red
        "accent": fg(174, 129, 255),        # Purple
        "cpu": fg(166, 226, 46),
        "gpu": fg(230, 219, 116),
        "mem": fg(102, 217, 239),
        "disk": fg(174, 129, 255),
        "net": fg(102, 217, 239),
        "process": fg(248, 248, 242),
        "selected": fg(249, 38, 114),
        "graph_fill": fg(102, 217, 239),
        "graph_empty": fg(117, 113, 94),
        "header": fg(102, 217, 239) + ANSI["bold"],
        "footer": fg(117, 113, 94),
    },

    # Solarized Dark theme
    "solarized": {
        "name": "Solarized",
        "title": fg(38, 139, 210),          # Blue
        "border": fg(88, 110, 117),         # Base01
        "label": fg(147, 161, 161),         # Base1
        "value": fg(131, 148, 150),         # Base0
        "low": fg(133, 153, 0),             # Green
        "mid": fg(181, 137, 0),             # Yellow
        "high": fg(220, 50, 47),            # Red
        "accent": fg(108, 113, 196),        # Violet
        "cpu": fg(133, 153, 0),
        "gpu": fg(181, 137, 0),
        "mem": fg(42, 161, 152),            # Cyan
        "disk": fg(108, 113, 196),
        "net": fg(38, 139, 210),
        "process": fg(147, 161, 161),
        "selected": fg(38, 139, 210),
        "graph_fill": fg(38, 139, 210),
        "graph_empty": fg(88, 110, 117),
        "header": fg(38, 139, 210) + ANSI["bold"],
        "footer": fg(88, 110, 117),
    },

    # Tokyo Night theme
    "tokyo": {
        "name": "Tokyo Night",
        "title": fg(122, 162, 247),         # Blue
        "border": fg(65, 72, 104),          # Comment
        "label": fg(192, 202, 245),         # Foreground
        "value": fg(169, 177, 214),
        "low": fg(158, 206, 106),           # Green
        "mid": fg(224, 175, 104),           # Yellow
        "high": fg(247, 118, 142),          # Red
        "accent": fg(187, 154, 247),        # Purple
        "cpu": fg(158, 206, 106),
        "gpu": fg(224, 175, 104),
        "mem": fg(125, 207, 255),           # Cyan
        "disk": fg(187, 154, 247),
        "net": fg(122, 162, 247),
        "process": fg(192, 202, 245),
        "selected": fg(255, 158, 100),      # Orange
        "graph_fill": fg(122, 162, 247),
        "graph_empty": fg(65, 72, 104),
        "header": fg(122, 162, 247) + ANSI["bold"],
        "footer": fg(86, 95, 137),
    },

    # Catppuccin Mocha theme
    "catppuccin": {
        "name": "Catppuccin",
        "title": fg(137, 180, 250),         # Blue
        "border": fg(108, 112, 134),        # Overlay0
        "label": fg(205, 214, 244),         # Text
        "value": fg(186, 194, 222),         # Subtext1
        "low": fg(166, 227, 161),           # Green
        "mid": fg(249, 226, 175),           # Yellow
        "high": fg(243, 139, 168),          # Red
        "accent": fg(203, 166, 247),        # Mauve
        "cpu": fg(166, 227, 161),
        "gpu": fg(249, 226, 175),
        "mem": fg(148, 226, 213),           # Teal
        "disk": fg(203, 166, 247),
        "net": fg(137, 180, 250),
        "process": fg(205, 214, 244),
        "selected": fg(245, 194, 231),      # Pink
        "graph_fill": fg(137, 180, 250),
        "graph_empty": fg(108, 112, 134),
        "header": fg(137, 180, 250) + ANSI["bold"],
        "footer": fg(127, 132, 156),
    },
}


def get_theme(name: str) -> Dict[str, str]:
    """
    Get theme by name.

    Args:
        name: Theme name (case-insensitive)

    Returns:
        Theme dictionary, or default theme if not found
    """
    return THEMES.get(name.lower(), THEMES["default"])


def get_theme_names() -> List[str]:
    """Get list of available theme names"""
    return list(THEMES.keys())


def apply_theme_color(theme: Dict[str, str], key: str, text: str) -> str:
    """
    Apply theme color to text.

    Args:
        theme: Theme dictionary
        key: Color key (e.g., 'title', 'border')
        text: Text to colorize

    Returns:
        Colored text with reset code
    """
    color = theme.get(key, "")
    return f"{color}{text}{ANSI['reset']}"


def get_usage_color(theme: Dict[str, str], percent: float) -> str:
    """
    Get color based on usage percentage.

    Args:
        theme: Theme dictionary
        percent: Usage percentage (0-100)

    Returns:
        ANSI color code
    """
    if percent < 50:
        return theme.get("low", ANSI["bright_green"])
    elif percent < 80:
        return theme.get("mid", ANSI["bright_yellow"])
    else:
        return theme.get("high", ANSI["bright_red"])
