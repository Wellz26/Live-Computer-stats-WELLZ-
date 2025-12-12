#!/usr/bin/env python3
"""
Wellz - Gaming PC Stats Dashboard
A btop-inspired system monitoring tool

v2.0.0 - Interactive dashboard with graphs, themes, and process management
"""

import argparse
import sys

# Check for psutil
try:
    import psutil
except ImportError:
    print("\033[91mError: psutil not installed. Run: pip install psutil\033[0m")
    sys.exit(1)


def run_interactive(config_path=None):
    """Run the interactive dashboard (default mode)"""
    try:
        from .ui.app import WellzApp
        app = WellzApp(config_path=config_path)
        app.run()
    except ImportError as e:
        print(f"\033[91mError loading interactive mode: {e}\033[0m")
        print("Falling back to legacy mode...")
        run_legacy_live()
    except Exception as e:
        print(f"\033[91mError: {e}\033[0m")
        sys.exit(1)


def run_legacy_once():
    """Run legacy static mode (show stats once)"""
    from .core.collectors import (
        get_cpu_info, get_gpu_info, get_memory_info,
        get_disk_info, get_network_info, get_system_info,
        get_os_type, get_os_logo
    )

    # Import rendering helpers from legacy code
    import os
    import re

    # Colors
    RESET = "\033[0m"
    BOLD = "\033[1m"
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    THEME = {
        "title": BRIGHT_CYAN,
        "border": BRIGHT_BLACK,
        "label": BRIGHT_WHITE,
        "value": "\033[37m",
        "low": BRIGHT_GREEN,
        "mid": BRIGHT_YELLOW,
        "high": BRIGHT_RED,
        "accent": BRIGHT_MAGENTA,
        "cpu": BRIGHT_GREEN,
        "gpu": BRIGHT_YELLOW,
        "mem": BRIGHT_BLUE,
        "disk": BRIGHT_MAGENTA,
        "net": BRIGHT_CYAN,
    }

    def get_usage_color(percent):
        if percent < 50:
            return THEME["low"]
        elif percent < 80:
            return THEME["mid"]
        return THEME["high"]

    def create_bar(percent, width=20):
        filled = int(width * percent / 100)
        empty = width - filled
        color = get_usage_color(percent)
        return f"{color}{'█' * filled}{BRIGHT_BLACK}{'░' * empty}{RESET}"

    def format_bytes(b):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if b < 1024:
                return f"{b:.1f}{unit}"
            b /= 1024
        return f"{b:.1f}PB"

    def box_top(w, title=""):
        if title:
            padding = w - len(title) - 4
            return f"{BRIGHT_BLACK}╭─{RESET}{BRIGHT_CYAN} {title} {RESET}{BRIGHT_BLACK}{'─' * padding}╮{RESET}"
        return f"{BRIGHT_BLACK}╭{'─' * w}╮{RESET}"

    def box_line(content, w):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        visible = len(ansi_escape.sub('', content))
        padding = max(0, w - visible - 2)
        return f"{BRIGHT_BLACK}│{RESET} {content}{' ' * padding}{BRIGHT_BLACK}│{RESET}"

    def box_mid(w):
        return f"{BRIGHT_BLACK}├{'─' * w}┤{RESET}"

    def box_bottom(w):
        return f"{BRIGHT_BLACK}╰{'─' * w}╯{RESET}"

    # Gather data
    os_type = get_os_type()
    logo_color, logo_lines = get_os_logo(os_type)
    cpu = get_cpu_info()
    gpu = get_gpu_info()
    mem = get_memory_info()
    disks = get_disk_info()
    net = get_network_info()
    sys_info = get_system_info()

    # Header
    print(f"""
{BRIGHT_CYAN}{BOLD}██╗    ██╗███████╗██╗     ██╗     ███████╗{RESET}
{BRIGHT_CYAN}{BOLD}██║    ██║██╔════╝██║     ██║     ╚══███╔╝{RESET}
{BRIGHT_CYAN}{BOLD}██║ █╗ ██║█████╗  ██║     ██║       ███╔╝ {RESET}
{BRIGHT_CYAN}{BOLD}██║███╗██║██╔══╝  ██║     ██║      ███╔╝  {RESET}
{BRIGHT_CYAN}{BOLD}╚███╔███╔╝███████╗███████╗███████╗███████╗{RESET}
{BRIGHT_CYAN}{BOLD} ╚══╝╚══╝ ╚══════╝╚══════╝╚══════╝╚══════╝{RESET}
""")

    box_w = 38

    # System box
    sys_lines = [box_top(box_w, "SYSTEM")]
    sys_lines.append(box_line(f"{THEME['label']}OS{RESET}      {sys_info['os']} {sys_info['release']}", box_w))
    sys_lines.append(box_line(f"{THEME['label']}Host{RESET}    {sys_info['hostname']}", box_w))
    sys_lines.append(box_line(f"{THEME['label']}Arch{RESET}    {sys_info['arch']}", box_w))
    sys_lines.append(box_line(f"{THEME['label']}Uptime{RESET}  {sys_info['uptime']}", box_w))
    sys_lines.append(box_mid(box_w))
    for line in logo_lines[:7]:
        sys_lines.append(box_line(f"{logo_color}{line}{RESET}", box_w))
    sys_lines.append(box_bottom(box_w))

    # CPU box
    cpu_lines = [box_top(box_w, "CPU")]
    model = cpu['model'][:32] + "..." if len(cpu['model']) > 35 else cpu['model']
    cpu_lines.append(box_line(f"{THEME['value']}{model}{RESET}", box_w))
    cpu_lines.append(box_line(f"{THEME['label']}Cores{RESET} {cpu['cores']}  {THEME['label']}Threads{RESET} {cpu['threads']}  {THEME['label']}Freq{RESET} {cpu['freq_current']:.0f}MHz", box_w))
    cpu_lines.append(box_mid(box_w))
    cpu_lines.append(box_line(f"{THEME['label']}Total{RESET}  [{create_bar(cpu['usage'], 20)}] {cpu['usage']:5.1f}%", box_w))

    # Per-core
    cores = cpu['per_core'][:8]
    if cores:
        core_str1 = ""
        for i, c in enumerate(cores[:4]):
            color = get_usage_color(c)
            core_str1 += f"{THEME['label']}{i}{RESET}{color}{'█' * int(c/20):<5}{RESET}"
        cpu_lines.append(box_line(core_str1, box_w))
        if len(cores) > 4:
            core_str2 = ""
            for i, c in enumerate(cores[4:8], 4):
                color = get_usage_color(c)
                core_str2 += f"{THEME['label']}{i}{RESET}{color}{'█' * int(c/20):<5}{RESET}"
            cpu_lines.append(box_line(core_str2, box_w))
    cpu_lines.append(box_bottom(box_w))

    # Print side by side
    max_len = max(len(sys_lines), len(cpu_lines))
    while len(sys_lines) < max_len:
        sys_lines.append(" " * (box_w + 2))
    while len(cpu_lines) < max_len:
        cpu_lines.append(" " * (box_w + 2))
    for sl, cl in zip(sys_lines, cpu_lines):
        print(f"  {sl}  {cl}")

    print()

    # GPU box
    gpu_lines = [box_top(box_w, "GPU")]
    gpu_name = gpu['name'][:32] + "..." if len(gpu['name']) > 35 else gpu['name']
    gpu_lines.append(box_line(f"{THEME['value']}{gpu_name}{RESET}", box_w))
    if gpu['usage'] is not None:
        gpu_lines.append(box_line(f"{THEME['label']}Usage{RESET}  [{create_bar(gpu['usage'], 20)}] {gpu['usage']:5.1f}%", box_w))
        if gpu['vram_total']:
            vram_pct = (gpu['vram_used'] / gpu['vram_total']) * 100
            gpu_lines.append(box_line(f"{THEME['label']}VRAM{RESET}   [{create_bar(vram_pct, 20)}] {gpu['vram_used']:.0f}/{gpu['vram_total']:.0f}MB", box_w))
        if gpu['temp']:
            temp_color = get_usage_color(gpu['temp'])
            gpu_lines.append(box_line(f"{THEME['label']}Temp{RESET}   {temp_color}{gpu['temp']:.0f}C{RESET}", box_w))
    else:
        gpu_lines.append(box_line(f"{BRIGHT_BLACK}Stats unavailable{RESET}", box_w))
    gpu_lines.append(box_bottom(box_w))

    # Memory box
    mem_lines = [box_top(box_w, "MEMORY")]
    mem_lines.append(box_line(f"{THEME['label']}RAM{RESET}    [{create_bar(mem['percent'], 20)}] {mem['used']:.1f}/{mem['total']:.1f}GB", box_w))
    mem_lines.append(box_line(f"{THEME['label']}Avail{RESET}  {mem['available']:.1f}GB", box_w))
    if mem['swap_total'] > 0:
        mem_lines.append(box_line(f"{THEME['label']}Swap{RESET}   [{create_bar(mem['swap_percent'], 20)}] {mem['swap_used']:.1f}/{mem['swap_total']:.1f}GB", box_w))
    mem_lines.append(box_bottom(box_w))

    # Print side by side
    max_len = max(len(gpu_lines), len(mem_lines))
    while len(gpu_lines) < max_len:
        gpu_lines.append(" " * (box_w + 2))
    while len(mem_lines) < max_len:
        mem_lines.append(" " * (box_w + 2))
    for gl, ml in zip(gpu_lines, mem_lines):
        print(f"  {gl}  {ml}")

    print()

    # Disk box
    disk_lines = [box_top(box_w, "DISK")]
    for disk in disks[:3]:
        mount = disk['mount'][:10]
        disk_lines.append(box_line(f"{THEME['label']}{mount:<10}{RESET} [{create_bar(disk['percent'], 15)}] {disk['used']:.0f}/{disk['total']:.0f}GB", box_w))
    disk_lines.append(box_bottom(box_w))

    # Network box
    net_lines = [box_top(box_w, "NETWORK")]
    net_lines.append(box_line(f"{THEME['label']}Host{RESET}  {net['hostname']}", box_w))
    for iface, ip in list(net['ips'].items())[:2]:
        net_lines.append(box_line(f"{THEME['label']}{iface[:6]:<6}{RESET} {ip}", box_w))
    net_lines.append(box_mid(box_w))
    net_lines.append(box_line(f"{THEME['low']}TX{RESET} {format_bytes(net['bytes_sent']):<12} {THEME['accent']}RX{RESET} {format_bytes(net['bytes_recv'])}", box_w))
    net_lines.append(box_bottom(box_w))

    # Print side by side
    max_len = max(len(disk_lines), len(net_lines))
    while len(disk_lines) < max_len:
        disk_lines.append(" " * (box_w + 2))
    while len(net_lines) < max_len:
        net_lines.append(" " * (box_w + 2))
    for dl, nl in zip(disk_lines, net_lines):
        print(f"  {dl}  {nl}")

    # Footer
    print()
    print(f"  {BRIGHT_BLACK}{'─' * 78}{RESET}")
    print(f"  {BRIGHT_BLACK}Wellz v2.0.0 | Use 'wellz' for interactive mode{RESET}")
    print()


