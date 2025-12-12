<p align="center">
  <img src="https://img.shields.io/badge/version-2.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.7+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
</p>

<h1 align="center">
  <br>
  WELLZ
  <br>
</h1>

<h4 align="center">A btop-Inspired Gaming PC Stats Dashboard for Your Terminal & Desktop</h4>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#themes">Themes</a> •
  <a href="#keyboard-shortcuts">Keyboard Shortcuts</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#screenshots">Screenshots</a>
</p>

---

```
██╗    ██╗███████╗██╗     ██╗     ███████╗
██║    ██║██╔════╝██║     ██║     ╚══███╔╝
██║ █╗ ██║█████╗  ██║     ██║       ███╔╝
██║███╗██║██╔══╝  ██║     ██║      ███╔╝
╚███╔███╔╝███████╗███████╗███████╗███████╗
 ╚══╝╚══╝ ╚══════╝╚══════╝╚══════╝╚══════╝
```

## What's New in v2.0.0

- **Interactive Dashboard** - Full btop-style TUI with keyboard navigation
- **Real-time Graphs** - Braille-rendered CPU, Memory, Network, and Disk I/O graphs
- **8 Built-in Themes** - Default, Dracula, Nord, Gruvbox, Monokai, Solarized, Tokyo Night, Catppuccin
- **Process Manager** - View, sort, filter, and kill processes with vim-style controls
- **Config File Support** - Customize via `~/.config/wellz/config.toml`
- **Updated GUI Widget** - Graphs, themes, detailed system info

---

## Features

### Interactive Terminal Dashboard
- **Braille Graphs** - High-resolution history graphs for CPU, Memory, Network, Disk
- **Process Manager** - Sort by CPU/MEM/PID, filter with `/`, kill with `K`
- **Vim-style Navigation** - `j/k` scroll, `g/G` top/bottom, `/` search
- **Theme Switching** - Press `c` to cycle through 8 themes
- **Panel Toggling** - Number keys `1-6` toggle sections on/off
- **Responsive Layout** - Adapts to terminal size

### Desktop Widget (GUI)
- **Always-On-Top** - Stays visible while gaming
- **Mini Graphs** - Sparkline graphs for CPU, GPU, Memory
- **5 Themes** - Click Theme button to cycle
- **Detailed Info** - CPU name, GPU name/temp/VRAM, OS, uptime
- **Draggable** - Position anywhere on screen

### Hardware Monitoring

| Component | Metrics |
|-----------|---------|
| **CPU** | Model name, Usage %, Per-core bars, Frequency, Cores/Threads, History graph |
| **GPU** | Model name, Usage %, VRAM Used/Total, Temperature (NVIDIA) |
| **Memory** | RAM Used/Total/Available, Swap, History graph |
| **Disk** | Multiple partitions, Used/Total, I/O speed graph |
| **Network** | Hostname, IP addresses, TX/RX speeds, History graph |
| **Processes** | PID, User, CPU%, MEM%, Name, Tree view |

---

## Installation

### Prerequisites
- Python 3.7+
- pip
- For GUI: Tkinter (`python3-tk`)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/Wellz26/Live-Computer-stats-WELLZ-.git
cd Live-Computer-stats-WELLZ-

# Install
pip install .
```

### Alternative Methods

```bash
# User install (no sudo)
pip install . --user

# Development mode
pip install -e .

# Force reinstall
pip install . --force-reinstall
```

---

## Usage

### Interactive Dashboard (Default)

```bash
wellz                  # Launch interactive dashboard
wellz --theme dracula  # Start with specific theme
wellz --config ~/my.toml  # Use custom config
```

### Legacy Modes

```bash
wellz -s              # Static output (show once and exit)
wellz -l              # Legacy live mode (no keyboard controls)
wellz -l -i 2         # Legacy live with 2s refresh
```

### Desktop Widget

```bash
wellz-gui             # Launch GUI widget
```

### All Options

| Command | Description |
|---------|-------------|
| `wellz` | Interactive dashboard (default) |
| `wellz -s` | Static output |
| `wellz -l` | Legacy live mode |
| `wellz -l -i N` | Legacy live, N second refresh |
| `wellz --theme NAME` | Use specific theme |
| `wellz --config PATH` | Use custom config file |
| `wellz-gui` | Desktop widget |

---

## Keyboard Shortcuts

### Navigation
| Key | Action |
|-----|--------|
| `j` / `Down` | Move down |
| `k` / `Up` | Move up |
| `g` | Go to top |
| `G` | Go to bottom |
| `Tab` | Next section |

### Process Management
| Key | Action |
|-----|--------|
| `/` | Search/filter processes |
| `Enter` | Select process |
| `K` | Kill selected process (SIGTERM) |
| `S` | Signal menu (SIGKILL, SIGHUP, etc.) |
| `t` | Toggle tree view |

### Display
| Key | Action |
|-----|--------|
| `1` | Toggle CPU panel |
| `2` | Toggle Memory panel |
| `3` | Toggle Network panel |
| `4` | Toggle Disk panel |
| `5` | Toggle GPU panel |
| `6` | Toggle Process panel |
| `c` | Cycle themes |
| `+` / `-` | Adjust refresh rate |
| `r` | Reset view |

### General
| Key | Action |
|-----|--------|
| `?` | Help overlay |
| `q` | Quit |

---

## Themes

8 built-in themes available:

| Theme | Description |
|-------|-------------|
| `default` | Dark blue/cyan (GitHub-inspired) |
| `dracula` | Purple/pink/cyan |
| `nord` | Arctic blue/frost |
| `gruvbox` | Warm retro orange/yellow |
| `monokai` | Classic Monokai |
| `solarized` | Solarized dark |
| `tokyo` | Tokyo Night |
| `catppuccin` | Catppuccin Mocha |

Switch themes:
- **CLI**: Press `c` or use `--theme NAME`
- **GUI**: Click "Theme" button

---

## Configuration

Wellz reads config from `~/.config/wellz/config.toml`

### Example Config

```toml
[general]
refresh_rate = 1.0
history_size = 120

