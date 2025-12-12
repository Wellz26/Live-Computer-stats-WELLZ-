"""
Wellz Box Widget - Container with borders and title
"""

import re
from typing import List, Optional, Tuple
from .base import Widget, ColorMixin


class Box(Widget, ColorMixin):
    """Box container with Unicode borders and optional title"""

    # Border character sets
    BORDERS = {
        "single": {
            "tl": "┌", "tr": "┐", "bl": "└", "br": "┘",
            "h": "─", "v": "│", "lt": "├", "rt": "┤",
            "tt": "┬", "bt": "┴", "x": "┼"
        },
        "double": {
            "tl": "╔", "tr": "╗", "bl": "╚", "br": "╝",
            "h": "═", "v": "║", "lt": "╠", "rt": "╣",
            "tt": "╦", "bt": "╩", "x": "╬"
        },
        "rounded": {
            "tl": "╭", "tr": "╮", "bl": "╰", "br": "╯",
            "h": "─", "v": "│", "lt": "├", "rt": "┤",
            "tt": "┬", "bt": "┴", "x": "┼"
        },
        "heavy": {
            "tl": "┏", "tr": "┓", "bl": "┗", "br": "┛",
            "h": "━", "v": "┃", "lt": "┣", "rt": "┫",
            "tt": "┳", "bt": "┻", "x": "╋"
        },
        "ascii": {
            "tl": "+", "tr": "+", "bl": "+", "br": "+",
            "h": "-", "v": "|", "lt": "+", "rt": "+",
            "tt": "+", "bt": "+", "x": "+"
        },
    }

    def __init__(self, width: int, height: int,
                 title: str = "", border_style: str = "rounded"):
        """
        Initialize box.

        Args:
            width: Total width including borders
            height: Total height including borders
            title: Optional title for top border
            border_style: Style name from BORDERS dict
        """
        super().__init__(width, height)
        self.title = title
        self.border = self.BORDERS.get(border_style, self.BORDERS["rounded"])
        self.content: List[str] = []
        self.border_color = "\033[90m"  # Default gray
        self.title_color = "\033[96m"   # Default cyan
        self.padding = 1  # Space between border and content

    def set_title(self, title: str) -> None:
        """Set box title"""
        self.title = title

    def set_border_style(self, style: str) -> None:
        """Change border style"""
        if style in self.BORDERS:
            self.border = self.BORDERS[style]

    def set_colors(self, border: str = "", title: str = "") -> None:
        """Set border and title colors"""
        if border:
            self.border_color = border
        if title:
            self.title_color = title

    def set_content(self, content: List[str]) -> None:
        """Set box content as list of lines"""
        self.content = content

    def add_line(self, line: str) -> None:
        """Add a line to content"""
        self.content.append(line)

    def clear_content(self) -> None:
        """Clear all content"""
        self.content = []

    def _get_visible_len(self, text: str) -> int:
        """Get visible length excluding ANSI codes"""
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return len(ansi_escape.sub('', text))

    def render(self) -> List[str]:
        """Render the box with content"""
        RESET = "\033[0m"
        lines = []
        inner_width = self.width - 2  # Subtract border characters

        # Top border with optional title
        if self.title:
            title_str = f" {self.title} "
            title_display = f"{self.title_color}{title_str}{RESET}"
            title_len = len(title_str)
            padding = inner_width - title_len - 1
            if padding < 0:
                padding = 0
            top = (f"{self.border_color}{self.border['tl']}{self.border['h']}{RESET}"
                   f"{title_display}"
                   f"{self.border_color}{self.border['h'] * padding}{self.border['tr']}{RESET}")
        else:
            top = (f"{self.border_color}{self.border['tl']}"
                   f"{self.border['h'] * inner_width}"
                   f"{self.border['tr']}{RESET}")
        lines.append(top)

        # Content lines
        content_height = self.height - 2  # Subtract top and bottom borders
        for i in range(content_height):
            if i < len(self.content):
                line_content = self.content[i]
                visible_len = self._get_visible_len(line_content)
                padding = inner_width - visible_len - self.padding
                if padding < 0:
                    # Truncate content if too long
                    # This is tricky with ANSI codes, so just cut visible chars
                    padding = 0
                line = (f"{self.border_color}{self.border['v']}{RESET}"
                        f"{' ' * self.padding}{line_content}{' ' * padding}"
                        f"{self.border_color}{self.border['v']}{RESET}")
            else:
                # Empty line
                line = (f"{self.border_color}{self.border['v']}{RESET}"
                        f"{' ' * inner_width}"
                        f"{self.border_color}{self.border['v']}{RESET}")
            lines.append(line)

        # Bottom border
        bottom = (f"{self.border_color}{self.border['bl']}"
                  f"{self.border['h'] * inner_width}"
                  f"{self.border['br']}{RESET}")
        lines.append(bottom)

        return lines

    def render_separator(self) -> str:
        """Render a horizontal separator line"""
        RESET = "\033[0m"
        inner_width = self.width - 2
        return (f"{self.border_color}{self.border['lt']}"
                f"{self.border['h'] * inner_width}"
                f"{self.border['rt']}{RESET}")


def create_box_top(width: int, title: str = "",
                   border_color: str = "\033[90m",
                   title_color: str = "\033[96m") -> str:
    """Create just the top border of a box"""
    RESET = "\033[0m"
    inner_width = width - 2

    if title:
        title_str = f" {title} "
        padding = inner_width - len(title_str) - 1
        if padding < 0:
            padding = 0
        return (f"{border_color}╭─{RESET}"
                f"{title_color}{title_str}{RESET}"
                f"{border_color}{'─' * padding}╮{RESET}")
    return f"{border_color}╭{'─' * inner_width}╮{RESET}"


def create_box_line(content: str, width: int,
                    border_color: str = "\033[90m") -> str:
    """Create a single line within a box"""
    RESET = "\033[0m"

    # Calculate visible length
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    visible_len = len(ansi_escape.sub('', content))

    inner_width = width - 2
    padding = inner_width - visible_len - 1
    if padding < 0:
        padding = 0

    return f"{border_color}│{RESET} {content}{' ' * padding}{border_color}│{RESET}"


def create_box_separator(width: int, border_color: str = "\033[90m") -> str:
    """Create a horizontal separator within a box"""
    RESET = "\033[0m"
    inner_width = width - 2
    return f"{border_color}├{'─' * inner_width}┤{RESET}"


def create_box_bottom(width: int, border_color: str = "\033[90m") -> str:
    """Create the bottom border of a box"""
    RESET = "\033[0m"
    inner_width = width - 2
    return f"{border_color}╰{'─' * inner_width}╯{RESET}"
