#!/usr/bin/env python3
"""
Wellz GUI - Gaming PC Stats Widget v3.0
A premium system monitor widget with smooth charts and modern design
Inspired by btop and modern system monitors
"""

import subprocess
import sys
import threading
import time
import platform
import socket
import os
from collections import deque
from typing import Dict, List, Tuple, Optional

try:
    import tkinter as tk
    from tkinter import font as tkfont
    from tkinter import ttk
except ImportError:
    print("Error: tkinter not available. Install python3-tk")
    sys.exit(1)

try:
    import psutil
except ImportError:
    print("Error: psutil not installed. Run: pip install psutil")
    sys.exit(1)


# ============================================================================
# THEMES - Extended collection
# ============================================================================

THEMES = {
    "midnight": {
        "name": "Midnight",
        "bg": "#0a0e14",
        "bg_secondary": "#0d1117",
        "bg_card": "#161b22",
        "bg_card_hover": "#1c2128",
        "border": "#30363d",
        "border_light": "#484f58",
        "text": "#e6edf3",
        "text_secondary": "#8b949e",
        "text_dim": "#6e7681",
        "accent": "#58a6ff",
        "accent_secondary": "#388bfd",
        "cpu": "#3fb950",
        "cpu_gradient": ["#238636", "#3fb950", "#56d364"],
        "gpu": "#f0883e",
        "gpu_gradient": ["#bd561d", "#f0883e", "#f4a261"],
        "mem": "#58a6ff",
        "mem_gradient": ["#1f6feb", "#58a6ff", "#79c0ff"],
        "disk": "#a371f7",
        "disk_gradient": ["#8957e5", "#a371f7", "#d2a8ff"],
        "net": "#39d353",
        "net_gradient": ["#238636", "#39d353", "#6bc46d"],
        "temp": "#f85149",
        "temp_gradient": ["#da3633", "#f85149", "#ff7b72"],
        "success": "#3fb950",
        "warning": "#d29922",
        "danger": "#f85149",
        "chart_grid": "#21262d",
    },
    "dracula": {
        "name": "Dracula",
        "bg": "#1e1f29",
        "bg_secondary": "#21222c",
        "bg_card": "#282a36",
        "bg_card_hover": "#343746",
        "border": "#44475a",
        "border_light": "#6272a4",
        "text": "#f8f8f2",
        "text_secondary": "#bfbfbf",
        "text_dim": "#6272a4",
        "accent": "#bd93f9",
        "accent_secondary": "#ff79c6",
        "cpu": "#50fa7b",
        "cpu_gradient": ["#3ae374", "#50fa7b", "#69ff94"],
        "gpu": "#f1fa8c",
        "gpu_gradient": ["#e6db74", "#f1fa8c", "#ffffa5"],
        "mem": "#8be9fd",
        "mem_gradient": ["#6dd5ed", "#8be9fd", "#a4f0ff"],
        "disk": "#ff79c6",
        "disk_gradient": ["#ff5cac", "#ff79c6", "#ff92d0"],
        "net": "#bd93f9",
        "net_gradient": ["#9d79d9", "#bd93f9", "#d4afff"],
        "temp": "#ff5555",
        "temp_gradient": ["#ff3838", "#ff5555", "#ff7777"],
        "success": "#50fa7b",
        "warning": "#ffb86c",
        "danger": "#ff5555",
        "chart_grid": "#343746",
    },
    "nord": {
        "name": "Nord",
        "bg": "#242933",
        "bg_secondary": "#2e3440",
        "bg_card": "#3b4252",
        "bg_card_hover": "#434c5e",
        "border": "#4c566a",
        "border_light": "#616e88",
        "text": "#eceff4",
        "text_secondary": "#d8dee9",
        "text_dim": "#7b88a1",
        "accent": "#88c0d0",
        "accent_secondary": "#81a1c1",
        "cpu": "#a3be8c",
        "cpu_gradient": ["#8fbcbb", "#a3be8c", "#b4d89e"],
        "gpu": "#ebcb8b",
        "gpu_gradient": ["#d4a959", "#ebcb8b", "#f5dfa4"],
        "mem": "#81a1c1",
        "mem_gradient": ["#5e81ac", "#81a1c1", "#9cb6d3"],
        "disk": "#b48ead",
        "disk_gradient": ["#9d7a94", "#b48ead", "#c9a3c0"],
        "net": "#88c0d0",
        "net_gradient": ["#6ba5b5", "#88c0d0", "#a5d4e0"],
        "temp": "#bf616a",
        "temp_gradient": ["#a94d56", "#bf616a", "#d38086"],
        "success": "#a3be8c",
        "warning": "#ebcb8b",
        "danger": "#bf616a",
        "chart_grid": "#434c5e",
    },
    "cyberpunk": {
        "name": "Cyberpunk",
        "bg": "#0a0a0f",
        "bg_secondary": "#12121a",
        "bg_card": "#1a1a24",
        "bg_card_hover": "#24243a",
        "border": "#2d2d44",
        "border_light": "#4a4a6a",
        "text": "#ffffff",
        "text_secondary": "#b8b8d0",
        "text_dim": "#6a6a8a",
        "accent": "#00fff9",
        "accent_secondary": "#ff00ff",
        "cpu": "#00ff9f",
        "cpu_gradient": ["#00cc7a", "#00ff9f", "#4dffb8"],
        "gpu": "#ffee00",
        "gpu_gradient": ["#ccbe00", "#ffee00", "#fff74d"],
        "mem": "#00fff9",
        "mem_gradient": ["#00ccc7", "#00fff9", "#4dfffb"],
        "disk": "#ff00ff",
        "disk_gradient": ["#cc00cc", "#ff00ff", "#ff4dff"],
        "net": "#ff3366",
        "net_gradient": ["#cc2952", "#ff3366", "#ff6688"],
        "temp": "#ff6600",
        "temp_gradient": ["#cc5200", "#ff6600", "#ff8533"],
        "success": "#00ff9f",
        "warning": "#ffee00",
        "danger": "#ff3366",
        "chart_grid": "#1f1f2e",
    },
    "gruvbox": {
        "name": "Gruvbox",
        "bg": "#1d2021",
        "bg_secondary": "#282828",
        "bg_card": "#3c3836",
        "bg_card_hover": "#504945",
        "border": "#665c54",
        "border_light": "#7c6f64",
        "text": "#ebdbb2",
        "text_secondary": "#d5c4a1",
        "text_dim": "#a89984",
        "accent": "#fe8019",
        "accent_secondary": "#fabd2f",
        "cpu": "#b8bb26",
        "cpu_gradient": ["#98971a", "#b8bb26", "#d5d94a"],
        "gpu": "#fabd2f",
        "gpu_gradient": ["#d79921", "#fabd2f", "#fdd663"],
        "mem": "#83a598",
        "mem_gradient": ["#689d6a", "#83a598", "#9dbcb0"],
        "disk": "#d3869b",
        "disk_gradient": ["#b16286", "#d3869b", "#e4a4b4"],
        "net": "#8ec07c",
        "net_gradient": ["#6ba562", "#8ec07c", "#aed49c"],
        "temp": "#fb4934",
        "temp_gradient": ["#cc241d", "#fb4934", "#fc6e5f"],
        "success": "#b8bb26",
        "warning": "#fabd2f",
        "danger": "#fb4934",
        "chart_grid": "#504945",
    },
    "tokyo": {
        "name": "Tokyo Night",
        "bg": "#16161e",
        "bg_secondary": "#1a1b26",
        "bg_card": "#24283b",
        "bg_card_hover": "#2f3451",
        "border": "#3b4261",
        "border_light": "#545c7e",
        "text": "#c0caf5",
        "text_secondary": "#a9b1d6",
        "text_dim": "#565f89",
        "accent": "#7aa2f7",
        "accent_secondary": "#bb9af7",
        "cpu": "#9ece6a",
        "cpu_gradient": ["#7eb356", "#9ece6a", "#b4de8a"],
        "gpu": "#e0af68",
        "gpu_gradient": ["#c99a52", "#e0af68", "#ecc488"],
        "mem": "#7aa2f7",
        "mem_gradient": ["#5a8af7", "#7aa2f7", "#9abaff"],
        "disk": "#bb9af7",
        "disk_gradient": ["#9d7af7", "#bb9af7", "#d4baff"],
        "net": "#7dcfff",
        "net_gradient": ["#5ab9e5", "#7dcfff", "#9ee0ff"],
        "temp": "#f7768e",
        "temp_gradient": ["#e55a74", "#f7768e", "#ff96aa"],
        "success": "#9ece6a",
        "warning": "#e0af68",
        "danger": "#f7768e",
        "chart_grid": "#2a2e42",
    },
    "catppuccin": {
        "name": "Catppuccin",
        "bg": "#11111b",
        "bg_secondary": "#1e1e2e",
        "bg_card": "#313244",
        "bg_card_hover": "#45475a",
        "border": "#45475a",
        "border_light": "#585b70",
        "text": "#cdd6f4",
        "text_secondary": "#bac2de",
        "text_dim": "#6c7086",
        "accent": "#cba6f7",
        "accent_secondary": "#f5c2e7",
        "cpu": "#a6e3a1",
        "cpu_gradient": ["#8bd587", "#a6e3a1", "#c0f0bb"],
        "gpu": "#f9e2af",
        "gpu_gradient": ["#f5d18a", "#f9e2af", "#fcf0cc"],
        "mem": "#89b4fa",
        "mem_gradient": ["#6a9cf7", "#89b4fa", "#a8ccfc"],
        "disk": "#f5c2e7",
        "disk_gradient": ["#f0a8d9", "#f5c2e7", "#fadcf0"],
        "net": "#94e2d5",
        "net_gradient": ["#76d4c3", "#94e2d5", "#b2f0e4"],
        "temp": "#f38ba8",
        "temp_gradient": ["#e96d8e", "#f38ba8", "#f8a9be"],
        "success": "#a6e3a1",
        "warning": "#f9e2af",
        "danger": "#f38ba8",
        "chart_grid": "#3b3d52",
    },
    "matrix": {
        "name": "Matrix",
        "bg": "#000000",
        "bg_secondary": "#0a0a0a",
        "bg_card": "#0d1a0d",
        "bg_card_hover": "#122612",
        "border": "#1a3a1a",
        "border_light": "#2a5a2a",
        "text": "#00ff00",
        "text_secondary": "#00cc00",
        "text_dim": "#008800",
        "accent": "#00ff00",
        "accent_secondary": "#00cc00",
        "cpu": "#00ff00",
        "cpu_gradient": ["#00aa00", "#00ff00", "#44ff44"],
        "gpu": "#00ff00",
        "gpu_gradient": ["#00aa00", "#00ff00", "#44ff44"],
        "mem": "#00ff00",
        "mem_gradient": ["#00aa00", "#00ff00", "#44ff44"],
        "disk": "#00ff00",
        "disk_gradient": ["#00aa00", "#00ff00", "#44ff44"],
        "net": "#00ff00",
        "net_gradient": ["#00aa00", "#00ff00", "#44ff44"],
        "temp": "#ff0000",
        "temp_gradient": ["#aa0000", "#ff0000", "#ff4444"],
        "success": "#00ff00",
        "warning": "#ffff00",
        "danger": "#ff0000",
        "chart_grid": "#0a1a0a",
    },
}


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_os_type() -> str:
    """Detect OS type"""
    system = platform.system().lower()
    if system == "linux":
        try:
            with open("/etc/os-release", "r") as f:
                content = f.read().lower()
                for distro in ["kali", "arch", "ubuntu", "debian", "fedora",
                               "manjaro", "mint", "pop", "redhat", "suse", "gentoo"]:
                    if distro in content:
                        return distro
        except:
            pass
        return "linux"
    elif system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    return "linux"


