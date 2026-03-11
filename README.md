# Specc

> [!NOTE]
> **Environment Update**
>
> I was previously working on a borrowed PC running Ubuntu 22, where I had limited permissions (no `sudo` access). I no longer have access to that machine and am now using a Windows laptop.
>
> The new setup includes WSL with Ubuntu 24, which changes my development workflow. While this makes continuing certain Linux-based tasks more challenging, it also allows me to expand support and testing for Windows environments.
>
> I hope to return to a full Ubuntu setup in the future, as it remains my preferred OS.
>
> Thank you for your understanding.


> [!IMPORTANT]
> **Specc is currently in Alpha (v0.1.2).**
> Hardware sensor mappings are experimental and have only been validated on Ubuntu 22.04 LTS with AMD/NVIDIA hardware. Do not rely on this tool for mission-critical monitoring yet.

**Specc** is a lightweight, native system profiler designed specifically for the Ubuntu ecosystem. Built with Python 3.10, it gathers granular hardware specifications, OS metadata, and real-time thermal data into a structured JSON format or a clean terminal dashboard.

## Features

* **Terminal Dashboard**: Instant, color-coded hardware summary via `rich`.
* **Thermal Intelligence**: Automatically detects AMD (`k10temp`) and Intel (`coretemp`) thermal paths.
* **Hardware Profiling**: Extracts CPU core counts, RAM capacity, and storage metadata.
* **Snap Ready**: Built with strict confinement in mind, utilizing `hardware-observe` and `system-observe` interfaces.
* **CI/CD Integrated**: Automated Snap builds via GitHub Actions.

## Installation

### Development Mode
To set up a local development environment:

```bash
git clone https://github.com/Doccy-Dev/specc.git
cd specc
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

```

### Building & Testing the Snap

```bash
snapcraft
sudo snap install specc_*.snap --dangerous

# Connect interfaces for hardware access
sudo snap connect specc:hardware-observe
sudo snap connect specc:system-observe
sudo snap connect specc:mount-observe

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

### Example

```bash
~$ specc
╭───────────────────────╮
│ Specc System Profiler │
╰─────── v0.1.2 ────────╯
              Hardware & OS               
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Component ┃ Detail                     ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ OS        │ Ubuntu 22.04.5 LTS         │
│ Kernel    │ 6.8.0-101-generic          │
│ CPU       │ x86_64 Processor (8 Cores) │
│ Memory    │ 31.24 GB                   │
└───────────┴────────────────────────────┘

🌡️ Thermals
  • cpu temp: 54.875°C
  • gpu_temp: N/A
  • mb temp: 38.0°C
  • nvme temp: 40.85°C
```

**JSON Export:**

```bash
specc --output report.json

```

## Roadmap

* [x] **Live Monitoring**: Implemented `--live` flag (1s default) for real-time thermal tracking via `rich.live`.
* [ ] **Windows compatibility**: to get the project in current state working with Windows.
    - _I dont know how to do this on windows... any help would be good!_ - _How do people ask the community for help anyway?_
* [ ] **HUD**: Build a stand alone heads up display designed to run as always on, `--live` info.
* [ ] **GPU Telemetry**: Integrate `nvidia-smi` and `rocm-smi` to replace "N/A" with actual temps/models.

## Security & Confinement

In alignment with Canonical’s security standards, `specc` supports **Strict Confinement**.

| Interface | Purpose |
| --- | --- |
| `hardware-observe` | Reading thermal sensors and fan speeds |
| `system-observe` | Accessing `/proc` and hardware metadata |
| `mount-observe` | Accessing storage and partition metadata |

---
