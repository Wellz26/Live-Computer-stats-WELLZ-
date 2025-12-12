#!/usr/bin/env python3
"""
Wellz GUI - Gaming PC Stats Widget v2.0
A btop-inspired always-on-top system monitor widget with graphs
"""

import subprocess
import sys
import threading
import time
import platform
import socket
from collections import deque

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
# THEMES
# ============================================================================

THEMES = {
    "default": {
        "name": "Default",
        "bg": "#0d1117",
        "bg_box": "#161b22",
        "border": "#30363d",
        "text": "#c9d1d9",
        "text_dim": "#8b949e",
        "title": "#58a6ff",
        "cpu": "#3fb950",
        "gpu": "#d29922",
        "mem": "#58a6ff",
        "disk": "#a371f7",
        "net": "#39c5cf",
        "low": "#3fb950",
        "mid": "#d29922",
        "high": "#f85149",
        "graph": "#58a6ff",
    },
    "dracula": {
        "name": "Dracula",
        "bg": "#282a36",
        "bg_box": "#44475a",
        "border": "#6272a4",
        "text": "#f8f8f2",
        "text_dim": "#6272a4",
        "title": "#bd93f9",
        "cpu": "#50fa7b",
        "gpu": "#f1fa8c",
        "mem": "#8be9fd",
        "disk": "#ff79c6",
        "net": "#8be9fd",
        "low": "#50fa7b",
        "mid": "#ffb86c",
        "high": "#ff5555",
        "graph": "#bd93f9",
    },
    "nord": {
        "name": "Nord",
        "bg": "#2e3440",
        "bg_box": "#3b4252",
        "border": "#4c566a",
        "text": "#eceff4",
        "text_dim": "#d8dee9",
        "title": "#88c0d0",
        "cpu": "#a3be8c",
        "gpu": "#ebcb8b",
        "mem": "#81a1c1",
        "disk": "#b48ead",
        "net": "#88c0d0",
        "low": "#a3be8c",
        "mid": "#ebcb8b",
        "high": "#bf616a",
        "graph": "#88c0d0",
    },
    "gruvbox": {
        "name": "Gruvbox",
        "bg": "#282828",
        "bg_box": "#3c3836",
        "border": "#665c54",
        "text": "#ebdbb2",
        "text_dim": "#a89984",
        "title": "#fe8019",
        "cpu": "#b8bb26",
        "gpu": "#fabd2f",
        "mem": "#83a598",
        "disk": "#d3869b",
        "net": "#fe8019",
        "low": "#b8bb26",
        "mid": "#fabd2f",
        "high": "#fb4934",
        "graph": "#fe8019",
    },
    "monokai": {
        "name": "Monokai",
        "bg": "#272822",
        "bg_box": "#3e3d32",
        "border": "#75715e",
        "text": "#f8f8f2",
        "text_dim": "#75715e",
        "title": "#66d9ef",
        "cpu": "#a6e22e",
        "gpu": "#e6db74",
        "mem": "#66d9ef",
        "disk": "#ae81ff",
        "net": "#66d9ef",
        "low": "#a6e22e",
        "mid": "#e6db74",
        "high": "#f92672",
        "graph": "#66d9ef",
    },
}


# ============================================================================
# OS DETECTION
# ============================================================================

def get_os_type():
    """Detect OS type"""
    system = platform.system().lower()
    if system == "linux":
        try:
            with open("/etc/os-release", "r") as f:
                content = f.read().lower()
                for distro in ["kali", "arch", "ubuntu", "debian", "fedora",
                               "manjaro", "mint", "pop", "redhat", "suse"]:
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


def get_os_icon(os_type):
    """Return a simple text icon for the OS"""
    icons = {
        "windows": "[WIN]",
        "macos": "[MAC]",
        "linux": "[TUX]",
        "arch": "[ARCH]",
        "ubuntu": "[UBU]",
        "debian": "[DEB]",
        "fedora": "[FED]",
        "manjaro": "[MAN]",
        "kali": "[KALI]",
        "mint": "[MINT]",
        "pop": "[POP]",
        "redhat": "[RHEL]",
        "suse": "[SUSE]",
    }
    return icons.get(os_type, "[SYS]")


# ============================================================================
# GRAPH WIDGET
# ============================================================================

