"""
Wellz Data Collectors - System information gathering
Extracted and enhanced from cli.py
"""

import os
import platform
import socket
import subprocess
import time
from typing import Any, Dict, List, Optional, Tuple

try:
    import psutil
except ImportError:
    psutil = None


# ============================================================================
# OS DETECTION
# ============================================================================

def get_os_type() -> str:
    """Detect OS type and distribution"""
    system = platform.system().lower()

    if system == "linux":
        try:
            with open("/etc/os-release", "r") as f:
                content = f.read().lower()
                # Check in specific order (most specific first)
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


def get_os_logo(os_type: str) -> Tuple[str, List[str]]:
    """
    Return ASCII art logo for the detected OS.

    Returns:
        Tuple of (color_code, list_of_logo_lines)
    """
    # ANSI color codes
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_GREEN = "\033[92m"
    ORANGE = "\033[38;2;233;84;32m"

    logos = {
        "windows": (BRIGHT_CYAN, [
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

        "macos": (BRIGHT_WHITE, [
            "                 .:'            ",
            "             __ :'__            ",
            "          .'`  `-'  ``.         ",
            "         :          .-'         ",
            "        :          :            ",
            "         :         `-;          ",
            "          `.__.-.__.'           ",
        ]),

        "linux": (BRIGHT_YELLOW, [
            "        .--.        ",
            "       |o_o |       ",
            "       |:_/ |       ",
            "      //   \\ \\      ",
            "     (|     | )     ",
            "    /'\\_   _/`\\     ",
            "    \\___)=(___/     ",
        ]),

        "arch": (BRIGHT_CYAN, [
            "       /\\          ",
            "      /  \\         ",
            "     /    \\        ",
            "    /      \\       ",
            "   /   ,,   \\      ",
            "  /   |  |   \\     ",
            " /_-''    ''-_\\    ",
        ]),

        "ubuntu": (ORANGE, [
            "           .-/+oossssoo+/-.          ",
            "       `:+ssssssssssssssssss+:`      ",
            "     -+ssssssssssssssssssyyssss+-    ",
            "   .ossssssssssssssssss  dMMMNy sso. ",
            "  /sssssssssss hdmmNNmmyNMMMMh  ssss\\",
            " +sssssssss hNMMMMMMMMMMMMMh +ssssss+",
            "/ssssssss hNMMMMMMMMMNdy  ssssssssss\\",
        ]),

        "debian": (BRIGHT_RED, [
            "       _,met$$$$$gg.       ",
            "    ,g$$$$$$$$$$$$$$$P.    ",
            "  ,g$$P\"\"       \"\"\"Y$$.\". ",
            " ,$$P'              `$$$. ",
            "',$$P       ,ggs.     `$$b:",
            "`d$$'     ,$P\"'   .    $$$",
            " $$P      d$'     ,    $$$P",
        ]),

        "fedora": (BRIGHT_BLUE, [
            "        ,'''''.          ",
            "       |   ,.  |         ",
            "       |  |  '_'         ",
            "  ,....|  |..            ",
            ".'  ,_____   ``'.        ",
            "|  'fffff' `'  |         ",
            "|   f   f     ;          ",
        ]),

        "manjaro": (BRIGHT_GREEN, [
            "||||||||| ||||",
            "||||||||| ||||",
            "||||      ||||",
            "|||| |||| ||||",
            "|||| |||| ||||",
            "|||| |||| ||||",
            "|||| |||| ||||",
        ]),

        "kali": (BRIGHT_BLUE, [
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

        "mint": (BRIGHT_GREEN, [
            "             ...-:::::-...              ",
            "          .-MMMMMMMMMMMMMMM-.           ",
            "      .-MMMM`..-:::::::-..`MMMM-.       ",
            "    .:MMMM.:MMMMMMMMMMMMMMM:.MMMM:.     ",
            "   -MMM-M---MMMMMMMMMMMMMMMMMMM.MMM-    ",
            " `:MMM:MM`  :MMMM:....::-...-MMMM:MMM:` ",
            " :MMM:MMM`  :MM:`  ``    ``  `:MMM:MMM: ",
        ]),

        "pop": (BRIGHT_CYAN, [
            "             /////////////             ",
            "         /////////////////////         ",
            "      ///////*767////////*//////       ",
            "    //////767///////767/////////       ",
            "   /////767/////////767//////////      ",
            "  /////767//////////767///////////     ",
            " ///////767/////////767////////////    ",
        ]),

        "redhat": (BRIGHT_RED, [
            "           .MMM..:MMMMMMM       ",
            "          MMMMMMMMMMMMMMMMMM    ",
            "          MMMMMMMMMMMMMMMMMMMM. ",
            "         MMMMMMMMMMMMMMMMMMMMMM ",
            "        ,MMMMMMMMMMMMMMMMMMMMMM:",
            "        MMMMMMMMMMMMMMMMMMMMMMMM",
            "  .MMMM'  MMMMMMMMMMMMMMMMMMMMMM",
        ]),

        "suse": (BRIGHT_GREEN, [
            "           .;ldkO0000Okdl;.          ",
            "       .;d00xl:^'    '^:LO00d;.      ",
            "     .d00l'                'o00d.    ",
            "   .d0Kd'                    :O0d.   ",
            "  .OK       ;d;                lKO.  ",
            " .0K    .   ,;                  lKK. ",
            " :K0   :0x        lNWWNl        aNKd ",
        ]),
    }

    return logos.get(os_type, logos["linux"])


# ============================================================================
# SYSTEM INFO COLLECTORS
# ============================================================================

def get_cpu_info(interval: float = 0.1) -> Dict[str, Any]:
    """
    Get CPU information including per-core usage.

    Args:
        interval: Time to wait for CPU measurement (seconds)

    Returns:
        Dict with model, usage, per_core, freq_current, freq_max, cores, threads
    """
    if psutil is None:
        return {
            "model": "psutil not installed",
            "usage": 0,
            "per_core": [],
            "freq_current": 0,
            "freq_max": 0,
            "cores": 0,
            "threads": 0
        }

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
                result = subprocess.run(
                    ["sysctl", "-n", "machdep.cpu.brand_string"],
                    capture_output=True, text=True
                )
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
            "model": f"Error: {e}",
            "usage": 0,
            "per_core": [],
            "freq_current": 0,
            "freq_max": 0,
            "cores": 0,
            "threads": 0
        }


def get_gpu_info() -> Dict[str, Any]:
    """
    Get GPU information.

    Returns:
        Dict with name, usage, vram_used, vram_total, temp
    """
    gpu_info = {
        "name": "No GPU detected",
        "usage": None,
        "vram_used": None,
        "vram_total": None,
        "temp": None
    }

    # Try NVIDIA GPU
    try:
        result = subprocess.run(
            ["nvidia-smi",
             "--query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu",
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

    # Try AMD GPU (rocm-smi)
    try:
        result = subprocess.run(
            ["rocm-smi", "--showuse", "--showtemp", "--showmeminfo", "vram"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            # Parse rocm-smi output
            lines = result.stdout.strip().split("\n")
            for line in lines:
                if "GPU use" in line:
                    gpu_info["usage"] = float(line.split()[-1].rstrip("%"))
                elif "Temperature" in line:
                    gpu_info["temp"] = float(line.split()[-1].rstrip("c"))
            gpu_info["name"] = "AMD GPU"
            return gpu_info
    except:
        pass

    # Try to detect GPU from lspci
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


def get_memory_info() -> Dict[str, float]:
    """
    Get RAM and swap information.

    Returns:
        Dict with total, used, available, percent, swap_total, swap_used, swap_percent
    """
    if psutil is None:
        return {
            "total": 0, "used": 0, "available": 0, "percent": 0,
            "swap_total": 0, "swap_used": 0, "swap_percent": 0
        }

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


def get_disk_info() -> List[Dict[str, Any]]:
    """
    Get disk information for all mounted partitions.

    Returns:
        List of dicts with mount, device, total, used, percent
    """
    if psutil is None:
        return []

    disks = []
    try:
        partitions = psutil.disk_partitions()
        for p in partitions:
            try:
                # Skip certain filesystem types
                if p.fstype in ['squashfs', 'tmpfs', 'devtmpfs']:
                    continue
                usage = psutil.disk_usage(p.mountpoint)
                disks.append({
                    "mount": p.mountpoint,
                    "device": p.device,
                    "fstype": p.fstype,
                    "total": usage.total / (1024**3),
                    "used": usage.used / (1024**3),
                    "free": usage.free / (1024**3),
                    "percent": usage.percent
                })
            except (PermissionError, OSError):
                pass
    except:
        pass

    # Fallback to root
    if not disks:
        try:
            usage = psutil.disk_usage("/")
            disks.append({
                "mount": "/",
                "device": "root",
                "fstype": "unknown",
                "total": usage.total / (1024**3),
                "used": usage.used / (1024**3),
                "free": usage.free / (1024**3),
                "percent": usage.percent
            })
        except:
            pass

    return disks


def get_disk_io() -> Dict[str, int]:
    """
    Get disk I/O counters.

    Returns:
        Dict with read_bytes, write_bytes, read_count, write_count
    """
    if psutil is None:
        return {"read_bytes": 0, "write_bytes": 0, "read_count": 0, "write_count": 0}

    try:
        io = psutil.disk_io_counters()
        return {
            "read_bytes": io.read_bytes,
            "write_bytes": io.write_bytes,
            "read_count": io.read_count,
            "write_count": io.write_count
        }
    except:
        return {"read_bytes": 0, "write_bytes": 0, "read_count": 0, "write_count": 0}


def get_network_info() -> Dict[str, Any]:
    """
    Get network information.

    Returns:
        Dict with hostname, ips, bytes_sent, bytes_recv, packets_sent, packets_recv
    """
    if psutil is None:
        return {
            "hostname": "Unknown",
            "ips": {},
            "bytes_sent": 0,
            "bytes_recv": 0,
            "packets_sent": 0,
            "packets_recv": 0
        }

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
        return {
            "hostname": "Unknown",
            "ips": {},
            "bytes_sent": 0,
            "bytes_recv": 0,
            "packets_sent": 0,
            "packets_recv": 0
        }


def get_system_info() -> Dict[str, str]:
    """
    Get OS and system information.

    Returns:
        Dict with os, release, version, arch, uptime, hostname
    """
    try:
        boot_time = psutil.boot_time() if psutil else time.time()
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
        return {
            "os": "Unknown",
            "release": "",
            "version": "",
            "arch": "",
            "uptime": "N/A",
            "hostname": "Unknown"
        }


def get_process_list(sort_by: str = "cpu", limit: int = 50) -> List[Dict[str, Any]]:
    """
    Get list of running processes.

    Args:
        sort_by: Sort key - "cpu", "memory", "pid", "name"
        limit: Maximum number of processes to return

    Returns:
        List of dicts with pid, name, username, cpu_percent, memory_percent, status
    """
    if psutil is None:
        return []

    processes = []
    try:
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent',
                                          'memory_percent', 'status', 'ppid']):
            try:
                pinfo = proc.info
                processes.append({
                    "pid": pinfo['pid'],
                    "name": pinfo['name'] or "unknown",
                    "username": pinfo['username'] or "unknown",
                    "cpu_percent": pinfo['cpu_percent'] or 0,
                    "memory_percent": pinfo['memory_percent'] or 0,
                    "status": pinfo['status'] or "unknown",
                    "ppid": pinfo['ppid'] or 0
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    except:
        pass

    # Sort
    sort_keys = {
        "cpu": lambda x: x['cpu_percent'],
        "memory": lambda x: x['memory_percent'],
        "pid": lambda x: x['pid'],
        "name": lambda x: x['name'].lower()
    }
    key_func = sort_keys.get(sort_by, sort_keys["cpu"])
    processes.sort(key=key_func, reverse=(sort_by in ["cpu", "memory"]))

    return processes[:limit]


def get_load_average() -> Tuple[float, float, float]:
    """
    Get system load average (1, 5, 15 minutes).

    Returns:
        Tuple of (load1, load5, load15)
    """
    try:
        if hasattr(os, 'getloadavg'):
            return os.getloadavg()
    except:
        pass
    return (0.0, 0.0, 0.0)
