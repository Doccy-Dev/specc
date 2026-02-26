import argparse
import json
import sys
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Local project imports
from src.config import Config
from src.logger import setup_logger
from src.system_info import gather_os_data, gather_thermal_data, gather_hardware_specs

def parse_args():
    """Defines CLI arguments for the tool."""
    parser = argparse.ArgumentParser(description='Specc: A native Ubuntu hardware profiler.')
    parser.add_argument('--output', type=str, help='Custom path for the JSON report')
    return parser.parse_args()

def print_console_report(report):
    """Renders a beautiful CLI dashboard using Rich."""
    console = Console()
    
    # 1. Header
    console.print(Panel("[bold blue]Specc System Profiler[/bold blue]", subtitle="v0.1.1", expand=False))

    # 2. Hardware Table
    hw_table = Table(title="Hardware & OS", show_header=True, header_style="bold magenta")
    hw_table.add_column("Component", style="dim")
    hw_table.add_column("Detail")

    sys_info = report["System"]
    hw_info = report["Hardware"]

    # Use .get() with defaults to avoid KeyErrors
    hw_table.add_row("OS", sys_info.get('distro', 'Ubuntu'))
    hw_table.add_row("Kernel", sys_info.get('kernel', 'Unknown'))
    hw_table.add_row("CPU", f"{hw_info.get('cpu_model')} ({hw_info.get('cores')} Cores)")
    hw_table.add_row("Memory", f"{hw_info.get('ram_total_gb')} GB")
    
    console.print(hw_table)

    # 3. Thermal Section
    console.print("\n[bold]🌡️ Thermals[/bold]")
    thermals = report["Thermals"]
    
    if not thermals:
        console.print("  [yellow]No thermal sensors detected.[/yellow]")
    else:
        for sensor, temp in thermals.items():
            if temp is None:
                console.print(f"  • {sensor}: [dim]N/A[/dim]")
                continue
                
            color = "green"
            if temp > 75: color = "red"
            elif temp > 60: color = "yellow"
            
            console.print(f"  • {sensor.replace('_', ' ')}: [{color}]{temp}°C[/{color}]")

def main(): 
    args = parse_args()
    config = Config()
    logger = setup_logger(config)
    
    # Gather data
    report = {
        "Metadata": {
            "Generated_At": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
            "Unit": "Celsius",
            "Schema_Version": "0.1.1"
        },
        "System": gather_os_data(),
        "Thermals": gather_thermal_data(),
        "Hardware": gather_hardware_specs()
    }

    if args.output:
        try:
            with open(args.output, 'w') as f:
                json.dump(report, f, indent=4)
            logger.info(f"Report generated: {args.output}")
            print(f"✅ JSON report saved to {args.output}")
        except IOError as e:
            logger.error(f"File System Error: {e}")
            print(f"❌ Error: {e}")
    else:
        print_console_report(report)

if __name__ == "__main__":
    main()