class MiniGraph:
    """Mini sparkline graph widget"""

    def __init__(self, parent, width=280, height=30, color="#58a6ff", bg="#161b22", maxlen=60):
        self.data = deque([0] * maxlen, maxlen=maxlen)
        self.color = color
        self.bg = bg
        self.canvas = tk.Canvas(parent, width=width, height=height,
                                bg=bg, highlightthickness=0)
        self.width = width
        self.height = height

    def pack(self, **kwargs):
        self.canvas.pack(**kwargs)

    def update(self, value):
        """Add new value and redraw"""
        self.data.append(value)
        self.draw()

    def set_color(self, color, bg):
        """Update colors"""
        self.color = color
        self.bg = bg
        self.canvas.configure(bg=bg)

    def draw(self):
        """Draw the graph"""
        self.canvas.delete("all")

        if not self.data:
            return

        # Get dimensions
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10:
            w = self.width
        if h < 10:
            h = self.height

        # Calculate points
        max_val = max(max(self.data), 1)
        points = []
        step = w / (len(self.data) - 1) if len(self.data) > 1 else w

        for i, val in enumerate(self.data):
            x = i * step
            y = h - (val / max_val * (h - 4)) - 2
            points.append((x, y))

        # Draw filled area
        if len(points) >= 2:
            fill_points = [(0, h)] + points + [(w, h)]
            flat_points = [coord for point in fill_points for coord in point]

            # Create gradient effect with lighter fill
            self.canvas.create_polygon(flat_points, fill=self.color,
                                       outline="", stipple="gray50")

            # Draw line on top
            line_points = [coord for point in points for coord in point]
            self.canvas.create_line(line_points, fill=self.color, width=2, smooth=True)


# ============================================================================
# MAIN WIDGET CLASS
# ============================================================================

