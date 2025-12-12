"""
Wellz Base Widget - Abstract base class for all widgets
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple


class Widget(ABC):
    """Abstract base class for all UI widgets"""

    def __init__(self, width: int, height: int):
        """
        Initialize widget with dimensions.

        Args:
            width: Widget width in characters
            height: Widget height in lines
        """
        self.width = width
        self.height = height
        self.visible = True

    @abstractmethod
    def render(self) -> List[str]:
        """
        Render the widget to a list of strings.

        Returns:
            List of strings, one per line
        """
        pass

    def resize(self, width: int, height: int) -> None:
        """Resize the widget"""
        self.width = width
        self.height = height

    def show(self) -> None:
        """Make widget visible"""
        self.visible = True

    def hide(self) -> None:
        """Hide widget"""
        self.visible = False

    def toggle(self) -> bool:
        """Toggle visibility, returns new state"""
        self.visible = not self.visible
        return self.visible


class ColorMixin:
    """Mixin for widgets that support coloring"""

    RESET = "\033[0m"

    def colorize(self, text: str, color: str) -> str:
        """Apply color to text"""
        if color:
            return f"{color}{text}{self.RESET}"
        return text

    def strip_ansi(self, text: str) -> str:
        """Remove ANSI codes from text"""
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def visible_len(self, text: str) -> int:
        """Get visible length of text (excluding ANSI codes)"""
        return len(self.strip_ansi(text))


class ContainerWidget(Widget):
    """Widget that contains other widgets"""

    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.children: List[Widget] = []

    def add(self, widget: Widget) -> None:
        """Add a child widget"""
        self.children.append(widget)

    def remove(self, widget: Widget) -> None:
        """Remove a child widget"""
        if widget in self.children:
            self.children.remove(widget)

    def clear(self) -> None:
        """Remove all children"""
        self.children.clear()

    def render(self) -> List[str]:
        """Render all visible children"""
        lines = []
        for child in self.children:
            if child.visible:
                lines.extend(child.render())
        return lines
