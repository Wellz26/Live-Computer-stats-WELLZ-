"""
Wellz Help Panel - Keyboard shortcut reference overlay
"""

from typing import Dict, List
from ..widgets.box import create_box_top, create_box_line, create_box_bottom, create_box_separator


class HelpPanel:
    """Help overlay showing keyboard shortcuts"""

    def __init__(self, width: int = 60):
        """
        Initialize help panel.

        Args:
            width: Panel width
        """
        self.width = width
        self.theme: Dict[str, str] = {}
        self.visible = False

    def set_theme(self, theme: Dict[str, str]) -> None:
        """Set color theme"""
        self.theme = theme

    def toggle(self) -> bool:
        """Toggle visibility, returns new state"""
        self.visible = not self.visible
        return self.visible

    def show(self) -> None:
        """Show help panel"""
        self.visible = True

    def hide(self) -> None:
        """Hide help panel"""
        self.visible = False

    def render(self) -> List[str]:
        """Render help panel"""
        if not self.visible:
            return []

        RESET = "\033[0m"
        lines = []

        border_color = self.theme.get("border", "\033[90m")
        title_color = self.theme.get("title", "\033[96m")
        label_color = self.theme.get("label", "\033[97m")
        accent_color = self.theme.get("accent", "\033[95m")
        dim_color = "\033[90m"

        # Keyboard shortcuts
        shortcuts = [
            ("Navigation", [
                ("j / Down", "Move down"),
                ("k / Up", "Move up"),
                ("g", "Go to top"),
                ("G", "Go to bottom"),
                ("Tab", "Switch panel focus"),
            ]),
            ("Panels", [
                ("1", "Toggle CPU panel"),
                ("2", "Toggle Memory panel"),
                ("3", "Toggle Network panel"),
                ("4", "Toggle Disk panel"),
                ("5", "Toggle GPU panel"),
                ("p", "Toggle Process list"),
            ]),
            ("Process Control", [
                ("/", "Search/filter processes"),
                ("Enter", "Select process"),
                ("K", "Kill process (SIGTERM)"),
                ("s", "Signal menu"),
                ("t", "Toggle tree view"),
            ]),
            ("Display", [
                ("c", "Next theme"),
                ("C", "Previous theme"),
                ("+", "Increase refresh rate"),
                ("-", "Decrease refresh rate"),
                ("r", "Reset view"),
            ]),
            ("General", [
                ("?", "Toggle this help"),
                ("q", "Quit"),
            ]),
        ]

        # Calculate total height
        total_lines = 2  # Top and bottom borders
        for section, items in shortcuts:
            total_lines += 2 + len(items)  # Section header + separator + items

        # Top border
        lines.append(create_box_top(self.width, "HELP - Keyboard Shortcuts", border_color, title_color))

        # Render sections
        for section, items in shortcuts:
            # Section header
            lines.append(create_box_line(f"{accent_color}{section}{RESET}", self.width, border_color))
            lines.append(create_box_separator(self.width, border_color))

            # Shortcut items
            for key, description in items:
                key_str = f"{label_color}{key:<12}{RESET}"
                line = f"{key_str} {dim_color}{description}{RESET}"
                lines.append(create_box_line(line, self.width, border_color))

            lines.append(create_box_line("", self.width, border_color))

        # Footer
        lines.append(create_box_line(f"{dim_color}Press ? or Esc to close{RESET}", self.width, border_color))

        # Bottom border
        lines.append(create_box_bottom(self.width, border_color))

        return lines
