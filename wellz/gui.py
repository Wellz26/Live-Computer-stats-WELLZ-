#!/usr/bin/env python3
"""
Wellz GUI - Gaming PC Stats Widget
A compact always-on-top system monitor widget
"""

import subprocess
import sys
import threading
import time
import platform
import socket
from datetime import timedelta

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    print("Error: tkinter not available. Install python3-tk")
    sys.exit(1)

try:
    import psutil
except ImportError:
    print("Error: psutil not installed. Run: pip install psutil")
    sys.exit(1)


class WellzWidget:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Wellz")

        # Make window always on top
        self.root.attributes("-topmost", True)

        # Remove window decorations for a cleaner look (optional)
        # self.root.overrideredirect(True)

        # Set window size and position (top-right corner)
        self.width = 280
        self.height = 420
        screen_width = self.root.winfo_screenwidth()
        x_position = screen_width - self.width - 20
        y_position = 40
        self.root.geometry(f"{self.width}x{self.height}+{x_position}+{y_position}")

        # Dark theme colors
        self.bg_color = "#1a1a2e"
        self.fg_color = "#eaeaea"
        self.accent_cyan = "#00d9ff"
        self.accent_green = "#00ff88"
        self.accent_yellow = "#ffcc00"
        self.accent_red = "#ff4444"
        self.accent_blue = "#4488ff"
        self.accent_magenta = "#ff44ff"
        self.box_bg = "#16213e"

        self.root.configure(bg=self.bg_color)

        # Make window semi-transparent (Linux/X11)
        try:
            self.root.attributes("-alpha", 0.95)
        except:
            pass

        # Create main frame
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Header
        header = tk.Label(
            self.main_frame,
            text="WELLZ",
            font=("Consolas", 16, "bold"),
            fg=self.accent_cyan,
            bg=self.bg_color
        )
        header.pack(pady=(0, 5))

        subtitle = tk.Label(
            self.main_frame,
            text="Gaming PC Stats",
            font=("Consolas", 9),
            fg="#888888",
            bg=self.bg_color
        )
        subtitle.pack(pady=(0, 10))

        # Stats sections
        self.cpu_frame = self.create_stat_section("CPU", self.accent_green)
        self.gpu_frame = self.create_stat_section("GPU", self.accent_yellow)
        self.ram_frame = self.create_stat_section("RAM", self.accent_blue)
        self.disk_frame = self.create_stat_section("DISK", self.accent_magenta)

        # Control buttons
        btn_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        close_btn = tk.Button(
            btn_frame,
            text="Close",
            command=self.root.destroy,
            bg="#333344",
            fg=self.fg_color,
            activebackground="#444455",
            activeforeground=self.fg_color,
            relief=tk.FLAT,
            font=("Consolas", 9),
            cursor="hand2"
        )
        close_btn.pack(side=tk.RIGHT, padx=2)

        # Allow dragging the window
        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.do_drag)

        # Start update thread
        self.running = True
        self.update_thread = threading.Thread(target=self.update_loop, daemon=True)
        self.update_thread.start()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def start_drag(self, event):
        self.drag_x = event.x
        self.drag_y = event.y

    def do_drag(self, event):
        x = self.root.winfo_x() + event.x - self.drag_x
        y = self.root.winfo_y() + event.y - self.drag_y
        self.root.geometry(f"+{x}+{y}")

    def create_stat_section(self, title, color):
        frame = tk.Frame(self.main_frame, bg=self.box_bg, relief=tk.FLAT)
        frame.pack(fill=tk.X, pady=4)

        # Title
        title_label = tk.Label(
            frame,
            text=f" {title}",
            font=("Consolas", 10, "bold"),
            fg=color,
            bg=self.box_bg,
            anchor="w"
        )
        title_label.pack(fill=tk.X, padx=8, pady=(6, 2))

        # Info label
        info_label = tk.Label(
            frame,
            text="Loading...",
            font=("Consolas", 9),
            fg=self.fg_color,
            bg=self.box_bg,
            anchor="w"
        )
        info_label.pack(fill=tk.X, padx=8, pady=(0, 2))

        # Progress bar frame
        bar_frame = tk.Frame(frame, bg=self.box_bg)
        bar_frame.pack(fill=tk.X, padx=8, pady=(0, 6))

        # Custom progress bar using canvas
        canvas = tk.Canvas(
            bar_frame,
            height=12,
            bg="#0a0a15",
            highlightthickness=0
        )
        canvas.pack(fill=tk.X)

        # Percentage label
        pct_label = tk.Label(
            bar_frame,
            text="0%",
            font=("Consolas", 9, "bold"),
            fg=color,
            bg=self.box_bg
        )
        pct_label.pack(anchor="e")

        return {
            "frame": frame,
            "info": info_label,
            "canvas": canvas,
            "pct": pct_label,
            "color": color
        }

    def get_color_for_percent(self, percent):
        if percent < 50:
            return self.accent_green
        elif percent < 80:
            return self.accent_yellow
        else:
            return self.accent_red

    def update_progress_bar(self, section, percent, info_text):
        try:
            section["info"].config(text=info_text)
            section["pct"].config(text=f"{percent:.1f}%")

            canvas = section["canvas"]
            canvas.delete("all")

            width = canvas.winfo_width()
            if width < 10:
                width = 250

            filled_width = int(width * percent / 100)
            color = self.get_color_for_percent(percent)

            # Background
            canvas.create_rectangle(0, 0, width, 12, fill="#0a0a15", outline="")
            # Filled portion
            if filled_width > 0:
                canvas.create_rectangle(0, 0, filled_width, 12, fill=color, outline="")
        except tk.TclError:
            pass  # Widget destroyed

    def get_cpu_info(self):
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_freq = psutil.cpu_freq()
            freq_str = f"{cpu_freq.current:.0f}MHz" if cpu_freq else "N/A"

            # Get CPU model
            cpu_model = "CPU"
            try:
                with open("/proc/cpuinfo", "r") as f:
                    for line in f:
                        if "model name" in line:
                            cpu_model = line.split(":")[1].strip()
                            # Shorten the name
                            if "Intel" in cpu_model:
                                parts = cpu_model.split()
                                cpu_model = " ".join(parts[1:4]) if len(parts) > 3 else cpu_model[:20]
                            elif "AMD" in cpu_model:
                                cpu_model = cpu_model.replace("AMD ", "")[:20]
                            else:
                                cpu_model = cpu_model[:20]
                            break
            except:
                cpu_model = platform.processor()[:20] or "CPU"

            return cpu_percent, f"{cpu_model} @ {freq_str}"
        except:
            return 0, "Error"

    def get_gpu_info(self):
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,utilization.gpu,memory.used,memory.total",
                 "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=2
            )
            if result.returncode == 0:
                parts = result.stdout.strip().split(", ")
                if len(parts) >= 4:
                    name = parts[0].replace("NVIDIA ", "").replace("GeForce ", "")[:20]
                    usage = float(parts[1])
                    vram_used = float(parts[2])
                    vram_total = float(parts[3])
                    return usage, f"{name} ({vram_used:.0f}/{vram_total:.0f}MB)"
        except:
            pass
        return None, "No GPU stats"

    def get_ram_info(self):
        try:
            mem = psutil.virtual_memory()
            used_gb = mem.used / (1024**3)
            total_gb = mem.total / (1024**3)
            return mem.percent, f"{used_gb:.1f} / {total_gb:.1f} GB"
        except:
            return 0, "Error"

    def get_disk_info(self):
        try:
            disk = psutil.disk_usage("/")
            used_gb = disk.used / (1024**3)
            total_gb = disk.total / (1024**3)
            return disk.percent, f"{used_gb:.0f} / {total_gb:.0f} GB"
        except:
            return 0, "Error"

    def update_stats(self):
        try:
            # CPU
            cpu_pct, cpu_info = self.get_cpu_info()
            self.root.after(0, lambda: self.update_progress_bar(self.cpu_frame, cpu_pct, cpu_info))

            # GPU
            gpu_pct, gpu_info = self.get_gpu_info()
            if gpu_pct is not None:
                self.root.after(0, lambda: self.update_progress_bar(self.gpu_frame, gpu_pct, gpu_info))
            else:
                self.root.after(0, lambda: self.update_progress_bar(self.gpu_frame, 0, gpu_info))

            # RAM
            ram_pct, ram_info = self.get_ram_info()
            self.root.after(0, lambda: self.update_progress_bar(self.ram_frame, ram_pct, ram_info))

            # Disk
            disk_pct, disk_info = self.get_disk_info()
            self.root.after(0, lambda: self.update_progress_bar(self.disk_frame, disk_pct, disk_info))

        except Exception as e:
            pass

    def update_loop(self):
        while self.running:
            self.update_stats()
            time.sleep(1)

    def on_close(self):
        self.running = False
        self.root.destroy()

    def run(self):
        self.root.mainloop()


def main():
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
