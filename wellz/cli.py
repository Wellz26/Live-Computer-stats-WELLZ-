#!/usr/bin/env python3
"""
Wellz - Gaming PC Stats Dashboard
A visually artistic system stats display for your gaming rig
"""

import argparse
import os
import platform
import socket
import subprocess
import sys
import time
from datetime import timedelta

try:
    import psutil
except ImportError:
    print("\033[91mError: psutil not installed. Run: pip install psutil\033[0m")
    sys.exit(1)

# ANSI Color codes
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Regular colors
    BLACK = "\033[30m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

    # Background colors
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"

    # Cursor control
    HIDE_CURSOR = "\033[?25l"
    SHOW_CURSOR = "\033[?25h"
    CLEAR_SCREEN = "\033[2J\033[H"


def get_color_for_percent(percent):
    """Return color based on usage percentage"""
    if percent < 50:
        return Colors.GREEN
    elif percent < 80:
        return Colors.YELLOW
    else:
        return Colors.RED


def create_bar(percent, width=20, filled_char="█", empty_char="░"):
    """Create a progress bar with color"""
    filled = int(width * percent / 100)
    empty = width - filled
    color = get_color_for_percent(percent)
    return f"{color}{filled_char * filled}{Colors.DIM}{empty_char * empty}{Colors.RESET}"


def get_cpu_info(interval=0.1):
    """Get CPU information"""
    try:
        cpu_percent = psutil.cpu_percent(interval=interval)
        cpu_freq = psutil.cpu_freq()
        cpu_count = psutil.cpu_count()
        cpu_count_physical = psutil.cpu_count(logical=False)

        # Try to get CPU model
        cpu_model = "Unknown CPU"
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line:
                        cpu_model = line.split(":")[1].strip()
                        break
        except:
            cpu_model = platform.processor() or "Unknown CPU"

        freq_str = f"{cpu_freq.current:.0f}MHz" if cpu_freq else "N/A"

        return {
            "model": cpu_model,
            "usage": cpu_percent,
            "freq": freq_str,
            "cores": cpu_count_physical,
            "threads": cpu_count
        }
    except Exception as e:
        return {"model": "Error", "usage": 0, "freq": "N/A", "cores": 0, "threads": 0}


