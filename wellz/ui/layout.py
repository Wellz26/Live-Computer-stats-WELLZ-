"""
Wellz Layout Manager - Responsive panel layout
"""

from typing import List, Tuple, Optional
import os


class Layout:
    """Manages responsive panel layout based on terminal size"""

    # Minimum sizes
    MIN_WIDTH = 80
    MIN_HEIGHT = 24

    # Panel widths
    PANEL_WIDTH_SMALL = 38
    PANEL_WIDTH_MEDIUM = 42
    PANEL_WIDTH_LARGE = 50

    def __init__(self):
        """Initialize layout manager"""
        self.term_width = 100
        self.term_height = 40
        self.panel_width = self.PANEL_WIDTH_SMALL
        self.update_size()

    def update_size(self) -> Tuple[int, int]:
        """
        Update terminal size and recalculate layout.

        Returns:
            Tuple of (width, height)
        """
        try:
            size = os.get_terminal_size()
            self.term_width = max(self.MIN_WIDTH, size.columns)
            self.term_height = max(self.MIN_HEIGHT, size.lines)
        except:
            self.term_width = 100
            self.term_height = 40

        # Calculate panel width based on terminal width
        if self.term_width >= 160:
            self.panel_width = self.PANEL_WIDTH_LARGE
        elif self.term_width >= 100:
            self.panel_width = self.PANEL_WIDTH_MEDIUM
        else:
            self.panel_width = self.PANEL_WIDTH_SMALL

        return self.term_width, self.term_height

    def get_panel_width(self) -> int:
        """Get current panel width"""
        return self.panel_width

    def get_graph_height(self) -> int:
        """Get graph height based on terminal height"""
        if self.term_height >= 50:
            return 6
        elif self.term_height >= 40:
            return 5
        else:
            return 4

    def get_process_height(self) -> int:
        """Get process panel height"""
        # Leave room for other panels
        return max(10, self.term_height - 35)

    def can_fit_side_by_side(self, num_panels: int = 2) -> bool:
        """Check if panels can fit side by side"""
        return self.term_width >= (self.panel_width + 2) * num_panels

    def combine_rows(self, *rows: List[str], gap: int = 2) -> List[str]:
        """
        Combine multiple panel columns side by side.

        Args:
            *rows: Panel render outputs to combine
            gap: Space between panels

        Returns:
            Combined lines
        """
        if not rows:
            return []

        # Filter out empty rows
        rows = [r for r in rows if r]
        if not rows:
            return []

        # Find max height
        max_height = max(len(r) for r in rows)

        # Pad shorter columns
        padded = []
        for row in rows:
            if row:
                # Get width from first line (accounting for ANSI codes)
                first_line = row[0] if row else ""
                visible_width = self._visible_len(first_line)

                # Pad to max height
                while len(row) < max_height:
                    row.append(" " * visible_width)
                padded.append(row)

        # Combine lines
        combined = []
        gap_str = " " * gap
        for i in range(max_height):
            line_parts = []
            for col in padded:
                if i < len(col):
                    line_parts.append(col[i])
            combined.append(gap_str.join(line_parts))

        return combined

    @staticmethod
    def _visible_len(text: str) -> int:
        """Get visible length excluding ANSI codes"""
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return len(ansi_escape.sub('', text))

    def center_text(self, text: str, width: Optional[int] = None) -> str:
        """Center text within width"""
        w = width or self.term_width
        visible = self._visible_len(text)
        if visible >= w:
            return text
        padding = (w - visible) // 2
        return " " * padding + text

    def render_header(self, version: str = "2.0.0") -> List[str]:
        """Render the WELLZ header"""
        BRIGHT_CYAN = "\033[96m"
        BOLD = "\033[1m"
        RESET = "\033[0m"

        header_lines = [
            f"{BRIGHT_CYAN}{BOLD}██╗    ██╗███████╗██╗     ██╗     ███████╗{RESET}",
            f"{BRIGHT_CYAN}{BOLD}██║    ██║██╔════╝██║     ██║     ╚══███╔╝{RESET}",
            f"{BRIGHT_CYAN}{BOLD}██║ █╗ ██║█████╗  ██║     ██║       ███╔╝ {RESET}",
            f"{BRIGHT_CYAN}{BOLD}██║███╗██║██╔══╝  ██║     ██║      ███╔╝  {RESET}",
            f"{BRIGHT_CYAN}{BOLD}╚███╔███╔╝███████╗███████╗███████╗███████╗{RESET}",
            f"{BRIGHT_CYAN}{BOLD} ╚══╝╚══╝ ╚══════╝╚══════╝╚══════╝╚══════╝{RESET}",
        ]

        # Center header if terminal is wide enough
        if self.term_width > 50:
            header_lines = [self.center_text(line) for line in header_lines]

        return [""] + header_lines + [""]

    def render_footer(self, version: str = "2.0.0", theme: str = "default",
                      refresh_rate: float = 1.0, live: bool = True) -> List[str]:
        """Render the footer with status info"""
        DIM = "\033[90m"
        GREEN = "\033[92m"
        RESET = "\033[0m"

        status_parts = [f"Wellz v{version}"]
        if live:
            status_parts.append(f"{GREEN}[LIVE {refresh_rate}s]{RESET}")
        status_parts.append(f"Theme: {theme}")
        status_parts.append("Press ? for help")

        status = f"{DIM}{' | '.join(status_parts)}{RESET}"

        footer = [
            "",
            f"  {DIM}{'─' * (self.term_width - 4)}{RESET}",
            f"  {status}",
            "",
        ]

        return footer


class LayoutManager:
    """High-level layout manager for the dashboard"""

    def __init__(self):
        self.layout = Layout()

        # Panel visibility
        self.show_cpu = True
        self.show_memory = True
        self.show_network = True
        self.show_disk = True
        self.show_gpu = True
        self.show_processes = True
        self.show_header = True

    def toggle_panel(self, panel: str) -> bool:
        """Toggle panel visibility, returns new state"""
        attr = f"show_{panel}"
        if hasattr(self, attr):
            setattr(self, attr, not getattr(self, attr))
            return getattr(self, attr)
        return False

    def update_size(self) -> Tuple[int, int]:
        """Update terminal size"""
        return self.layout.update_size()

    def get_panel_config(self) -> dict:
        """Get panel configuration based on current layout"""
        return {
            "width": self.layout.get_panel_width(),
            "graph_height": self.layout.get_graph_height(),
            "process_height": self.layout.get_process_height(),
        }
