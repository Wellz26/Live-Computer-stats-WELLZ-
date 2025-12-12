"""
Wellz CPU Panel - CPU usage display with graph
"""

from typing import Dict, Any, List, Optional
from ..widgets.graph import create_graph, sparkline
from ..widgets.bar import create_bar
from ..widgets.box import create_box_top, create_box_line, create_box_bottom, create_box_separator


class CPUPanel:
    """CPU monitoring panel with graph and per-core display"""

    def __init__(self, width: int = 40, show_graph: bool = True,
                 graph_height: int = 5, graph_style: str = "braille"):
        """
        Initialize CPU panel.

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
        self.max_cores_display = 8
        self.theme: Dict[str, str] = {}

    def set_theme(self, theme: Dict[str, str]) -> None:
        """Set color theme"""
        self.theme = theme

    def render(self, cpu_data: Dict[str, Any],
               history: Optional[List[float]] = None) -> List[str]:
        """
        Render the CPU panel.

        Args:
            cpu_data: CPU data from collectors.get_cpu_info()
            history: Optional history data for graph

        Returns:
            List of lines
        """
        RESET = "\033[0m"
        lines = []

        border_color = self.theme.get("border", "\033[90m")
        title_color = self.theme.get("cpu", "\033[92m")
        label_color = self.theme.get("label", "\033[97m")
        value_color = self.theme.get("value", "\033[37m")
        graph_color = self.theme.get("graph_fill", "\033[96m")

        # Top border with title
        lines.append(create_box_top(self.width, "CPU", border_color, title_color))

        # CPU model (truncated if needed)
        model = cpu_data.get("model", "Unknown CPU")
        max_model_len = self.width - 4
        if len(model) > max_model_len:
            model = model[:max_model_len - 3] + "..."
        lines.append(create_box_line(f"{value_color}{model}{RESET}", self.width, border_color))

        # Cores, threads, frequency
        cores = cpu_data.get("cores", 0)
        threads = cpu_data.get("threads", 0)
        freq = cpu_data.get("freq_current", 0)
        info_line = (f"{label_color}Cores{RESET} {cores}  "
                     f"{label_color}Threads{RESET} {threads}  "
                     f"{label_color}Freq{RESET} {freq:.0f}MHz")
        lines.append(create_box_line(info_line, self.width, border_color))

        # Separator
        lines.append(create_box_separator(self.width, border_color))

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

        # Total CPU usage bar
        usage = cpu_data.get("usage", 0)
        bar = create_bar(usage, width=self.width - 18)
        total_line = f"{label_color}Total{RESET}  [{bar}] {usage:5.1f}%"
        lines.append(create_box_line(total_line, self.width, border_color))

        # Per-core usage (compact display)
        per_core = cpu_data.get("per_core", [])[:self.max_cores_display]
        if per_core:
            # Display cores in rows of 4
            core_strs = []
            for i, usage in enumerate(per_core):
                color = self._get_usage_color(usage)
                # Mini bar using block chars
                bar_len = int(usage / 20)  # 5 chars max
                bar_str = "█" * bar_len
                core_strs.append(f"{label_color}{i}{RESET}{color}{bar_str:<5}{RESET}")

            # Split into rows of 4
            for row_start in range(0, len(core_strs), 4):
                row = core_strs[row_start:row_start + 4]
                lines.append(create_box_line(" ".join(row), self.width, border_color))

        # Bottom border
        lines.append(create_box_bottom(self.width, border_color))

        return lines

    def _get_usage_color(self, percent: float) -> str:
        """Get color based on usage percentage"""
        if percent < 50:
            return self.theme.get("low", "\033[92m")
        elif percent < 80:
            return self.theme.get("mid", "\033[93m")
        else:
            return self.theme.get("high", "\033[91m")
