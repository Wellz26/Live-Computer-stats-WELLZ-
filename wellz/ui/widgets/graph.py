"""
Wellz Graph Widget - Braille, block, and ASCII graph rendering
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Union


# Braille character mapping
# Each braille character is a 2x4 grid of dots
# Dot positions:
#   0 3
#   1 4
#   2 5
#   6 7
# Character = 0x2800 + sum of dot values (1,2,4,8,16,32,64,128)

BRAILLE_BASE = 0x2800

# Dot values for each position in 2x4 grid
BRAILLE_DOTS = [
    [0x01, 0x08],  # Row 0
    [0x02, 0x10],  # Row 1
    [0x04, 0x20],  # Row 2
    [0x40, 0x80],  # Row 3
]

# Block characters for block-style graphs
BLOCK_CHARS = " ▁▂▃▄▅▆▇█"

# ASCII characters for ASCII-style graphs (fallback)
ASCII_CHARS = " ._-=+#@"


class GraphRenderer(ABC):
    """Abstract base class for graph renderers"""

    @abstractmethod
    def render(self, data: List[float], width: int, height: int,
               min_val: float = 0, max_val: float = 100,
               color: str = "", empty_color: str = "") -> List[str]:
        """
        Render data as a graph.

        Args:
            data: List of values to graph
            width: Width in characters
            height: Height in lines
            min_val: Minimum value (0 on graph)
            max_val: Maximum value (top of graph)
            color: ANSI color code for filled areas
            empty_color: ANSI color code for empty areas

        Returns:
            List of strings representing the graph
        """
        pass


class BrailleGraph(GraphRenderer):
    """
    High-resolution graph using braille characters.
    Each character cell represents 2x4 dots for smooth curves.
    """

    def render(self, data: List[float], width: int, height: int,
               min_val: float = 0, max_val: float = 100,
               color: str = "", empty_color: str = "") -> List[str]:
        """Render graph using braille characters"""
        RESET = "\033[0m"

        # Braille gives us 2x resolution horizontally, 4x vertically
        dots_width = width * 2
        dots_height = height * 4

        # Normalize data to fit graph
        if not data:
            data = [0]

        # Fit data to width (take last N points or interpolate)
        if len(data) > dots_width:
            data = data[-dots_width:]
        elif len(data) < dots_width:
            # Pad with zeros at beginning
            data = [0.0] * (dots_width - len(data)) + list(data)

        # Create dot matrix
        dots = [[False] * dots_width for _ in range(dots_height)]

        # Fill dots based on data values
        value_range = max_val - min_val if max_val != min_val else 1

        for x, value in enumerate(data):
            # Clamp value
            value = max(min_val, min(max_val, value))

            # Calculate height in dots
            normalized = (value - min_val) / value_range
            fill_height = int(normalized * dots_height)

            # Fill from bottom up
            for y in range(fill_height):
                if y < dots_height:
                    dots[dots_height - 1 - y][x] = True

        # Convert dot matrix to braille characters
        lines = []
        for row in range(height):
            line = ""
            for col in range(width):
                # Get 2x4 dot block
                char_val = 0
                for dy in range(4):
                    for dx in range(2):
                        dot_y = row * 4 + dy
                        dot_x = col * 2 + dx
                        if dot_x < dots_width and dot_y < dots_height:
                            if dots[dot_y][dot_x]:
                                char_val |= BRAILLE_DOTS[dy][dx]

                braille_char = chr(BRAILLE_BASE + char_val)

                # Apply color based on whether cell has any dots
                if char_val > 0:
                    line += f"{color}{braille_char}{RESET}" if color else braille_char
                else:
                    line += f"{empty_color}{braille_char}{RESET}" if empty_color else braille_char

            lines.append(line)

        return lines

    def render_dual(self, data1: List[float], data2: List[float],
                    width: int, height: int,
                    min_val: float = 0, max_val: float = 100,
                    color1: str = "", color2: str = "") -> List[str]:
        """
        Render two data series on same graph (e.g., upload/download).
        Uses different dot patterns for each series.
        """
        RESET = "\033[0m"

        dots_width = width * 2
        dots_height = height * 4

        # Normalize both data series
        for data in [data1, data2]:
            if len(data) > dots_width:
                data[:] = data[-dots_width:]
            elif len(data) < dots_width:
                data[:] = [0.0] * (dots_width - len(data)) + list(data)

        # Create dot matrices
        dots1 = [[False] * dots_width for _ in range(dots_height)]
        dots2 = [[False] * dots_width for _ in range(dots_height)]

        value_range = max_val - min_val if max_val != min_val else 1

        # Fill dots for both series
        for data, dots in [(data1, dots1), (data2, dots2)]:
            for x, value in enumerate(data[:dots_width]):
                value = max(min_val, min(max_val, value))
                normalized = (value - min_val) / value_range
                fill_height = int(normalized * dots_height)

                for y in range(fill_height):
                    if y < dots_height:
                        dots[dots_height - 1 - y][x] = True

        # Convert to braille with dual coloring
        lines = []
        for row in range(height):
            line = ""
            for col in range(width):
                char_val = 0
                has_series1 = False
                has_series2 = False

                for dy in range(4):
                    for dx in range(2):
                        dot_y = row * 4 + dy
                        dot_x = col * 2 + dx
                        if dot_x < dots_width and dot_y < dots_height:
                            # Use left column for series 1, right for series 2
                            if dx == 0 and dots1[dot_y][dot_x]:
                                char_val |= BRAILLE_DOTS[dy][dx]
                                has_series1 = True
                            elif dx == 1 and dots2[dot_y][dot_x]:
                                char_val |= BRAILLE_DOTS[dy][dx]
                                has_series2 = True

                braille_char = chr(BRAILLE_BASE + char_val)

                # Color based on which series is present
                if has_series1 and has_series2:
                    line += f"{color1}{braille_char}{RESET}"
                elif has_series1:
                    line += f"{color1}{braille_char}{RESET}"
                elif has_series2:
                    line += f"{color2}{braille_char}{RESET}"
                else:
                    line += braille_char

            lines.append(line)

        return lines


class BlockGraph(GraphRenderer):
    """
    Block-style graph using Unicode block elements.
    More compatible than braille but lower resolution.
    """

    def render(self, data: List[float], width: int, height: int,
               min_val: float = 0, max_val: float = 100,
               color: str = "", empty_color: str = "") -> List[str]:
        """Render graph using block characters"""
        RESET = "\033[0m"

        if not data:
            data = [0]

        # Fit data to width
        if len(data) > width:
            data = data[-width:]
        elif len(data) < width:
            data = [0.0] * (width - len(data)) + list(data)

        # Block chars give us 8 levels per character height
        levels = height * 8
        value_range = max_val - min_val if max_val != min_val else 1

        # Build columns of heights
        columns = []
        for value in data:
            value = max(min_val, min(max_val, value))
            normalized = (value - min_val) / value_range
            col_height = int(normalized * levels)
            columns.append(col_height)

        # Build lines from top to bottom
        lines = []
        for row in range(height):
            line = ""
            row_bottom = (height - 1 - row) * 8
            row_top = row_bottom + 8

            for col_height in columns:
                if col_height >= row_top:
                    # Full block
                    char = BLOCK_CHARS[8]
                elif col_height <= row_bottom:
                    # Empty
                    char = BLOCK_CHARS[0]
                else:
                    # Partial block
                    partial = col_height - row_bottom
                    char = BLOCK_CHARS[partial]

                if char != " ":
                    line += f"{color}{char}{RESET}" if color else char
                else:
                    line += f"{empty_color}{char}{RESET}" if empty_color else char

            lines.append(line)

        return lines


class AsciiGraph(GraphRenderer):
    """
    ASCII-only graph for maximum compatibility.
    Uses simple characters that work in any terminal.
    """

    def render(self, data: List[float], width: int, height: int,
               min_val: float = 0, max_val: float = 100,
               color: str = "", empty_color: str = "") -> List[str]:
        """Render graph using ASCII characters"""
        RESET = "\033[0m"

        if not data:
            data = [0]

        # Fit data to width
        if len(data) > width:
            data = data[-width:]
        elif len(data) < width:
            data = [0.0] * (width - len(data)) + list(data)

        # ASCII chars give us len(ASCII_CHARS)-1 levels per character height
        levels_per_char = len(ASCII_CHARS) - 1
        levels = height * levels_per_char
        value_range = max_val - min_val if max_val != min_val else 1

        # Build columns of heights
        columns = []
        for value in data:
            value = max(min_val, min(max_val, value))
            normalized = (value - min_val) / value_range
            col_height = int(normalized * levels)
            columns.append(col_height)

        # Build lines from top to bottom
        lines = []
        for row in range(height):
            line = ""
            row_bottom = (height - 1 - row) * levels_per_char
            row_top = row_bottom + levels_per_char

            for col_height in columns:
                if col_height >= row_top:
                    char = ASCII_CHARS[-1]
                elif col_height <= row_bottom:
                    char = ASCII_CHARS[0]
                else:
                    partial = col_height - row_bottom
                    char = ASCII_CHARS[min(partial, len(ASCII_CHARS) - 1)]

                if char != " ":
                    line += f"{color}{char}{RESET}" if color else char
                else:
                    line += f"{empty_color}{char}{RESET}" if empty_color else char

            lines.append(line)

        return lines


def create_graph(style: str = "braille") -> GraphRenderer:
    """
    Factory function to create graph renderer.

    Args:
        style: "braille", "block", or "ascii"

    Returns:
        GraphRenderer instance
    """
    renderers = {
        "braille": BrailleGraph,
        "block": BlockGraph,
        "ascii": AsciiGraph,
    }
    renderer_class = renderers.get(style.lower(), BrailleGraph)
    return renderer_class()


def sparkline(data: List[float], width: int = 20,
              min_val: float = 0, max_val: float = 100,
              color: str = "") -> str:
    """
    Create a single-line sparkline graph.

    Args:
        data: Values to graph
        width: Width in characters
        min_val: Minimum value
        max_val: Maximum value
        color: ANSI color code

    Returns:
        Single line string
    """
    RESET = "\033[0m"

    if not data:
        return " " * width

    # Fit data to width
    if len(data) > width:
        data = data[-width:]
    elif len(data) < width:
        data = [0.0] * (width - len(data)) + list(data)

    value_range = max_val - min_val if max_val != min_val else 1
    result = ""

    for value in data:
        value = max(min_val, min(max_val, value))
        normalized = (value - min_val) / value_range
        index = int(normalized * (len(BLOCK_CHARS) - 1))
        char = BLOCK_CHARS[index]
        result += f"{color}{char}{RESET}" if color and char != " " else char

    return result
