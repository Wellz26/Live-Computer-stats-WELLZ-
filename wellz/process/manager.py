"""
Wellz Process Manager - Process listing and tree building
"""

import os
from typing import Any, Dict, List, Optional, Set

try:
    import psutil
except ImportError:
    psutil = None


class ProcessManager:
    """Manages process listing, filtering, and tree building"""

    def __init__(self):
        """Initialize process manager"""
        self._process_cache: List[Dict[str, Any]] = []
        self._tree_cache: Dict[int, List[int]] = {}

    def get_processes(self, sort_by: str = "cpu",
                      descending: bool = True,
                      limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get list of running processes.

        Args:
            sort_by: Sort key - "cpu", "memory", "pid", "name"
            descending: Sort in descending order
            limit: Maximum number of processes

        Returns:
            List of process dictionaries
        """
        if psutil is None:
            return []

        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent',
                                              'memory_percent', 'status', 'ppid',
                                              'create_time', 'cmdline']):
                try:
                    pinfo = proc.info
                    processes.append({
                        "pid": pinfo['pid'],
                        "name": pinfo['name'] or "unknown",
                        "username": pinfo['username'] or "unknown",
                        "cpu_percent": pinfo['cpu_percent'] or 0.0,
                        "memory_percent": pinfo['memory_percent'] or 0.0,
                        "status": pinfo['status'] or "unknown",
                        "ppid": pinfo['ppid'] or 0,
                        "create_time": pinfo.get('create_time', 0),
                        "cmdline": pinfo.get('cmdline', []),
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
        except Exception:
            pass

        # Sort
        sort_keys = {
            "cpu": lambda x: x['cpu_percent'],
            "memory": lambda x: x['memory_percent'],
            "pid": lambda x: x['pid'],
            "name": lambda x: x['name'].lower(),
        }
        key_func = sort_keys.get(sort_by, sort_keys["cpu"])

        # Determine sort direction
        reverse = descending if sort_by in ["cpu", "memory"] else not descending
        processes.sort(key=key_func, reverse=reverse)

        self._process_cache = processes
        return processes[:limit]

    def build_tree(self, processes: Optional[List[Dict[str, Any]]] = None) -> Dict[int, List[int]]:
        """
        Build process tree (parent -> children mapping).

        Args:
            processes: Process list (uses cache if not provided)

        Returns:
            Dictionary mapping parent PID to list of child PIDs
        """
        if processes is None:
            processes = self._process_cache

        tree: Dict[int, List[int]] = {}

        for proc in processes:
            ppid = proc.get("ppid", 0)
            pid = proc.get("pid", 0)

            if ppid not in tree:
                tree[ppid] = []
            tree[ppid].append(pid)

        self._tree_cache = tree
        return tree

    def get_tree_processes(self, sort_by: str = "cpu",
                           limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get processes in tree order (parents before children).

        Args:
            sort_by: Sort key for siblings
            limit: Maximum number of processes

        Returns:
            List of processes with tree depth information
        """
        processes = self.get_processes(sort_by=sort_by, descending=True, limit=500)
        tree = self.build_tree(processes)

        # Create PID -> process mapping
        pid_map = {p['pid']: p for p in processes}

        # Build ordered list starting from root processes
        result: List[Dict[str, Any]] = []
        visited: Set[int] = set()

        def add_subtree(pid: int, depth: int):
            if pid in visited or len(result) >= limit:
                return
            visited.add(pid)

            if pid in pid_map:
                proc = pid_map[pid].copy()
                proc['tree_depth'] = depth
                result.append(proc)

            # Add children
            for child_pid in tree.get(pid, []):
                add_subtree(child_pid, depth + 1)

        # Start from init/systemd (PID 1) or orphan processes
        root_pids = set()

        # Find processes whose parent is not in our list
        all_pids = set(p['pid'] for p in processes)
        for proc in processes:
            ppid = proc.get('ppid', 0)
            if ppid not in all_pids or ppid == 0:
                root_pids.add(proc['pid'])

        # Sort root pids by CPU for consistent ordering
        sorted_roots = sorted(root_pids,
                              key=lambda p: pid_map.get(p, {}).get('cpu_percent', 0),
                              reverse=True)

        for pid in sorted_roots:
            add_subtree(pid, 0)

        return result[:limit]

    def filter_processes(self, processes: List[Dict[str, Any]],
                         query: str) -> List[Dict[str, Any]]:
        """
        Filter processes by search query.

        Args:
            processes: List of processes to filter
            query: Search query (matches name, username, PID)

        Returns:
            Filtered list of processes
        """
        if not query:
            return processes

        query = query.lower()
        return [
            p for p in processes
            if query in p.get('name', '').lower()
            or query in p.get('username', '').lower()
            or query in str(p.get('pid', ''))
            or any(query in arg.lower() for arg in p.get('cmdline', []))
        ]

    def get_process_info(self, pid: int) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific process.

        Args:
            pid: Process ID

        Returns:
            Process information dictionary or None
        """
        if psutil is None:
            return None

        try:
            proc = psutil.Process(pid)
            with proc.oneshot():
                info = {
                    "pid": proc.pid,
                    "name": proc.name(),
                    "username": proc.username(),
                    "status": proc.status(),
                    "ppid": proc.ppid(),
                    "cpu_percent": proc.cpu_percent(),
                    "memory_percent": proc.memory_percent(),
                    "memory_info": proc.memory_info()._asdict(),
                    "create_time": proc.create_time(),
                    "cmdline": proc.cmdline(),
                    "cwd": proc.cwd() if hasattr(proc, 'cwd') else None,
                    "exe": proc.exe() if hasattr(proc, 'exe') else None,
                    "num_threads": proc.num_threads(),
                    "nice": proc.nice(),
                }

                # Try to get additional info (may require elevated privileges)
                try:
                    info["connections"] = len(proc.connections())
                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    info["connections"] = 0

                try:
                    info["open_files"] = len(proc.open_files())
                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    info["open_files"] = 0

                return info

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return None

    def get_children(self, pid: int) -> List[int]:
        """Get child PIDs of a process"""
        if psutil is None:
            return []

        try:
            proc = psutil.Process(pid)
            return [c.pid for c in proc.children()]
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return []

    def get_parent(self, pid: int) -> Optional[int]:
        """Get parent PID of a process"""
        if psutil is None:
            return None

        try:
            proc = psutil.Process(pid)
            parent = proc.parent()
            return parent.pid if parent else None
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None
