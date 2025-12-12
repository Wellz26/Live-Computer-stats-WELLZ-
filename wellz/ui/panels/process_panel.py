"""
Wellz Process Panel - Process list with sorting and selection
"""

from typing import Dict, Any, List, Optional
from ..widgets.box import create_box_top, create_box_line, create_box_bottom, create_box_separator


class ProcessPanel:
    """Process list panel with sorting and tree view"""

    def __init__(self, width: int = 80, height: int = 15):
        """
        Initialize process panel.

        Args:
            width: Panel width
            height: Panel height (including borders)
        """
        self.width = width
        self.height = height
        self.theme: Dict[str, str] = {}

        # Selection state
        self.selected_index = 0
        self.scroll_offset = 0

        # Sort state
        self.sort_by = "cpu"
        self.sort_descending = True

        # Display options
        self.tree_view = False
        self.search_filter = ""

    def set_theme(self, theme: Dict[str, str]) -> None:
        """Set color theme"""
        self.theme = theme

    def set_sort(self, sort_by: str, descending: bool = True) -> None:
        """Set sort column and direction"""
        self.sort_by = sort_by
        self.sort_descending = descending

    def toggle_tree_view(self) -> bool:
        """Toggle tree view mode, returns new state"""
        self.tree_view = not self.tree_view
        return self.tree_view

    def set_filter(self, filter_str: str) -> None:
        """Set search filter"""
        self.search_filter = filter_str.lower()
        self.selected_index = 0
        self.scroll_offset = 0

    def move_selection(self, delta: int) -> None:
        """Move selection by delta"""
        self.selected_index += delta

    def select_top(self) -> None:
        """Select first item"""
        self.selected_index = 0
        self.scroll_offset = 0

    def select_bottom(self, total: int) -> None:
        """Select last item"""
        self.selected_index = max(0, total - 1)

    def get_selected_pid(self, processes: List[Dict[str, Any]]) -> Optional[int]:
        """Get PID of selected process"""
        filtered = self._filter_processes(processes)
        if 0 <= self.selected_index < len(filtered):
            return filtered[self.selected_index].get("pid")
        return None

    def _filter_processes(self, processes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply search filter to processes"""
        if not self.search_filter:
            return processes
        return [p for p in processes
                if self.search_filter in p.get("name", "").lower()
                or self.search_filter in p.get("username", "").lower()
                or self.search_filter in str(p.get("pid", ""))]

    def render(self, processes: List[Dict[str, Any]]) -> List[str]:
        """
        Render the process panel.

        Args:
            processes: Process list from collectors.get_process_list()

        Returns:
            List of lines
        """
        RESET = "\033[0m"
        lines = []

        border_color = self.theme.get("border", "\033[90m")
        title_color = self.theme.get("process", "\033[97m")
        label_color = self.theme.get("label", "\033[97m")
        selected_color = self.theme.get("selected", "\033[96m")
        value_color = self.theme.get("value", "\033[37m")
        dim_color = "\033[90m"

        # Filter processes
        filtered = self._filter_processes(processes)

        # Clamp selection
        if filtered:
            self.selected_index = max(0, min(self.selected_index, len(filtered) - 1))
        else:
            self.selected_index = 0

        # Title with count
        title = f"PROCESSES ({len(filtered)})"
        if self.search_filter:
            title += f" /{self.search_filter}"
        if self.tree_view:
            title += " [TREE]"

        lines.append(create_box_top(self.width, title, border_color, title_color))

        # Header row
        # Sort indicators
        pid_sort = "v" if self.sort_by == "pid" else " "
        user_sort = "v" if self.sort_by == "name" else " "
        cpu_sort = "v" if self.sort_by == "cpu" else " "
        mem_sort = "v" if self.sort_by == "memory" else " "

        header = (f"{label_color}PID{pid_sort:<5}  "
                  f"USER{user_sort:<9}  "
                  f"CPU%{cpu_sort:<4}  "
                  f"MEM%{mem_sort:<4}  "
                  f"NAME{RESET}")
        lines.append(create_box_line(header, self.width, border_color))
        lines.append(create_box_separator(self.width, border_color))

        # Calculate visible area
        content_height = self.height - 4  # borders + header + separator

        # Adjust scroll offset to keep selection visible
        if self.selected_index < self.scroll_offset:
            self.scroll_offset = self.selected_index
        elif self.selected_index >= self.scroll_offset + content_height:
            self.scroll_offset = self.selected_index - content_height + 1

        # Render visible processes
        visible_start = self.scroll_offset
        visible_end = min(visible_start + content_height, len(filtered))

        for i in range(visible_start, visible_end):
            proc = filtered[i]
            is_selected = (i == self.selected_index)

            pid = proc.get("pid", 0)
            user = proc.get("username", "?")[:10]
            cpu = proc.get("cpu_percent", 0)
            mem = proc.get("memory_percent", 0)
            name = proc.get("name", "?")

            # Truncate name to fit
            max_name_len = self.width - 45
            if len(name) > max_name_len:
                name = name[:max_name_len - 2] + ".."

            # Tree indentation (if in tree view and has parent)
            tree_prefix = ""
            if self.tree_view:
                ppid = proc.get("ppid", 0)
                if ppid > 1:
                    tree_prefix = "  "

            # Color based on CPU/MEM usage
            if is_selected:
                row_color = selected_color
                prefix = ">"
            else:
                row_color = value_color
                prefix = " "

            # Format CPU/MEM with color
            cpu_color = self._get_usage_color(cpu)
            mem_color = self._get_usage_color(mem)

            line = (f"{row_color}{prefix}{RESET}"
                    f"{row_color}{pid:<7}{RESET}  "
                    f"{dim_color}{user:<10}{RESET}  "
                    f"{cpu_color}{cpu:5.1f}{RESET}  "
                    f"{mem_color}{mem:5.1f}{RESET}  "
                    f"{row_color}{tree_prefix}{name}{RESET}")

            lines.append(create_box_line(line, self.width, border_color))

        # Fill remaining rows if needed
        for _ in range(content_height - (visible_end - visible_start)):
            lines.append(create_box_line("", self.width, border_color))

        # Bottom border
        lines.append(create_box_bottom(self.width, border_color))

        return lines

    def _get_usage_color(self, percent: float) -> str:
        """Get color based on usage percentage"""
        if percent < 25:
            return self.theme.get("low", "\033[92m")
        elif percent < 50:
            return self.theme.get("mid", "\033[93m")
        else:
            return self.theme.get("high", "\033[91m")
