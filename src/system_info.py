import psutil
import os
import platform # Added for better distro detection
import logging

logger = logging.getLogger(__name__)

def gather_os_data():
    try:
        uname = os.uname()
        # platform.freedesktop_os_release() is great for Ubuntu/Debian 
        # to get the "Pretty Name" like "Ubuntu 22.04.3 LTS"
        try:
            distro_info = platform.freedesktop_os_release()
            distro = distro_info.get("PRETTY_NAME", "Ubuntu")
        except:
            distro = "Ubuntu"

        return {
            "distro": distro,
            "kernel": uname.release,
            "arch": uname.machine
        }
    except Exception as e:
        logger.error("OS Data Failure: %s", str(e))
        return {"distro": "Linux", "kernel": "Unknown", "arch": "Unknown"}

def gather_thermal_data():
    try:
        temps = psutil.sensors_temperatures()
        
        # Return raw floats so the UI can decide on the color/formatting
        cpu_key = next((k for k in ['k10temp', 'coretemp', 'cpu_thermal'] if k in temps), None)
        cpu_val = temps[cpu_key][0].current if cpu_key else None

        nvme_key = temps.get('nvme', [])
        nvme_val = nvme_key[0].current if nvme_key else None

        mb_key = temps.get('gigabyte_wmi', [])
        mb_val = mb_key[0].current if mb_key else None

        return {
            "cpu_temp": cpu_val,
            "gpu_temp": None, 
            "mb_temp": mb_val,
            "nvme_temp": nvme_val
        }
    except Exception as e:
        logger.warning("Could not read thermal data: %s", str(e))
        return {}

def gather_hardware_specs():
    try:
        return {
            "cpu_model": "x86_64 Processor", # Placeholder until lscpu integration
            "cores": psutil.cpu_count(logical=False),
            "threads": psutil.cpu_count(),
            "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        }
    except Exception as e:
        logger.error("Hardware Spec Failure: %s", str(e))
        return {}