[display]
show_cpu = true
show_memory = true
show_network = true
show_disk = true
show_gpu = true
show_processes = true
graph_style = "braille"  # braille, block, ascii

[theme]
name = "dracula"

[processes]
sort_by = "cpu"
sort_descending = true
tree_view = false
```

### Graph Styles

| Style | Description |
|-------|-------------|
| `braille` | High-resolution using braille characters (default) |
| `block` | Block characters (▁▂▃▄▅▆▇█) |
| `ascii` | ASCII-only fallback |

---

## Screenshots

### Interactive Dashboard
```
┌─ CPU ─────────────────────────┐┌─ MEMORY ──────────────────────┐
│ Intel Core i5-6500 @ 3.2GHz   ││ RAM  [████████░░] 8.2/16.0 GB │
│ ⣿⣿⣷⣶⣤⣀⠀⠀⠀⠀⣀⣤⣶⣾⣿⣿ 42%            ││ ⣿⣿⣷⣶⣤⣀⠀⠀⠀⠀⣀⣤⣶⣾⣿⣿ 51%            │
│ Core 0 [████░░] 45%           ││ Swap [░░░░░░░░░░] 0.0/8.0 GB  │
│ Core 1 [██░░░░] 23%           │└───────────────────────────────┘
│ Core 2 [███░░░] 38%           │┌─ NETWORK ─────────────────────┐
│ Core 3 [█░░░░░] 12%           ││ ↑ 1.2 MB/s    ↓ 5.4 MB/s     │
└───────────────────────────────┘│ ⣿⣿⣷⣶⣤⣀⠀⠀⠀⠀⣀⣤⣶⣾⣿⣿              │
┌─ GPU ─────────────────────────┐│ TX: 1.5 GB    RX: 8.2 GB     │
│ NVIDIA GeForce RTX 3080       │└───────────────────────────────┘
│ Usage [██████░░░░] 23%        │┌─ PROCESSES ───────────────────┐
│ VRAM  2048/10240 MB           ││ PID   CPU%  MEM%  NAME        │
│ Temp  45°C                    ││ 1234  45.2  12.3  firefox     │
└───────────────────────────────┘│ 5678   8.1   4.2  code        │
                                 │ 9012   3.2   2.1  terminal    │
                                 └───────────────────────────────┘
```

### GUI Widget
- Always-on-top floating widget
- Shows CPU, GPU, Memory, Disk, Network
- Mini sparkline graphs
- Theme switching

---

## Supported Systems

### Linux Distributions
Kali, Arch, Ubuntu, Debian, Fedora, Manjaro, Mint, Pop!_OS, Red Hat, openSUSE

### Other Platforms
- **macOS** - Full support
- **Windows** - Full support

### GPU Support
| GPU | Support |
|-----|---------|
| NVIDIA | Full (usage, VRAM, temp via nvidia-smi) |
| AMD | Detection only |
| Intel | Detection only |

---

## Project Structure

```
wellz/
├── wellz/
│   ├── __init__.py
│   ├── cli.py              # Main entry point
│   ├── gui.py              # Desktop widget
│   ├── core/
│   │   ├── collectors.py   # Data collection
│   │   └── history.py      # Graph history buffers
│   ├── config/
│   │   ├── manager.py      # Config loading
│   │   ├── themes.py       # Theme definitions
│   │   └── default.toml    # Default config
│   ├── ui/
│   │   ├── app.py          # Main TUI application
│   │   ├── input_handler.py
│   │   ├── layout.py
│   │   ├── widgets/        # Graph, bar, box widgets
│   │   └── panels/         # CPU, Memory, GPU, etc. panels
│   └── process/
│       ├── manager.py      # Process listing
│       └── signals.py      # Kill/signal utilities
├── setup.py
├── pyproject.toml
└── README.md
```

---

## Troubleshooting

### Command not found
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Tkinter not found (for GUI)
```bash
# Debian/Ubuntu/Kali
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

### No GPU stats
```bash
nvidia-smi  # Check if nvidia-smi works
```

---

## Updating

```bash
cd Live-Computer-stats-WELLZ-
git pull origin main
pip install . --force-reinstall
```

---

## License

MIT License - see [LICENSE](LICENSE)

---

## Author

**Wellz26** - [@Wellz26](https://github.com/Wellz26)

---

<p align="center">
  <b>If you find Wellz useful, give it a star!</b>
</p>
