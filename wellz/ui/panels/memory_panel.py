"""
Wellz Memory Panel - RAM and swap usage display
"""

from typing import Dict, Any, List, Optional
from ..widgets.graph import create_graph
from ..widgets.bar import create_bar
from ..widgets.box import create_box_top, create_box_line, create_box_bottom, create_box_separator


class MemoryPanel:
    """Memory monitoring panel with graph"""

    def __init__(self, width: int = 40, show_graph: bool = True,
                 graph_height: int = 5, graph_style: str = "braille"):
        """
        Initialize memory panel.

        Args:
            width: Panel width
            show_graph: Whether to show history graph
            graph_height: Height of graph in lines
            graph_style: Graph style (braille, block, ascii)
        """
        self.width = width
        self.show_graph = show_graph
        self.graph_height = graph_height
        self.graph_renderer = create_graph(graph_style)
        self.theme: Dict[str, str] = {}

    def set_theme(self, theme: Dict[str, str]) -> None:
        """Set color theme"""
        self.theme = theme

    def render(self, mem_data: Dict[str, Any],
               history: Optional[List[float]] = None) -> List[str]:
        """
        Render the memory panel.

        Args:
            mem_data: Memory data from collectors.get_memory_info()
            history: Optional history data for graph

        Returns:
            List of lines
        """
        RESET = "\033[0m"
        lines = []

        border_color = self.theme.get("border", "\033[90m")
        title_color = self.theme.get("mem", "\033[94m")
        label_color = self.theme.get("label", "\033[97m")
        graph_color = self.theme.get("graph_fill", "\033[96m")

        # Top border
        lines.append(create_box_top(self.width, "MEMORY", border_color, title_color))

        # Graph (if enabled and history available)
        if self.show_graph and history:
            graph_width = self.width - 4
            graph_lines = self.graph_renderer.render(
                history, graph_width, self.graph_height,
                min_val=0, max_val=100,
                color=graph_color
            )
            for gline in graph_lines:
                lines.append(create_box_line(gline, self.width, border_color))

            lines.append(create_box_separator(self.width, border_color))

        # RAM usage bar
        ram_percent = mem_data.get("percent", 0)
        ram_used = mem_data.get("used", 0)
        ram_total = mem_data.get("total", 0)

        bar_width = self.width - 24
        bar = create_bar(ram_percent, width=bar_width)
        ram_line = f"{label_color}RAM{RESET}    [{bar}] {ram_used:.1f}/{ram_total:.1f}GB"
        lines.append(create_box_line(ram_line, self.width, border_color))

        # Available memory
        available = mem_data.get("available", 0)
        avail_line = f"{label_color}Avail{RESET}  {available:.1f}GB"
        lines.append(create_box_line(avail_line, self.width, border_color))

        # Swap usage (if present)
        swap_total = mem_data.get("swap_total", 0)
        if swap_total > 0:
            swap_percent = mem_data.get("swap_percent", 0)
            swap_used = mem_data.get("swap_used", 0)

            bar = create_bar(swap_percent, width=bar_width)
            swap_line = f"{label_color}Swap{RESET}   [{bar}] {swap_used:.1f}/{swap_total:.1f}GB"
            lines.append(create_box_line(swap_line, self.width, border_color))

        # Bottom border
        lines.append(create_box_bottom(self.width, border_color))

        return lines
