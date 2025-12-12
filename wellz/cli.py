#!/usr/bin/env python3
"""
Wellz - Gaming PC Stats Dashboard
A btop-inspired system stats display for your gaming rig
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


# ============================================================================
# ANSI COLORS & STYLING
# ============================================================================

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"

    # Regular colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # Cursor control
    HIDE_CURSOR = "\033[?25l"
    SHOW_CURSOR = "\033[?25h"
    CLEAR_SCREEN = "\033[2J\033[H"

    # 256 color support
    @staticmethod
    def rgb(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"

    @staticmethod
    def bg_rgb(r, g, b):
        return f"\033[48;2;{r};{g};{b}m"


# Theme colors
THEME = {
    "title": Colors.BRIGHT_CYAN,
    "border": Colors.BRIGHT_BLACK,
    "label": Colors.BRIGHT_WHITE,
    "value": Colors.WHITE,
    "low": Colors.BRIGHT_GREEN,
    "mid": Colors.BRIGHT_YELLOW,
    "high": Colors.BRIGHT_RED,
    "accent": Colors.BRIGHT_MAGENTA,
    "cpu": Colors.BRIGHT_GREEN,
    "gpu": Colors.BRIGHT_YELLOW,
    "mem": Colors.BRIGHT_BLUE,
    "disk": Colors.BRIGHT_MAGENTA,
    "net": Colors.BRIGHT_CYAN,
}


# ============================================================================
# OS DETECTION & ASCII LOGOS
# ============================================================================

def get_os_type():
    """Detect OS type and distribution"""
    system = platform.system().lower()

    if system == "linux":
        # Try to detect Linux distribution
        try:
            with open("/etc/os-release", "r") as f:
                content = f.read().lower()
                if "kali" in content:
                    return "kali"
                elif "arch" in content:
                    return "arch"
                elif "ubuntu" in content:
                    return "ubuntu"
                elif "debian" in content:
                    return "debian"
                elif "fedora" in content:
                    return "fedora"
                elif "manjaro" in content:
                    return "manjaro"
                elif "mint" in content:
                    return "mint"
                elif "pop" in content:
                    return "pop"
                elif "centos" in content or "rhel" in content:
                    return "redhat"
                elif "opensuse" in content or "suse" in content:
                    return "suse"
        except:
            pass
        return "linux"
    elif system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    return "linux"


def get_os_logo(os_type):
    """Return ASCII art logo for the detected OS"""

    logos = {
        "windows": (Colors.BRIGHT_CYAN, [
            "################  ################",
            "################  ################",
            "################  ################",
            "################  ################",
            "################  ################",
            "################  ################",
            "################  ################",
            "                                  ",
            "################  ################",
            "################  ################",
            "################  ################",
            "################  ################",
            "################  ################",
            "################  ################",
            "################  ################",
        ]),

        "macos": (Colors.BRIGHT_WHITE, [
            "                 .:'            ",
            "             __ :'__            ",
            "          .'`  `-'  ``.         ",
            "         :          .-'         ",
            "        :          :            ",
            "         :         `-;          ",
            "          `.__.-.__.'           ",
        ]),

        "linux": (Colors.BRIGHT_YELLOW, [
            "        .--.        ",
            "       |o_o |       ",
            "       |:_/ |       ",
            "      //   \\ \\      ",
            "     (|     | )     ",
            "    /'\\_   _/`\\     ",
            "    \\___)=(___/     ",
        ]),

        "arch": (Colors.BRIGHT_CYAN, [
            "       /\\          ",
            "      /  \\         ",
            "     /    \\        ",
            "    /      \\       ",
            "   /   ,,   \\      ",
            "  /   |  |   \\     ",
            " /_-''    ''-_\\    ",
        ]),

        "ubuntu": (Colors.rgb(233, 84, 32), [
            "           .-/+oossssoo+/-.          ",
            "       `:+ssssssssssssssssss+:`      ",
            "     -+ssssssssssssssssssyyssss+-    ",
            "   .ossssssssssssssssss  dMMMNy sso. ",
            "  /sssssssssss hdmmNNmmyNMMMMh  ssss\\",
            " +sssssssss hNMMMMMMMMMMMMMh +ssssss+",
            "/ssssssss hNMMMMMMMMMNdy  ssssssssss\\",
            "osssssss  hMMMMMMMNdy ssssssssssssso ",
            "/ssssssss hMMMMMhssssssssssssssssss\\ ",
            "+sssssssss  hNMMNy+ssssssssssssssss+ ",
            " \\sssssssssss  +   yNMNhssssssssss/  ",
            "  \\ssss  ++   oy+   oNMMMhsssssss/   ",
            "   .ossssssss+NMMh  +NMMMMNsssso.    ",
            "     -+sssssssssso++osssssss+-       ",
            "       `:+ssssssssssssssss+:`        ",
            "           .-/+oossssoo+/-.          ",
        ]),

        "debian": (Colors.BRIGHT_RED, [
            "       _,met$$$$$gg.       ",
            "    ,g$$$$$$$$$$$$$$$P.    ",
            "  ,g$$P\"\"       \"\"\"Y$$.\". ",
            " ,$$P'              `$$$. ",
            "',$$P       ,ggs.     `$$b:",
            "`d$$'     ,$P\"'   .    $$$",
            " $$P      d$'     ,    $$$P",
            " $$:      $$.   -    ,d$$' ",
            " $$;      Y$b._   _,d$P'  ",
            " Y$$.    `.`\"Y$$$$P\"'     ",
            " `$$b      \"-.__          ",
            "  `Y$$                    ",
            "   `Y$$.                  ",
            "     `$$b.                ",
            "       `Y$$b.             ",
            "          `\"Y$b._         ",
        ]),

        "fedora": (Colors.BRIGHT_BLUE, [
            "        ,'''''.          ",
            "       |   ,.  |         ",
            "       |  |  '_'         ",
            "  ,....|  |..            ",
            ".'  ,googol_ ``'.        ",
            "|  'g$$g' `'  |          ",
            "|   $   $     ;          ",
            " ;  g$$$$$g.  ,'         ",
            "  ' _g$$$$$g. '          ",
            "  .'   g$g   '.          ",
            " :      `      ;         ",
            "  `.googol_,-'           ",
            "     `''''`              ",
        ]),

        "manjaro": (Colors.BRIGHT_GREEN, [
            "||||||||| ||||",
            "||||||||| ||||",
            "||||      ||||",
            "|||| |||| ||||",
            "|||| |||| ||||",
            "|||| |||| ||||",
            "|||| |||| ||||",
        ]),

        "kali": (Colors.BRIGHT_BLUE, [
            "      ..         ",
            "    .WWWW.       ",
            "   .WW  WW.      ",
            "  .WW    WW.     ",
            "  WW  ..  WW     ",
            "  WW WWWW WW     ",
            "   WW    WW      ",
            "    WWWWWW       ",
            "      WW         ",
            "   KALI LINUX    ",
        ]),

        "mint": (Colors.BRIGHT_GREEN, [
            "             ...-:::::-...              ",
            "          .-MMMMMMMMMMMMMMM-.           ",
            "      .-MMMM`..-:::::::-..`MMMM-.       ",
            "    .:MMMM.:MMMMMMMMMMMMMMM:.MMMM:.     ",
            "   -MMM-M---MMMMMMMMMMMMMMMMMMM.MMM-    ",
            " `:MMM:MM`  :MMMM:....::-...-MMMM:MMM:` ",
            " :MMM:MMM`  :MM:`  ``    ``  `:MMM:MMM: ",
            ".MMM.MMMM`  :MM.  -MM.  .MM-  `MMMM.MMM.",
            ":MMM:MMMM`  :MM.  -MM-  .MM:  `MMMM-Loss",
            ":MMM:MMMM`  :MM.  -MM-  .MM:  `MMMM:MMM:",
            ":MMM:MMMM`  :MM.  -MM-  .MM:  `MMMM-MMM:",
            ".MMM.MMMM`  :MM:--'MM:--'MM:  `MMMM.MMM.",
            " :MMM:MMM-  `-MMMMMMMMMMMM-`  -Loss:MMM:",
            "  :MMM:MMM:`                `:MMM:MMM:  ",
            "   .MMM.MMMM:--------------:MMMM.MMM.   ",
            "     '-MMMM.-MMMMMMMMMMMMMMM-.MMMM-'    ",
            "       '.-MMMM``--googol_-Loss-.'   ",
            "            '-MMMMMMMMMMMMM-'           ",
            "               ``-googol_``         ",
        ]),

        "pop": (Colors.BRIGHT_CYAN, [
            "             /////////////             ",
            "         /////////////////////         ",
            "      ///////*767telegramTG*//////     ",
            "    //////7telegramTG7telegramTG/////  ",
            "   /////telegramTelegramTelegramTG//// ",
            "  /////7telegramTG7telegramTG7telegrTG/",
            " ///////telegramTelegramTelegramTG////",
            "////////7telegramTG7telegramTG7tele///",
            "/////////telegramTelegramTelegramT////",
            "//////////7telegramTG7telegramTG/////",
            "///////////telegramTelegramTele/////",
            "////////////7telegramTG7teleg//////",
            "/////////////telegramTelegrT//////",
            "//////////////7telegramTG7///////",
            "///////////////telegram////////",
        ]),

        "redhat": (Colors.BRIGHT_RED, [
            "           .MMM..:MMMMMMM       ",
            "          MMMMMMMMMMMMMMMMMM    ",
            "          MMMMMMMMMMMMMMMMMMMM. ",
            "         MMMMMMMMMMMMMMMMMMMMMM ",
            "        ,MMMMMMMMMMMMMMMMMMMMMM:",
            "        MMMMMMMMMMMMMMMMMMMMMMMM",
            "  .MMMM'  MMMMMMMMMMMMMMMMMMMMMM",
            " MMMMMM    `MMMMMMMMMMMMMMMMMMMM",
            "MMMMMMMM      MMMMMMMMMMMMMMMMMM",
            "MMMMMMMMM.       `MMMMMMMMMMMMM'",
            "MMMMMMMMMMM.                    ",
            "`MMMMMMMMMMMMM.                 ",
            " `MMMMMMMMMMMMMMMMM.            ",
            "    `MMMMMMMMMMMMMMMMMM.        ",
            "        ``MMMMMMMMMMMMM         ",
        ]),

        "suse": (Colors.BRIGHT_GREEN, [
            "           .;ldkO0000Okdl;.          ",
            "       .;d00xl:^'    '^:LO00d;.      ",
            "     .d00l'                'o00d.    ",
            "   .d0Kd'  Macos             :O0d.   ",
            "  .OK    windows   ;d;          lKO. ",
            " .0K    linUx  .  ,;             lKK.",
            " :K0   :0x        lNWWNl         aNKd",
            " .00,  :Kd        ONNNNNk        KK0.",
            "  :KK, .0K;       kNNNNN0 '.   'd0Kd ",
            "   ;KK0, l0x;.   .oKNNN0l ;x; .d00'  ",
            "    .kKKK'.'d0dp. .:c;. okodx00d'    ",
            "      .0KKK. kKKKKKK0KKKKKKdc'       ",
            "        ':KK.'KKKKKKKKK0d'           ",
            "           ':d00KKKKKKKKK0x:'        ",
        ]),
    }

    return logos.get(os_type, logos["linux"])


# ============================================================================
# SYSTEM INFO COLLECTORS
# ============================================================================

def get_cpu_info(interval=0.1):
    """Get CPU information including per-core usage"""
    try:
        cpu_percent = psutil.cpu_percent(interval=interval)
        cpu_per_core = psutil.cpu_percent(interval=0, percpu=True)
        cpu_freq = psutil.cpu_freq()
        cpu_count = psutil.cpu_count()
        cpu_count_physical = psutil.cpu_count(logical=False)

        # Get CPU model
        cpu_model = "Unknown CPU"
        try:
            if platform.system() == "Linux":
                with open("/proc/cpuinfo", "r") as f:
                    for line in f:
                        if "model name" in line:
                            cpu_model = line.split(":")[1].strip()
                            break
            elif platform.system() == "Darwin":
                result = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"],
                                       capture_output=True, text=True)
                if result.returncode == 0:
                    cpu_model = result.stdout.strip()
            elif platform.system() == "Windows":
                cpu_model = platform.processor()
        except:
            cpu_model = platform.processor() or "Unknown CPU"

        freq_current = cpu_freq.current if cpu_freq else 0
        freq_max = cpu_freq.max if cpu_freq and cpu_freq.max else freq_current

        return {
            "model": cpu_model,
            "usage": cpu_percent,
            "per_core": cpu_per_core,
            "freq_current": freq_current,
            "freq_max": freq_max,
            "cores": cpu_count_physical or cpu_count,
            "threads": cpu_count
        }
    except Exception as e:
        return {
            "model": "Error", "usage": 0, "per_core": [],
            "freq_current": 0, "freq_max": 0, "cores": 0, "threads": 0
        }


def get_gpu_info():
    """Get GPU information"""
    gpu_info = {"name": "No GPU detected", "usage": None, "vram_used": None,
                "vram_total": None, "temp": None}

    # Try NVIDIA GPU
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            parts = result.stdout.strip().split(", ")
            if len(parts) >= 5:
                gpu_info["name"] = parts[0]
                gpu_info["usage"] = float(parts[1])
                gpu_info["vram_used"] = float(parts[2])
                gpu_info["vram_total"] = float(parts[3])
                gpu_info["temp"] = float(parts[4])
                return gpu_info
    except:
        pass

    # Try AMD GPU
    try:
        result = subprocess.run(["lspci"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                if "VGA" in line or "3D" in line:
                    if "AMD" in line or "ATI" in line:
                        gpu_info["name"] = "AMD GPU"
                    elif "Intel" in line:
                        gpu_info["name"] = "Intel Graphics"
                    elif "NVIDIA" in line:
                        gpu_info["name"] = "NVIDIA GPU"
                    break
    except:
        pass

    return gpu_info


def get_memory_info():
    """Get RAM and swap information"""
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return {
        "total": mem.total / (1024**3),
        "used": mem.used / (1024**3),
        "available": mem.available / (1024**3),
        "percent": mem.percent,
        "swap_total": swap.total / (1024**3),
        "swap_used": swap.used / (1024**3),
        "swap_percent": swap.percent
    }


def get_disk_info():
    """Get disk information for all mounted partitions"""
    disks = []
    try:
        partitions = psutil.disk_partitions()
        for p in partitions:
            try:
                usage = psutil.disk_usage(p.mountpoint)
                disks.append({
                    "mount": p.mountpoint,
                    "device": p.device,
                    "total": usage.total / (1024**3),
                    "used": usage.used / (1024**3),
                    "percent": usage.percent
                })
            except:
                pass
    except:
        pass

    if not disks:
        try:
            usage = psutil.disk_usage("/")
            disks.append({
                "mount": "/",
                "device": "root",
                "total": usage.total / (1024**3),
                "used": usage.used / (1024**3),
                "percent": usage.percent
            })
        except:
            pass

    return disks


def get_network_info():
    """Get network information"""
    try:
        hostname = socket.gethostname()

        # Get IP addresses
        interfaces = psutil.net_if_addrs()
        ips = {}
        for iface, addrs in interfaces.items():
            for addr in addrs:
                if addr.family == socket.AF_INET and not addr.address.startswith("127."):
                    ips[iface] = addr.address

        net_io = psutil.net_io_counters()

        return {
            "hostname": hostname,
            "ips": ips,
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv
        }
    except:
        return {"hostname": "Unknown", "ips": {}, "bytes_sent": 0, "bytes_recv": 0,
                "packets_sent": 0, "packets_recv": 0}


def get_system_info():
    """Get OS and system information"""
    try:
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time

        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)

        if days > 0:
            uptime = f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            uptime = f"{hours}h {minutes}m"
        else:
            uptime = f"{minutes}m"

        return {
            "os": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "arch": platform.machine(),
            "uptime": uptime,
            "hostname": socket.gethostname()
        }
    except:
        return {"os": "Unknown", "release": "", "version": "",
                "arch": "", "uptime": "N/A", "hostname": "Unknown"}


# ============================================================================
# RENDERING HELPERS
# ============================================================================

def get_usage_color(percent):
    """Get color based on usage percentage"""
    if percent < 50:
        return THEME["low"]
    elif percent < 80:
        return THEME["mid"]
    else:
        return THEME["high"]


def create_bar(percent, width=20, filled="█", empty="░", color=None):
    """Create a progress bar"""
    filled_width = int(width * percent / 100)
    empty_width = width - filled_width

    if color is None:
        color = get_usage_color(percent)

    return f"{color}{filled * filled_width}{Colors.BRIGHT_BLACK}{empty * empty_width}{Colors.RESET}"


def create_graph_bar(percent, width=10):
    """Create a vertical-style graph bar using block characters"""
    blocks = " ▁▂▃▄▅▆▇█"
    color = get_usage_color(percent)

    full_blocks = int(percent / 100 * width)
    remainder = (percent / 100 * width) - full_blocks
    partial_idx = int(remainder * 8)

    bar = "█" * full_blocks
    if partial_idx > 0 and full_blocks < width:
        bar += blocks[partial_idx]
    bar = bar.ljust(width, " ")

    return f"{color}{bar}{Colors.RESET}"


def format_bytes(bytes_val):
    """Format bytes to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024:
            return f"{bytes_val:.1f}{unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f}PB"


