# Specc

> [!NOTE]
> **Development Status & Environment**
> I am currently developing on a Windows laptop using WSL (Ubuntu 24). Due to limited internet connectivity, **I rely heavily on GitHub Action pipelines for initial build validation.** >
> While code is pushed frequently to trigger these automated builds, **official releases (tags) are always manually tested and validated** on physical hardware before being published. Thank you for your patience as the project evolves in this hybrid environment.

> [!IMPORTANT]
> **Specc is currently in Alpha (v0.1.3).**
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
git clone https://github.com/doccy/specc.git
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

* [x] **Done (v0.1.2)**: **Live Monitoring**: Implemented `--live` flag (1s default) for real-time thermal tracking via `rich.live`.
* [x] **Done (v0.1.3)**: **Windows Compatibility**: Initial support for Windows OS metadata and WMI thermals.
* [ ] **Next (v0.1.4)**: **Upcoming (v0.2.0)**: **GPU Telemetry**: Integrate `nvidia-smi` and `rocm-smi` to replace "N/A" with actual temps/models.
* [ ] **Native JSON Schema**: Validation for output consistency using `jsonschema`.
* [ ] **Cross-Platform**: Port `os.uname` and thermal pathing to `platform` for Windows/macOS support.

## Security & Confinement

In alignment with Canonical’s security standards, `specc` supports **Strict Confinement**.

| Interface | Purpose |
| --- | --- |
| `hardware-observe` | Reading thermal sensors and fan speeds |
| `system-observe` | Accessing `/proc` and hardware metadata |
| `mount-observe` | Accessing storage and partition metadata |

---

