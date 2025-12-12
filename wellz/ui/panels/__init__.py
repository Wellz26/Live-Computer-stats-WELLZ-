"""Wellz UI Panels - Dashboard panel components"""

from .cpu_panel import CPUPanel
from .memory_panel import MemoryPanel
from .network_panel import NetworkPanel
from .disk_panel import DiskPanel
from .gpu_panel import GPUPanel
from .process_panel import ProcessPanel
from .help_panel import HelpPanel

__all__ = [
    "CPUPanel",
    "MemoryPanel",
    "NetworkPanel",
    "DiskPanel",
    "GPUPanel",
    "ProcessPanel",
    "HelpPanel",
]