def get_gpu_info():
    """Get GPU information (NVIDIA)"""
    gpu_info = {"name": "No GPU detected", "usage": None, "vram_used": None, "vram_total": None}

    # Try NVIDIA GPU
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,utilization.gpu,memory.used,memory.total",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            parts = result.stdout.strip().split(", ")
            if len(parts) >= 4:
                gpu_info["name"] = parts[0]
                gpu_info["usage"] = float(parts[1])
                gpu_info["vram_used"] = float(parts[2])
                gpu_info["vram_total"] = float(parts[3])
                return gpu_info
    except:
        pass

    # Try AMD GPU (basic detection)
    try:
        result = subprocess.run(["lspci"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                if "VGA" in line or "3D" in line:
                    if "AMD" in line or "ATI" in line:
                        gpu_info["name"] = "AMD GPU (detected via lspci)"
                    elif "Intel" in line:
                        gpu_info["name"] = "Intel Integrated Graphics"
                    elif "NVIDIA" in line:
                        gpu_info["name"] = "NVIDIA GPU (nvidia-smi unavailable)"
                    break
    except:
        pass

    return gpu_info


def get_ram_info():
    """Get RAM information"""
    mem = psutil.virtual_memory()
    return {
        "total": mem.total / (1024**3),  # GB
        "used": mem.used / (1024**3),
        "percent": mem.percent
    }


def get_disk_info():
    """Get disk information"""
    try:
        disk = psutil.disk_usage("/")
        return {
            "total": disk.total / (1024**3),  # GB
            "used": disk.used / (1024**3),
            "percent": disk.percent
        }
    except:
        return {"total": 0, "used": 0, "percent": 0}


def get_network_info():
    """Get network information"""
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)

        net_io = psutil.net_io_counters()
        sent = net_io.bytes_sent / (1024**2)  # MB
        recv = net_io.bytes_recv / (1024**2)

        return {
            "hostname": hostname,
            "ip": ip,
            "sent_mb": sent,
            "recv_mb": recv
        }
    except:
        return {"hostname": "Unknown", "ip": "N/A", "sent_mb": 0, "recv_mb": 0}


def get_os_info():
    """Get OS information"""
    try:
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        uptime = str(timedelta(seconds=int(uptime_seconds)))

        return {
            "os": f"{platform.system()} {platform.release()}",
            "uptime": uptime,
            "arch": platform.machine()
        }
    except:
        return {"os": "Unknown", "uptime": "N/A", "arch": "Unknown"}


def print_dashboard(live_mode=False):
    """Print the gaming PC dashboard"""

    # Gather all info
    cpu = get_cpu_info(interval=0.1 if live_mode else 0.5)
    gpu = get_gpu_info()
    ram = get_ram_info()
    disk = get_disk_info()
    net = get_network_info()
    os_info = get_os_info()

    # ASCII Art Header
    header = f"""
{Colors.CYAN}{Colors.BOLD}
    ██╗    ██╗███████╗██╗     ██╗     ███████╗
    ██║    ██║██╔════╝██║     ██║     ╚══███╔╝
    ██║ █╗ ██║█████╗  ██║     ██║       ███╔╝
    ██║███╗██║██╔══╝  ██║     ██║      ███╔╝
    ╚███╔███╔╝███████╗███████╗███████╗███████╗
     ╚══╝╚══╝ ╚══════╝╚══════╝╚══════╝╚══════╝
{Colors.RESET}{Colors.DIM}         ⚡ Gaming PC Stats Dashboard ⚡{Colors.RESET}
"""
    print(header)

    # Box drawing characters
    TL = "╭"  # Top-left
    TR = "╮"  # Top-right
    BL = "╰"  # Bottom-left
    BR = "╯"  # Bottom-right
    H = "─"   # Horizontal
    V = "│"   # Vertical

    box_width = 58

    # System info section
    print(f"  {Colors.MAGENTA}{TL}{H * box_width}{TR}{Colors.RESET}")
    print(f"  {Colors.MAGENTA}{V}{Colors.RESET}  {Colors.BOLD}🖥️  SYSTEM{Colors.RESET}{' ' * 47}{Colors.MAGENTA}{V}{Colors.RESET}")
    print(f"  {Colors.MAGENTA}{V}{Colors.RESET}  {Colors.DIM}OS:{Colors.RESET} {os_info['os']:<30} {Colors.DIM}Arch:{Colors.RESET} {os_info['arch']:<10}{Colors.MAGENTA}{V}{Colors.RESET}")
    print(f"  {Colors.MAGENTA}{V}{Colors.RESET}  {Colors.DIM}Uptime:{Colors.RESET} {os_info['uptime']:<47}{Colors.MAGENTA}{V}{Colors.RESET}")
    print(f"  {Colors.MAGENTA}{BL}{H * box_width}{BR}{Colors.RESET}")
    print()

    # CPU Section
    print(f"  {Colors.GREEN}{TL}{H * box_width}{TR}{Colors.RESET}")
    print(f"  {Colors.GREEN}{V}{Colors.RESET}  {Colors.BOLD}🔥 CPU{Colors.RESET}{' ' * 50}{Colors.GREEN}{V}{Colors.RESET}")

    # Truncate CPU model if too long
    cpu_model = cpu['model'][:42] + "..." if len(cpu['model']) > 45 else cpu['model']
    print(f"  {Colors.GREEN}{V}{Colors.RESET}  {Colors.CYAN}{cpu_model:<55}{Colors.GREEN}{V}{Colors.RESET}")
    print(f"  {Colors.GREEN}{V}{Colors.RESET}  Cores: {cpu['cores']}  Threads: {cpu['threads']}  Freq: {cpu['freq']:<24}{Colors.GREEN}{V}{Colors.RESET}")
    print(f"  {Colors.GREEN}{V}{Colors.RESET}  Usage: [{create_bar(cpu['usage'], 30)}] {cpu['usage']:5.1f}%     {Colors.GREEN}{V}{Colors.RESET}")
    print(f"  {Colors.GREEN}{BL}{H * box_width}{BR}{Colors.RESET}")
    print()

    # GPU Section
    print(f"  {Colors.YELLOW}{TL}{H * box_width}{TR}{Colors.RESET}")
    print(f"  {Colors.YELLOW}{V}{Colors.RESET}  {Colors.BOLD}🎮 GPU{Colors.RESET}{' ' * 50}{Colors.YELLOW}{V}{Colors.RESET}")

    gpu_name = gpu['name'][:45] + "..." if len(gpu['name']) > 48 else gpu['name']
    print(f"  {Colors.YELLOW}{V}{Colors.RESET}  {Colors.CYAN}{gpu_name:<55}{Colors.YELLOW}{V}{Colors.RESET}")

    if gpu['usage'] is not None:
        print(f"  {Colors.YELLOW}{V}{Colors.RESET}  Usage: [{create_bar(gpu['usage'], 30)}] {gpu['usage']:5.1f}%     {Colors.YELLOW}{V}{Colors.RESET}")
        if gpu['vram_total']:
            vram_percent = (gpu['vram_used'] / gpu['vram_total']) * 100
            print(f"  {Colors.YELLOW}{V}{Colors.RESET}  VRAM:  [{create_bar(vram_percent, 30)}] {gpu['vram_used']:.0f}/{gpu['vram_total']:.0f} MB  {Colors.YELLOW}{V}{Colors.RESET}")
    else:
        print(f"  {Colors.YELLOW}{V}{Colors.RESET}  {Colors.DIM}(Usage stats unavailable - install nvidia-smi){Colors.RESET}       {Colors.YELLOW}{V}{Colors.RESET}")

    print(f"  {Colors.YELLOW}{BL}{H * box_width}{BR}{Colors.RESET}")
    print()

    # RAM Section
    print(f"  {Colors.BLUE}{TL}{H * box_width}{TR}{Colors.RESET}")
    print(f"  {Colors.BLUE}{V}{Colors.RESET}  {Colors.BOLD}💾 RAM{Colors.RESET}{' ' * 50}{Colors.BLUE}{V}{Colors.RESET}")
    print(f"  {Colors.BLUE}{V}{Colors.RESET}  Memory: [{create_bar(ram['percent'], 30)}] {ram['used']:.1f}/{ram['total']:.1f} GB  {Colors.BLUE}{V}{Colors.RESET}")
    print(f"  {Colors.BLUE}{BL}{H * box_width}{BR}{Colors.RESET}")
    print()

    # Disk Section
    print(f"  {Colors.MAGENTA}{TL}{H * box_width}{TR}{Colors.RESET}")
    print(f"  {Colors.MAGENTA}{V}{Colors.RESET}  {Colors.BOLD}💿 DISK{Colors.RESET}{' ' * 49}{Colors.MAGENTA}{V}{Colors.RESET}")
    print(f"  {Colors.MAGENTA}{V}{Colors.RESET}  Storage: [{create_bar(disk['percent'], 30)}] {disk['used']:.0f}/{disk['total']:.0f} GB  {Colors.MAGENTA}{V}{Colors.RESET}")
    print(f"  {Colors.MAGENTA}{BL}{H * box_width}{BR}{Colors.RESET}")
    print()

    # Network Section
    print(f"  {Colors.CYAN}{TL}{H * box_width}{TR}{Colors.RESET}")
    print(f"  {Colors.CYAN}{V}{Colors.RESET}  {Colors.BOLD}🌐 NETWORK{Colors.RESET}{' ' * 46}{Colors.CYAN}{V}{Colors.RESET}")
    print(f"  {Colors.CYAN}{V}{Colors.RESET}  Host: {net['hostname']:<25} IP: {net['ip']:<16}{Colors.CYAN}{V}{Colors.RESET}")
    print(f"  {Colors.CYAN}{V}{Colors.RESET}  {Colors.GREEN}↑{Colors.RESET} Sent: {net['sent_mb']:.1f} MB    {Colors.BLUE}↓{Colors.RESET} Recv: {net['recv_mb']:.1f} MB{' ' * 21}{Colors.CYAN}{V}{Colors.RESET}")
    print(f"  {Colors.CYAN}{BL}{H * box_width}{BR}{Colors.RESET}")
    print()

    # Footer
    mode_text = "[LIVE]" if live_mode else ""
    print(f"  {Colors.DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print(f"  {Colors.DIM}Wellz v1.0.0 | Your Gaming Rig Stats {mode_text}{Colors.RESET}")
    if live_mode:
        print(f"  {Colors.DIM}Press Ctrl+C to exit{Colors.RESET}")
    print()


def run_live_mode(interval=1.0):
    """Run dashboard in continuous live mode"""
    print(Colors.HIDE_CURSOR, end="")
    try:
        while True:
            print(Colors.CLEAR_SCREEN, end="")
            print_dashboard(live_mode=True)
            time.sleep(interval)
    except KeyboardInterrupt:
        pass
    finally:
        print(Colors.SHOW_CURSOR, end="")
        print(f"\n{Colors.YELLOW}Exiting live mode...{Colors.RESET}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Wellz - Gaming PC Stats Dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  wellz              Show stats once
  wellz -l           Live mode (continuous updates)
  wellz -l -i 2      Live mode with 2 second refresh
  wellz-gui          Launch GUI widget (separate command)
        """
    )
    parser.add_argument(
        "-l", "--live",
        action="store_true",
        help="Enable live mode (continuous refresh)"
    )
    parser.add_argument(
        "-i", "--interval",
        type=float,
        default=1.0,
        help="Refresh interval in seconds for live mode (default: 1.0)"
    )

    args = parser.parse_args()

    try:
        if args.live:
            run_live_mode(interval=args.interval)
        else:
            print_dashboard()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted.{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()
