"""
Wellz History Buffer - Circular buffer for graph data
"""

import time
from collections import deque
from typing import List, Optional, Tuple


class HistoryBuffer:
    """Circular buffer for storing time-series data for graphs"""

    def __init__(self, maxlen: int = 120):
        """
        Initialize buffer with maximum length.

        Args:
            maxlen: Maximum number of data points to store (default 120 = 2 min at 1s interval)
        """
        self._buffer: deque = deque(maxlen=maxlen)
        self._timestamps: deque = deque(maxlen=maxlen)
        self._maxlen = maxlen

    def append(self, value: float) -> None:
        """Add a value to the buffer with current timestamp"""
        self._buffer.append(value)
        self._timestamps.append(time.time())

    def get_data(self) -> List[float]:
        """Get all values as a list"""
        return list(self._buffer)

    def get_timestamps(self) -> List[float]:
        """Get all timestamps as a list"""
        return list(self._timestamps)

    def get_latest(self) -> Optional[float]:
        """Get the most recent value"""
        return self._buffer[-1] if self._buffer else None

    def get_min(self) -> Optional[float]:
        """Get minimum value in buffer"""
        return min(self._buffer) if self._buffer else None

    def get_max(self) -> Optional[float]:
        """Get maximum value in buffer"""
        return max(self._buffer) if self._buffer else None

    def get_avg(self) -> Optional[float]:
        """Get average value in buffer"""
        return sum(self._buffer) / len(self._buffer) if self._buffer else None

    def __len__(self) -> int:
        return len(self._buffer)

    def is_empty(self) -> bool:
        return len(self._buffer) == 0

    def clear(self) -> None:
        """Clear all data"""
        self._buffer.clear()
        self._timestamps.clear()


class NetworkSpeedBuffer(HistoryBuffer):
    """Specialized buffer for network speed calculations"""

    def __init__(self, maxlen: int = 120):
        super().__init__(maxlen)
        self._last_bytes: Optional[int] = None
        self._last_time: Optional[float] = None

    def update(self, total_bytes: int) -> float:
        """
        Update with total bytes and calculate speed.

        Args:
            total_bytes: Total bytes transferred (cumulative)

        Returns:
            Speed in bytes/second
        """
        current_time = time.time()
        speed = 0.0

        if self._last_bytes is not None and self._last_time is not None:
            time_delta = current_time - self._last_time
            if time_delta > 0:
                byte_delta = total_bytes - self._last_bytes
                speed = byte_delta / time_delta

        self._last_bytes = total_bytes
        self._last_time = current_time
        self.append(speed)

        return speed


class DiskIOBuffer:
    """Buffer for disk I/O tracking (read + write speeds)"""

    def __init__(self, maxlen: int = 120):
        self.read_buffer = NetworkSpeedBuffer(maxlen)
        self.write_buffer = NetworkSpeedBuffer(maxlen)

    def update(self, read_bytes: int, write_bytes: int) -> Tuple[float, float]:
        """
        Update with total read/write bytes.

        Returns:
            Tuple of (read_speed, write_speed) in bytes/second
        """
        read_speed = self.read_buffer.update(read_bytes)
        write_speed = self.write_buffer.update(write_bytes)
        return read_speed, write_speed

    def get_read_data(self) -> List[float]:
        return self.read_buffer.get_data()

    def get_write_data(self) -> List[float]:
        return self.write_buffer.get_data()


