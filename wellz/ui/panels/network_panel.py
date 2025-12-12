"""
Wellz Network Panel - Network usage and speed display
"""

from typing import Dict, Any, List, Optional, Tuple
from ..widgets.graph import BrailleGraph, create_graph
from ..widgets.box import create_box_top, create_box_line, create_box_bottom, create_box_separator


def format_speed(bytes_per_sec: float) -> str:
    """Format bytes/second to human readable speed"""
    if bytes_per_sec < 1024:
        return f"{bytes_per_sec:.0f} B/s"
    elif bytes_per_sec < 1024 * 1024:
        return f"{bytes_per_sec / 1024:.1f} KB/s"
    elif bytes_per_sec < 1024 * 1024 * 1024:
        return f"{bytes_per_sec / (1024 * 1024):.1f} MB/s"
    else:
        return f"{bytes_per_sec / (1024 * 1024 * 1024):.2f} GB/s"


def format_bytes(total_bytes: int) -> str:
    """Format total bytes to human readable"""
    if total_bytes < 1024:
        return f"{total_bytes}B"
    elif total_bytes < 1024 * 1024:
        return f"{total_bytes / 1024:.1f}KB"
    elif total_bytes < 1024 * 1024 * 1024:
        return f"{total_bytes / (1024 * 1024):.1f}MB"
    else:
        return f"{total_bytes / (1024 * 1024 * 1024):.1f}GB"


class NetworkPanel:
    """Network monitoring panel with speed graph"""

    def __init__(self, width: int = 40, show_graph: bool = True,
                 graph_height: int = 5, graph_style: str = "braille"):
        """
        Initialize network panel.

        Args:
            width: Panel width
            show_graph: Whether to show speed graph
            graph_height: Height of graph in lines
            graph_style: Graph style (braille, block, ascii)
        """
        self.width = width
        self.show_graph = show_graph
        self.graph_height = graph_height
        self.graph_renderer = BrailleGraph() if graph_style == "braille" else create_graph(graph_style)
        self.theme: Dict[str, str] = {}

    def set_theme(self, theme: Dict[str, str]) -> None:
        """Set color theme"""
        self.theme = theme

    def render(self, net_data: Dict[str, Any],
               upload_speed: float = 0,
               download_speed: float = 0,
               upload_history: Optional[List[float]] = None,
               download_history: Optional[List[float]] = None) -> List[str]:
        """
        Render the network panel.

        Args:
            net_data: Network data from collectors.get_network_info()
            upload_speed: Current upload speed in bytes/sec
            download_speed: Current download speed in bytes/sec
            upload_history: Upload speed history for graph
            download_history: Download speed history for graph

        Returns:
            List of lines
        """
        RESET = "\033[0m"
        lines = []

        border_color = self.theme.get("border", "\033[90m")
        title_color = self.theme.get("net", "\033[96m")
        label_color = self.theme.get("label", "\033[97m")
        low_color = self.theme.get("low", "\033[92m")
        accent_color = self.theme.get("accent", "\033[95m")

        # Top border
        lines.append(create_box_top(self.width, "NETWORK", border_color, title_color))

        # Hostname
        hostname = net_data.get("hostname", "Unknown")
        lines.append(create_box_line(f"{label_color}Host{RESET}  {hostname}", self.width, border_color))

        # IP addresses (show first 2)
        ips = net_data.get("ips", {})
        for iface, ip in list(ips.items())[:2]:
            iface_short = iface[:6]
            lines.append(create_box_line(f"{label_color}{iface_short:<6}{RESET} {ip}", self.width, border_color))

        lines.append(create_box_separator(self.width, border_color))

        # Graph (if enabled and history available)
        if self.show_graph and upload_history and download_history:
            graph_width = self.width - 4

            # Find max for scaling
            all_speeds = upload_history + download_history
            max_speed = max(all_speeds) if all_speeds else 1
            if max_speed < 1024:
                max_speed = 1024  # Minimum 1 KB/s scale

            # Render dual graph for upload/download
            if isinstance(self.graph_renderer, BrailleGraph):
                graph_lines = self.graph_renderer.render_dual(
                    upload_history, download_history,
                    graph_width, self.graph_height,
                    min_val=0, max_val=max_speed,
                    color1=low_color, color2=accent_color
                )
            else:
                # Fallback: just show download
                graph_lines = self.graph_renderer.render(
                    download_history, graph_width, self.graph_height,
                    min_val=0, max_val=max_speed,
                    color=accent_color
                )

            for gline in graph_lines:
                lines.append(create_box_line(gline, self.width, border_color))

            lines.append(create_box_separator(self.width, border_color))

        # Current speeds
        up_str = format_speed(upload_speed)
        down_str = format_speed(download_speed)
        speed_line = f"{low_color}^ {up_str:<12}{RESET} {accent_color}v {down_str}{RESET}"
        lines.append(create_box_line(speed_line, self.width, border_color))

        # Total transferred
        tx = net_data.get("bytes_sent", 0)
        rx = net_data.get("bytes_recv", 0)
        totals_line = f"{low_color}TX{RESET} {format_bytes(tx):<12} {accent_color}RX{RESET} {format_bytes(rx)}"
        lines.append(create_box_line(totals_line, self.width, border_color))

        # Bottom border
        lines.append(create_box_bottom(self.width, border_color))

        return lines
