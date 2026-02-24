import argparse
import json
from datetime import datetime
from src.config import Config
from src.logger import setup_logger
from src.system_info import gather_os_data, gather_thermal_data, gather_hardware_specs

def parse_args():
    """Defines CLI arguments for the tool."""
    parser = argparse.ArgumentParser(description='Specc: A native Ubuntu hardware profiler.')
    parser.add_argument('--output', type=str, help='Custom path for the JSON report')
    return parser.parse_args()

def main(): 
    """Primary execution flow for gathering and exporting system telemetry."""
    args = parse_args()
    config = Config()
    logger = setup_logger(config)
    
    # Priority: CLI argument > Config default
    output_file = args.output if args.output else config.output_file

    # Structured data aggregation
    report = {
        "Metadata": {
            "Generated_At": str(datetime.now()), 
            "Unit": "Celsius",
            "Schema_Version": "0.1.0"
        },
        "System": gather_os_data(),
        "Thermals": gather_thermal_data(),
        "Hardware": gather_hardware_specs()
    }

    try:
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=4)
        logger.info(f"Report successfully generated at: {output_file}")
    except IOError as e:
        logger.error(f"File System Error: Could not write to {output_file} - {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()