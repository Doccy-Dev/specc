# This module is responsible for gathering system information on Linux-based systems. 
# It uses the psutil library to access hardware and thermal data, and the platform library to gather OS

import os
import platform
import psutil

def gather_os_data():
    try:
        distro_info = platform.freedesktop_os_release() # This function provides detailed information about the Linux distribution, including a user-friendly name in the PRETTY_NAME field. However, it may not be available on all systems, so we wrap it in a try-except block to provide a fallback.
        distro = distro_info.get("PRETTY_NAME", "Ubuntu")
    except:
        distro = "Linux"
    
    return {
        "distro": distro,
        "kernel": os.uname().release,
        "arch": os.uname().machine
    }

def gather_thermal_data(): # Linux provides access to thermal data through the psutil library, which can read from the system's thermal sensors. However, the availability and accuracy of this data can vary widely between different hardware and drivers, so we use a 'best effort' approach to gather CPU, motherboard, and NVMe temperatures when available.
    temps = psutil.sensors_temperatures()
    cpu_key = next((k for k in ['k10temp', 'coretemp', 'cpu_thermal'] if k in temps), None) # Different Linux systems may report CPU temperatures under different keys, so we check for common ones in a specific order to find the most likely candidate for CPU temperature data.
    return {
        "cpu_temp": temps[cpu_key][0].current if cpu_key else None, # If we found a valid CPU temperature key, we take the first sensor's current temperature as the CPU temperature. If not, we return None to indicate that CPU temperature data is not available.
        "mb_temp": temps.get('gigabyte_wmi', [None])[0].current if 'gigabyte_wmi' in temps else None, # Some Gigabyte motherboards expose a WMI interface that can provide motherboard temperature data, but this is not common and may not be available on all systems. We check for the presence of the 'gigabyte_wmi' key in the temperatures data and attempt to read the first sensor's current temperature if it exists.
        "nvme_temp": temps.get('nvme', [None])[0].current if 'nvme' in temps else None # NVMe SSDs can report their temperature through the 'nvme' key in the sensors data, but this is also not guaranteed to be available on all systems. We check for the presence of the 'nvme' key and attempt to read the first sensor's current temperature if it exists.
    }

def gather_hardware_specs(): # Linux provides detailed hardware specifications through the psutil library and the /proc/cpuinfo file. We use psutil to get the number of physical cores and total RAM, and we read from /proc/cpuinfo to get the CPU model name, which is typically more detailed than what psutil provides. However, we wrap the CPU model retrieval in a try-except block to provide a fallback in case of any issues accessing /proc/cpuinfo.
    cpu_model = "x86_64 Processor"
    try:
        # A lightweight way to get the actual name on Linux
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if "model name" in line:
                    cpu_model = line.split(":")[1].strip() # The model name is typically in the format "model name : Intel(R) Core(TM) i7-9700K CPU @ 3.60GHz", so we split on the colon and take the second part, stripping any extra whitespace for a cleaner output. We break after finding the first occurrence of "model name" since it should be the same for all processors in the system. If we encounter any issues reading from /proc/cpuinfo, we catch the exception and fall
                    break
    except:
        pass

    return {
        "cpu_model": cpu_model,
        "cores": psutil.cpu_count(logical=False),
        "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
    }
# Linux is my home. It's where I learned to code and where I feel most comfortable working with hardware and system information.
# im thinking of asking for dontations to help fund a new linux machine (my first computer i acually own) 
# that way i can use the OS i love! look out snapcraft, im coming for you!