# System Information Gathering Module
# This module is responsible for gathering all system information, including hardware specs, thermal data, and OS details. It serves as the main interface for the rest of the application to access system information, abstracting away the underlying platform-specific implementations. The actual data gathering is delegated to platform-specific modules (Windows.py, Debian.py, Mac.py), which are imported and used based on the detected operating system. This design allows for a clean separation of concerns and makes it easier to maintain and extend support for different platforms in the future.
# this modeule will change to a interpritar for the systems/ folder where the spacifics will acually be found and used. this is the main interface for the rest of the application to access system information, abstracting away the underlying platform-specific implementations. the actual data gathering is delegated to platform-specific modules (Windows.py, Debian.py, Mac.py), which are imported and used based on the detected operating system. this design allows for a clean separation of concerns and makes it easier to maintain and extend support for different platforms in the future.

import platform
import logging

logger = logging.getLogger(__name__)

def get_provider():
    """Returns the correct provider module based on the OS."""
    sys_type = platform.system()
    if sys_type == "Windows":
        from . import windows as provider
    elif sys_type == "Linux":
        from . import linux as provider
    else:
        raise NotImplementedError(f"OS {sys_type} not supported by Specc.")
    return provider

def gather_os_data():
    return get_provider().gather_os_data()

def gather_thermal_data():
    return get_provider().gather_thermal_data()

def gather_hardware_specs():
    return get_provider().gather_hardware_specs()

# file converted to act as a translator between the system information gathering and the rest of the application. it will import the correct provider based on the detected operating system and provide a unified interface for gathering system information. this allows the rest of the application to access system information without worrying about platform-specific details, making it easier to maintain and extend support for different platforms in the future. 