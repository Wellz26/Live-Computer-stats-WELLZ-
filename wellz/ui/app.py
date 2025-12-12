"""
Wellz Application - Main interactive dashboard
"""

import sys
import time
import signal
from typing import Optional, List

from ..core import (
    get_cpu_info, get_gpu_info, get_memory_info,
    get_disk_info, get_disk_io, get_network_info, get_system_info,
    get_os_type, get_os_logo, get_process_list, SystemHistory
)
from ..config import get_config, get_theme, get_theme_names
from .layout import Layout, LayoutManager
from .input_handler import InputHandler, Action, NonBlockingInput
from .panels import (
    CPUPanel, MemoryPanel, NetworkPanel,
    DiskPanel, GPUPanel, ProcessPanel, HelpPanel
)


class WellzApp:
    """Main Wellz interactive application"""

    VERSION = "2.0.0"

    # ANSI codes
    CLEAR_SCREEN = "\033[2J\033[H"
    HIDE_CURSOR = "\033[?25l"
    SHOW_CURSOR = "\033[?25h"
    RESET = "\033[0m"

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize Wellz application.

        Args:
            config_path: Optional custom config file path
        """
        # Load configuration
        self.config = get_config(config_path)

        # Initialize theme
        self.theme_names = get_theme_names()
        self.theme_index = self.theme_names.index(self.config.theme_name) \
            if self.config.theme_name in self.theme_names else 0
        self.theme = get_theme(self.theme_names[self.theme_index])

        # Initialize layout
        self.layout_manager = LayoutManager()
        self.layout = self.layout_manager.layout

        # Initialize history tracking
        self.history = SystemHistory(self.config.history_size)

        # Initialize panels
        self._init_panels()

        # State
        self.running = False
        self.refresh_rate = self.config.refresh_rate
        self.show_help = False
        self.search_mode = False
        self.search_query = ""

        # Process update counter (update less frequently)
        self.process_update_counter = 0
        self.process_update_interval = self.config.get("processes", "update_interval", 2)

        # Setup signal handlers
        signal.signal(signal.SIGWINCH, self._handle_resize)

    def _init_panels(self) -> None:
        """Initialize all panels with current settings"""
        panel_config = self.layout_manager.get_panel_config()
        width = panel_config["width"]
        graph_height = panel_config["graph_height"]
        graph_style = self.config.graph_style

        self.cpu_panel = CPUPanel(width, self.config.show_graphs, graph_height, graph_style)
        self.memory_panel = MemoryPanel(width, self.config.show_graphs, graph_height, graph_style)
        self.network_panel = NetworkPanel(width, self.config.show_graphs, graph_height, graph_style)
        self.disk_panel = DiskPanel(width, self.config.show_graphs, graph_height - 1, graph_style)
        self.gpu_panel = GPUPanel(width, self.config.show_graphs, graph_height - 1, graph_style)

        process_width = min(width * 2 + 4, self.layout.term_width - 4)
        process_height = panel_config["process_height"]
        self.process_panel = ProcessPanel(process_width, process_height)

        self.help_panel = HelpPanel(60)

        # Apply theme to all panels
        self._apply_theme()

    def _apply_theme(self) -> None:
        """Apply current theme to all panels"""
        self.cpu_panel.set_theme(self.theme)
        self.memory_panel.set_theme(self.theme)
        self.network_panel.set_theme(self.theme)
        self.disk_panel.set_theme(self.theme)
        self.gpu_panel.set_theme(self.theme)
        self.process_panel.set_theme(self.theme)
        self.help_panel.set_theme(self.theme)
        self.gpu_panel.set_temp_unit(self.config.temp_unit)

    def _handle_resize(self, signum, frame) -> None:
        """Handle terminal resize"""
        self.layout.update_size()
        self._init_panels()

    def next_theme(self) -> None:
        """Switch to next theme"""
        self.theme_index = (self.theme_index + 1) % len(self.theme_names)
        self.theme = get_theme(self.theme_names[self.theme_index])
        self._apply_theme()

    def prev_theme(self) -> None:
        """Switch to previous theme"""
        self.theme_index = (self.theme_index - 1) % len(self.theme_names)
        self.theme = get_theme(self.theme_names[self.theme_index])
        self._apply_theme()

    def adjust_refresh_rate(self, delta: float) -> None:
        """Adjust refresh rate"""
        self.refresh_rate = max(0.5, min(10.0, self.refresh_rate + delta))

    def collect_data(self) -> dict:
        """Collect all system data"""
        data = {
            "cpu": get_cpu_info(interval=0.05),
            "memory": get_memory_info(),
            "network": get_network_info(),
            "disk": get_disk_info(),
            "disk_io": get_disk_io(),
            "gpu": get_gpu_info(),
            "system": get_system_info(),
            "os_type": get_os_type(),
        }

        # Update history
        self.history.update_cpu(data["cpu"]["usage"], data["cpu"]["per_core"])
        self.history.update_memory(data["memory"]["percent"], data["memory"]["swap_percent"])

        up_speed, down_speed = self.history.update_network(
            data["network"]["bytes_sent"],
            data["network"]["bytes_recv"]
        )
        data["upload_speed"] = up_speed
        data["download_speed"] = down_speed

        read_speed, write_speed = self.history.update_disk_io(
            data["disk_io"]["read_bytes"],
            data["disk_io"]["write_bytes"]
        )
        data["read_speed"] = read_speed
        data["write_speed"] = write_speed

        gpu = data["gpu"]
        vram_pct = (gpu["vram_used"] / gpu["vram_total"] * 100) \
            if gpu.get("vram_total") else None
        self.history.update_gpu(gpu.get("usage"), vram_pct, gpu.get("temp"))

        # Update processes periodically
        self.process_update_counter += 1
        if self.process_update_counter >= self.process_update_interval:
            data["processes"] = get_process_list(
                sort_by=self.process_panel.sort_by,
                limit=self.config.max_processes + 10
            )
            self.process_update_counter = 0
        else:
            data["processes"] = None

        return data

    def render(self, data: dict, processes: List[dict]) -> str:
        """Render the full dashboard"""
        output_lines = []

        # Header
        if self.layout_manager.show_header:
            output_lines.extend(self.layout.render_header(self.VERSION))

        # Get graph width for history
        graph_width = self.layout.get_panel_width() - 4

        # Row 1: System/CPU + GPU/Memory
        row1_left = []
        row1_right = []

        if self.layout_manager.show_cpu:
            cpu_history = self.history.get_cpu_graph_data(graph_width)
            row1_left = self.cpu_panel.render(data["cpu"], cpu_history)

        if self.layout_manager.show_memory:
            mem_history = self.history.get_memory_graph_data(graph_width)
            row1_right = self.memory_panel.render(data["memory"], mem_history)

        if row1_left or row1_right:
            combined = self.layout.combine_rows(row1_left, row1_right)
            output_lines.extend(["  " + line for line in combined])
            output_lines.append("")

        # Row 2: GPU + Network
        row2_left = []
        row2_right = []

        if self.layout_manager.show_gpu:
            gpu_history = self.history.get_gpu_graph_data(graph_width)
            row2_left = self.gpu_panel.render(data["gpu"], gpu_history)

        if self.layout_manager.show_network:
            up_hist, down_hist = self.history.get_network_graph_data(graph_width)
            row2_right = self.network_panel.render(
                data["network"],
                data["upload_speed"],
                data["download_speed"],
                up_hist, down_hist
            )

        if row2_left or row2_right:
            combined = self.layout.combine_rows(row2_left, row2_right)
            output_lines.extend(["  " + line for line in combined])
            output_lines.append("")

        # Row 3: Disk
        if self.layout_manager.show_disk:
            read_hist, write_hist = self.history.get_disk_io_graph_data(graph_width)
            disk_lines = self.disk_panel.render(
                data["disk"],
                data["read_speed"],
                data["write_speed"],
                read_hist, write_hist
            )
            output_lines.extend(["  " + line for line in disk_lines])
            output_lines.append("")

        # Row 4: Processes
        if self.layout_manager.show_processes and processes:
            process_lines = self.process_panel.render(processes)
            output_lines.extend(["  " + line for line in process_lines])

        # Footer
        output_lines.extend(self.layout.render_footer(
            self.VERSION,
            self.theme_names[self.theme_index],
            self.refresh_rate,
            live=True
        ))

        # Help overlay (if visible)
        if self.show_help:
            help_lines = self.help_panel.render()
            # Overlay help in center - for now just append
            output_lines.append("")
            output_lines.extend(["  " + line for line in help_lines])

        return "\n".join(output_lines)

    def handle_action(self, action: Action, input_handler: InputHandler) -> bool:
        """
        Handle user action.

        Args:
            action: Action to handle
            input_handler: Input handler for reading additional input

        Returns:
            False if should quit, True otherwise
        """
        if action == Action.QUIT:
            return False

        elif action == Action.TOGGLE_HELP:
            self.show_help = not self.show_help

        elif action == Action.UP:
            self.process_panel.move_selection(-1)

        elif action == Action.DOWN:
            self.process_panel.move_selection(1)

        elif action == Action.PAGE_UP:
            self.process_panel.move_selection(-10)

        elif action == Action.PAGE_DOWN:
            self.process_panel.move_selection(10)

        elif action == Action.TOP:
            self.process_panel.select_top()

        elif action == Action.BOTTOM:
            self.process_panel.select_bottom(100)  # Will be clamped

        elif action == Action.SEARCH:
            # Exit raw mode briefly for search input
            input_handler.exit_raw_mode()
            sys.stdout.write(f"\r{' ' * 60}\rSearch: ")
            sys.stdout.flush()
            try:
                query = input()
                self.process_panel.set_filter(query)
            except:
                pass
            input_handler.enter_raw_mode()

        elif action == Action.CANCEL:
            if self.show_help:
                self.show_help = False
            else:
                self.process_panel.set_filter("")

        elif action == Action.TOGGLE_TREE:
            self.process_panel.toggle_tree_view()

        elif action == Action.TOGGLE_CPU:
            self.layout_manager.show_cpu = not self.layout_manager.show_cpu

        elif action == Action.TOGGLE_MEMORY:
            self.layout_manager.show_memory = not self.layout_manager.show_memory

        elif action == Action.TOGGLE_NETWORK:
            self.layout_manager.show_network = not self.layout_manager.show_network

        elif action == Action.TOGGLE_DISK:
            self.layout_manager.show_disk = not self.layout_manager.show_disk

        elif action == Action.TOGGLE_GPU:
            self.layout_manager.show_gpu = not self.layout_manager.show_gpu

        elif action == Action.TOGGLE_PROCESSES:
            self.layout_manager.show_processes = not self.layout_manager.show_processes

        elif action == Action.THEME_NEXT:
            self.next_theme()

        elif action == Action.THEME_PREV:
            self.prev_theme()

        elif action == Action.REFRESH_UP:
            self.adjust_refresh_rate(-0.5)

        elif action == Action.REFRESH_DOWN:
            self.adjust_refresh_rate(0.5)

        elif action == Action.RESET_VIEW:
            self.layout_manager.show_cpu = True
            self.layout_manager.show_memory = True
            self.layout_manager.show_network = True
            self.layout_manager.show_disk = True
            self.layout_manager.show_gpu = True
            self.layout_manager.show_processes = True
            self.process_panel.set_filter("")
            self.show_help = False

        elif action == Action.KILL_PROCESS:
            pid = self.process_panel.get_selected_pid([])  # Need actual processes
            if pid:
                try:
                    import os
                    os.kill(pid, signal.SIGTERM)
                except:
                    pass

        return True

    def run(self) -> None:
        """Run the interactive dashboard"""
        self.running = True
        processes = []

        # Hide cursor and clear screen
        sys.stdout.write(self.HIDE_CURSOR)
        sys.stdout.write(self.CLEAR_SCREEN)
        sys.stdout.flush()

        try:
            with NonBlockingInput() as input_handler:
                while self.running:
                    # Collect data
                    data = self.collect_data()

                    # Update processes if new data available
                    if data["processes"] is not None:
                        processes = data["processes"]

                    # Render
                    sys.stdout.write(self.CLEAR_SCREEN)
                    sys.stdout.write(self.render(data, processes))
                    sys.stdout.flush()

                    # Handle input with timeout
                    start_time = time.time()
                    while time.time() - start_time < self.refresh_rate:
                        remaining = self.refresh_rate - (time.time() - start_time)
                        key = input_handler.read_key(timeout=min(0.1, remaining))
                        if key:
                            action = input_handler.get_action(key)
                            if not self.handle_action(action, input_handler):
                                self.running = False
                                break

        except KeyboardInterrupt:
            pass
        finally:
            # Show cursor and reset
            sys.stdout.write(self.SHOW_CURSOR)
            sys.stdout.write(self.RESET)
            sys.stdout.write("\n")
            sys.stdout.flush()

    def run_once(self) -> None:
        """Render dashboard once (non-interactive)"""
        data = self.collect_data()
        # Need to collect twice for speed calculations
        time.sleep(0.1)
        data = self.collect_data()
        processes = get_process_list(sort_by="cpu", limit=20)
        print(self.render(data, processes))