def box_top(width, title="", color=None):
    """Create top border of a box"""
    c = color or THEME["border"]
    if title:
        title_str = f" {title} "
        padding = width - len(title_str) - 2
        return f"{c}╭─{Colors.RESET}{THEME['title']}{title_str}{Colors.RESET}{c}{'─' * padding}╮{Colors.RESET}"
    return f"{c}╭{'─' * width}╮{Colors.RESET}"


def box_mid(width, color=None):
    """Create middle separator of a box"""
    c = color or THEME["border"]
    return f"{c}├{'─' * width}┤{Colors.RESET}"


def box_bottom(width, color=None):
    """Create bottom border of a box"""
    c = color or THEME["border"]
    return f"{c}╰{'─' * width}╯{Colors.RESET}"


def box_line(content, width, color=None):
    """Create a line within a box"""
    c = color or THEME["border"]
    # Strip ANSI codes to calculate true length
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    visible_len = len(ansi_escape.sub('', content))
    padding = width - visible_len - 2
    if padding < 0:
        padding = 0
    return f"{c}│{Colors.RESET} {content}{' ' * padding}{c}│{Colors.RESET}"


# ============================================================================
# MAIN DASHBOARD RENDERER
# ============================================================================

def render_dashboard(live_mode=False):
    """Render the full dashboard"""

    # Gather all system info
    os_type = get_os_type()
    logo_color, logo_lines = get_os_logo(os_type)

    cpu = get_cpu_info(interval=0.1 if live_mode else 0.5)
    gpu = get_gpu_info()
    mem = get_memory_info()
    disks = get_disk_info()
    net = get_network_info()
    sys_info = get_system_info()

    # Terminal width (default 100 if can't detect)
    try:
        term_width = os.get_terminal_size().columns
    except:
        term_width = 100

    # Clamp to reasonable size
    term_width = max(80, min(term_width, 140))

    output = []

    # ========== HEADER ==========
    header = f"""
{THEME['title']}{Colors.BOLD}██╗    ██╗███████╗██╗     ██╗     ███████╗{Colors.RESET}
{THEME['title']}{Colors.BOLD}██║    ██║██╔════╝██║     ██║     ╚══███╔╝{Colors.RESET}
{THEME['title']}{Colors.BOLD}██║ █╗ ██║█████╗  ██║     ██║       ███╔╝ {Colors.RESET}
{THEME['title']}{Colors.BOLD}██║███╗██║██╔══╝  ██║     ██║      ███╔╝  {Colors.RESET}
{THEME['title']}{Colors.BOLD}╚███╔███╔╝███████╗███████╗███████╗███████╗{Colors.RESET}
{THEME['title']}{Colors.BOLD} ╚══╝╚══╝ ╚══════╝╚══════╝╚══════╝╚══════╝{Colors.RESET}
"""
    output.append(header)

    # ========== SYSTEM INFO + LOGO SECTION ==========
    box_w = 38

    # Left side: OS Logo and info
    sys_lines = []
    sys_lines.append(box_top(box_w, "SYSTEM", THEME["border"]))
    sys_lines.append(box_line(f"{THEME['label']}OS{Colors.RESET}      {sys_info['os']} {sys_info['release']}", box_w))
    sys_lines.append(box_line(f"{THEME['label']}Host{Colors.RESET}    {sys_info['hostname']}", box_w))
    sys_lines.append(box_line(f"{THEME['label']}Arch{Colors.RESET}    {sys_info['arch']}", box_w))
    sys_lines.append(box_line(f"{THEME['label']}Uptime{Colors.RESET}  {sys_info['uptime']}", box_w))
    sys_lines.append(box_mid(box_w))

    # Add logo lines
    for line in logo_lines[:7]:
        sys_lines.append(box_line(f"{logo_color}{line}{Colors.RESET}", box_w))

    sys_lines.append(box_bottom(box_w))

    # Right side: CPU Box
    cpu_box_w = 38
    cpu_lines = []
    cpu_lines.append(box_top(cpu_box_w, "CPU", THEME["cpu"]))

    # CPU model (truncated if needed)
    model = cpu['model'][:32] + "..." if len(cpu['model']) > 35 else cpu['model']
    cpu_lines.append(box_line(f"{THEME['value']}{model}{Colors.RESET}", cpu_box_w))
    cpu_lines.append(box_line(f"{THEME['label']}Cores{Colors.RESET} {cpu['cores']}  {THEME['label']}Threads{Colors.RESET} {cpu['threads']}  {THEME['label']}Freq{Colors.RESET} {cpu['freq_current']:.0f}MHz", cpu_box_w))
    cpu_lines.append(box_mid(cpu_box_w))

    # Total CPU usage bar
    cpu_lines.append(box_line(f"{THEME['label']}Total{Colors.RESET}  [{create_bar(cpu['usage'], 20)}] {cpu['usage']:5.1f}%", cpu_box_w))

    # Per-core usage (show first 8 cores max in compact form)
    cores = cpu['per_core'][:8]
    if cores:
        core_str1 = ""
        core_str2 = ""
        for i, c in enumerate(cores[:4]):
            color = get_usage_color(c)
            core_str1 += f"{THEME['label']}{i}{Colors.RESET}{color}{'█' * int(c/20):<5}{Colors.RESET}"
        for i, c in enumerate(cores[4:8], 4):
            color = get_usage_color(c)
            core_str2 += f"{THEME['label']}{i}{Colors.RESET}{color}{'█' * int(c/20):<5}{Colors.RESET}"

        if core_str1:
            cpu_lines.append(box_line(core_str1, cpu_box_w))
        if core_str2:
            cpu_lines.append(box_line(core_str2, cpu_box_w))

    cpu_lines.append(box_bottom(cpu_box_w))

    # Pad to same length
    max_len = max(len(sys_lines), len(cpu_lines))
    while len(sys_lines) < max_len:
        sys_lines.append(" " * (box_w + 2))
    while len(cpu_lines) < max_len:
        cpu_lines.append(" " * (cpu_box_w + 2))

    # Combine side by side
    for sl, cl in zip(sys_lines, cpu_lines):
        output.append(f"  {sl}  {cl}")

    output.append("")

    # ========== GPU + MEMORY SECTION ==========
    gpu_box_w = 38
    mem_box_w = 38

    # GPU Box
    gpu_lines = []
    gpu_lines.append(box_top(gpu_box_w, "GPU", THEME["gpu"]))

    gpu_name = gpu['name'][:32] + "..." if len(gpu['name']) > 35 else gpu['name']
    gpu_lines.append(box_line(f"{THEME['value']}{gpu_name}{Colors.RESET}", gpu_box_w))

    if gpu['usage'] is not None:
        gpu_lines.append(box_line(f"{THEME['label']}Usage{Colors.RESET}  [{create_bar(gpu['usage'], 20)}] {gpu['usage']:5.1f}%", gpu_box_w))
        if gpu['vram_total']:
            vram_pct = (gpu['vram_used'] / gpu['vram_total']) * 100
            gpu_lines.append(box_line(f"{THEME['label']}VRAM{Colors.RESET}   [{create_bar(vram_pct, 20)}] {gpu['vram_used']:.0f}/{gpu['vram_total']:.0f}MB", gpu_box_w))
        if gpu['temp']:
            temp_color = get_usage_color(gpu['temp'])
            gpu_lines.append(box_line(f"{THEME['label']}Temp{Colors.RESET}   {temp_color}{gpu['temp']:.0f}C{Colors.RESET}", gpu_box_w))
    else:
        gpu_lines.append(box_line(f"{Colors.BRIGHT_BLACK}Stats unavailable{Colors.RESET}", gpu_box_w))

    gpu_lines.append(box_bottom(gpu_box_w))

    # Memory Box
    mem_lines = []
    mem_lines.append(box_top(mem_box_w, "MEMORY", THEME["mem"]))
    mem_lines.append(box_line(f"{THEME['label']}RAM{Colors.RESET}    [{create_bar(mem['percent'], 20)}] {mem['used']:.1f}/{mem['total']:.1f}GB", mem_box_w))
    mem_lines.append(box_line(f"{THEME['label']}Avail{Colors.RESET}  {mem['available']:.1f}GB", mem_box_w))
    if mem['swap_total'] > 0:
        mem_lines.append(box_line(f"{THEME['label']}Swap{Colors.RESET}   [{create_bar(mem['swap_percent'], 20)}] {mem['swap_used']:.1f}/{mem['swap_total']:.1f}GB", mem_box_w))
    mem_lines.append(box_bottom(mem_box_w))

    # Pad to same length
    max_len = max(len(gpu_lines), len(mem_lines))
    while len(gpu_lines) < max_len:
        gpu_lines.append(" " * (gpu_box_w + 2))
    while len(mem_lines) < max_len:
        mem_lines.append(" " * (mem_box_w + 2))

    for gl, ml in zip(gpu_lines, mem_lines):
        output.append(f"  {gl}  {ml}")

    output.append("")

    # ========== DISK + NETWORK SECTION ==========
    disk_box_w = 38
    net_box_w = 38

    # Disk Box
    disk_lines = []
    disk_lines.append(box_top(disk_box_w, "DISK", THEME["disk"]))

    for i, disk in enumerate(disks[:3]):  # Show max 3 disks
        mount = disk['mount'][:10] if len(disk['mount']) > 10 else disk['mount']
        disk_lines.append(box_line(f"{THEME['label']}{mount:<10}{Colors.RESET} [{create_bar(disk['percent'], 15)}] {disk['used']:.0f}/{disk['total']:.0f}GB", disk_box_w))

    disk_lines.append(box_bottom(disk_box_w))

    # Network Box
    net_lines = []
    net_lines.append(box_top(net_box_w, "NETWORK", THEME["net"]))
    net_lines.append(box_line(f"{THEME['label']}Host{Colors.RESET}  {net['hostname']}", net_box_w))

    # Show first IP
    for iface, ip in list(net['ips'].items())[:2]:
        net_lines.append(box_line(f"{THEME['label']}{iface[:6]:<6}{Colors.RESET} {ip}", net_box_w))

    net_lines.append(box_mid(net_box_w))
    net_lines.append(box_line(f"{THEME['low']}TX{Colors.RESET} {format_bytes(net['bytes_sent']):<12} {THEME['accent']}RX{Colors.RESET} {format_bytes(net['bytes_recv'])}", net_box_w))
    net_lines.append(box_bottom(net_box_w))

    # Pad to same length
    max_len = max(len(disk_lines), len(net_lines))
    while len(disk_lines) < max_len:
        disk_lines.append(" " * (disk_box_w + 2))
    while len(net_lines) < max_len:
        net_lines.append(" " * (net_box_w + 2))

    for dl, nl in zip(disk_lines, net_lines):
        output.append(f"  {dl}  {nl}")

    # ========== FOOTER ==========
    output.append("")
    mode_str = f" {Colors.BRIGHT_GREEN}[LIVE]{Colors.RESET}" if live_mode else ""
    output.append(f"  {Colors.BRIGHT_BLACK}{'─' * 78}{Colors.RESET}")
    output.append(f"  {Colors.BRIGHT_BLACK}Wellz v1.1.0{mode_str}  {Colors.RESET}")

    if live_mode:
        output.append(f"  {Colors.BRIGHT_BLACK}Press Ctrl+C to exit{Colors.RESET}")

    output.append("")

    return "\n".join(output)


def run_live_mode(interval=1.0):
    """Run dashboard in continuous live mode"""
    print(Colors.HIDE_CURSOR, end="", flush=True)
    try:
        while True:
            print(Colors.CLEAR_SCREEN, end="", flush=True)
            print(render_dashboard(live_mode=True))
            time.sleep(interval)
    except KeyboardInterrupt:
        pass
    finally:
        print(Colors.SHOW_CURSOR, end="", flush=True)
        print(f"\n{Colors.BRIGHT_YELLOW}Exiting...{Colors.RESET}")


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
            print(render_dashboard())
    except KeyboardInterrupt:
        print(f"\n{Colors.BRIGHT_YELLOW}Interrupted.{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.BRIGHT_RED}Error: {e}{Colors.RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()
