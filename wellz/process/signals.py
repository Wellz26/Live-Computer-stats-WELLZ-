"""
Wellz Process Signals - Signal handling utilities
"""

import os
import signal
from typing import Dict, Optional, Tuple

# Common signals with descriptions
SIGNALS: Dict[str, Tuple[int, str]] = {
    "SIGTERM": (signal.SIGTERM, "Terminate gracefully"),
    "SIGKILL": (signal.SIGKILL, "Force kill (cannot be caught)"),
    "SIGSTOP": (signal.SIGSTOP, "Stop/pause process"),
    "SIGCONT": (signal.SIGCONT, "Continue stopped process"),
    "SIGHUP": (signal.SIGHUP, "Hangup (reload config)"),
    "SIGINT": (signal.SIGINT, "Interrupt (like Ctrl+C)"),
    "SIGQUIT": (signal.SIGQUIT, "Quit with core dump"),
    "SIGUSR1": (signal.SIGUSR1, "User defined signal 1"),
    "SIGUSR2": (signal.SIGUSR2, "User defined signal 2"),
}


def send_signal(pid: int, sig: int) -> Tuple[bool, str]:
    """
    Send a signal to a process.

    Args:
        pid: Process ID
        sig: Signal number (e.g., signal.SIGTERM)

    Returns:
        Tuple of (success, message)
    """
    try:
        os.kill(pid, sig)
        return True, f"Signal sent to PID {pid}"
    except ProcessLookupError:
        return False, f"Process {pid} not found"
    except PermissionError:
        return False, f"Permission denied for PID {pid}"
    except Exception as e:
        return False, f"Error: {str(e)}"


def kill_process(pid: int, force: bool = False) -> Tuple[bool, str]:
    """
    Kill a process.

    Args:
        pid: Process ID
        force: Use SIGKILL instead of SIGTERM

    Returns:
        Tuple of (success, message)
    """
    sig = signal.SIGKILL if force else signal.SIGTERM
    return send_signal(pid, sig)


def stop_process(pid: int) -> Tuple[bool, str]:
    """Stop/pause a process with SIGSTOP"""
    return send_signal(pid, signal.SIGSTOP)


def continue_process(pid: int) -> Tuple[bool, str]:
    """Continue a stopped process with SIGCONT"""
    return send_signal(pid, signal.SIGCONT)


def get_signal_by_name(name: str) -> Optional[int]:
    """
    Get signal number by name.

    Args:
        name: Signal name (e.g., "SIGTERM" or "TERM")

    Returns:
        Signal number or None if not found
    """
    # Normalize name
    name = name.upper()
    if not name.startswith("SIG"):
        name = "SIG" + name

    if name in SIGNALS:
        return SIGNALS[name][0]

    # Try as attribute of signal module
    return getattr(signal, name, None)


def list_signals() -> Dict[str, Tuple[int, str]]:
    """Get dictionary of available signals with descriptions"""
    return SIGNALS.copy()
