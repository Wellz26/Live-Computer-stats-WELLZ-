<p align="center">
  <img src="https://img.shields.io/badge/version-1.1.0-blue.svg" alt="Version">
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
  <a href="#supported-systems">Supported Systems</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#screenshots">Screenshots</a> •
  <a href="#updating">Updating</a> •
  <a href="#license">License</a>
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

## Overview

**Wellz** is a btop-inspired, lightweight system monitoring tool designed for gamers and power users. It features a beautiful terminal dashboard with ASCII art OS logos and a sleek desktop widget that stays on top of your screen.

---

## Features

### Terminal Dashboard (btop-style)
- **Side-by-Side Panel Layout** - Clean, organized information display
- **OS Detection with ASCII Logos** - Automatically detects your OS and shows its logo
- **Per-Core CPU Usage** - Visual bars for each CPU core
- **Live Mode** - Real-time updating with customizable refresh rate
- **Color-Coded Metrics** - Green (0-49%), Yellow (50-79%), Red (80-100%)
- **No Emojis** - Clean ASCII-only interface

### Desktop Widget (GUI)
- **Always-On-Top** - Stays visible while gaming or working
- **Dark Theme** - btop-inspired dark color scheme
- **Draggable** - Position it anywhere on your screen
- **OS Badge** - Shows detected operating system

### Hardware Monitoring

| Component | Metrics |
|-----------|---------|
| **CPU** | Model, Total Usage %, Per-Core Usage, Frequency, Cores/Threads |
| **GPU** | Model, Usage %, VRAM Used/Total, Temperature (NVIDIA) |
| **Memory** | RAM Used/Total, Available, Swap Usage |
| **Disk** | Multiple partitions, Used/Total per mount |
| **Network** | Hostname, IP addresses, TX/RX totals |
| **System** | OS, Kernel, Architecture, Uptime |

---

## Supported Systems

Wellz automatically detects your operating system and displays the appropriate ASCII logo:

### Linux Distributions
| Distro | Logo | Distro | Logo |
|--------|------|--------|------|
| Kali Linux | Dragon | Arch Linux | Arch symbol |
| Ubuntu | Circle of friends | Debian | Swirl |
| Fedora | Infinity | Manjaro | Bars |
| Linux Mint | Leaf | Pop!_OS | Pop |
| Red Hat | Hat | openSUSE | Chameleon |
| Generic Linux | Tux | | |

### Other Platforms
| Platform | Support |
|----------|---------|
| **macOS** | Full support with Apple logo |
| **Windows** | Full support with Windows logo |

---

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- For GUI: Tkinter (usually pre-installed)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/Wellz26/Live-Computer-stats-WELLZ-.git
cd Live-Computer-stats-WELLZ-

# Install the package
pip install .
```

### Alternative Methods

```bash
# User install (no sudo)
pip install . --user

# System-wide
sudo pip install .

# Development mode
pip install -e .
```

### Post-Installation

Add to your PATH if needed:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

---

## Usage

### Terminal Dashboard

```bash
# Show stats once
wellz

# Live mode (continuous updates)
wellz -l

# Live mode with 2 second refresh
wellz -l -i 2

# Show help
wellz --help
```

### Desktop Widget

```bash
# Launch GUI widget
wellz-gui
```

### Commands

| Command | Description |
|---------|-------------|
| `wellz` | Show stats once |
| `wellz -l` | Live mode (1s refresh) |
| `wellz -l -i N` | Live mode (N second refresh) |
| `wellz-gui` | Desktop widget |

---

## Screenshots

### Terminal Dashboard (Kali Linux)
```
╭─ SYSTEM ──────────────────────────────╮  ╭─ CPU ───────────────────────────────╮
│ OS      Linux 6.1.0-kali              │  │ Intel(R) Core(TM) i5-6500 CPU @ ... │
│ Host    gaming-pc                     │  │ Cores 4  Threads 4  Freq 3200MHz   │
│ Arch    x86_64                        │  ├──────────────────────────────────────┤
│ Uptime  5h 32m                        │  │ Total  [████████░░░░░░░░░░░░]  42.5% │
├──────────────────────────────────────┤  │ 0██   1███  2█    3████              │
│       ..                              │  ╰──────────────────────────────────────╯
│     .WWWW.                            │
│    .WW  WW.      KALI LINUX           │
│   .WW    WW.                          │
│   WW  ..  WW                          │
│   WW WWWW WW                          │
│    WW    WW                           │
╰──────────────────────────────────────╯

╭─ GPU ─────────────────────────────────╮  ╭─ MEMORY ────────────────────────────╮
│ NVIDIA GeForce RTX 3080               │  │ RAM    [████████████░░░░░░░░] 12.4/32.0GB │
│ Usage  [██████░░░░░░░░░░░░░░]  23.0%  │  │ Avail  19.6GB                       │
│ VRAM   [████░░░░░░░░░░░░░░░░] 2048/10240MB │  │ Swap   [░░░░░░░░░░░░░░░░░░░░] 0.0/8.0GB │
│ Temp   45C                            │  ╰──────────────────────────────────────╯
╰──────────────────────────────────────╯

╭─ DISK ────────────────────────────────╮  ╭─ NETWORK ───────────────────────────╮
│ /          [████████░░░░░░░] 256/512GB │  │ Host  gaming-pc                     │
│ /home      [██████░░░░░░░░░] 128/256GB │  │ eth0  192.168.1.100                 │
╰──────────────────────────────────────╯  ├──────────────────────────────────────┤
                                          │ TX 1.5GB         RX 8.2GB            │
                                          ╰──────────────────────────────────────╯
```

### Color Coding

| Color | Usage | Status |
|-------|-------|--------|
| Green | 0-49% | Healthy |
| Yellow | 50-79% | Moderate |
| Red | 80-100% | High Load |

---

## Updating

```bash
# Navigate to repo
cd Live-Computer-stats-WELLZ-

# Pull latest
git pull origin main

# Reinstall
pip install . --upgrade
```

**Or fresh install:**
```bash
pip uninstall wellz
rm -rf Live-Computer-stats-WELLZ-
git clone https://github.com/Wellz26/Live-Computer-stats-WELLZ-.git
cd Live-Computer-stats-WELLZ-
pip install .
```

---

## Configuration

### GPU Support

| GPU | Support Level |
|-----|---------------|
| NVIDIA | Full (usage, VRAM, temp via nvidia-smi) |
| AMD | Detection only (full support coming) |
| Intel | Detection only |

### Dependencies

| Package | Purpose | Required |
|---------|---------|----------|
| `psutil` | System metrics | Yes |
| `tkinter` | GUI widget | For GUI only |

---

## Troubleshooting

### Command not found
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Tkinter not found
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
# Check nvidia-smi
nvidia-smi
```

---

## Project Structure

```
wellz/
├── wellz/
│   ├── __init__.py      # Package info
│   ├── cli.py           # Terminal dashboard
│   └── gui.py           # Desktop widget
├── setup.py
├── pyproject.toml
├── README.md
└── LICENSE
```

---

## Roadmap

- [x] btop-style interface
- [x] OS detection with ASCII logos
- [x] Per-core CPU monitoring
- [x] GPU temperature (NVIDIA)
- [ ] AMD GPU full support
- [ ] CPU temperature
- [ ] Fan speed monitoring
- [ ] Custom themes
- [ ] Config file support

---

## License

MIT License - see [LICENSE](LICENSE)

---

## Author

**Wellz26** - [@Wellz26](https://github.com/Wellz26)

---

<p align="center">
  <b>If you find Wellz useful, give it a star on GitHub!</b>
</p>
