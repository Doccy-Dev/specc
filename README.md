# Specc

> [!NOTE]
> **Development Status & Environment**
> I am currently developing on a Windows laptop using WSL (Ubuntu 24). Due to limited internet connectivity, **I rely heavily on GitHub Action pipelines for initial build validation.** >
> While code is pushed frequently to trigger these automated builds, **official releases (tags) are always manually tested and validated** on physical hardware before being published. Thank you for your patience as the project evolves in this hybrid environment.

> [!IMPORTANT]
> **Specc is currently in Alpha (v0.1.3).**
> Cross-platform support is new. Hardware sensor mappings are experimental and have been validated on Ubuntu 22.04 (AMD/NVIDIA) and Windows 11. Do not rely on this tool for mission-critical monitoring yet.

**Specc** is a lightweight, native system profiler designed for Linux and Windows. Built with Python, it gathers granular hardware specifications, OS metadata, and real-time thermal data into a structured JSON format or a clean terminal dashboard.

## Features

* **Terminal Dashboard**: Instant, color-coded hardware summary via `rich`.
* **Cross-Platform**: Native support for **Ubuntu (Snap)** and **Windows (.exe)**.
* **Thermal Intelligence**: Automatically detects AMD (`k10temp`), Intel (`coretemp`), and Windows WMI thermal paths.
* **Hardware Profiling**: Extracts CPU model names, core counts, RAM capacity, and storage metadata.
* **CI/CD Integrated**: Automated builds for Snaps and Windows Executables via GitHub Actions.

## Installation

### Windows (Standalone)

Download the latest `specc.exe` from the **Releases** page. No Python installation is required for the standalone executable.

> *Note: Running as Administrator is recommended on Windows to allow thermal sensor access via WMI.*

### Linux (Snap)

```bash
sudo snap install specc
# Connect interfaces for hardware access
sudo snap connect specc:hardware-observe
sudo snap connect specc:system-observe
sudo snap connect specc:mount-observe

```

### Development Mode

To set up a local development environment:

```bash
git clone https://github.com/Doccy-Dev/specc.git
cd specc
python3 -m venv .venv
# Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

pip install -e .

```

## Usage

**Interactive Dashboard (Default):**

```bash
specc

```

or

```bash
specc --live # to get real time data

```

**JSON Export:**

```bash
specc --output report.json

```

## Roadmap

* [x] **Live Monitoring**: Real-time thermal tracking via `rich.live`.
* [x] **Windows Compatibility**: Initial support for Windows OS metadata and WMI thermals.
* [ ] **Winget Support**: Official manifest for Windows Package Manager.
* [ ] **GPU Telemetry**: Integrate `nvidia-smi` and `rocm-smi` across all platforms.
* [ ] **Heads Up Display (HUD)**: A dedicated "always-on-top" monitoring mode.

## Security & Confinement (Linux)

In alignment with Canonical’s security standards, `specc` supports **Strict Confinement**.

| Interface | Purpose |
| --- | --- |
| `hardware-observe` | Reading thermal sensors and fan speeds |
| `system-observe` | Accessing `/proc` and hardware metadata |
| `mount-observe` | Accessing storage and partition metadata |

---
