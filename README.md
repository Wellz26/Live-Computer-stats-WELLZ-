<p align="center">
  <img src="https://img.shields.io/badge/version-3.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.7+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
</p>

<h1 align="center">
  <br>
  WELLZ
  <br>
</h1>

<h4 align="center">A Premium Gaming PC Stats Dashboard for Your Terminal & Desktop</h4>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#themes">Themes</a> •
  <a href="#keyboard-shortcuts">Keyboard Shortcuts</a> •
  <a href="#configuration">Configuration</a>
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

## What's New in v3.0.0

### GUI Overhaul
- **8 Premium Themes** - Midnight, Dracula, Nord, Cyberpunk, Gruvbox, Tokyo Night, Catppuccin, Matrix
- **Smooth Line Charts** - Gradient fills with grid lines
- **Per-Core CPU Monitoring** - Visual grid with mini progress bars
- **Temperature Colors** - Blue (cool) → Cyan → Green → Yellow → Orange → Red (hot)
- **Opacity Slider** - Adjust transparency (50-100%)

### New Security Panels
- **Connected Devices** - USB devices & Network interfaces with IPs
- **Open Ports** - Listening ports with service names
- **Security Status** - VPN, Firewall, SSH, Root processes, Failed logins, Updates

### Additional Features
- **Battery Monitoring** - Percentage with charging status
- **Real-time Network Speeds** - Upload/Download in B/s, KB/s, MB/s
- **Disk I/O Speeds** - Read/Write rates
- **Top Processes** - Name, CPU%, MEM%
- **Logo** - Custom SVG/PNG logo
- **GitHub Footer** - Clickable link to repo

---

## Features

### Desktop Widget (GUI) - v3.0

| Panel | Information |
|-------|-------------|
| **System** | OS, Host, Arch, Uptime, Battery |
| **CPU** | Model, Usage %, Per-core bars, Frequency, Temperature |
| **GPU** | Model, Usage %, VRAM, Temperature |
| **Memory** | RAM Used/Total, Swap, History graph |
| **Disk** | Used/Total, Read/Write I/O speeds |
| **Network** | IP, Upload/Download speeds, TX/RX totals |
| **Top Processes** | Name, CPU%, MEM% (top 4) |
| **Connected Devices** | USB devices, Network interfaces |
| **Open Ports** | Port, Protocol, Service name |
| **Security Status** | VPN, Firewall, SSH, Root procs, Failed logins, Updates |

### Interactive Terminal Dashboard
- **Braille Graphs** - High-resolution history graphs
- **Process Manager** - Sort by CPU/MEM/PID, filter with `/`, kill with `K`
- **Vim-style Navigation** - `j/k` scroll, `g/G` top/bottom
- **Theme Switching** - Press `c` to cycle themes
- **Responsive Layout** - Adapts to terminal size

---

## Installation

### Prerequisites
- Python 3.7+
- pip
- For GUI: Tkinter (`python3-tk`) and Pillow (`pip install pillow`)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/Wellz26/Live-Computer-stats-WELLZ-.git
cd Live-Computer-stats-WELLZ-

# Install
pip install .

# For GUI logo support
pip install pillow
```

### Linux Dependencies

```bash
# Debian/Ubuntu/Kali
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

---

## Usage

### Desktop Widget (GUI)

```bash
wellz-gui             # Launch GUI widget
```

### Interactive Dashboard

```bash
wellz                  # Launch interactive dashboard
wellz --theme dracula  # Start with specific theme
```

### Legacy Modes

```bash
wellz -s              # Static output (show once and exit)
wellz -l              # Legacy live mode
wellz -l -i 2         # Legacy live with 2s refresh
```

---

## Themes

### GUI Themes (8 total)

| Theme | Style |
|-------|-------|
| `midnight` | Dark blue/cyan (GitHub-inspired) |
| `dracula` | Purple/pink/cyan |
| `nord` | Arctic blue/frost |
| `cyberpunk` | Neon cyan/magenta/yellow |
| `gruvbox` | Warm retro orange/yellow |
| `tokyo` | Tokyo Night purple/blue |
| `catppuccin` | Catppuccin Mocha pastels |
| `matrix` | Green on black |

Switch themes by clicking the **Theme** button in the GUI.

---

## Keyboard Shortcuts (Terminal)

### Navigation
| Key | Action |
|-----|--------|
| `j` / `Down` | Move down |
| `k` / `Up` | Move up |
| `g` | Go to top |
| `G` | Go to bottom |

### Display
| Key | Action |
|-----|--------|
| `1-6` | Toggle panels |
| `c` | Cycle themes |
| `?` | Help overlay |
| `q` | Quit |

---

## Configuration

Config file: `~/.config/wellz/config.toml`

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
graph_style = "braille"

[theme]
name = "dracula"
```

---

## Security Features

The GUI includes security monitoring:

| Feature | Status Colors |
|---------|---------------|
| **VPN** | Green (connected), Red (disconnected) |
| **Firewall** | Green (active), Red (inactive) |
| **SSH** | Yellow (running), Green (stopped) |
| **Root Processes** | Green (<50), Yellow (>50) |
| **Failed Logins** | Green (<5), Yellow (5-20), Red (>20) |
| **Updates** | Green (up to date), Yellow (pending) |

---

## Supported Systems

### Platforms
- **Linux** - Kali, Arch, Ubuntu, Debian, Fedora, Manjaro, Mint, Pop!_OS
- **macOS** - Full support
- **Windows** - Full support

### GPU Support
| GPU | Support |
|-----|---------|
| NVIDIA | Full (usage, VRAM, temp via nvidia-smi) |
| AMD | Detection only |
| Intel | Detection only |

---

## Troubleshooting

### Command not found
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Tkinter not found
```bash
sudo apt install python3-tk
```

### No GPU stats
```bash
nvidia-smi  # Check if nvidia-smi works
```

### Logo not showing
```bash
pip install pillow
```

---

## License

MIT License - see [LICENSE](LICENSE)

---

## Author

**Wellz26** - [@Wellz26](https://github.com/Wellz26)

---

<p align="center">
  <b>If you like WELLZ, leave a star!</b>
</p>