def run_legacy_live(interval=1.0):
    """Run legacy live mode"""
    import time

    HIDE_CURSOR = "\033[?25l"
    SHOW_CURSOR = "\033[?25h"
    CLEAR = "\033[2J\033[H"

    print(HIDE_CURSOR, end="", flush=True)
    try:
        while True:
            print(CLEAR, end="", flush=True)
            run_legacy_once()
            print(f"  \033[92m[LIVE]\033[0m Press Ctrl+C to exit")
            time.sleep(interval)
    except KeyboardInterrupt:
        pass
    finally:
        print(SHOW_CURSOR, end="", flush=True)
        print("\n\033[93mExiting...\033[0m")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Wellz - A btop-inspired Gaming PC Stats Dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  wellz              Interactive dashboard (default)
  wellz -s           Simple static output
  wellz -l           Legacy live mode
  wellz -l -i 2      Legacy live with 2s refresh
  wellz --theme nord Use Nord theme
  wellz-gui          Launch GUI widget
        """
    )
    parser.add_argument(
        "-s", "--static",
        action="store_true",
        help="Static output mode (show stats once and exit)"
    )
    parser.add_argument(
        "-l", "--legacy",
        action="store_true",
        help="Legacy live mode (no interactive controls)"
    )
    parser.add_argument(
        "-i", "--interval",
        type=float,
        default=1.0,
        help="Refresh interval for legacy mode (default: 1.0)"
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to custom config file"
    )
    parser.add_argument(
        "--theme",
        type=str,
        help="Theme name (default, dracula, nord, gruvbox, monokai, solarized, tokyo, catppuccin)"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="Wellz v2.0.0"
    )

    args = parser.parse_args()

    try:
        if args.static:
            run_legacy_once()
        elif args.legacy:
            run_legacy_live(args.interval)
        else:
            # Set theme if specified
            if args.theme:
                from .config import get_config
                config = get_config(args.config)
                config.theme_name = args.theme
            run_interactive(args.config)
    except KeyboardInterrupt:
        print("\n\033[93mInterrupted.\033[0m")
        sys.exit(0)
    except Exception as e:
        print(f"\033[91mError: {e}\033[0m")
        sys.exit(1)


if __name__ == "__main__":
    main()