class WellzWidget:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Wellz")

        # Theme
        self.theme_names = list(THEMES.keys())
        self.theme_index = 0
        self.colors = THEMES[self.theme_names[0]].copy()

        # Make window always on top
        self.root.attributes("-topmost", True)

        # Set window size and position (top-right corner)
        self.width = 340
        self.height = 580
        screen_width = self.root.winfo_screenwidth()
        x_position = screen_width - self.width - 20
        y_position = 40
        self.root.geometry(f"{self.width}x{self.height}+{x_position}+{y_position}")

        self.root.configure(bg=self.colors["bg"])

        # Try to make window semi-transparent
        try:
            self.root.attributes("-alpha", 0.95)
        except:
            pass

        # Create main frame
        self.main_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Header
        self.create_header()

        # Stats sections with graphs
        self.cpu_section = self.create_section("CPU", self.colors["cpu"], show_graph=True)
        self.gpu_section = self.create_section("GPU", self.colors["gpu"], show_graph=True)
        self.mem_section = self.create_section("MEMORY", self.colors["mem"], show_graph=True)
        self.disk_section = self.create_section("DISK", self.colors["disk"], show_graph=False)
        self.net_section = self.create_section("NETWORK", self.colors["net"], show_graph=False)

        # Control buttons
        self.create_controls()

        # Allow dragging the window
        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.do_drag)

        # Start update thread
        self.running = True
        self.update_thread = threading.Thread(target=self.update_loop, daemon=True)
        self.update_thread.start()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_header(self):
        """Create the header section"""
        self.header_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        self.header_frame.pack(fill=tk.X, pady=(0, 10))

        # Title
        self.title_label = tk.Label(
            self.header_frame,
            text="WELLZ",
            font=("Consolas", 18, "bold"),
            fg=self.colors["title"],
            bg=self.colors["bg"]
        )
        self.title_label.pack(side=tk.LEFT)

        # OS indicator
        os_type = get_os_type()
        os_icon = get_os_icon(os_type)
        self.os_label = tk.Label(
            self.header_frame,
            text=os_icon,
            font=("Consolas", 10),
            fg=self.colors["text_dim"],
            bg=self.colors["bg"]
        )
        self.os_label.pack(side=tk.RIGHT)

    def create_section(self, title, color, show_graph=False):
        """Create a stats section"""
        # Container frame
        container = tk.Frame(self.main_frame, bg=self.colors["bg_box"],
                            highlightbackground=self.colors["border"],
                            highlightthickness=1)
        container.pack(fill=tk.X, pady=4)

        # Title bar
        title_frame = tk.Frame(container, bg=self.colors["bg_box"])
        title_frame.pack(fill=tk.X, padx=8, pady=(6, 2))

        title_label = tk.Label(
            title_frame,
            text=title,
            font=("Consolas", 10, "bold"),
            fg=color,
            bg=self.colors["bg_box"]
        )
        title_label.pack(side=tk.LEFT)

        # Value label (for percentage/main stat)
        value_label = tk.Label(
            title_frame,
            text="0%",
            font=("Consolas", 10, "bold"),
            fg=self.colors["text"],
            bg=self.colors["bg_box"]
        )
        value_label.pack(side=tk.RIGHT)

        # Graph (if enabled)
        graph = None
        if show_graph:
            graph = MiniGraph(container, width=300, height=35,
                             color=color, bg=self.colors["bg_box"])
            graph.pack(fill=tk.X, padx=8, pady=(2, 0))

        # Info label
        info_label = tk.Label(
            container,
            text="Loading...",
            font=("Consolas", 9),
            fg=self.colors["text_dim"],
            bg=self.colors["bg_box"],
            anchor="w"
        )
        info_label.pack(fill=tk.X, padx=8, pady=(2, 2))

        # Progress bar canvas
        bar_frame = tk.Frame(container, bg=self.colors["bg_box"])
        bar_frame.pack(fill=tk.X, padx=8, pady=(0, 6))

        canvas = tk.Canvas(
            bar_frame,
            height=8,
            bg=self.colors["border"],
            highlightthickness=0
        )
        canvas.pack(fill=tk.X)

        return {
            "container": container,
            "title": title_label,
            "value": value_label,
            "info": info_label,
            "canvas": canvas,
            "color": color,
            "graph": graph,
            "title_frame": title_frame,
        }

    def create_controls(self):
        """Create control buttons"""
        self.btn_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        self.btn_frame.pack(fill=tk.X, pady=(10, 0))

        # Theme button
        self.theme_btn = tk.Button(
            self.btn_frame,
            text="Theme",
            command=self.next_theme,
            bg=self.colors["bg_box"],
            fg=self.colors["text"],
            activebackground=self.colors["border"],
            activeforeground=self.colors["text"],
            relief=tk.FLAT,
            font=("Consolas", 9),
            cursor="hand2",
            padx=10
        )
        self.theme_btn.pack(side=tk.LEFT)

        # Close button
        self.close_btn = tk.Button(
            self.btn_frame,
            text="Close",
            command=self.root.destroy,
            bg=self.colors["bg_box"],
            fg=self.colors["text"],
            activebackground=self.colors["border"],
            activeforeground=self.colors["text"],
            relief=tk.FLAT,
            font=("Consolas", 9),
            cursor="hand2",
            padx=10
        )
        self.close_btn.pack(side=tk.RIGHT)

        # Version label
        self.version_label = tk.Label(
            self.btn_frame,
            text="v2.0.0",
            font=("Consolas", 9),
            fg=self.colors["text_dim"],
            bg=self.colors["bg"]
        )
        self.version_label.pack(side=tk.LEFT, padx=10)

    def next_theme(self):
        """Switch to next theme"""
        self.theme_index = (self.theme_index + 1) % len(self.theme_names)
        self.colors = THEMES[self.theme_names[self.theme_index]].copy()
        self.apply_theme()

    def apply_theme(self):
        """Apply current theme to all widgets"""
        bg = self.colors["bg"]
        bg_box = self.colors["bg_box"]
        border = self.colors["border"]
        text = self.colors["text"]
        text_dim = self.colors["text_dim"]

        self.root.configure(bg=bg)
        self.main_frame.configure(bg=bg)
        self.header_frame.configure(bg=bg)
        self.title_label.configure(fg=self.colors["title"], bg=bg)
        self.os_label.configure(fg=text_dim, bg=bg)
        self.btn_frame.configure(bg=bg)
        self.theme_btn.configure(bg=bg_box, fg=text, activebackground=border)
        self.close_btn.configure(bg=bg_box, fg=text, activebackground=border)
        self.version_label.configure(fg=text_dim, bg=bg)

        # Update sections
        for section, color_key in [
            (self.cpu_section, "cpu"),
            (self.gpu_section, "gpu"),
            (self.mem_section, "mem"),
            (self.disk_section, "disk"),
            (self.net_section, "net"),
        ]:
            color = self.colors[color_key]
            section["color"] = color
            section["container"].configure(bg=bg_box, highlightbackground=border)
            section["title_frame"].configure(bg=bg_box)
            section["title"].configure(fg=color, bg=bg_box)
            section["value"].configure(fg=text, bg=bg_box)
            section["info"].configure(fg=text_dim, bg=bg_box)
            section["canvas"].configure(bg=border)
            if section["graph"]:
                section["graph"].set_color(color, bg_box)

    def start_drag(self, event):
        self.drag_x = event.x
        self.drag_y = event.y

    def do_drag(self, event):
        x = self.root.winfo_x() + event.x - self.drag_x
        y = self.root.winfo_y() + event.y - self.drag_y
        self.root.geometry(f"+{x}+{y}")

    def get_color_for_percent(self, percent):
        """Get color based on usage percentage"""
        if percent < 50:
            return self.colors["low"]
        elif percent < 80:
            return self.colors["mid"]
        else:
            return self.colors["high"]

    def update_bar(self, section, percent, value_text, info_text):
        """Update a section's progress bar and labels"""
        try:
            section["value"].config(text=value_text)
            section["info"].config(text=info_text)

            canvas = section["canvas"]
            canvas.delete("all")

            width = canvas.winfo_width()
            if width < 10:
                width = 300

            # Background
            canvas.create_rectangle(0, 0, width, 8, fill=self.colors["border"], outline="")

            # Filled bar
            filled_width = int(width * percent / 100)
            if filled_width > 0:
                color = self.get_color_for_percent(percent)
                canvas.create_rectangle(0, 0, filled_width, 8, fill=color, outline="")

            # Update graph if present
            if section["graph"]:
                section["graph"].update(percent)

        except tk.TclError:
            pass

    def get_cpu_info(self):
        """Get CPU stats"""
        try:
            percent = psutil.cpu_percent(interval=0.1)
            freq = psutil.cpu_freq()
            freq_str = f"{freq.current:.0f}MHz" if freq else "N/A"
            cores = psutil.cpu_count(logical=False) or psutil.cpu_count()
            threads = psutil.cpu_count()
            return percent, f"{percent:.1f}%", f"{cores}C/{threads}T @ {freq_str}"
        except:
            return 0, "0%", "Error"

    def get_gpu_info(self):
        """Get GPU stats"""
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu",
                 "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=2
            )
            if result.returncode == 0:
                parts = result.stdout.strip().split(", ")
                if len(parts) >= 4:
                    usage = float(parts[0])
                    vram_used = float(parts[1])
                    vram_total = float(parts[2])
                    temp = float(parts[3])
                    return usage, f"{usage:.0f}%", f"{vram_used:.0f}/{vram_total:.0f}MB | {temp:.0f}C"
        except:
            pass
        return 0, "N/A", "No GPU stats"

    def get_mem_info(self):
        """Get memory stats"""
        try:
            mem = psutil.virtual_memory()
            used_gb = mem.used / (1024**3)
            total_gb = mem.total / (1024**3)
            return mem.percent, f"{mem.percent:.1f}%", f"{used_gb:.1f} / {total_gb:.1f} GB"
        except:
            return 0, "0%", "Error"

    def get_disk_info(self):
        """Get disk stats"""
        try:
            disk = psutil.disk_usage("/")
            used_gb = disk.used / (1024**3)
            total_gb = disk.total / (1024**3)
            return disk.percent, f"{disk.percent:.1f}%", f"{used_gb:.0f} / {total_gb:.0f} GB"
        except:
            return 0, "0%", "Error"

    def get_net_info(self):
        """Get network stats"""
        try:
            net = psutil.net_io_counters()
            sent_mb = net.bytes_sent / (1024**2)
            recv_mb = net.bytes_recv / (1024**2)

            # Format nicely
            if sent_mb > 1024:
                sent_str = f"{sent_mb/1024:.1f}GB"
            else:
                sent_str = f"{sent_mb:.0f}MB"

            if recv_mb > 1024:
                recv_str = f"{recv_mb/1024:.1f}GB"
            else:
                recv_str = f"{recv_mb:.0f}MB"

            return 0, "", f"TX: {sent_str} | RX: {recv_str}"
        except:
            return 0, "", "Error"

    def update_stats(self):
        """Update all stats"""
        try:
            # CPU
            cpu_pct, cpu_val, cpu_info = self.get_cpu_info()
            self.root.after(0, lambda: self.update_bar(self.cpu_section, cpu_pct, cpu_val, cpu_info))

            # GPU
            gpu_pct, gpu_val, gpu_info = self.get_gpu_info()
            self.root.after(0, lambda: self.update_bar(self.gpu_section, gpu_pct, gpu_val, gpu_info))

            # Memory
            mem_pct, mem_val, mem_info = self.get_mem_info()
            self.root.after(0, lambda: self.update_bar(self.mem_section, mem_pct, mem_val, mem_info))

            # Disk
            disk_pct, disk_val, disk_info = self.get_disk_info()
            self.root.after(0, lambda: self.update_bar(self.disk_section, disk_pct, disk_val, disk_info))

            # Network (no percentage bar)
            net_pct, net_val, net_info = self.get_net_info()
            self.root.after(0, lambda: self.update_bar(self.net_section, 0, "", net_info))

        except Exception as e:
            pass

    def update_loop(self):
        """Background update loop"""
        while self.running:
            self.update_stats()
            time.sleep(1)

    def on_close(self):
        """Handle window close"""
        self.running = False
        self.root.destroy()

    def run(self):
        """Start the widget"""
        self.root.mainloop()


def main():
    """Main entry point"""
    try:
        widget = WellzWidget()
        widget.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
