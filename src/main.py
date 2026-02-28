import argparse
import json
import sys
import time
from datetime import datetime
from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.live import Live

# Local project imports
from src.config import Config
from src.logger import setup_logger
from src.system_info import gather_os_data, gather_thermal_data, gather_hardware_specs

def parse_args():
    """Defines CLI arguments for the tool."""
    parser = argparse.ArgumentParser(description='Specc: A native Ubuntu hardware profiler.')
    parser.add_argument('--output', type=str, help='Custom path for the JSON report')
    parser.add_argument('--live', action='store_true', help='Enable live monitoring (updates thermals periodically)')
    parser.add_argument('--interval', type=float, help='Sampling interval in seconds (overrides config)', default=None)
    return parser.parse_args()

def make_renderable(report):
    """Builds and returns a Rich renderable for the given report.

    This allows `rich.live` to update the entire dashboard as a single object.
    """
    # Header
    header = Panel("[bold blue]Specc System Profiler[/bold blue]", subtitle="v0.1.2", expand=False)

    # Hardware Table
    hw_table = Table(title="Hardware & OS", show_header=True, header_style="bold magenta")
    hw_table.add_column("Component", style="dim")
    hw_table.add_column("Detail")

    sys_info = report.get("System", {})
    hw_info = report.get("Hardware", {})

    hw_table.add_row("OS", sys_info.get('distro', 'Ubuntu'))
    hw_table.add_row("Kernel", sys_info.get('kernel', 'Unknown'))
    hw_table.add_row("CPU", f"{hw_info.get('cpu_model')} ({hw_info.get('cores')} Cores)")
    hw_table.add_row("Memory", f"{hw_info.get('ram_total_gb')} GB")

    # Thermals
    thermals_panel = Table.grid()
    thermals_panel.add_column()
    thermals = report.get("Thermals", {})
    if not thermals:
        thermals_panel.add_row("  [yellow]No thermal sensors detected.[/yellow]")
    else:
        for sensor, temp in thermals.items():
            if temp is None:
                thermals_panel.add_row(f"  • {sensor.replace('_', ' ')}: [dim]N/A[/dim]")
                continue

            color = "green"
            if temp > 75:
                color = "red"
            elif temp > 60:
                color = "yellow"

            thermals_panel.add_row(f"  • {sensor.replace('_', ' ')}: [{color}]{temp}°C[/{color}]")

    thermals_block = Panel(Group("\n[bold]🌡️ Thermals[/bold]", thermals_panel), expand=False)

    return Group(header, hw_table, thermals_block)

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

    # If user requested a JSON output, write once and exit
    if args.output:
        try:
            with open(args.output, 'w') as f:
                json.dump(report, f, indent=4)
            logger.info(f"Report generated: {args.output}")
            print(f"✅ JSON report saved to {args.output}")
        except IOError as e:
            logger.error(f"File System Error: {e}")
            print(f"❌ Error: {e}")
        return

    console = Console()

    # Live monitoring
    if args.live:
        interval = args.interval if args.interval is not None else config.sampling_interval
        try:
            with Live(make_renderable(report), refresh_per_second=4, console=console) as live:
                while True:
                    report["Thermals"] = gather_thermal_data()
                    report["Metadata"]["Generated_At"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    live.update(make_renderable(report))
                    time.sleep(interval)
        except KeyboardInterrupt:
            print("\nExiting live monitoring.")
            return

    # Non-live: render once
    console.print(make_renderable(report))

if __name__ == "__main__":
    main()