class SystemHistory:
    """
    Central history manager for all system metrics.
    Stores history buffers for CPU, Memory, Network, Disk, GPU.
    """

    def __init__(self, maxlen: int = 120):
        """
        Initialize all history buffers.

        Args:
            maxlen: Maximum history length (data points)
        """
        self.maxlen = maxlen

        # CPU history (total and per-core)
        self.cpu_total = HistoryBuffer(maxlen)
        self.cpu_cores: List[HistoryBuffer] = []
        self._cpu_core_count: Optional[int] = None

        # Memory history
        self.memory_percent = HistoryBuffer(maxlen)
        self.swap_percent = HistoryBuffer(maxlen)

        # Network history (speeds)
        self.net_upload = NetworkSpeedBuffer(maxlen)
        self.net_download = NetworkSpeedBuffer(maxlen)

        # Disk I/O history
        self.disk_io = DiskIOBuffer(maxlen)

        # GPU history
        self.gpu_usage = HistoryBuffer(maxlen)
        self.gpu_memory = HistoryBuffer(maxlen)
        self.gpu_temp = HistoryBuffer(maxlen)

    def update_cpu(self, total: float, per_core: List[float]) -> None:
        """Update CPU history with new values"""
        self.cpu_total.append(total)

        # Initialize per-core buffers if needed
        if self._cpu_core_count is None or self._cpu_core_count != len(per_core):
            self._cpu_core_count = len(per_core)
            self.cpu_cores = [HistoryBuffer(self.maxlen) for _ in range(len(per_core))]

        # Update per-core history
        for i, usage in enumerate(per_core):
            if i < len(self.cpu_cores):
                self.cpu_cores[i].append(usage)

    def update_memory(self, mem_percent: float, swap_percent: float) -> None:
        """Update memory history"""
        self.memory_percent.append(mem_percent)
        self.swap_percent.append(swap_percent)

    def update_network(self, bytes_sent: int, bytes_recv: int) -> Tuple[float, float]:
        """
        Update network history and return current speeds.

        Returns:
            Tuple of (upload_speed, download_speed) in bytes/second
        """
        upload_speed = self.net_upload.update(bytes_sent)
        download_speed = self.net_download.update(bytes_recv)
        return upload_speed, download_speed

    def update_disk_io(self, read_bytes: int, write_bytes: int) -> Tuple[float, float]:
        """
        Update disk I/O history and return current speeds.

        Returns:
            Tuple of (read_speed, write_speed) in bytes/second
        """
        return self.disk_io.update(read_bytes, write_bytes)

    def update_gpu(self, usage: Optional[float], memory_percent: Optional[float],
                   temp: Optional[float]) -> None:
        """Update GPU history"""
        if usage is not None:
            self.gpu_usage.append(usage)
        if memory_percent is not None:
            self.gpu_memory.append(memory_percent)
        if temp is not None:
            self.gpu_temp.append(temp)

    def get_cpu_graph_data(self, width: int) -> List[float]:
        """Get CPU history data, padded/truncated to specified width"""
        data = self.cpu_total.get_data()
        return self._fit_to_width(data, width)

    def get_memory_graph_data(self, width: int) -> List[float]:
        """Get memory history data, padded/truncated to specified width"""
        data = self.memory_percent.get_data()
        return self._fit_to_width(data, width)

    def get_network_graph_data(self, width: int) -> Tuple[List[float], List[float]]:
        """Get network history data (upload, download)"""
        upload = self._fit_to_width(self.net_upload.get_data(), width)
        download = self._fit_to_width(self.net_download.get_data(), width)
        return upload, download

    def get_disk_io_graph_data(self, width: int) -> Tuple[List[float], List[float]]:
        """Get disk I/O history data (read, write)"""
        read = self._fit_to_width(self.disk_io.get_read_data(), width)
        write = self._fit_to_width(self.disk_io.get_write_data(), width)
        return read, write

    def get_gpu_graph_data(self, width: int) -> List[float]:
        """Get GPU usage history data"""
        data = self.gpu_usage.get_data()
        return self._fit_to_width(data, width)

    @staticmethod
    def _fit_to_width(data: List[float], width: int) -> List[float]:
        """Pad or truncate data to fit specified width"""
        if len(data) >= width:
            return data[-width:]
        else:
            # Pad with zeros at the beginning
            padding = [0.0] * (width - len(data))
            return padding + list(data)

    def clear_all(self) -> None:
        """Clear all history buffers"""
        self.cpu_total.clear()
        for core in self.cpu_cores:
            core.clear()
        self.memory_percent.clear()
        self.swap_percent.clear()
        self.net_upload.clear()
        self.net_download.clear()
        self.disk_io.read_buffer.clear()
        self.disk_io.write_buffer.clear()
        self.gpu_usage.clear()
        self.gpu_memory.clear()
        self.gpu_temp.clear()
