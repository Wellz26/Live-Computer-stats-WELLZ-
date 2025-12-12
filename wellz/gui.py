#!/usr/bin/env python3
"""
Wellz GUI - Gaming PC Stats Widget
A btop-inspired always-on-top system monitor widget
"""

import subprocess
import sys
import threading
import time
import platform
import socket

try:
    import tkinter as tk
    from tkinter import font as tkfont
except ImportError:
    print("Error: tkinter not available. Install python3-tk")
    sys.exit(1)

try:
    import psutil
except ImportError:
    print("Error: psutil not installed. Run: pip install psutil")
    sys.exit(1)


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
# MAIN WIDGET CLASS
# ============================================================================

class WellzWidget:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Wellz")

        # Make window always on top
        self.root.attributes("-topmost", True)

        # Set window size and position (top-right corner)
        self.width = 320
        self.height = 480
        screen_width = self.root.winfo_screenwidth()
        x_position = screen_width - self.width - 20
        y_position = 40
        self.root.geometry(f"{self.width}x{self.height}+{x_position}+{y_position}")

        # Dark theme colors (btop-inspired)
        self.colors = {
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
        }

        self.root.configure(bg=self.colors["bg"])

        # Try to make window semi-transparent
        try:
            self.root.attributes("-alpha", 0.95)
        except:
            pass

        # Remove window decorations for cleaner look (optional)
        # self.root.overrideredirect(True)

        # Create main frame
        self.main_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Header
        self.create_header()

        # Stats sections
        self.cpu_section = self.create_section("CPU", self.colors["cpu"])
        self.gpu_section = self.create_section("GPU", self.colors["gpu"])
        self.mem_section = self.create_section("MEMORY", self.colors["mem"])
        self.disk_section = self.create_section("DISK", self.colors["disk"])
        self.net_section = self.create_section("NETWORK", self.colors["net"])

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
        header_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        header_frame.pack(fill=tk.X, pady=(0, 10))

        # Title
        title = tk.Label(
            header_frame,
            text="WELLZ",
            font=("Consolas", 18, "bold"),
            fg=self.colors["title"],
            bg=self.colors["bg"]
        )
        title.pack(side=tk.LEFT)

        # OS indicator
        os_type = get_os_type()
        os_icon = get_os_icon(os_type)
        os_label = tk.Label(
            header_frame,
            text=os_icon,
            font=("Consolas", 10),
            fg=self.colors["text_dim"],
            bg=self.colors["bg"]
        )
        os_label.pack(side=tk.RIGHT)

    def create_section(self, title, color):
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

        # Info label
        info_label = tk.Label(
            container,
            text="Loading...",
            font=("Consolas", 9),
            fg=self.colors["text_dim"],
            bg=self.colors["bg_box"],
            anchor="w"
        )
        info_label.pack(fill=tk.X, padx=8, pady=(0, 2))

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
            "color": color
        }

    def create_controls(self):
        """Create control buttons"""
        btn_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        close_btn = tk.Button(
            btn_frame,
            text="Close",
            command=self.root.destroy,
            bg=self.colors["bg_box"],
            fg=self.colors["text"],
            activebackground=self.colors["border"],
            activeforeground=self.colors["text"],
            relief=tk.FLAT,
            font=("Consolas", 9),
            cursor="hand2",
            padx=15
        )
        close_btn.pack(side=tk.RIGHT)

        # Version label
        version_label = tk.Label(
            btn_frame,
            text="v1.0.0",
            font=("Consolas", 9),
            fg=self.colors["text_dim"],
            bg=self.colors["bg"]
        )
        version_label.pack(side=tk.LEFT)

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
                width = 280

            # Background
            canvas.create_rectangle(0, 0, width, 8, fill=self.colors["border"], outline="")

            # Filled bar
            filled_width = int(width * percent / 100)
            if filled_width > 0:
                color = self.get_color_for_percent(percent)
                canvas.create_rectangle(0, 0, filled_width, 8, fill=color, outline="")
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