def get_os_name() -> str:
    """Get full OS name"""
    system = platform.system()
    if system == "Linux":
        try:
            with open("/etc/os-release", "r") as f:
                for line in f:
                    if line.startswith("PRETTY_NAME="):
                        return line.split("=")[1].strip().strip('"')
        except:
            pass
        return f"Linux {platform.release()}"
    elif system == "Darwin":
        return f"macOS {platform.mac_ver()[0]}"
    elif system == "Windows":
        return f"Windows {platform.release()}"
    return system


def format_bytes(b: float, per_second: bool = False) -> str:
    """Format bytes to human readable"""
    suffix = "/s" if per_second else ""
    if b >= 1024**3:
        return f"{b/1024**3:.1f} GB{suffix}"
    elif b >= 1024**2:
        return f"{b/1024**2:.1f} MB{suffix}"
    elif b >= 1024:
        return f"{b/1024:.1f} KB{suffix}"
    else:
        return f"{b:.0f} B{suffix}"


def interpolate_color(color1: str, color2: str, factor: float) -> str:
    """Interpolate between two hex colors"""
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
    r = int(r1 + (r2 - r1) * factor)
    g = int(g1 + (g2 - g1) * factor)
    b = int(b1 + (b2 - b1) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"


# ============================================================================
# SMOOTH LINE CHART WIDGET
# ============================================================================

class SmoothLineChart:
    """Smooth animated line chart with gradient fill"""

    def __init__(self, parent, width: int = 300, height: int = 80,
                 colors: List[str] = None, bg: str = "#161b22",
                 grid_color: str = "#21262d", maxlen: int = 60,
                 show_grid: bool = True, line_width: int = 2):

        self.data = deque([0.0] * maxlen, maxlen=maxlen)
        self.colors = colors or ["#1f6feb", "#58a6ff", "#79c0ff"]
        self.bg = bg
        self.grid_color = grid_color
        self.show_grid = show_grid
        self.line_width = line_width
        self.max_value = 100
        self.auto_scale = False

        self.canvas = tk.Canvas(parent, width=width, height=height,
                                bg=bg, highlightthickness=0)
        self.width = width
        self.height = height

        # Animation
        self.target_data = list(self.data)
        self.current_data = list(self.data)
        self.animating = False

    def pack(self, **kwargs):
        self.canvas.pack(**kwargs)

    def grid(self, **kwargs):
        self.canvas.grid(**kwargs)

    def update(self, value: float, animate: bool = True):
        """Add new value and redraw"""
        self.data.append(value)
        if self.auto_scale:
            self.max_value = max(max(self.data) * 1.1, 1)
        self.draw()

    def set_colors(self, colors: List[str], bg: str, grid: str):
        """Update colors"""
        self.colors = colors
        self.bg = bg
        self.grid_color = grid
        self.canvas.configure(bg=bg)

    def draw(self):
        """Draw the chart"""
        self.canvas.delete("all")

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10:
            w = self.width
        if h < 10:
            h = self.height

        padding = 4
        chart_h = h - padding * 2
        chart_w = w - padding * 2

        # Draw grid
        if self.show_grid:
            # Horizontal lines
            for i in range(5):
                y = padding + (chart_h * i / 4)
                self.canvas.create_line(padding, y, w - padding, y,
                                       fill=self.grid_color, width=1)
            # Vertical lines
            for i in range(7):
                x = padding + (chart_w * i / 6)
                self.canvas.create_line(x, padding, x, h - padding,
                                       fill=self.grid_color, width=1)

        if not self.data or max(self.data) == 0:
            return

        # Calculate points
        points = []
        data_list = list(self.data)
        step = chart_w / (len(data_list) - 1) if len(data_list) > 1 else chart_w

        for i, val in enumerate(data_list):
            x = padding + i * step
            normalized = min(val / self.max_value, 1.0)
            y = padding + chart_h - (normalized * chart_h)
            points.append((x, y))

        if len(points) < 2:
            return

        # Draw gradient fill
        fill_points = [(padding, h - padding)]
        fill_points.extend(points)
        fill_points.append((w - padding, h - padding))

        # Create gradient effect with multiple polygons
        num_bands = 8
        for i in range(num_bands):
            band_points = []
            factor = i / num_bands
            next_factor = (i + 1) / num_bands

            for px, py in points:
                band_top = py + (h - padding - py) * factor
                band_points.append((px, band_top))

            for px, py in reversed(points):
                band_bottom = py + (h - padding - py) * next_factor
                band_points.append((px, band_bottom))

            if len(band_points) >= 3:
                color = interpolate_color(self.colors[1], self.bg, factor * 0.85)
                flat = [coord for point in band_points for coord in point]
                self.canvas.create_polygon(flat, fill=color, outline="")

        # Draw smooth line using bezier-like curves
        if len(points) >= 2:
            # Create smooth curve points
            smooth_points = []
            for i in range(len(points)):
                smooth_points.extend(points[i])

            self.canvas.create_line(smooth_points, fill=self.colors[1],
                                   width=self.line_width, smooth=True,
                                   splinesteps=32)

            # Draw glow effect
            self.canvas.create_line(smooth_points, fill=self.colors[2],
                                   width=self.line_width + 2, smooth=True,
                                   splinesteps=32, stipple="gray50")


# ============================================================================
# ANIMATED PROGRESS BAR
# ============================================================================

class AnimatedProgressBar:
    """Smooth animated progress bar with gradient"""

    def __init__(self, parent, width: int = 300, height: int = 12,
                 colors: List[str] = None, bg: str = "#30363d",
                 border_radius: int = 6):

        self.colors = colors or ["#238636", "#3fb950", "#56d364"]
        self.bg = bg
        self.value = 0
        self.target_value = 0

        self.canvas = tk.Canvas(parent, width=width, height=height,
                                bg=bg, highlightthickness=0)
        self.width = width
        self.height = height

    def pack(self, **kwargs):
        self.canvas.pack(**kwargs)

    def grid(self, **kwargs):
        self.canvas.grid(**kwargs)

    def set_colors(self, colors: List[str], bg: str):
        """Update colors"""
        self.colors = colors
        self.bg = bg
        self.canvas.configure(bg=bg)

    def update(self, value: float):
        """Update value and redraw"""
        self.value = min(max(value, 0), 100)
        self.draw()

    def draw(self):
        """Draw the progress bar"""
        self.canvas.delete("all")

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10:
            w = self.width
        if h < 10:
            h = self.height

        # Background bar
        self.canvas.create_rectangle(0, 0, w, h, fill=self.bg, outline="")

        # Filled portion
        filled_w = int(w * self.value / 100)
        if filled_w > 0:
            # Gradient effect
            num_segments = max(1, filled_w // 3)
            for i in range(num_segments):
                x1 = int(i * filled_w / num_segments)
                x2 = int((i + 1) * filled_w / num_segments)
                factor = i / num_segments
                color = interpolate_color(self.colors[0], self.colors[1], factor)
                self.canvas.create_rectangle(x1, 0, x2, h, fill=color, outline="")

            # Highlight on top
            self.canvas.create_rectangle(0, 0, filled_w, h // 3,
                                        fill=self.colors[2], outline="",
                                        stipple="gray50")


# ============================================================================
# MINI BAR (for per-core display)
# ============================================================================

class MiniBar:
    """Tiny progress bar for per-core CPU display"""

    def __init__(self, parent, width: int = 40, height: int = 8,
                 color: str = "#3fb950", bg: str = "#30363d"):
        self.color = color
        self.bg = bg
        self.value = 0

        self.canvas = tk.Canvas(parent, width=width, height=height,
                                bg=bg, highlightthickness=0)
        self.width = width
        self.height = height

    def pack(self, **kwargs):
        self.canvas.pack(**kwargs)

    def grid(self, **kwargs):
        self.canvas.grid(**kwargs)

    def update(self, value: float, color: str = None):
        """Update value and redraw"""
        self.value = min(max(value, 0), 100)
        if color:
            self.color = color
        self.draw()

    def draw(self):
        """Draw the bar"""
        self.canvas.delete("all")
        w, h = self.width, self.height

        # Background
        self.canvas.create_rectangle(0, 0, w, h, fill=self.bg, outline="")

        # Filled
        filled_w = int(w * self.value / 100)
        if filled_w > 0:
            self.canvas.create_rectangle(0, 0, filled_w, h,
                                        fill=self.color, outline="")


# ============================================================================
# MAIN WIDGET CLASS
# ============================================================================

class WellzWidget:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WELLZ System Monitor")

        # Theme
        self.theme_names = list(THEMES.keys())
        self.theme_index = 0
        self.colors = THEMES[self.theme_names[0]].copy()

        # Cache for static info
        self.cpu_name = self._get_cpu_name()
        self.gpu_name = "Detecting..."
        self.os_name = get_os_name()
        self.hostname = socket.gethostname()
        self.cpu_cores = psutil.cpu_count(logical=False) or psutil.cpu_count() or 4
        self.cpu_threads = psutil.cpu_count() or 8

        # Network speed tracking
        self.last_net_io = psutil.net_io_counters()
        self.last_net_time = time.time()
        self.net_upload_speed = 0.0
        self.net_download_speed = 0.0

        # Disk I/O tracking
        self.last_disk_io = psutil.disk_io_counters()
        self.last_disk_time = time.time()
        self.disk_read_speed = 0.0
        self.disk_write_speed = 0.0

        # Window setup
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(False)  # Keep window decorations for now

        # Window size and position
        self.width = 420
        self.height = 900
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = screen_width - self.width - 20
        y_position = 40
        self.root.geometry(f"{self.width}x{self.height}+{x_position}+{y_position}")
        self.root.minsize(380, 700)
        self.root.configure(bg=self.colors["bg"])

        # Transparency
        try:
            self.root.attributes("-alpha", 0.96)
        except:
            pass

        # Create scrollable frame
        self._create_scrollable_frame()

        # Create UI sections
        self._create_header()
        self._create_system_section()
        self._create_cpu_section()
        self._create_gpu_section()
        self._create_memory_section()
        self._create_disk_section()
        self._create_network_section()
        self._create_processes_section()
        self._create_controls()

        # Dragging
        self.root.bind("<Button-1>", self._start_drag)
        self.root.bind("<B1-Motion>", self._do_drag)

        # Start update thread
        self.running = True
        self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self.update_thread.start()

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _create_scrollable_frame(self):
        """Create a scrollable main frame"""
        # Main container
        self.container = tk.Frame(self.root, bg=self.colors["bg"])
        self.container.pack(fill=tk.BOTH, expand=True)

        # Canvas for scrolling
        self.canvas = tk.Canvas(self.container, bg=self.colors["bg"],
                               highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.container, orient="vertical",
                                       command=self.canvas.yview)

        self.main_frame = tk.Frame(self.canvas, bg=self.colors["bg"])

        self.main_frame.bind("<Configure>",
                            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.main_frame,
                                                       anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        # Hide scrollbar by default, show on hover

        # Bind mousewheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

        # Resize canvas frame width
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def _on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

    def _create_card(self, title: str, color: str) -> Dict:
        """Create a styled card container"""
        card = tk.Frame(self.main_frame, bg=self.colors["bg_card"],
                       highlightbackground=self.colors["border"],
                       highlightthickness=1)
        card.pack(fill=tk.X, pady=6, padx=2)

        # Header
        header = tk.Frame(card, bg=self.colors["bg_card"])
        header.pack(fill=tk.X, padx=12, pady=(10, 6))

        title_label = tk.Label(header, text=title,
                              font=("Segoe UI", 11, "bold"),
                              fg=color, bg=self.colors["bg_card"])
        title_label.pack(side=tk.LEFT)

        value_label = tk.Label(header, text="",
                              font=("Segoe UI", 11, "bold"),
                              fg=self.colors["text"], bg=self.colors["bg_card"])
        value_label.pack(side=tk.RIGHT)

        # Content frame
        content = tk.Frame(card, bg=self.colors["bg_card"])
        content.pack(fill=tk.X, padx=12, pady=(0, 10))

        return {
            "card": card,
            "header": header,
            "title": title_label,
            "value": value_label,
            "content": content,
            "color": color,
        }

    def _create_header(self):
        """Create the header section"""
        self.header_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        self.header_frame.pack(fill=tk.X, pady=(0, 10))

        # Title
        title_frame = tk.Frame(self.header_frame, bg=self.colors["bg"])
        title_frame.pack(fill=tk.X)

        self.title_label = tk.Label(title_frame, text="WELLZ",
                                   font=("Segoe UI", 24, "bold"),
                                   fg=self.colors["accent"],
                                   bg=self.colors["bg"])
        self.title_label.pack(side=tk.LEFT)

        self.version_label = tk.Label(title_frame, text="v3.0",
                                     font=("Segoe UI", 10),
                                     fg=self.colors["text_dim"],
                                     bg=self.colors["bg"])
        self.version_label.pack(side=tk.LEFT, padx=(8, 0), pady=(12, 0))

        self.theme_label = tk.Label(title_frame,
                                   text=f"[ {self.colors['name']} ]",
                                   font=("Segoe UI", 10),
                                   fg=self.colors["text_secondary"],
                                   bg=self.colors["bg"])
        self.theme_label.pack(side=tk.RIGHT, pady=(12, 0))

    def _create_system_section(self):
        """Create system info section"""
        card = self._create_card("SYSTEM", self.colors["accent"])
        self.sys_card = card

        # Info labels
        self.sys_labels = {}
        info_items = [
            ("os", "OS"),
            ("host", "Host"),
            ("arch", "Arch"),
            ("uptime", "Uptime"),
        ]

        for key, label in info_items:
            row = tk.Frame(card["content"], bg=self.colors["bg_card"])
            row.pack(fill=tk.X, pady=1)

            lbl = tk.Label(row, text=f"{label}:", width=8, anchor="w",
                          font=("Segoe UI", 9),
                          fg=self.colors["text_dim"],
                          bg=self.colors["bg_card"])
            lbl.pack(side=tk.LEFT)

            val = tk.Label(row, text="...", anchor="w",
                          font=("Segoe UI", 9),
                          fg=self.colors["text"],
                          bg=self.colors["bg_card"])
            val.pack(side=tk.LEFT, fill=tk.X, expand=True)

            self.sys_labels[key] = val

    def _create_cpu_section(self):
        """Create CPU monitoring section"""
        card = self._create_card("CPU", self.colors["cpu"])
        self.cpu_card = card

        # CPU name
        self.cpu_name_label = tk.Label(card["content"], text=self.cpu_name,
                                       font=("Segoe UI", 9),
                                       fg=self.colors["text_secondary"],
                                       bg=self.colors["bg_card"],
                                       anchor="w")
        self.cpu_name_label.pack(fill=tk.X, pady=(0, 6))

        # Main chart
        self.cpu_chart = SmoothLineChart(card["content"], width=360, height=70,
                                        colors=self.colors["cpu_gradient"],
                                        bg=self.colors["bg_card"],
                                        grid_color=self.colors["chart_grid"])
        self.cpu_chart.pack(fill=tk.X, pady=(0, 8))

        # Progress bar
        self.cpu_bar = AnimatedProgressBar(card["content"], width=360, height=10,
                                          colors=self.colors["cpu_gradient"],
                                          bg=self.colors["border"])
        self.cpu_bar.pack(fill=tk.X, pady=(0, 8))

        # Per-core section
        cores_label = tk.Label(card["content"], text="Per-Core Usage",
                              font=("Segoe UI", 9, "bold"),
                              fg=self.colors["text_secondary"],
                              bg=self.colors["bg_card"],
                              anchor="w")
        cores_label.pack(fill=tk.X, pady=(4, 4))

        self.core_frame = tk.Frame(card["content"], bg=self.colors["bg_card"])
        self.core_frame.pack(fill=tk.X)

        self.core_bars = []
        self.core_labels = []

        # Create grid of core indicators
        cols = 4
        for i in range(min(self.cpu_threads, 16)):
            row_idx = i // cols
            col_idx = i % cols

            frame = tk.Frame(self.core_frame, bg=self.colors["bg_card"])
            frame.grid(row=row_idx, column=col_idx, padx=4, pady=2, sticky="w")

            lbl = tk.Label(frame, text=f"C{i}", width=3,
                          font=("Consolas", 8),
                          fg=self.colors["text_dim"],
                          bg=self.colors["bg_card"])
            lbl.pack(side=tk.LEFT)

            bar = MiniBar(frame, width=50, height=8,
                         color=self.colors["cpu"],
                         bg=self.colors["border"])
            bar.pack(side=tk.LEFT, padx=(2, 0))

            pct = tk.Label(frame, text="0%", width=4,
                          font=("Consolas", 8),
                          fg=self.colors["text_dim"],
                          bg=self.colors["bg_card"])
            pct.pack(side=tk.LEFT)

            self.core_bars.append(bar)
            self.core_labels.append(pct)

        # Stats row
        stats_frame = tk.Frame(card["content"], bg=self.colors["bg_card"])
        stats_frame.pack(fill=tk.X, pady=(8, 0))

        self.cpu_freq_label = tk.Label(stats_frame, text="Freq: -- MHz",
                                       font=("Segoe UI", 9),
                                       fg=self.colors["text_dim"],
                                       bg=self.colors["bg_card"])
        self.cpu_freq_label.pack(side=tk.LEFT)

        self.cpu_temp_label = tk.Label(stats_frame, text="Temp: --C",
                                       font=("Segoe UI", 9),
                                       fg=self.colors["text_dim"],
                                       bg=self.colors["bg_card"])
        self.cpu_temp_label.pack(side=tk.RIGHT)

    def _create_gpu_section(self):
        """Create GPU monitoring section"""
        card = self._create_card("GPU", self.colors["gpu"])
        self.gpu_card = card

        # GPU name
        self.gpu_name_label = tk.Label(card["content"], text="Detecting...",
                                       font=("Segoe UI", 9),
                                       fg=self.colors["text_secondary"],
                                       bg=self.colors["bg_card"],
                                       anchor="w")
        self.gpu_name_label.pack(fill=tk.X, pady=(0, 6))

        # Chart
        self.gpu_chart = SmoothLineChart(card["content"], width=360, height=60,
                                        colors=self.colors["gpu_gradient"],
                                        bg=self.colors["bg_card"],
                                        grid_color=self.colors["chart_grid"])
        self.gpu_chart.pack(fill=tk.X, pady=(0, 8))

        # Progress bar
        self.gpu_bar = AnimatedProgressBar(card["content"], width=360, height=10,
                                          colors=self.colors["gpu_gradient"],
                                          bg=self.colors["border"])
        self.gpu_bar.pack(fill=tk.X, pady=(0, 8))

        # Stats
        stats_frame = tk.Frame(card["content"], bg=self.colors["bg_card"])
        stats_frame.pack(fill=tk.X)

        self.gpu_vram_label = tk.Label(stats_frame, text="VRAM: --",
                                       font=("Segoe UI", 9),
                                       fg=self.colors["text_dim"],
                                       bg=self.colors["bg_card"])
        self.gpu_vram_label.pack(side=tk.LEFT)

        self.gpu_temp_label = tk.Label(stats_frame, text="Temp: --C",
                                       font=("Segoe UI", 9),
                                       fg=self.colors["temp"],
                                       bg=self.colors["bg_card"])
        self.gpu_temp_label.pack(side=tk.RIGHT)

    def _create_memory_section(self):
        """Create memory monitoring section"""
        card = self._create_card("MEMORY", self.colors["mem"])
        self.mem_card = card

        # Chart
        self.mem_chart = SmoothLineChart(card["content"], width=360, height=60,
                                        colors=self.colors["mem_gradient"],
                                        bg=self.colors["bg_card"],
                                        grid_color=self.colors["chart_grid"])
        self.mem_chart.pack(fill=tk.X, pady=(0, 8))

        # Progress bar
        self.mem_bar = AnimatedProgressBar(card["content"], width=360, height=10,
                                          colors=self.colors["mem_gradient"],
                                          bg=self.colors["border"])
        self.mem_bar.pack(fill=tk.X, pady=(0, 8))

        # Stats
        stats_frame = tk.Frame(card["content"], bg=self.colors["bg_card"])
        stats_frame.pack(fill=tk.X)

        self.mem_used_label = tk.Label(stats_frame, text="Used: --",
                                       font=("Segoe UI", 9),
                                       fg=self.colors["text_dim"],
                                       bg=self.colors["bg_card"])
        self.mem_used_label.pack(side=tk.LEFT)

        self.mem_total_label = tk.Label(stats_frame, text="Total: --",
                                        font=("Segoe UI", 9),
                                        fg=self.colors["text_dim"],
                                        bg=self.colors["bg_card"])
        self.mem_total_label.pack(side=tk.RIGHT)

        # Swap
        swap_frame = tk.Frame(card["content"], bg=self.colors["bg_card"])
        swap_frame.pack(fill=tk.X, pady=(6, 0))

        self.swap_label = tk.Label(swap_frame, text="Swap: --",
                                   font=("Segoe UI", 9),
                                   fg=self.colors["text_dim"],
                                   bg=self.colors["bg_card"])
        self.swap_label.pack(side=tk.LEFT)

    def _create_disk_section(self):
        """Create disk monitoring section"""
        card = self._create_card("DISK", self.colors["disk"])
        self.disk_card = card

        # Progress bar
        self.disk_bar = AnimatedProgressBar(card["content"], width=360, height=10,
                                           colors=self.colors["disk_gradient"],
                                           bg=self.colors["border"])
        self.disk_bar.pack(fill=tk.X, pady=(0, 8))

        # Stats
        stats_frame = tk.Frame(card["content"], bg=self.colors["bg_card"])
        stats_frame.pack(fill=tk.X)

        self.disk_used_label = tk.Label(stats_frame, text="Used: --",
                                        font=("Segoe UI", 9),
                                        fg=self.colors["text_dim"],
                                        bg=self.colors["bg_card"])
        self.disk_used_label.pack(side=tk.LEFT)

        self.disk_total_label = tk.Label(stats_frame, text="Total: --",
                                         font=("Segoe UI", 9),
                                         fg=self.colors["text_dim"],
                                         bg=self.colors["bg_card"])
        self.disk_total_label.pack(side=tk.RIGHT)

        # I/O speeds
        io_frame = tk.Frame(card["content"], bg=self.colors["bg_card"])
        io_frame.pack(fill=tk.X, pady=(6, 0))

        self.disk_read_label = tk.Label(io_frame, text="Read: --",
                                        font=("Segoe UI", 9),
                                        fg=self.colors["success"],
                                        bg=self.colors["bg_card"])
        self.disk_read_label.pack(side=tk.LEFT)

        self.disk_write_label = tk.Label(io_frame, text="Write: --",
                                         font=("Segoe UI", 9),
                                         fg=self.colors["warning"],
                                         bg=self.colors["bg_card"])
        self.disk_write_label.pack(side=tk.RIGHT)

    def _create_network_section(self):
        """Create network monitoring section"""
        card = self._create_card("NETWORK", self.colors["net"])
        self.net_card = card

        # IP address
        self.net_ip_label = tk.Label(card["content"], text="IP: --",
                                     font=("Segoe UI", 9),
                                     fg=self.colors["text_secondary"],
                                     bg=self.colors["bg_card"],
                                     anchor="w")
        self.net_ip_label.pack(fill=tk.X, pady=(0, 6))

        # Speed chart
        self.net_chart = SmoothLineChart(card["content"], width=360, height=50,
                                        colors=self.colors["net_gradient"],
                                        bg=self.colors["bg_card"],
                                        grid_color=self.colors["chart_grid"],
                                        maxlen=60)
        self.net_chart.auto_scale = True
        self.net_chart.pack(fill=tk.X, pady=(0, 8))

        # Speeds
        speed_frame = tk.Frame(card["content"], bg=self.colors["bg_card"])
        speed_frame.pack(fill=tk.X)

        # Upload
        up_frame = tk.Frame(speed_frame, bg=self.colors["bg_card"])
        up_frame.pack(side=tk.LEFT)

        tk.Label(up_frame, text="", font=("Segoe UI", 9),
                fg=self.colors["success"], bg=self.colors["bg_card"]).pack(side=tk.LEFT)
        self.net_up_label = tk.Label(up_frame, text="0 B/s",
                                     font=("Segoe UI", 9, "bold"),
                                     fg=self.colors["success"],
                                     bg=self.colors["bg_card"])
        self.net_up_label.pack(side=tk.LEFT, padx=(4, 0))

        # Download
        down_frame = tk.Frame(speed_frame, bg=self.colors["bg_card"])
        down_frame.pack(side=tk.RIGHT)

        tk.Label(down_frame, text="", font=("Segoe UI", 9),
                fg=self.colors["accent"], bg=self.colors["bg_card"]).pack(side=tk.LEFT)
        self.net_down_label = tk.Label(down_frame, text="0 B/s",
                                       font=("Segoe UI", 9, "bold"),
                                       fg=self.colors["accent"],
                                       bg=self.colors["bg_card"])
        self.net_down_label.pack(side=tk.LEFT, padx=(4, 0))

        # Total transferred
        total_frame = tk.Frame(card["content"], bg=self.colors["bg_card"])
        total_frame.pack(fill=tk.X, pady=(6, 0))

        self.net_tx_label = tk.Label(total_frame, text="TX: --",
                                     font=("Segoe UI", 9),
                                     fg=self.colors["text_dim"],
                                     bg=self.colors["bg_card"])
        self.net_tx_label.pack(side=tk.LEFT)

        self.net_rx_label = tk.Label(total_frame, text="RX: --",
                                     font=("Segoe UI", 9),
                                     fg=self.colors["text_dim"],
                                     bg=self.colors["bg_card"])
        self.net_rx_label.pack(side=tk.RIGHT)

    def _create_processes_section(self):
        """Create top processes section"""
        card = self._create_card("TOP PROCESSES", self.colors["accent"])
        self.proc_card = card

        # Header row
        header = tk.Frame(card["content"], bg=self.colors["bg_card"])
        header.pack(fill=tk.X, pady=(0, 4))

        tk.Label(header, text="Name", width=20, anchor="w",
                font=("Consolas", 8, "bold"),
                fg=self.colors["text_dim"],
                bg=self.colors["bg_card"]).pack(side=tk.LEFT)
        tk.Label(header, text="CPU%", width=8, anchor="e",
                font=("Consolas", 8, "bold"),
                fg=self.colors["text_dim"],
                bg=self.colors["bg_card"]).pack(side=tk.LEFT)
        tk.Label(header, text="MEM%", width=8, anchor="e",
                font=("Consolas", 8, "bold"),
                fg=self.colors["text_dim"],
                bg=self.colors["bg_card"]).pack(side=tk.LEFT)

        # Process rows
        self.proc_rows = []
        for i in range(5):
            row = tk.Frame(card["content"], bg=self.colors["bg_card"])
            row.pack(fill=tk.X, pady=1)

            name = tk.Label(row, text="--", width=20, anchor="w",
                           font=("Consolas", 9),
                           fg=self.colors["text"],
                           bg=self.colors["bg_card"])
            name.pack(side=tk.LEFT)

            cpu = tk.Label(row, text="--", width=8, anchor="e",
                          font=("Consolas", 9),
                          fg=self.colors["cpu"],
                          bg=self.colors["bg_card"])
            cpu.pack(side=tk.LEFT)

            mem = tk.Label(row, text="--", width=8, anchor="e",
                          font=("Consolas", 9),
                          fg=self.colors["mem"],
                          bg=self.colors["bg_card"])
            mem.pack(side=tk.LEFT)

            self.proc_rows.append({"name": name, "cpu": cpu, "mem": mem})

    def _create_controls(self):
        """Create control buttons"""
        self.btn_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        self.btn_frame.pack(fill=tk.X, pady=(12, 4))

        # Theme button
        self.theme_btn = tk.Button(self.btn_frame, text="Theme",
                                  command=self._next_theme,
                                  bg=self.colors["bg_card"],
                                  fg=self.colors["text"],
                                  activebackground=self.colors["bg_card_hover"],
                                  activeforeground=self.colors["text"],
                                  relief=tk.FLAT,
                                  font=("Segoe UI", 9),
                                  cursor="hand2",
                                  padx=12, pady=4)
        self.theme_btn.pack(side=tk.LEFT)

        # Close button
        self.close_btn = tk.Button(self.btn_frame, text="Close",
                                  command=self.root.destroy,
                                  bg=self.colors["bg_card"],
                                  fg=self.colors["text"],
                                  activebackground=self.colors["danger"],
                                  activeforeground=self.colors["text"],
                                  relief=tk.FLAT,
                                  font=("Segoe UI", 9),
                                  cursor="hand2",
                                  padx=12, pady=4)
        self.close_btn.pack(side=tk.RIGHT)

        # Opacity slider
        opacity_frame = tk.Frame(self.btn_frame, bg=self.colors["bg"])
        opacity_frame.pack(side=tk.LEFT, padx=20)

        tk.Label(opacity_frame, text="Opacity:",
                font=("Segoe UI", 8),
                fg=self.colors["text_dim"],
                bg=self.colors["bg"]).pack(side=tk.LEFT)

        self.opacity_scale = tk.Scale(opacity_frame, from_=50, to=100,
                                     orient=tk.HORIZONTAL, length=80,
                                     bg=self.colors["bg"],
                                     fg=self.colors["text"],
                                     troughcolor=self.colors["bg_card"],
                                     highlightthickness=0,
                                     sliderrelief=tk.FLAT,
                                     command=self._set_opacity,
                                     showvalue=False)
        self.opacity_scale.set(96)
        self.opacity_scale.pack(side=tk.LEFT)

    # ========================================================================
    # DATA COLLECTION
    # ========================================================================

    def _get_cpu_name(self) -> str:
        """Get CPU model name"""
        try:
            if platform.system() == "Linux":
                with open("/proc/cpuinfo", "r") as f:
                    for line in f:
                        if "model name" in line:
                            name = line.split(":")[1].strip()
                            if len(name) > 40:
                                name = name[:37] + "..."
                            return name
            elif platform.system() == "Darwin":
                result = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"],
                                       capture_output=True, text=True)
                if result.returncode == 0:
                    return result.stdout.strip()[:40]
            elif platform.system() == "Windows":
                return platform.processor()[:40]
        except:
            pass
        return "Unknown CPU"

    def _get_cpu_temp(self) -> Optional[float]:
        """Get CPU temperature"""
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for name in ['coretemp', 'cpu_thermal', 'k10temp', 'zenpower']:
                    if name in temps:
                        return temps[name][0].current
                # Try first available
                for name, entries in temps.items():
                    if entries:
                        return entries[0].current
        except:
            pass
        return None

    def _get_gpu_info(self) -> Tuple[float, str, float, float, Optional[float]]:
        """Get GPU info: (usage%, name, vram_used, vram_total, temp)"""
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu",
                 "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=2
            )
            if result.returncode == 0:
                parts = result.stdout.strip().split(", ")
                if len(parts) >= 5:
                    name = parts[0][:40]
                    usage = float(parts[1])
                    vram_used = float(parts[2])
                    vram_total = float(parts[3])
                    temp = float(parts[4])
                    return usage, name, vram_used, vram_total, temp
        except:
            pass
        return 0, "No NVIDIA GPU", 0, 0, None

    def _get_top_processes(self, n: int = 5) -> List[Dict]:
        """Get top N processes by CPU usage"""
        try:
            procs = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    info = proc.info
                    if info['cpu_percent'] is not None:
                        procs.append(info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            # Sort by CPU usage
            procs.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            return procs[:n]
        except:
            return []

    def _get_network_speed(self) -> Tuple[float, float]:
        """Get current network upload/download speeds in bytes/sec"""
        try:
            current = psutil.net_io_counters()
            current_time = time.time()

            time_delta = current_time - self.last_net_time
            if time_delta > 0:
                upload = (current.bytes_sent - self.last_net_io.bytes_sent) / time_delta
                download = (current.bytes_recv - self.last_net_io.bytes_recv) / time_delta
            else:
                upload, download = 0, 0

            self.last_net_io = current
            self.last_net_time = current_time

            return upload, download
        except:
            return 0, 0

    def _get_disk_io_speed(self) -> Tuple[float, float]:
        """Get current disk read/write speeds in bytes/sec"""
        try:
            current = psutil.disk_io_counters()
            current_time = time.time()

            time_delta = current_time - self.last_disk_time
            if time_delta > 0 and current and self.last_disk_io:
                read_speed = (current.read_bytes - self.last_disk_io.read_bytes) / time_delta
                write_speed = (current.write_bytes - self.last_disk_io.write_bytes) / time_delta
            else:
                read_speed, write_speed = 0, 0

            self.last_disk_io = current
            self.last_disk_time = current_time

            return read_speed, write_speed
        except:
            return 0, 0

    def _get_ip_address(self) -> str:
        """Get primary IP address"""
        try:
            for iface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == socket.AF_INET and not addr.address.startswith("127."):
                        return addr.address
        except:
            pass
        return "N/A"

    def _get_uptime(self) -> str:
        """Get system uptime string"""
        try:
            uptime_sec = time.time() - psutil.boot_time()
            days = int(uptime_sec // 86400)
            hours = int((uptime_sec % 86400) // 3600)
            mins = int((uptime_sec % 3600) // 60)

            if days > 0:
                return f"{days}d {hours}h {mins}m"
            elif hours > 0:
                return f"{hours}h {mins}m"
            else:
                return f"{mins}m"
        except:
            return "N/A"

    # ========================================================================
    # UI UPDATE
    # ========================================================================

    def _update_stats(self):
        """Update all statistics"""
        try:
            # System info
            self.root.after(0, lambda: self.sys_labels["os"].config(text=self.os_name))
            self.root.after(0, lambda: self.sys_labels["host"].config(text=self.hostname))
            self.root.after(0, lambda: self.sys_labels["arch"].config(text=platform.machine()))
            self.root.after(0, lambda: self.sys_labels["uptime"].config(text=self._get_uptime()))

            # CPU
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_freq = psutil.cpu_freq()
            cpu_temp = self._get_cpu_temp()
            per_cpu = psutil.cpu_percent(percpu=True)

            self.root.after(0, lambda: self.cpu_card["value"].config(text=f"{cpu_percent:.1f}%"))
            self.root.after(0, lambda: self.cpu_chart.update(cpu_percent))
            self.root.after(0, lambda: self.cpu_bar.update(cpu_percent))

            freq_str = f"{cpu_freq.current:.0f} MHz" if cpu_freq else "--"
            self.root.after(0, lambda: self.cpu_freq_label.config(text=f"Freq: {freq_str}"))

            temp_str = f"{cpu_temp:.0f}C" if cpu_temp else "--"
            temp_color = self.colors["danger"] if cpu_temp and cpu_temp > 80 else self.colors["text_dim"]
            self.root.after(0, lambda: self.cpu_temp_label.config(text=f"Temp: {temp_str}", fg=temp_color))

            # Per-core
            for i, pct in enumerate(per_cpu[:len(self.core_bars)]):
                color = self._get_usage_color(pct)
                self.root.after(0, lambda i=i, pct=pct, c=color: (
                    self.core_bars[i].update(pct, c),
                    self.core_labels[i].config(text=f"{pct:.0f}%")
                ))

            # GPU
            gpu_usage, gpu_name, vram_used, vram_total, gpu_temp = self._get_gpu_info()
            self.root.after(0, lambda: self.gpu_card["value"].config(text=f"{gpu_usage:.0f}%"))
            self.root.after(0, lambda: self.gpu_name_label.config(text=gpu_name))
            self.root.after(0, lambda: self.gpu_chart.update(gpu_usage))
            self.root.after(0, lambda: self.gpu_bar.update(gpu_usage))

            vram_str = f"{vram_used:.0f}/{vram_total:.0f} MB" if vram_total > 0 else "--"
            self.root.after(0, lambda: self.gpu_vram_label.config(text=f"VRAM: {vram_str}"))

            if gpu_temp:
                temp_color = self.colors["danger"] if gpu_temp > 80 else self.colors["temp"]
                self.root.after(0, lambda: self.gpu_temp_label.config(text=f"Temp: {gpu_temp:.0f}C", fg=temp_color))

            # Memory
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()

            self.root.after(0, lambda: self.mem_card["value"].config(text=f"{mem.percent:.1f}%"))
            self.root.after(0, lambda: self.mem_chart.update(mem.percent))
            self.root.after(0, lambda: self.mem_bar.update(mem.percent))
            self.root.after(0, lambda: self.mem_used_label.config(
                text=f"Used: {format_bytes(mem.used)}"))
            self.root.after(0, lambda: self.mem_total_label.config(
                text=f"Total: {format_bytes(mem.total)}"))
            self.root.after(0, lambda: self.swap_label.config(
                text=f"Swap: {format_bytes(swap.used)} / {format_bytes(swap.total)} ({swap.percent:.0f}%)"))

            # Disk
            disk = psutil.disk_usage("/")
            read_speed, write_speed = self._get_disk_io_speed()

            self.root.after(0, lambda: self.disk_card["value"].config(text=f"{disk.percent:.1f}%"))
            self.root.after(0, lambda: self.disk_bar.update(disk.percent))
            self.root.after(0, lambda: self.disk_used_label.config(
                text=f"Used: {format_bytes(disk.used)}"))
            self.root.after(0, lambda: self.disk_total_label.config(
                text=f"Total: {format_bytes(disk.total)}"))
            self.root.after(0, lambda: self.disk_read_label.config(
                text=f"Read: {format_bytes(read_speed, True)}"))
            self.root.after(0, lambda: self.disk_write_label.config(
                text=f"Write: {format_bytes(write_speed, True)}"))

            # Network
            upload, download = self._get_network_speed()
            net = psutil.net_io_counters()
            ip = self._get_ip_address()

            # Use download speed for chart
            self.root.after(0, lambda: self.net_chart.update(download / 1024))  # KB/s
            self.root.after(0, lambda: self.net_ip_label.config(text=f"IP: {ip}"))
            self.root.after(0, lambda: self.net_up_label.config(text=format_bytes(upload, True)))
            self.root.after(0, lambda: self.net_down_label.config(text=format_bytes(download, True)))
            self.root.after(0, lambda: self.net_tx_label.config(text=f"TX: {format_bytes(net.bytes_sent)}"))
            self.root.after(0, lambda: self.net_rx_label.config(text=f"RX: {format_bytes(net.bytes_recv)}"))

            # Processes
            procs = self._get_top_processes(5)
            for i, row in enumerate(self.proc_rows):
                if i < len(procs):
                    p = procs[i]
                    name = p['name'][:18] if p['name'] else "--"
                    cpu_p = p['cpu_percent'] or 0
                    mem_p = p['memory_percent'] or 0
                    self.root.after(0, lambda r=row, n=name, c=cpu_p, m=mem_p: (
                        r["name"].config(text=n),
                        r["cpu"].config(text=f"{c:.1f}%"),
                        r["mem"].config(text=f"{m:.1f}%")
                    ))

        except Exception as e:
            pass

    def _get_usage_color(self, percent: float) -> str:
        """Get color based on usage percentage"""
        if percent < 50:
            return self.colors["success"]
        elif percent < 80:
            return self.colors["warning"]
        else:
            return self.colors["danger"]

    def _update_loop(self):
        """Background update loop"""
        while self.running:
            self._update_stats()
            time.sleep(1)

    # ========================================================================
    # THEME & CONTROLS
    # ========================================================================

    def _next_theme(self):
        """Switch to next theme"""
        self.theme_index = (self.theme_index + 1) % len(self.theme_names)
        self.colors = THEMES[self.theme_names[self.theme_index]].copy()
        self._apply_theme()

    def _apply_theme(self):
        """Apply current theme to all widgets"""
        bg = self.colors["bg"]
        bg_card = self.colors["bg_card"]
        border = self.colors["border"]
        text = self.colors["text"]
        text_sec = self.colors["text_secondary"]
        text_dim = self.colors["text_dim"]

        # Root and containers
        self.root.configure(bg=bg)
        self.container.configure(bg=bg)
        self.canvas.configure(bg=bg)
        self.main_frame.configure(bg=bg)

        # Header
        self.header_frame.configure(bg=bg)
        self.title_label.configure(fg=self.colors["accent"], bg=bg)
        self.version_label.configure(fg=text_dim, bg=bg)
        self.theme_label.configure(fg=text_sec, bg=bg,
                                  text=f"[ {self.colors['name']} ]")

        # Buttons
        self.btn_frame.configure(bg=bg)
        self.theme_btn.configure(bg=bg_card, fg=text,
                                activebackground=self.colors["bg_card_hover"])
        self.close_btn.configure(bg=bg_card, fg=text,
                                activebackground=self.colors["danger"])
        self.opacity_scale.configure(bg=bg, fg=text, troughcolor=bg_card)

        # Update all cards
        self._apply_theme_to_card(self.sys_card, self.colors["accent"])
        self._apply_theme_to_card(self.cpu_card, self.colors["cpu"])
        self._apply_theme_to_card(self.gpu_card, self.colors["gpu"])
        self._apply_theme_to_card(self.mem_card, self.colors["mem"])
        self._apply_theme_to_card(self.disk_card, self.colors["disk"])
        self._apply_theme_to_card(self.net_card, self.colors["net"])
        self._apply_theme_to_card(self.proc_card, self.colors["accent"])

        # System labels
        for lbl in self.sys_labels.values():
            lbl.configure(fg=text, bg=bg_card)

        # Charts and bars
        self.cpu_chart.set_colors(self.colors["cpu_gradient"], bg_card, self.colors["chart_grid"])
        self.gpu_chart.set_colors(self.colors["gpu_gradient"], bg_card, self.colors["chart_grid"])
        self.mem_chart.set_colors(self.colors["mem_gradient"], bg_card, self.colors["chart_grid"])
        self.net_chart.set_colors(self.colors["net_gradient"], bg_card, self.colors["chart_grid"])

        self.cpu_bar.set_colors(self.colors["cpu_gradient"], border)
        self.gpu_bar.set_colors(self.colors["gpu_gradient"], border)
        self.mem_bar.set_colors(self.colors["mem_gradient"], border)
        self.disk_bar.set_colors(self.colors["disk_gradient"], border)

        # Core bars
        for bar in self.core_bars:
            bar.canvas.configure(bg=border)
        for lbl in self.core_labels:
            lbl.configure(fg=text_dim, bg=bg_card)

        # CPU labels
        self.cpu_name_label.configure(fg=text_sec, bg=bg_card)
        self.cpu_freq_label.configure(fg=text_dim, bg=bg_card)
        self.cpu_temp_label.configure(bg=bg_card)
        self.core_frame.configure(bg=bg_card)

        # GPU labels
        self.gpu_name_label.configure(fg=text_sec, bg=bg_card)
        self.gpu_vram_label.configure(fg=text_dim, bg=bg_card)
        self.gpu_temp_label.configure(bg=bg_card)

        # Memory labels
        self.mem_used_label.configure(fg=text_dim, bg=bg_card)
        self.mem_total_label.configure(fg=text_dim, bg=bg_card)
        self.swap_label.configure(fg=text_dim, bg=bg_card)

        # Disk labels
        self.disk_used_label.configure(fg=text_dim, bg=bg_card)
        self.disk_total_label.configure(fg=text_dim, bg=bg_card)
        self.disk_read_label.configure(fg=self.colors["success"], bg=bg_card)
        self.disk_write_label.configure(fg=self.colors["warning"], bg=bg_card)

        # Network labels
        self.net_ip_label.configure(fg=text_sec, bg=bg_card)
        self.net_up_label.configure(fg=self.colors["success"], bg=bg_card)
        self.net_down_label.configure(fg=self.colors["accent"], bg=bg_card)
        self.net_tx_label.configure(fg=text_dim, bg=bg_card)
        self.net_rx_label.configure(fg=text_dim, bg=bg_card)

        # Process rows
        for row in self.proc_rows:
            row["name"].configure(fg=text, bg=bg_card)
            row["cpu"].configure(fg=self.colors["cpu"], bg=bg_card)
            row["mem"].configure(fg=self.colors["mem"], bg=bg_card)

    def _apply_theme_to_card(self, card: Dict, color: str):
        """Apply theme to a card"""
        bg_card = self.colors["bg_card"]
        border = self.colors["border"]
        text = self.colors["text"]

        card["card"].configure(bg=bg_card, highlightbackground=border)
        card["header"].configure(bg=bg_card)
        card["title"].configure(fg=color, bg=bg_card)
        card["value"].configure(fg=text, bg=bg_card)
        card["content"].configure(bg=bg_card)

        # Update all children frames
        for child in card["content"].winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=bg_card)
                for subchild in child.winfo_children():
                    if isinstance(subchild, tk.Label):
                        subchild.configure(bg=bg_card)
                    elif isinstance(subchild, tk.Frame):
                        subchild.configure(bg=bg_card)

    def _set_opacity(self, value):
        """Set window opacity"""
        try:
            self.root.attributes("-alpha", int(value) / 100)
        except:
            pass

    def _start_drag(self, event):
        self.drag_x = event.x
        self.drag_y = event.y

    def _do_drag(self, event):
        x = self.root.winfo_x() + event.x - self.drag_x
        y = self.root.winfo_y() + event.y - self.drag_y
        self.root.geometry(f"+{x}+{y}")

    def _on_close(self):
        """Handle window close"""
        self.running = False
        self.root.destroy()

    def run(self):
        """Start the widget"""
        self.root.mainloop()


# ============================================================================
# ENTRY POINT
# ============================================================================

def main():
    """Main entry point"""
    try:
        widget = WellzWidget()
        widget.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
