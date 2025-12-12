"""
Wellz Disk Panel - Disk usage and I/O display
"""

from typing import Dict, Any, List, Optional, Tuple
from ..widgets.graph import BrailleGraph, create_graph
from ..widgets.bar import create_bar
from ..widgets.box import create_box_top, create_box_line, create_box_bottom, create_box_separator


def format_speed(bytes_per_sec: float) -> str:
    """Format bytes/second to human readable speed"""
    if bytes_per_sec < 1024:
        return f"{bytes_per_sec:.0f}B/s"
    elif bytes_per_sec < 1024 * 1024:
        return f"{bytes_per_sec / 1024:.1f}KB/s"
    elif bytes_per_sec < 1024 * 1024 * 1024:
        return f"{bytes_per_sec / (1024 * 1024):.1f}MB/s"
    else:
        return f"{bytes_per_sec / (1024 * 1024 * 1024):.2f}GB/s"


class DiskPanel:
    """Disk usage and I/O monitoring panel"""

    def __init__(self, width: int = 40, show_graph: bool = True,
                 graph_height: int = 4, graph_style: str = "braille",
                 max_disks: int = 3):
        """
        Initialize disk panel.

        Args:
            width: Panel width
            show_graph: Whether to show I/O graph
            graph_height: Height of graph in lines
            graph_style: Graph style (braille, block, ascii)
            max_disks: Maximum number of disks to display
        """
        self.width = width
        self.show_graph = show_graph
        self.graph_height = graph_height
        self.graph_renderer = BrailleGraph() if graph_style == "braille" else create_graph(graph_style)
        self.max_disks = max_disks
        self.theme: Dict[str, str] = {}

    def set_theme(self, theme: Dict[str, str]) -> None:
        """Set color theme"""
        self.theme = theme

    def render(self, disk_data: List[Dict[str, Any]],
               read_speed: float = 0,
               write_speed: float = 0,
               read_history: Optional[List[float]] = None,
               write_history: Optional[List[float]] = None) -> List[str]:
        """
        Render the disk panel.

        Args:
            disk_data: Disk data from collectors.get_disk_info()
            read_speed: Current read speed in bytes/sec
            write_speed: Current write speed in bytes/sec
            read_history: Read speed history for graph
            write_history: Write speed history for graph

        Returns:
            List of lines
        """
        RESET = "\033[0m"
        lines = []

        border_color = self.theme.get("border", "\033[90m")
        title_color = self.theme.get("disk", "\033[95m")
        label_color = self.theme.get("label", "\033[97m")
        low_color = self.theme.get("low", "\033[92m")
        accent_color = self.theme.get("accent", "\033[95m")

        # Top border
        lines.append(create_box_top(self.width, "DISK", border_color, title_color))

        # I/O Graph (if enabled and history available)
        if self.show_graph and read_history and write_history:
            graph_width = self.width - 4

            # Find max for scaling
            all_speeds = read_history + write_history
            max_speed = max(all_speeds) if all_speeds else 1
            if max_speed < 1024:
                max_speed = 1024 * 1024  # Minimum 1 MB/s scale

            # Render dual graph for read/write
            if isinstance(self.graph_renderer, BrailleGraph):
                graph_lines = self.graph_renderer.render_dual(
                    read_history, write_history,
                    graph_width, self.graph_height,
                    min_val=0, max_val=max_speed,
                    color1=low_color, color2=accent_color
                )
            else:
                graph_lines = self.graph_renderer.render(
                    read_history, graph_width, self.graph_height,
                    min_val=0, max_val=max_speed,
                    color=low_color
                )

            for gline in graph_lines:
                lines.append(create_box_line(gline, self.width, border_color))

            # I/O speeds
            read_str = format_speed(read_speed)
            write_str = format_speed(write_speed)
            io_line = f"{low_color}R:{RESET} {read_str:<10} {accent_color}W:{RESET} {write_str}"
            lines.append(create_box_line(io_line, self.width, border_color))

            lines.append(create_box_separator(self.width, border_color))

        # Disk usage bars
        for disk in disk_data[:self.max_disks]:
            mount = disk.get("mount", "/")
            # Truncate mount point if too long
            max_mount_len = 10
            if len(mount) > max_mount_len:
                mount = mount[:max_mount_len - 2] + ".."

            percent = disk.get("percent", 0)
            used = disk.get("used", 0)
            total = disk.get("total", 0)

            bar_width = self.width - 28
            bar = create_bar(percent, width=bar_width)
            disk_line = f"{label_color}{mount:<10}{RESET} [{bar}] {used:.0f}/{total:.0f}GB"
            lines.append(create_box_line(disk_line, self.width, border_color))

        # Bottom border
        lines.append(create_box_bottom(self.width, border_color))

        return lines
