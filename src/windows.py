# this is the first attemp at windows support. 
# it will be a 'best effort' approach, as Windows does not provide the same level of access to hardware and thermal data as Linux does.
#  we will use the wmi module to attempt to gather CPU temperature data, but this may not work on all systems due to driver and hardware differences. 
# we will also gather basic hardware specs using wmi and psutil, but again, the level of detail may be limited compared to Linux. 
# the goal is to provide as much information as possible within the constraints of the Windows platform, while maintaining a consistent interface for the rest of the application.

import platform
import psutil
try:
    import wmi # Windows-specific module for hardware info
except ImportError:
    wmi = None # If wmi is not available, we can still run but with limited functionality.

def gather_os_data(): # Windows provides limited OS data compared to Linux, but we'll do our best.
    return {
        "distro": f"Windows {platform.release()}", 
        "kernel": platform.version(), # Windows doesn't have a traditional kernel version like Linux, but platform.version() gives us the build number which is the closest equivalent.
        "arch": platform.machine() # This will return 'AMD64' for 64-bit Windows, which is the most common architecture.
    }

def gather_thermal_data():
    # Windows is protective of thermals. This is the 'best effort' approach.
    data = {"cpu_temp": None, "mb_temp": None, "nvme_temp": None} # Windows doesn't provide a standard way to access motherboard or NVMe temps, and CPU temps often require admin privileges. We'll attempt to get CPU temp via WMI if available, but it may not work on all systems.
    if wmi:
        try:
            # Requires Admin privileges to return data
            w = wmi.WMI(namespace="root\\wmi") # This namespace is where thermal data is typically found on Windows.
            temps = w.MSAcpi_ThermalZoneTemperature() # This class provides temperature data for thermal zones, which often includes CPU temperature. However, the availability and accuracy of this data can vary widely between different hardware and drivers.
            if temps:
                # Convert deci-Kelvin to Celsius
                data["cpu_temp"] = (temps[0].CurrentTemperature / 10.0) - 273.15 
        except:
            pass
    return data

def gather_hardware_specs():
    cpu_model = "Windows Processor"
    if wmi:
        try:
            c = wmi.WMI() # This is the default namespace for general system information, including CPU details.
            cpu_model = c.Win32_Processor()[0].Name
        except:
            pass
            
    return {
        "cpu_model": cpu_model.strip(), # Windows often returns CPU model with extra whitespace, so we strip it for cleaner output.
        "cores": psutil.cpu_count(logical=False), # Windows doesn't differentiate between physical and logical cores in the same way as Linux, but psutil will return the correct number of physical cores when logical=False is used.
        "threads": psutil.cpu_count(), 
        "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2), # Windows provides total RAM in bytes, so we convert it to GB for consistency with Linux output.
    }

# I miss linux. I miss the freedom and control it gives you over your system. Windows is like a black box, and you never know what you're going to get. 
# But I'm determined to make this work, even if it means dealing with the limitations of the platform. 
# Let's see how much information we can gather from Windows and how we can present it in a useful way.