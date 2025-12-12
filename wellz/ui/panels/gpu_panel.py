"""
Wellz GPU Panel - GPU usage, VRAM, and temperature display
"""

from typing import Dict, Any, List, Optional
from ..widgets.graph import create_graph
from ..widgets.bar import create_bar
from ..widgets.box import create_box_top, create_box_line, create_box_bottom, create_box_separator


class GPUPanel:
    """GPU monitoring panel with usage graph"""

    def __init__(self, width: int = 40, show_graph: bool = True,
                 graph_height: int = 4, graph_style: str = "braille"):
        """
        Initialize GPU panel.

        Args:
            width: Panel width
            show_graph: Whether to show usage graph
            graph_height: Height of graph in lines
            graph_style: Graph style (braille, block, ascii)
        """
        self.width = width
        self.show_graph = show_graph
        self.graph_height = graph_height
        self.graph_renderer = create_graph(graph_style)
        self.theme: Dict[str, str] = {}
        self.temp_unit = "celsius"

    def set_theme(self, theme: Dict[str, str]) -> None:
        """Set color theme"""
        self.theme = theme

    def set_temp_unit(self, unit: str) -> None:
        """Set temperature unit (celsius or fahrenheit)"""
        self.temp_unit = unit

    def _format_temp(self, celsius: float) -> str:
        """Format temperature with unit"""
        if self.temp_unit == "fahrenheit":
            return f"{celsius * 9/5 + 32:.0f}F"
        return f"{celsius:.0f}C"

    def render(self, gpu_data: Dict[str, Any],
               history: Optional[List[float]] = None) -> List[str]:
        """
        Render the GPU panel.

        Args:
            gpu_data: GPU data from collectors.get_gpu_info()
            history: Optional usage history for graph

        Returns:
            List of lines
        """
        RESET = "\033[0m"
        lines = []

        border_color = self.theme.get("border", "\033[90m")
        title_color = self.theme.get("gpu", "\033[93m")
        label_color = self.theme.get("label", "\033[97m")
        value_color = self.theme.get("value", "\033[37m")
        graph_color = self.theme.get("graph_fill", "\033[96m")

        # Top border
        lines.append(create_box_top(self.width, "GPU", border_color, title_color))

        # GPU name
        gpu_name = gpu_data.get("name", "No GPU detected")
        max_name_len = self.width - 4
        if len(gpu_name) > max_name_len:
            gpu_name = gpu_name[:max_name_len - 3] + "..."
        lines.append(create_box_line(f"{value_color}{gpu_name}{RESET}", self.width, border_color))

        usage = gpu_data.get("usage")

        if usage is not None:
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

            # Usage bar
            bar_width = self.width - 20
            bar = create_bar(usage, width=bar_width)
            usage_line = f"{label_color}Usage{RESET}  [{bar}] {usage:5.1f}%"
            lines.append(create_box_line(usage_line, self.width, border_color))

            # VRAM usage
            vram_used = gpu_data.get("vram_used")
            vram_total = gpu_data.get("vram_total")
            if vram_used is not None and vram_total is not None and vram_total > 0:
                vram_percent = (vram_used / vram_total) * 100
                bar = create_bar(vram_percent, width=bar_width)
                vram_line = f"{label_color}VRAM{RESET}   [{bar}] {vram_used:.0f}/{vram_total:.0f}MB"
                lines.append(create_box_line(vram_line, self.width, border_color))

            # Temperature
            temp = gpu_data.get("temp")
            if temp is not None:
                temp_color = self._get_temp_color(temp)
                temp_str = self._format_temp(temp)
                temp_line = f"{label_color}Temp{RESET}   {temp_color}{temp_str}{RESET}"
                lines.append(create_box_line(temp_line, self.width, border_color))
        else:
            # No GPU stats available
            dim_color = "\033[90m"
            lines.append(create_box_line(f"{dim_color}Stats unavailable{RESET}", self.width, border_color))

        # Bottom border
        lines.append(create_box_bottom(self.width, border_color))

        return lines

    def _get_temp_color(self, temp: float) -> str:
        """Get color based on GPU temperature"""
        if temp < 60:
            return self.theme.get("low", "\033[92m")
        elif temp < 80:
            return self.theme.get("mid", "\033[93m")
        else:
            return self.theme.get("high", "\033[91m")
