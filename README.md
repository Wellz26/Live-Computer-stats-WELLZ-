<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.7+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/platform-Linux%20%7C%20macOS-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
</p>

<h1 align="center">
  <br>
  WELLZ
  <br>
</h1>

<h4 align="center">A Beautiful Gaming PC Stats Dashboard for Your Terminal & Desktop</h4>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#screenshots">Screenshots</a> •
  <a href="#configuration">Configuration</a> •
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
         ⚡ Gaming PC Stats Dashboard ⚡
```

## Overview

**Wellz** is a lightweight, visually stunning system monitoring tool designed for gamers and power users. It provides real-time hardware statistics through both a colorful terminal interface and a sleek desktop widget that stays on top of your screen.

Whether you're gaming, streaming, or just want to keep an eye on your system's performance, Wellz delivers the information you need in style.

---

## Features

### Terminal Dashboard
- **ASCII Art Interface** - Beautiful box-drawing characters and colored output
- **Live Mode** - Real-time updating stats with customizable refresh rate
- **Color-Coded Metrics** - Green (healthy), Yellow (moderate), Red (high load)

### Desktop Widget (GUI)
- **Always-On-Top** - Stays visible while gaming or working
- **Dark Gaming Theme** - Sleek dark interface that looks great on any setup
- **Draggable** - Position it anywhere on your screen
- **Compact Design** - Minimal footprint, maximum information

### Hardware Monitoring
| Component | Metrics |
|-----------|---------|
| **CPU** | Model, Usage %, Frequency, Cores/Threads |
| **GPU** | Model, Usage %, VRAM Used/Total (NVIDIA) |
| **RAM** | Used/Total GB, Usage % |
| **Disk** | Used/Total GB, Usage % |
| **Network** | Hostname, IP, Upload/Download totals |
| **System** | OS, Architecture, Uptime |

---

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- For GUI: Tkinter (usually pre-installed on Linux)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/Wellz26/Live-Computer-stats-WELLZ-.git
cd Live-Computer-stats-WELLZ-

# Install the package
pip install .
```

### Alternative Installation Methods

**Using pip with user flag (no sudo required):**
```bash
pip install . --user
```

**For system-wide installation:**
```bash
sudo pip install .
```

**Development mode:**
```bash
pip install -e .
```

### Post-Installation

After installation, ensure `~/.local/bin` is in your PATH:

```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"

# Reload your shell
source ~/.bashrc
```

---

## Usage

### Terminal Dashboard

```bash
# Display stats once
wellz

# Live mode - continuous updates (default: 1 second refresh)
wellz -l

# Live mode with custom refresh interval (e.g., 2 seconds)
wellz -l -i 2

# Show help
wellz --help
```

### Desktop Widget

```bash
# Launch the GUI widget
wellz-gui
```

The widget will appear in the top-right corner of your screen. You can:
- **Drag** it anywhere by clicking and dragging
- **Close** it using the Close button or window controls

### Command Reference

| Command | Description |
|---------|-------------|
| `wellz` | Show stats once and exit |
| `wellz -l` | Live mode with 1s refresh |
| `wellz -l -i <seconds>` | Live mode with custom refresh |
| `wellz --help` | Show help message |
| `wellz-gui` | Launch desktop widget |

---

## Screenshots

### Terminal Dashboard
```
  ╭──────────────────────────────────────────────────────────╮
  │  🖥️  SYSTEM                                               │
  │  OS: Linux 6.1.0-amd64              Arch: x86_64         │
  │  Uptime: 2:34:15                                         │
  ╰──────────────────────────────────────────────────────────╯

  ╭──────────────────────────────────────────────────────────╮
  │  🔥 CPU                                                   │
  │  AMD Ryzen 9 5900X 12-Core Processor                     │
  │  Cores: 12  Threads: 24  Freq: 3700MHz                   │
  │  Usage: [████████████░░░░░░░░░░░░░░░░░░]  42.5%          │
  ╰──────────────────────────────────────────────────────────╯

  ╭──────────────────────────────────────────────────────────╮
  │  🎮 GPU                                                   │
  │  NVIDIA GeForce RTX 3080                                 │
  │  Usage: [██████░░░░░░░░░░░░░░░░░░░░░░░░]  23.0%          │
  │  VRAM:  [████████░░░░░░░░░░░░░░░░░░░░░░] 2048/10240 MB   │
  ╰──────────────────────────────────────────────────────────╯

  ╭──────────────────────────────────────────────────────────╮
  │  💾 RAM                                                   │
  │  Memory: [████████████████░░░░░░░░░░░░░░] 12.4/32.0 GB   │
  ╰──────────────────────────────────────────────────────────╯

  ╭──────────────────────────────────────────────────────────╮
  │  💿 DISK                                                  │
  │  Storage: [████████████████████░░░░░░░░░░] 512/1024 GB   │
  ╰──────────────────────────────────────────────────────────╯

  ╭──────────────────────────────────────────────────────────╮
  │  🌐 NETWORK                                               │
  │  Host: gaming-pc                IP: 192.168.1.100        │
  │  ↑ Sent: 1542.3 MB    ↓ Recv: 8234.1 MB                  │
  ╰──────────────────────────────────────────────────────────╯
```

### Color Coding System

| Color | Usage Level | Status |
|-------|-------------|--------|
| 🟢 Green | 0% - 49% | Healthy |
| 🟡 Yellow | 50% - 79% | Moderate |
| 🔴 Red | 80% - 100% | High Load |

---

## Configuration

### GPU Support

**NVIDIA GPUs:**
Full support including usage percentage and VRAM monitoring. Requires `nvidia-smi` (included with NVIDIA drivers).

```bash
# Verify nvidia-smi is available
nvidia-smi
```

**AMD GPUs:**
Basic detection via `lspci`. Full monitoring support coming in future releases.

**Intel Integrated Graphics:**
Basic detection supported.

### Dependencies

| Package | Purpose | Required |
|---------|---------|----------|
| `psutil` | System metrics | Yes |
| `tkinter` | GUI widget | For GUI only |

Dependencies are automatically installed when using pip.

---

## Project Structure

```
wellz/
├── wellz/
│   ├── __init__.py      # Package initialization
│   ├── cli.py           # Terminal dashboard
│   └── gui.py           # Desktop widget
├── setup.py             # Package setup (legacy)
├── pyproject.toml       # Modern Python packaging
├── README.md            # Documentation
└── LICENSE              # MIT License
```

---

## Troubleshooting

### Command not found after installation

Add the local bin directory to your PATH:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Tkinter not found (GUI)

Install Tkinter for your distribution:

```bash
# Debian/Ubuntu
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
```

### No GPU stats showing

Ensure NVIDIA drivers and `nvidia-smi` are properly installed:
```bash
# Check if nvidia-smi works
nvidia-smi

# Install NVIDIA drivers (Ubuntu)
sudo apt install nvidia-driver-XXX
```

### Permission errors

Use the `--user` flag with pip:
```bash
pip install . --user
```

---

## Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## Roadmap

- [ ] AMD GPU full monitoring support
- [ ] Temperature readings (CPU/GPU)
- [ ] Fan speed monitoring
- [ ] Custom themes for GUI
- [ ] Configuration file support
- [ ] System tray integration
- [ ] Windows support

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author

**Wellz26**

- GitHub: [@Wellz26](https://github.com/Wellz26)

---

<p align="center">
  <b>If you find Wellz useful, please consider giving it a ⭐ on GitHub!</b>
</p>
