"""
Wellz Progress Bar Widget - Various progress bar styles
"""

from typing import Optional
from .base import Widget, ColorMixin


class ProgressBar(Widget, ColorMixin):
    """Customizable progress bar widget"""

    # Bar styles
    STYLES = {
        "default": {"filled": "█", "empty": "░", "left": "[", "right": "]"},
        "thin": {"filled": "━", "empty": "─", "left": "╸", "right": "╺"},
        "thick": {"filled": "█", "empty": " ", "left": "▐", "right": "▌"},
        "dots": {"filled": "●", "empty": "○", "left": "", "right": ""},
        "blocks": {"filled": "▰", "empty": "▱", "left": "", "right": ""},
        "ascii": {"filled": "#", "empty": "-", "left": "[", "right": "]"},
    }

    def __init__(self, width: int = 20, style: str = "default"):
        """
        Initialize progress bar.

        Args:
            width: Bar width in characters (excluding brackets)
            style: Style name from STYLES dict
        """
        super().__init__(width, 1)
        self.style = self.STYLES.get(style, self.STYLES["default"])
        self.value = 0.0
        self.max_value = 100.0
        self.show_percent = True
        self.color_by_value = True
        self.custom_color: Optional[str] = None

        # Colors for different value ranges
        self.color_low = "\033[92m"      # Bright green
        self.color_mid = "\033[93m"      # Bright yellow
        self.color_high = "\033[91m"     # Bright red
        self.color_empty = "\033[90m"    # Bright black (gray)

    def set_value(self, value: float, max_value: float = 100.0) -> None:
        """Set current value"""
        self.value = max(0, min(max_value, value))
        self.max_value = max_value

    def set_style(self, style: str) -> None:
        """Change bar style"""
        if style in self.STYLES:
            self.style = self.STYLES[style]

    def set_color(self, color: str) -> None:
        """Set custom color (disables auto coloring)"""
        self.custom_color = color
        self.color_by_value = False

    def get_color(self) -> str:
        """Get color based on current value percentage"""
        if self.custom_color:
            return self.custom_color

        if not self.color_by_value:
            return ""

        percent = (self.value / self.max_value * 100) if self.max_value > 0 else 0

        if percent < 50:
            return self.color_low
        elif percent < 80:
            return self.color_mid
        else:
            return self.color_high

    def render(self) -> list:
        """Render the progress bar"""
        return [self.render_line()]

    def render_line(self, width: Optional[int] = None,
                    show_percent: Optional[bool] = None,
                    show_brackets: bool = True) -> str:
        """
        Render bar as a single string.

        Args:
            width: Override width
            show_percent: Override show_percent setting
            show_brackets: Whether to show left/right brackets

        Returns:
            Formatted progress bar string
        """
        RESET = "\033[0m"
        bar_width = width or self.width
        show_pct = show_percent if show_percent is not None else self.show_percent

        # Calculate filled/empty widths
        percent = (self.value / self.max_value) if self.max_value > 0 else 0
        percent = max(0, min(1, percent))

        filled_width = int(bar_width * percent)
        empty_width = bar_width - filled_width

        # Get colors
        fill_color = self.get_color()

        # Build bar
        result = ""

        if show_brackets:
            result += self.style["left"]

        result += f"{fill_color}{self.style['filled'] * filled_width}{RESET}"
        result += f"{self.color_empty}{self.style['empty'] * empty_width}{RESET}"

        if show_brackets:
            result += self.style["right"]

        if show_pct:
            pct_val = percent * 100
            result += f" {pct_val:5.1f}%"

        return result


def create_bar(percent: float, width: int = 20,
               filled: str = "█", empty: str = "░",
               color: Optional[str] = None) -> str:
    """
    Quick function to create a simple progress bar string.

    Args:
        percent: Value 0-100
        width: Bar width
        filled: Character for filled portion
        empty: Character for empty portion
        color: Optional ANSI color code

    Returns:
        Progress bar string
    """
    RESET = "\033[0m"
    BRIGHT_BLACK = "\033[90m"

    percent = max(0, min(100, percent))
    filled_width = int(width * percent / 100)
    empty_width = width - filled_width

    # Auto color if not specified
    if color is None:
        if percent < 50:
            color = "\033[92m"  # Green
        elif percent < 80:
            color = "\033[93m"  # Yellow
        else:
            color = "\033[91m"  # Red

    return f"{color}{filled * filled_width}{RESET}{BRIGHT_BLACK}{empty * empty_width}{RESET}"


def create_labeled_bar(label: str, percent: float, value_str: str,
                       label_width: int = 6, bar_width: int = 20,
                       label_color: str = "\033[97m") -> str:
    """
    Create a labeled progress bar with value display.

    Example: "RAM    [████████░░░░░░░░] 8.2/16.0GB"

    Args:
        label: Label text (e.g., "RAM")
        percent: Value 0-100
        value_str: Value display string (e.g., "8.2/16.0GB")
        label_width: Width for label column
        bar_width: Width for bar
        label_color: Color for label

    Returns:
        Formatted labeled bar string
    """
    RESET = "\033[0m"

    padded_label = f"{label_color}{label:<{label_width}}{RESET}"
    bar = create_bar(percent, bar_width)

    return f"{padded_label} [{bar}] {value_str}"
