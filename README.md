# Specc

> [!IMPORTANT]
> **Specc is currently in Alpha.**
> Hardware sensor mappings are experimental and have only been validated on Ubuntu 22.04 LTS with AMD/NVIDIA hardware. Do not rely on this tool for mission-critical monitoring yet.


**Specc** is a lightweight, native system profiler designed specifically for the Ubuntu ecosystem. Built with Python 3.10, it gathers granular hardware specifications, OS metadata, and real-time thermal data into a structured JSON format.

**specc** is designed to be highly portable, secure, and ready for deployment via Snapcraft.

## Features

* **Thermal Intelligence**: Automatically detects AMD (`k10temp`) and Intel (`coretemp`) thermal paths.
* **Hardware Profiling**: Extracts CPU core counts, RAM capacity, and storage metadata.
* **Native Compatibility**: Optimized for Ubuntu 22.04 LTS (Python 3.10.12).
* **Snap Ready**: Built with strict confinement in mind, utilizing `hardware-observe` and `system-observe` interfaces.

## Installation

### Development Mode
To set up a local development environment:

```bash
git clone [https://github.com/doccy/specc.git](https://github.com/doccy/specc.git)
cd specc
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

```

### Building the Snap

`specc` is designed to be packaged as a Snap for cross-distro compatibility.

```bash
snapcraft
sudo snap install specc_*.snap --dangerous
# Connect interfaces for hardware access
sudo snap connect specc:hardware-observe

```

## Usage

Run the tool to generate a system report:

```bash
specc --output report.json

```

## Project Structure

* `src/main.py`: The entry point and CLI logic.
* `src/system_info.py`: Hardware and thermal data extraction logic.
* `snap/snapcraft.yaml`: Packaging configuration for the Ubuntu Snap Store.

## Roadmap

- [ ] **Windows Support**: Porting `os.uname` logic to `platform` for cross-OS compatibility.
- [ ] **GPU Telemetry**: Integration with `nvidia-smi` and `rocm-smi` for dedicated GPU thermals.
- [ ] **Native JSON Schema**: Validation for output consistency using `jsonschema`.
- [ ] **GitHub Actions**: Automated Snap builds on every push.

## Security & Confinement

In alignment with Canonical’s security standards, `specc` supports **Strict Confinement**. When running as a Snap, the following interfaces are required to access system telemetry:

| Interface | Purpose |
| --- | --- |
| `hardware-observe` | Reading thermal sensors and fan speeds |
| `system-observe` | Accessing `/proc` and hardware metadata |

---
