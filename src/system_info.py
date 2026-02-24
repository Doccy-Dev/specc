import psutil
import os
import logging

# Module-level logger for hardware telemetry errors
logger = logging.getLogger(__name__)

def gather_os_data():
    """Extracts core kernel and distribution metadata using the os module."""
    try:
        # os.uname() is standard on Unix-like systems (Linux, macOS)
        uname = os.uname()
        return {
            "OS_Name": uname.sysname,
            "Version": uname.version,
            "Architecture": uname.machine,
            "Kernel_Release": uname.release
        }
    except Exception as e:
        logger.error("OS Data Failure: %s", str(e))
        return None

def gather_thermal_data():
    """
    Reads thermal sensors from /sys/class/hwmon via psutil.
    Logic includes fallbacks for AMD (k10temp) and Intel (coretemp).
    """
    try:
        # sensors_temperatures() returns a dict of hardware monitoring objects
        temps = psutil.sensors_temperatures()
        
        # 1. CPU: Dynamic key lookup to support multiple CPU vendors
        cpu_key = next((k for k in ['k10temp', 'coretemp', 'cpu_thermal'] if k in temps), None)
        cpu_val = f"{temps[cpu_key][0].current}°C" if cpu_key else "N/A"

        # 2. Storage: Primary focus on NVMe controller telemetry
        nvme_key = temps.get('nvme', [])
        nvme_val = f"{nvme_key[0].current}°C" if nvme_key else "N/A"

        # 3. Motherboard: Specific WMI/SuperIO chip mappings
        # Note: 'gigabyte_wmi' is specific to certain AMD Gigabyte boards
        mb_key = temps.get('gigabyte_wmi', [])
        mb_val = f"{mb_key[0].current}°C" if mb_key else "N/A"

        return {
            "CPU": cpu_val,
            "GPU": "N/A", # Reserved for nvidia-smi / rocm-smi integration
            "Motherboard": mb_val,
            "NVMe_Drive": nvme_val
        }
    except Exception as e:
        # We use warning instead of error here because lack of sensor access
        # is common in virtualized or restricted (Snap) environments.
        logger.warning("Could not read thermal data: %s", str(e))
        return None

def gather_hardware_specs():
    """Gathers physical and logical hardware constraints."""
    try:
        return {
            "Physical_Cores": psutil.cpu_count(logical=False),
            "Logical_Processors": psutil.cpu_count(),
            "Total_RAM_GB": round(psutil.virtual_memory().total / (1024**3)),
            "GPU_Model": "NVIDIA"  # TODO: Implement pci-utils/lspci lookup
        }
    except Exception as e:
        logger.error("Hardware Spec Failure: %s", str(e))
        return None